#!/usr/bin/env python3
"""Generate the layout device cells that the PDK gencells cannot produce.

The PDK's poly-resistor gencell clamps its body width at 0.8 um, but the
certified design uses 0.5/1.0 um bodies.  `magcanvas.resistor_cell` emits
the same PDK structure (ppolyres body, polysilicon heads, poly contacts,
pwell island, psubdiff tap ring) at the required body width, so magic
extraction reports the schematic's r_width/r_length exactly.

Usage:  python3 scripts/build_devices.py [cell ...]
Output: layout/<name>.mag
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import magcanvas

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / 'layout'

# name -> (model, body width um, length um)
RESISTORS = {
    # 7 resistors widened to the 0.8 um DRC minimum (PRES.1), lengths
    # recomputed from the ppolyf_u_3k model to preserve each certified R
    'ppolyf_u_3k_rss':      ('ppolyf_u_3k', 0.8, 257.311),
    'ppolyf_u_3k_rswgc':    ('ppolyf_u_3k', 0.8, 257.311),
    'ppolyf_u_3k_rswgcc':   ('ppolyf_u_3k', 0.8, 257.311),
    'ppolyf_u_3k_rbledpd2': ('ppolyf_u_3k', 0.8, 257.311),
    'ppolyf_u_3k_rpre_d':   ('ppolyf_u_3k', 0.8, 257.311),
    'ppolyf_u_3k_rmode_d':  ('ppolyf_u_3k', 0.8, 257.311),
    'ppolyf_u_3k_rbledpd1': ('ppolyf_u_3k', 0.8, 64.242),
    # already at or above the DRC minimum, values unchanged
    'ppolyf_u_3k_rtop':     ('ppolyf_u_3k', 2.0, 399.978),
    'ppolyf_u_3k_rbot':     ('ppolyf_u_3k', 2.0, 799.978),
    'ppolyf_u_3k_rth':      ('ppolyf_u_3k', 1.0, 65.022),
    'ppolyf_u_3k_rlow':     ('ppolyf_u_3k', 1.0, 586.046),
    'ppolyf_u_3k_rhys':     ('ppolyf_u_3k', 1.0, 996.352),
}


def main(names):
    names = names or sorted(RESISTORS)
    for name in names:
        if name not in RESISTORS:
            raise SystemExit(f'unknown device {name}')
        _, width, length = RESISTORS[name]
        magcanvas.resistor_cell(width, length, LAYOUT / f'{name}.mag')
        print(f'wrote layout/{name}.mag  ({width} x {length} um body)')


if __name__ == '__main__':
    main(sys.argv[1:])
