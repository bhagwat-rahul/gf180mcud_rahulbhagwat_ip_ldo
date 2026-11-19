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
    """nfet_03v3 W=2 L=0.5, re-ported for routing.

    The PDK cell's gate contact metal sits 0.21 um from the S/D contact
    metal (rule 0.23) and cannot be escaped at W=2.  This variant removes
    both gate heads and the bulk bars, re-draws the gate poly as a stripe
    extending over field with p-well notches under the extensions (so no
    MOSCAP marker is generated), contacts the gate at the top, and brings
    S/D out above the tap strips.  Extraction stays nfet_03v3 w=2u l=0.5u.
    """
    c = Canvas(library_dir=str(LAYOUT))
    c.flatten('nfet_03v3_K8XTZ5', 0.0, 0.0)
    # bulk bars and links
    c.remove_rect('metal1', -1.315, 1.635, 1.315, 1.865)
    c.remove_rect('metal1', -1.315, -1.865, 1.315, -1.635)
    for x0, x1 in ((1.085, 1.315), (-1.315, -1.085)):
        c.remove_rect('metal1', x0, 1.35, x1, 1.635)
        c.remove_rect('metal1', x0, -1.635, x1, -1.35)
    # S/D contact end-caps
    for x0, x1 in ((0.395, 0.625), (-0.625, -0.395)):
        c.remove_rect('metal1', x0, 0.935, x1, 0.99)
        c.remove_rect('metal1', x0, -0.99, x1, -0.935)
    # both gate heads: poly rails/strips, contacts and their metal pieces
    for x0, y0, x1, y1 in ((-0.25, 1.395, 0.25, 1.46),
                           (-0.25, 1.165, -0.185, 1.395),
                           (0.185, 1.165, 0.25, 1.395),
                           (-0.25, 1.0, 0.25, 1.165),
                           (-0.25, -1.46, 0.25, -1.395),
                           (-0.25, -1.395, -0.185, -1.165),
                           (0.185, -1.395, 0.25, -1.165),
                           (-0.25, -1.165, 0.25, -1.0)):
        c.remove_rect('polysilicon', x0, y0, x1, y1)
    c.remove_rect('polycontact', -0.185, 1.165, 0.185, 1.395)
    c.remove_rect('polycontact', -0.185, -1.395, 0.185, -1.165)
    for x0, x1 in ((-0.24, -0.185), (0.185, 0.24)):
        c.remove_rect('metal1', x0, 1.165, x1, 1.395)
        c.remove_rect('metal1', x0, -1.395, x1, -1.165)
    # keep the poly landing inside the p-well (extend the well under both
    # gate poly extensions) and notch the p-substrate ring where the poly
    # crosses it, so no substrate MOS capacitor is formed there
    c.rect('pwell', -0.45, 1.0, 0.45, 2.75)
    c.rect('pwell', -0.45, -2.75, 0.45, -1.0)
    for y0, y1 in ((1.57, 1.93), (-1.93, -1.57)):
        c.remove_rect('psubdiff', -1.38, y0, 1.38, y1)
        c.rect('psubdiff', -1.38, y0, -0.45, y1)
        c.rect('psubdiff', 0.45, y0, 1.38, y1)
    # gate poly stripe, top contact and metal landing
    c.rect('polysilicon', -0.25, -1.46, 0.25, 2.62)
    c.rect('polycontact', -0.13, 2.12, 0.13, 2.38)
    c.rect('metal1', -0.25, 2.04, 0.25, 2.54)
    c.rect('via1', -0.13, 2.12, 0.13, 2.38)
    c.rect('metal2', -0.25, 2.05, 0.25, 2.55)
    # S/D fan-out
    for sign in (1, -1):
        xs = lambda a: sign * a
        x0, x1 = sorted((xs(0.395), xs(0.625)))
        c.rect('metal1', x0, 0.89, x1, 1.60)
        x0, x1 = sorted((xs(0.395), xs(2.40)))
        c.rect('metal1', x0, 1.60, x1, 1.83)
    # bulk landing pad on the left tap contact
    c.rect('metal1', -1.60, -1.30, -0.90, -0.90)
    c.write(str(LAYOUT / 'nfet_03v3_w2_l05_wide.mag'))
    print('wrote layout/nfet_03v3_w2_l05_wide.mag')


def _strip(canvas, layer):
    canvas.rects[layer] = []


def transistor_cell(model, w, l, name, workdir, gencell_proc):
    """Re-port a PDK MOSFET gencell with routing-friendly terminals.

    Keeps diffusion/implant/well/contact layers so extraction is unchanged,
    strips all metal1/poly/polycontact and rebuilds: a gate stripe with a
    contact landing above the guard ring, S/D fan-out above the tap strips,
    and one bulk pad on the left tap strip.  All terminal metal is derived
    from the gencell's real contact rectangles (no assumed coordinates).
    """
    gen = gencell(workdir, f'''load tgen
box 0 0 200000 200000
gencell {gencell_proc} T1 w {w} l {l} nf 1''',
                    f'{model}_*.mag')
    cell = Canvas(library_dir=str(LAYOUT))
    layers, uses, _ = parse_mag(gen)
    for layer, rects in layers.items():
        cell.rects.setdefault(layer, []).extend(rects)
    for layer in ('metal1', 'polysilicon', 'polycontact'):
        _strip(cell, layer)
    inv = 1 / 200.0
    def um(rect):
        return tuple(v * inv for v in rect)
    hl, chw = l / 2.0, w / 2.0
    pfet = model.startswith('pfet')
    well = 'nwell' if pfet else 'pwell'
    ringd = 'nsubdiff' if pfet else 'psubdiff'
    ringc = 'nsubdiffcont' if pfet else 'psubdiffcont'
    sdc = 'pdiffc' if pfet else 'ndiffc'
    # gate landing above the guard ring (ring top <= chw + 1.0)
    land_b, land_t = chw + 1.30, chw + 2.05
    # well under the gate landing
    cell.rect(well, -0.45, chw, 0.45, land_t + 0.13)
    cell.rect(well, -0.45, -land_t - 0.13, 0.45, -chw)
    # notch the guard ring where the gate poly stripe crosses it
    notch = hl + 0.20
    for rect in list(cell.rects.get(ringd, [])):
        X0, Y0, X1, Y1 = um(rect)
        if X0 < -notch and X1 > notch and (Y0 > chw - 0.1 or Y1 < -chw + 0.1):
            cell.rects[ringd].remove(rect)
            cell.rect(ringd, X0, Y0, -notch, Y1)
            cell.rect(ringd, notch, Y0, X1, Y1)
    # gate poly: stripe through the channel plus a wide landing
    cell.rect('polysilicon', -hl, -chw - 0.46, hl, land_b + 0.05)
    cell.rect('polysilicon', -0.28, land_b, 0.28, land_t)
    cell.rect('polycontact', -0.13, land_b + 0.25, 0.13, land_b + 0.51)
    cell.rect('metal1', -0.28, land_b + 0.17, 0.28, land_b + 0.59)
    cell.rect('via1', -0.13, land_b + 0.25, 0.13, land_b + 0.51)
    cell.rect('metal2', -0.26, land_b + 0.20, 0.26, land_b + 0.62)
    # S/D fan-out: riser over each contact bar, horizontal bar above it
    for rect in cell.rects.get(sdc, []):
        bx0, by0, bx1, by1 = um(rect)
        cell.rect('metal1', bx0, -0.20, bx1, chw + 0.76)
        if bx0 >= 0:
            cell.rect('metal1', bx0, chw + 0.76, bx1 + 2.0, chw + 1.02)
        else:
            cell.rect('metal1', bx0 - 2.0, chw + 0.76, bx1, chw + 1.02)
    # cover both tap contact strips so no contact sits at a metal line end
    taps = sorted((um(r) for r in cell.rects.get(ringc, [])), key=lambda r: r[0])
    for tx0, ty0, tx1, ty1 in taps:
        cell.rect('metal1', tx0 - 0.09, ty0 - 0.09, tx1 + 0.09, ty1 + 0.09)
    # bulk pad on the left tap strip
    tx0, ty0, tx1, ty1 = taps[0]
    cell.rect('metal1', tx0 - 0.60, ty0 - 0.09, tx1 + 0.09, ty0 + 0.35)
    cell.write(str(LAYOUT / f'{name}.mag'))
    print(f'wrote layout/{name}.mag  ({model} w={w} l={l})')


TRANSISTORS = {
    # ldo_pgood / ldo_load
    'pfet_03v3_w8_l05':   ('pfet_03v3', 8.0, 0.5, 'gf180mcu::pfet_03v3'),
    'nfet_03v3_w8_l1':    ('nfet_03v3', 8.0, 1.0, 'gf180mcu::nfet_03v3'),
    'pfet_03v3_w2_l2':    ('pfet_03v3', 2.0, 2.0, 'gf180mcu::pfet_03v3'),
    'nfet_03v3_w2_l05':   ('nfet_03v3', 2.0, 0.5, 'gf180mcu::nfet_03v3'),
    # ldo_bias
    'nfet_03v3_w2_l2':   ('nfet_03v3', 2.0, 2.0, 'gf180mcu::nfet_03v3'),
    'nfet_03v3_w1_l05':  ('nfet_03v3', 1.0, 0.5, 'gf180mcu::nfet_03v3'),
    'pfet_03v3_w4_l2':   ('pfet_03v3', 4.0, 2.0, 'gf180mcu::pfet_03v3'),
    'pfet_03v3_w4_l05':  ('pfet_03v3', 4.0, 0.5, 'gf180mcu::pfet_03v3'),
    'pfet_03v3_w022_l028': ('pfet_03v3', 0.22, 0.28, 'gf180mcu::pfet_03v3'),
    'pfet_03v3_w2_l05':  ('pfet_03v3', 2.0, 0.5, 'gf180mcu::pfet_03v3'),
}


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
    for cellname, (model, w, l, proc) in TRANSISTORS.items():
        if not names or cellname in names:
            transistor_cell(model, w, l, cellname, 't_' + cellname, proc)


if __name__ == '__main__':
    main(sys.argv[1:])
