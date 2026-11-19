#!/usr/bin/env python3
"""Generate the layout device cells that the PDK gencells cannot produce.

1. Poly resistors (PDK gencell clamps the body at 0.8 um; we need 0.8/1.0/2.0
   with exact certified lengths) - magcanvas.resistor_cell.
2. A single MIM unit capacitor (PDK gencell, kept as the array element).
3. A custom 2D MIM array whose unit pitch satisfies MIMTM.1 (>= 1.2 um from
   one unit's bottom plate to the next unit's virtual top plate).  The
   PDK's 40-unit stack is 0.06 um short of that rule.
4. A wider nfet cell at the same W/L: the PDK nfet is 2.4 um wide and its
   three terminal escapes cannot meet the 0.23 um metal1 spacing; the
   modified cell removes the redundant end-caps/bars and brings S/D out to
   the sides, leaving the gate pad clear.

Usage:  python3 scripts/build_devices.py [cell ...]
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import magcanvas
from magcanvas import Canvas, parse_mag, cell_bbox

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / 'layout'
RC = '/foss/pdks/gf180mcuD/libs.tech/magic/gf180mcuD.magicrc'

# name -> (model, body width um, length um)
RESISTORS = {
    'ppolyf_u_3k_rss':      ('ppolyf_u_3k', 0.8, 257.311),
    'ppolyf_u_3k_rswgc':    ('ppolyf_u_3k', 0.8, 257.311),
    'ppolyf_u_3k_rswgcc':   ('ppolyf_u_3k', 0.8, 257.311),
    'ppolyf_u_3k_rbledpd2': ('ppolyf_u_3k', 0.8, 257.311),
    'ppolyf_u_3k_rpre_d':   ('ppolyf_u_3k', 0.8, 257.311),
    'ppolyf_u_3k_rmode_d':  ('ppolyf_u_3k', 0.8, 257.311),
    'ppolyf_u_3k_rbledpd1': ('ppolyf_u_3k', 0.8, 64.242),
    'ppolyf_u_3k_rtop':     ('ppolyf_u_3k', 2.0, 399.978),
    'ppolyf_u_3k_rbot':     ('ppolyf_u_3k', 2.0, 799.978),
    'ppolyf_u_3k_rth':      ('ppolyf_u_3k', 1.0, 65.022),
    'ppolyf_u_3k_rlow':     ('ppolyf_u_3k', 1.0, 586.046),
    'ppolyf_u_3k_rhys':     ('ppolyf_u_3k', 1.0, 996.352),
}


CONTAINER = 'iic-osic-tools_xserver_uid_501'


def _container_path(path):
    return str(path).replace(str(ROOT),
                             '/foss/designs/current-designs/chipalooza3/gf180mcud_rahulbhagwat_ip_ldo')


def gencell(workdir, lines, pattern):
    workdir = ROOT / 'checks' / 'gen' / workdir
    workdir.mkdir(parents=True, exist_ok=True)
    for stale in workdir.glob('*.mag'):
        stale.unlink()
    tcl = workdir / 'gen.tcl'
    tcl.write_text(f'drc off\ncd {{{_container_path(workdir)}}}\n' + lines +
                   '\nwriteall force\nquit -noprompt\n')
    subprocess.run(['docker', 'exec', CONTAINER, 'bash', '-lc',
                    f'magic -dnull -noconsole -rcfile {RC} {_container_path(tcl)}'],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    hits = [p for p in workdir.glob(pattern)]
    if len(hits) != 1:
        raise RuntimeError(f'expected one cell matching {pattern}, got {hits}')
    return hits[0]


def make_unit_cap(width=20.0, length=12.2):
    """PDK MIM unit cap, copied into layout/ as the array element."""
    out = LAYOUT / 'cap_mim_2p0fF_unit.mag'
    if True:
        cell = gencell('unit_cap', f'''load capgen
box 0 0 200000 200000
gencell gf180mcu::cap_mim_2p0fF C1 w {width} l {length} nx 1 ny 1''',
                       'cap_mim_2p0fF_*.mag')
        out.write_text(cell.read_text())
    print(f'wrote {out.relative_to(ROOT)}')


def cap_array(nx, ny, pitch_x=25.0, pitch_y=15.5, name='cap_mim_array'):
    """2D MIM array with MIMTM.1-compliant pitch.

    Top plates are strapped by one vertical metal5 stub per column through
    the mimcapcontact pads, joined by a bus above the array.  Bottom plates
    use the unit cell's via4 edge bar: one vertical metal5 trunk per column
    along that bar, joined by a bus below the array.  The two buses are on
    opposite sides so the metal5 networks never cross.
    """
    unit = LAYOUT / 'cap_mim_2p0fF_unit.mag'
    if not unit.is_file():
        make_unit_cap()
    c = Canvas(library_dir=str(LAYOUT))
    for j in range(ny):
        for i in range(nx):
            c.flatten('cap_mim_2p0fF_unit', i * pitch_x, j * pitch_y)
    y_hi = (ny - 1) * pitch_y
    # top plates: vertical stub at each column centre through the pads,
    # then a bus above the array
    for i in range(nx):
        cx = i * pitch_x
        c.rect('metal5', cx - 0.3, -4.0, cx + 0.3, y_hi + 12.0)
        for j in range(ny):
            cy = j * pitch_y
            c.rect('metal5', cx - 8.0, cy - 4.0, cx + 8.0, cy + 4.0)
    c.rect('metal5', -0.3, y_hi + 9.0, (nx - 1) * pitch_x + 6.0, y_hi + 12.0)
    # bottom plates: trunk on each column's via4 bar, bus below the array
    for i in range(nx):
        cx = i * pitch_x
        c.rect('metal5', cx + 10.37, -12.0, cx + 10.97, y_hi + 8.0)
    c.rect('metal5', 10.37, -12.0, (nx - 1) * pitch_x + 10.97, -9.0)
    # landing pads on opposite sides
    c.rect('metal5', -8.0, y_hi + 9.0, -4.0, y_hi + 12.0)      # TOP
    c.rect('metal5', -8.0, -12.0, -4.0, -9.0)                    # BOT
    c.label('metal5', -8.0, y_hi + 9.0, -7.6, y_hi + 9.4, 'TOP', port='TOP')
    c.label('metal5', -8.0, -12.0, -7.6, -11.6, 'BOT', port='BOT')
    # connect the landing pads to the buses
    c.rect('metal5', -8.0, y_hi + 10.1, -0.3, y_hi + 10.9)
    c.rect('metal5', -8.0, -10.9, 10.97, -10.1)
    c.write(str(LAYOUT / f'{name}.mag'))
    print(f'wrote layout/{name}.mag  ({nx} x {ny} units, pitch {pitch_x} x {pitch_y})')


def nfet_wide():
    """PDK nfet_03v3 W=2 L=0.5 with routing-friendly terminal metal."""
    c = Canvas(library_dir=str(LAYOUT))
    c.flatten('nfet_03v3_K8XTZ5', 0.0, 0.0)
    # remove the bulk bars/links and the narrow contact-bar end-caps
    c.remove_rect('metal1', -1.315, 1.635, 1.315, 1.865)
    c.remove_rect('metal1', -1.315, -1.865, 1.315, -1.635)
    for x0, x1 in ((1.085, 1.315), (-1.315, -1.085)):
        c.remove_rect('metal1', x0, 1.35, x1, 1.635)
        c.remove_rect('metal1', x0, -1.635, x1, -1.35)
    for x0, x1 in ((0.395, 0.625), (-0.625, -0.395)):
        c.remove_rect('metal1', x0, 0.935, x1, 0.99)
        c.remove_rect('metal1', x0, -0.99, x1, -0.935)
    for x0, x1 in ((0.185, 0.24), (-0.24, -0.185)):
        c.remove_rect('metal1', x0, 1.165, x1, 1.395)
        c.remove_rect('metal1', x0, -1.395, x1, -1.165)
    # S/D risers flush with the contact-bar metal, then out above the taps
    c.rect('metal1', -0.625, 0.89, -0.395, 1.60)
    c.rect('metal1', -2.40, 1.60, -0.395, 1.83)
    c.rect('metal1', 0.395, 0.89, 0.625, 1.60)
    c.rect('metal1', 0.395, 1.60, 2.40, 1.83)
    # gate landing pad over the poly contact
    c.rect('metal1', -0.16, 1.15, 0.16, 1.45)
    # bulk landing pad on the left tap strip
    c.rect('metal1', -1.60, -1.30, -0.90, -0.90)
    c.write(str(LAYOUT / 'nfet_03v3_w2_l05_wide.mag'))
    print('wrote layout/nfet_03v3_w2_l05_wide.mag')


def main(names):
    names = names or []
    if not names or 'resistors' in names:
        for name in sorted(RESISTORS):
            _, width, length = RESISTORS[name]
            magcanvas.resistor_cell(width, length, LAYOUT / f'{name}.mag')
            print(f'wrote layout/{name}.mag  ({width} x {length} um body)')
    if not names or 'cap_unit' in names:
        make_unit_cap()
    if not names or 'cap_array' in names:
        cap_array(4, 10, 25.0, 15.5)
    if not names or 'nfet_wide' in names:
        nfet_wide()


if __name__ == '__main__':
    main(sys.argv[1:])
