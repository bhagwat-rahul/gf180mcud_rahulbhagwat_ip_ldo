#!/usr/bin/env python3
"""Check the LDO layout against the schematic sources.

Runs the GF180MCU Magic/Netgen verification loop on the saved .mag library:

    input-hierarchy   every cell file complete and on the right tech
    drc               KLayout DRC (foundry deck) zero-marker gate, plus a
                      Magic DRC diagnostic (this tech's magic DRC flags
                      tiles inside the PDK device cells themselves, so it
                      is reported but not gated)
    lvs               per-block and top-level LVS: flatten the layout cell,
                      extract, and compare against a multi-sheet xschem
                      netlist with netgen (gf180mcuD setup)
    antenna           Magic antenna check on the extracted netlist
    pex               Magic RC extraction (extresist) to a SPICE netlist
    klayout-drc       KLayout DRC deck only
    gds               GDS export sanity

Modeled on the Chipalooza2 PLL checker
(submitted-designs/chipalooza2/.../macros/pll_analog/layout/run_checks.py).

Usage (inside IIC-OSIC-TOOLS, from the repository root):

    python3 scripts/run_checks.py quick                # hierarchy + DRC + LVS
    python3 scripts/run_checks.py all                  # everything below
    python3 scripts/run_checks.py drc  [CELL ...]
    python3 scripts/run_checks.py lvs  [CELL ...]
    python3 scripts/run_checks.py antenna [CELL ...]
    python3 scripts/run_checks.py pex  [CELL ...]
    python3 scripts/run_checks.py klayout-drc [CELL ...]
    python3 scripts/run_checks.py gds  [CELL ...]

CELL names are layout cell names (default: every schematic block, then
ldo_top).  The layout library is `layout/`, the schematic sources
`schematics/` (including `schematics/load/`).  Sources are snapshotted
into a timestamped work directory before anything runs, so a check never
writes into the layout or schematic libraries.

Notes:
- Blocks are compared one by one (schematic block vs its layout cell)
  before the whole chip, so a failure points at one block.
- The layout side is flattened before extraction because the imported
  device cells carry no terminal labels; this is the only reliable way to
  recover terminal connectivity from those cells.  A real, routed cell
  library with labelled device terminals can drop the flatten step later.
- LVS is a gate: netgen must report "Circuits match uniquely." with no
  property errors.  PEX is a gate on extraction completing and producing a
  top subcircuit; it is not a simulation signoff.
"""

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / 'layout'
SCHEM = ROOT / 'schematics'
PDK = Path(os.environ.get('PDK_ROOT', '/foss/pdks')) / 'gf180mcuD'
RC = PDK / 'libs.tech/magic/gf180mcuD.magicrc'
NETGEN_SETUP = PDK / 'libs.tech/netgen/gf180mcuD_setup.tcl'
KLAYOUT_DRC = PDK / 'libs.tech/klayout/tech/drc/gf180mcu.drc'

# Children before ldo_top: netlist order and per-block check order.
BLOCKS = ('ldo_softstart', 'ldo_error_amp', 'ldo_power_stage', 'ldo_bias',
          'ldo_pgood', 'ldo_startup', 'ldo_load')
TOP = 'ldo_top'
CELLS = BLOCKS + (TOP,)
MODES = ('quick', 'all', 'drc', 'lvs', 'antenna', 'pex', 'klayout-drc', 'gds')

# Schematic sheets to netlist, children before parents.  ldo_load lives in
# schematics/load/; the rest are at the top level.
SHEETS = [(sheet, f'{sheet}.sch') for sheet in BLOCKS[:-1]]
SHEETS += [(BLOCKS[-1], f'load/{BLOCKS[-1]}.sch'), (TOP, f'{TOP}.sch')]


class Checks:
    """Snapshot the sources, then run Magic/Netgen/KLayout checks on them."""

    def __init__(self, cell, layout_dir=LAYOUT, schematic_dir=SCHEM, work_root=None):
        self.cell = cell
        self.work_root = Path(work_root) if work_root else ROOT / 'checks'
        self.work = self.work_root / cell / datetime.now().strftime('%Y%m%d-%H%M%S-%f')
        self.work.mkdir(parents=True)
        self.results = {}

        # Snapshot the .mag library: checks must never write into layout/.
        self.inputs = self.work / 'mag'
        shutil.copytree(layout_dir, self.inputs,
                        ignore=shutil.ignore_patterns('tools', '__pycache__'))

        # Snapshot the schematic tree (including schematics/load/).
        self.schematic = self.work / 'schematic'
        shutil.copytree(schematic_dir, self.schematic,
                        ignore=shutil.ignore_patterns('*.spice', '__pycache__'))

    # -- plumbing ---------------------------------------------------------

    def command(self, name, args, cwd=None):
        log = self.work / f'{name}.log'
        print(f'  Running {name} ...', flush=True)
        with log.open('w') as out:
            result = subprocess.run([str(a) for a in args],
                                    cwd=str(cwd or self.inputs),
                                    stdout=out, stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError(f'exit {result.returncode}; see {log}')
        return log.read_text(errors='replace')

    def magic(self, name, body, strict=True):
        """Run a Magic script in the work dir.  Returns (dir, log text)."""
        directory = self.work / name
        directory.mkdir(exist_ok=True)
        script = directory / 'run.tcl'
        script.write_text(f'''crashbackups stop
drc off
load {{{self.inputs / (self.cell + '.mag')}}}
select top cell
expand
cd {{{directory}}}
{body}
puts CHECK_SCRIPT_COMPLETED
quit -noprompt
''')
        log = self.command(name, ['magic', '-dnull', '-noconsole', '-rcfile', RC, script])
        if 'CHECK_SCRIPT_COMPLETED' not in log:
            raise RuntimeError(f'incomplete Magic run; see {name}/run.tcl and {name}.log')
        if strict:
            fatal = re.search(
                r'(?im)^(?:Error|Magic error|Tcl error)|Cannot open|'
                r'couldn.t (?:open|find)|Bad Device Location|'
                r'Missing (?:terminal|substrate) connection|'
                r'Unrecognized layer \(type\)|CIF output style .* is ambiguous|'
                r'[1-9]\d* problems occurred\.', log)
            if fatal:
                raise RuntimeError(f'Magic error "{fatal.group(0).strip()}"; '
                                   f'see {name}.log')
        return directory, log

    def extraction_errors(self, log):
        """Summarize Magic extraction feedback (flat extraction of imported
        device cells reports diff overlaps and shorted ports)."""
        counts = re.findall(r'^(\S+): (\d+) errors$', log, re.M)
        total = sum(int(n) for _, n in counts)
        if not total:
            return None
        first = []
        for line in log.splitlines():
            m = re.search(r'(?:Warning:\s+)?(Ports .+ electrically shorted\.?)', line)
            if m and m.group(1) not in first:
                first.append(m.group(1))
        detail = f'{total} extraction errors'
        if first:
            detail += '; first: ' + ' | '.join(first[:3])
        return detail

    # -- checks -----------------------------------------------------------

    def validate_hierarchy(self, cell=None, seen=None):
        """Every cell we need must be complete, on gf180mcuD, and non-empty."""
        cell = cell or self.cell
        seen = seen if seen is not None else set()
        if cell in seen:
            return 'complete saved hierarchy, correct technology'
        seen.add(cell)
        path = self.inputs / f'{cell}.mag'
        if not path.is_file():
            raise ValueError(f'{cell}: layout cell not found')
        text = path.read_text()
        if '\ntech gf180mcuD\n' not in text or '<< end >>' not in text:
            raise ValueError(f'{cell}: incomplete file or wrong technology')
        if not re.search(r'^(rect |use |rlabel |flabel )', text, re.M):
            raise ValueError(f'{cell}: empty layout')
        for child in re.findall(r'^use (\S+)', text, re.M):
            self.validate_hierarchy(child, seen)
        return f'complete saved hierarchy, correct technology ({len(seen)} cells)'

    def reference(self):
        """Netlist every schematic sheet and concatenate, children first."""
        directory = self.work_root / 'reference'
        netlists = directory / 'sheets'
        if (directory / 'schematic.spice').is_file():
            return directory / 'schematic.spice'
        netlists.mkdir(parents=True, exist_ok=True)
        env = dict(os.environ, PDK_ROOT=str(PDK.parent))
        for sheet, relpath in SHEETS:
            target = netlists / f'{sheet}.spice'
            command = (f'set spiceprefix 1; set top_is_subckt 1; set lvs_ignore 1; '
                       f'set ev_precision 5; set netlist_dir {{{netlists}}}; '
                       f'xschem set netlist_name {{{target.name}}}; xschem netlist')
            log = self.work_root / f'reference-{sheet}.log'
            with log.open('w') as out:
                result = subprocess.run(
                    ['xschem', '-s', '-r', '-x', '-q', '--rcfile',
                     str(self.schematic / 'xschemrc'), '--command', command,
                     str(self.schematic / relpath)],
                    cwd=str(self.schematic), env=env,
                    stdout=out, stderr=subprocess.STDOUT)
            if result.returncode or not target.is_file():
                raise RuntimeError(f'xschem netlist failed for {sheet}; see {log}')
            if not re.search(rf'^\.subckt\s+{sheet}\s', target.read_text(), re.M | re.I):
                raise RuntimeError(f'{sheet}.sch did not produce a subcircuit')
        combined = directory / 'schematic.spice'
        combined.write_text(''.join(
            (netlists / f'{sheet}.spice').read_text() + '\n' for sheet, _ in SHEETS))
        return combined

    def drc(self):
        """Magic DRC summary.  Informational only: this tech's magic DRC
        flags tiles inside PDK device cells themselves, so it cannot be a
        clean gate; the KLayout deck is the authoritative DRC."""
        _, log = self.magic('drc', '''drc euclidean on
drc style drc(full)
drc check
drc catchup
puts "DRC_LISTALL: [drc listall count]"''')
        match = re.search(r'^DRC_LISTALL: (.*)$', log, re.M)
        counts = [(cell, int(n)) for cell, n in
                  re.findall(r'\{(\S+) (\d+)\}', match[1] if match else '')]
        if not counts:
            return '0 Magic DRC error tiles'
        total = sum(n for _, n in counts)
        worst = sorted(counts, key=lambda item: -item[1])[:3]
        return (f'{total} Magic DRC error tiles (informational; gencell '
                f'false positives; worst: '
                + ', '.join(f'{cell} {n}' for cell, n in worst) + ')')

    def extraction(self, name, extra=''):
        """Flatten the cell, extract it flat, and return the work directory."""
        return self.magic(name, f'''flatten {self.cell}_flat
writeall force
load {self.cell}_flat
select top cell
extract path .
extract all
{extra}''', strict=False)

    def antenna(self):
        directory, log = self.extraction('antenna', '''feedback clear
antennacheck
feedback save antenna.feedback.tcl
set report [open antenna.txt w]
puts $report [feedback count]
close $report''')
        extraction = self.extraction_errors(log)
        count = int((directory / 'antenna.txt').read_text().strip())
        if count:
            raise RuntimeError(f'{count} Magic antenna markers; '
                               f'see antenna/antenna.feedback.tcl')
        if extraction:
            return f'0 antenna markers (extraction: {extraction})'
        return '0 Magic antenna markers'

    def lvs(self):
        directory, log = self.extraction('lvs', '''ext2spice lvs
ext2spice hierarchy off
ext2spice subcircuit top on
ext2spice -p . -o layout.spice
feedback save extraction.feedback.tcl''')
        netlist = directory / 'layout.spice'
        if not netlist.is_file() or not netlist.stat().st_size:
            raise RuntimeError('extraction produced no SPICE netlist; '
                               f'{self.extraction_errors(log) or "see lvs.log"}')
        text = netlist.read_text()
        if not re.search(rf'^\.subckt\s+{self.cell}_flat\s', text, re.M | re.I):
            raise RuntimeError('extracted netlist has no top subcircuit')
        devices = len(re.findall(r'^\s*[XMRC]\S*\s', text, re.M))
        reference = self.reference()
        report = directory / f'{self.cell}.lvs.out'
        self.command('lvs-netgen',
                     ['netgen', '-batch', 'lvs',
                      f'{netlist} {self.cell}_flat',
                      f'{reference} {self.cell}',
                      NETGEN_SETUP, report], cwd=directory)
        result = report.read_text()
        if 'Final result: Circuits match uniquely.' not in result:
            summary = [line.strip() for line in result.splitlines()
                       if re.search(r'(?i)circuit|device| net |property|mismatch|match',
                                    line)][-6:]
            detail = self.extraction_errors(log)
            if detail:
                raise RuntimeError(f'{detail}; Netgen: {" | ".join(summary)}')
            raise RuntimeError(f'Netgen topology/property mismatch; '
                               f'see {report}; {" | ".join(summary)}')
        if re.search(r'property errors', result, re.I):
            raise RuntimeError(f'Netgen property mismatch; see {report}')
        extraction = self.extraction_errors(log)
        if extraction:
            raise RuntimeError(f'extraction errors despite topology match '
                               f'({extraction}); see lvs/extraction.feedback.tcl')
        return (f'schematic and flat-extracted layout match '
                f'({devices} netlist device/instance statements)')

    def pex(self):
        directory, log = self.magic('pex', f'''flatten {self.cell}_pex
writeall force
load {self.cell}_pex
select top cell
extract path .
extract do capacitance
extract do coupling
extract do resistance
extract all
feedback save extraction.feedback
ext2sim labels on
ext2sim
extresist threshold 0
extresist minres 1
extresist mindelay 0
extresist all
ext2spice lvs
ext2spice resistor tee off
ext2spice hierarchy off
ext2spice subcircuit top on
ext2spice cthresh 0
ext2spice rthresh 0
ext2spice extresist on
ext2spice -p . -o {self.cell}_pex.spice''', strict=False)
        netlist = directory / f'{self.cell}_pex.spice'
        if not netlist.is_file() or not netlist.stat().st_size:
            raise RuntimeError('PEX produced no SPICE netlist; '
                               f'{self.extraction_errors(log) or "see pex.log"}')
        text = netlist.read_text()
        if not re.search(rf'^\.subckt\s+{self.cell}_pex\s', text, re.M | re.I):
            raise RuntimeError('PEX netlist has no expected top subcircuit')
        resistors = len(re.findall(r'^R\S+\s', text, re.M | re.I))
        capacitors = len(re.findall(r'^C\S+\s', text, re.M | re.I))
        extraction = self.extraction_errors(log)
        if extraction:
            raise RuntimeError(f'PEX extraction incomplete ({extraction}); '
                               f'netlist: {netlist}')
        return f'extracted {resistors} resistors, {capacitors} capacitors'

    def klayout_drc(self):
        stream = self.export()
        directory = self.work / 'drc-klayout'
        directory.mkdir()
        report = directory / f'{self.cell}.lyrdb'
        self.command('klayout-drc',
                     ['klayout', '-b', '-r', KLAYOUT_DRC,
                      f'-rd', f'input={stream}',
                      f'-rd', f'report={report}',
                      f'-rd', f'topcell={self.cell}',
                      f'-rd', 'variant=gf180mcuD',
                      f'-rd', 'run_mode=deep'],
                     cwd=directory)
        if not report.is_file():
            raise RuntimeError(f'KLayout DRC wrote no report; see {directory}')
        count = len(ET.parse(report).findall('.//items/item'))
        if count:
            raise RuntimeError(f'{count} KLayout DRC markers; see {report}')
        return f'0 KLayout DRC markers (full deck; GDS: {self._gds_note})'

    def export(self):
        if not getattr(self, '_gds', None):
            _, log = self.magic('export', f'gds write {{{self.work / (self.cell + ".gds")}}}',
                                strict=False)
            stream = self.work / f'{self.cell}.gds'
            if not stream.is_file() or not stream.stat().st_size:
                raise RuntimeError('empty GDS export; see export.log')
            problems = re.search(r'(\d+) problems occurred', log)
            self._gds_note = (f'{problems.group(1)} Magic CIF feedback entries '
                              f'(non-fatal)' if problems else 'clean write')
            self._gds = stream
        return self._gds

    # -- runner -----------------------------------------------------------

    def run(self, name, action, required=True):
        try:
            detail = action()
            self.results[name] = {'status': 'PASS', 'detail': detail}
        except (OSError, ValueError, RuntimeError, ET.ParseError, TypeError) as error:
            self.results[name] = {'status': 'FAIL', 'detail': str(error)}
        if not required:
            self.results[name]['required'] = False
        print(f"  {name}: {self.results[name]['status']} - "
              f"{self.results[name]['detail']}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('mode', choices=MODES)
    parser.add_argument('cells', nargs='*', metavar='CELL', help=', '.join(CELLS))
    parser.add_argument('--library', type=Path, default=LAYOUT,
                        help='layout .mag library (default: layout/)')
    parser.add_argument('--schematic-library', type=Path, default=SCHEM,
                        help='xschem source tree (default: schematics/)')
    args = parser.parse_args()
    layout_dir = args.library.resolve()
    schematic_dir = args.schematic_library.resolve()
    if not layout_dir.is_dir():
        parser.error(f'layout library not found: {layout_dir}')
    if not (schematic_dir / 'xschemrc').is_file():
        parser.error(f'xschem sources not found: {schematic_dir}')
    args.cells = args.cells or list(CELLS)
    for cell in args.cells:
        if cell not in CELLS:
            parser.error(f'unknown cell {cell}; choose from {", ".join(CELLS)}')
    if not RC.is_file():
        parser.error(f'PDK startup file not found: {RC}')
    mode = args.mode
    os.environ.setdefault('PDK_ROOT', str(PDK.parent))

    failed = False
    for cell in dict.fromkeys(args.cells):
        print(f'Checking {cell} (saved .mag sources)', flush=True)
        checks = Checks(cell, layout_dir, schematic_dir)
        checks.run('input-hierarchy', checks.validate_hierarchy)
        if checks.results['input-hierarchy']['status'] != 'PASS':
            mode_for_cell = None
        else:
            mode_for_cell = mode
        if mode_for_cell in ('all', 'quick', 'lvs'):
            checks.run('source-reference', lambda: str(checks.reference()))
        if mode_for_cell in ('all', 'quick', 'drc'):
            # This tech's magic DRC flags tiles inside the PDK device cells
            # themselves, so keep it as a diagnostic; KLayout is the gate.
            checks.run('drc-magic', checks.drc, required=False)
        if mode_for_cell in ('all', 'drc', 'klayout-drc'):
            checks.run('drc-klayout', checks.klayout_drc)
        if mode_for_cell in ('all', 'quick', 'lvs'):
            checks.run('lvs-netgen', checks.lvs)
        if mode_for_cell in ('all', 'antenna'):
            checks.run('antenna-magic', checks.antenna)
        if mode_for_cell in ('all', 'pex'):
            checks.run('pex-magic', checks.pex)
        if mode_for_cell in ('all', 'gds'):
            checks.run('gds-export',
                       lambda: f'{checks.export()} ({checks._gds_note})')
        (checks.work / 'summary.json').write_text(
            json.dumps(checks.results, indent=2) + '\n')
        (checks.work / 'summary.txt').write_text('\n'.join(
            f"{name}: {r['status']} - {r['detail']}"
            for name, r in checks.results.items()) + '\n')
        print(f'Reports: {checks.work}\n', flush=True)
        failed |= any(r['status'] != 'PASS'
                      for r in checks.results.values() if r.get('required', True))
    return int(failed)


if __name__ == '__main__':
    sys.exit(main())
