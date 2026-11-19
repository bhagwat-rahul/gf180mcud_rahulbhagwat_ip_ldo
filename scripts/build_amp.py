#!/usr/bin/env python3
"""Build layout/ldo_error_amp.mag.

14 single-finger arrays in one row at y=0 (gates up); 16 internal nets on
metal3 tracks y=30..45; VIN/VSS on metal3 rails y=-38/-40.  Resistors are
horizontal above the row, caps below; their terminals join the same
tracks/rails with metal2 drops.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from magcanvas import Canvas
from build_bias import wire, via
from build_softstart import down_to

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / 'layout'

# inst, cell, x, W, L, S, D, G, B
DEV = [
    ('XMPEN', 'amp_p50_l05', 0.0, 50.0, 0.5, 4, 'VIN', 'VP', 'ENB', 'VIN'),
    ('XMPBIAS', 'amp_p2_l2', 9.0, 2.0, 2.0, 1, 'VP', 'NB', 'PB', 'VIN'),
    ('XMNBIAS', 'amp_n16_l2', 18.0, 16.0, 2.0, 1, 'VSS', 'NB', 'NB', 'VSS'),
    ('XMPBOOST', 'amp_p50_l2', 27.0, 50.0, 2.0, 2, 'VP', 'RUN_BIAS', 'PB', 'VIN'),
    ('XMPMODE', 'amp_p40_l05', 36.6, 40.0, 0.5, 1, 'RUN_BIAS', 'NB', 'MODEG', 'VIN'),
    ('XMPLA', 'amp_p20_l05', 45.0, 20.0, 0.5, 1, 'VP', 'A', 'CMAVG', 'VIN'),
    ('XMPLB', 'amp_p20_l05', 54.0, 20.0, 0.5, 1, 'VP', 'EA', 'CMAVG', 'VIN'),
    ('XMNREF', 'amp_n40_l05', 63.0, 40.0, 0.5, 1, 'TAIL', 'A', 'VREF', 'VSS'),
    ('XMNFB', 'amp_n40_l05', 72.0, 40.0, 0.5, 1, 'TAIL', 'EA', 'VFB', 'VSS'),
    ('XMNTAIL', 'amp_n32_l2', 81.0, 32.0, 2.0, 2, 'VSS', 'TAIL', 'NB', 'VSS'),
    ('XMPMIRDRV', 'amp_p40_l1', 90.0, 40.0, 1.0, 2, 'VP', 'Q', 'A', 'VIN'),
    ('XMPDRV', 'amp_p40_l1', 99.0, 40.0, 1.0, 2, 'VP', 'GATE', 'EA', 'VIN'),
    ('XMNMIRDRV', 'amp_n40_l1', 108.0, 40.0, 1.0, 2, 'VSS', 'Q', 'Q', 'VSS'),
    ('XMNDRV', 'amp_n40_l1', 117.0, 40.0, 1.0, 2, 'VSS', 'GATE', 'Q', 'VSS'),
]

TRACK = {'NB': 30.0, 'PB': 31.0, 'A': 33.0,
         'EA': 34.0, 'CMAVG': 35.0, 'Q': 36.0, 'GATE': 37.0,
         'MC': 38.0, 'MODEG': 39.0, 'VREF': 40.0, 'VFB': 41.0,
         'ENB': 42.0, 'STBY': 43.0}
RAIL = {'RUN_BIAS': -35.0, 'VP': -36.0, 'TAIL': -37.0, 'VIN': -38.0, 'VSS': -40.0}


def main():
    c = Canvas(library_dir=str(LAYOUT))
    anchors = {}

    def add(net, x, y):
        anchors.setdefault(net, []).append((x, y))

    for inst, cell, x, W, L, n, S, D, G, B in DEV:
        c.flatten(cell, x, 0.0)
        hw = W / 2.0
        # gate pad (metal2), S/D buses (metal3), guard ring (metal1)
        add(G, x - 0.55, hw + 0.87)
        add(S, x - 0.32, -hw - 3.35)
        kk = n if n % 2 else n - 1
        add(D, x + (kk - 1) * (L + 0.64) + L + 0.32, -hw - 4.55)
        add(B, x - 1.45, 0.0)

    def stub(net, a, kind):
        y = TRACK.get(net, RAIL.get(net))
        if kind == 'm1':
            via(c, *a, 'metal1', 'metal2')
        elif kind == 'm3':
            via(c, *a, 'metal2', 'metal3')
        wire(c, 'metal2', a, (a[0], y))
        via(c, a[0], y, 'metal2', 'metal3')

    # transistor terminals
    for inst, cell, x, W, L, n, S, D, G, B in DEV:
        hw = W / 2.0
        stub(G, (x - 0.55, hw + 0.87), 'm2')
        stub(S, (x - 0.32, -hw - 3.35), 'm3')
        kk = n if n % 2 else n - 1
        stub(D, (x + (kk - 1) * (L + 0.64) + L + 0.32, -hw - 4.55), 'm3')
        stub(B, (x - 1.45, 0.0), 'm1')

    # ---- resistors (horizontal, rot=90) ------------------------------
    # Rmode: pads MODEG / STBY at y=55, left pad x=10
    c.flatten('ppolyf_u_3k_rswgc', 138.93, 55.0, rot=90)
    rm_l, rm_r = (10.0, 55.0), (267.86, 55.0)
    # RA: CMAVG / A, y=60
    c.flatten('ppolyf_u_3k_ra', 121.605, 60.0, rot=90)
    ra_l, ra_r = (10.0, 60.0), (233.21, 60.0)
    # RB: EA / CMAVG, y=65
    c.flatten('ppolyf_u_3k_ra', 121.605, 65.0, rot=90)
    rb_l, rb_r = (10.0, 65.0), (233.21, 65.0)
    # RZA: MC / EA at (280,30)
    c.flatten('ppolyf_u_rz', 280.0, 30.0)
    rz_hi, rz_lo = (280.0, 44.39), (280.0, 15.61)

    def jog(a, bx, by, net):
        via(c, *a, 'metal1', 'metal2')
        wire(c, 'metal2', a, (bx, a[1]))
        wire(c, 'metal2', (bx, a[1]), (bx, by))
        via(c, bx, by, 'metal2', 'metal3')
        add(net, bx, by)

    jog(rm_l, 2.0, TRACK['MODEG'], 'MODEG')
    jog(rm_r, 270.0, TRACK['STBY'], 'STBY')
    jog(ra_l, -2.0, TRACK['CMAVG'], 'CMAVG')
    jog(ra_r, 236.0, TRACK['A'], 'A')
    jog(rb_l, -6.0, TRACK['EA'], 'EA')
    jog(rb_r, 240.0, TRACK['CMAVG'], 'CMAVG')
    jog(rz_hi, 283.0, TRACK['MC'], 'MC')
    jog(rz_lo, 286.0, TRACK['EA'], 'EA')

    # ---- caps (below the row) ---------------------------------------
    c.flatten('cap_10', -30.0, -70.0)
    c.flatten('cap_20', -30.0, -110.0)
    cap10_top, cap10_bot = (-34.0, -44.0), (-35.0, -80.5)
    cap20_top, cap20_bot = (-36.0, -84.0), (-37.0, -120.5)

    def cap_stub(a, net):
        y = TRACK.get(net, RAIL.get(net))
        down_to(c, a[0], a[1], 'metal5', 'metal3')
        via(c, a[0], a[1], 'metal2', 'metal3', enc=0.07)
        wire(c, 'metal2', a, (a[0], y))
        via(c, a[0], y, 'metal2', 'metal3', enc=0.07)
        add(net, a[0], y)

    cap_stub(cap10_top, 'MODEG')
    cap_stub(cap10_bot, 'VSS')
    cap_stub(cap20_top, 'MC')
    cap_stub(cap20_bot, 'GATE')

    # ---- draw tracks and rails --------------------------------------
    for net, y in TRACK.items():
        pts = anchors.get(net, [])
        if not pts:
            continue
        xs = [p[0] for p in pts]
        wire(c, 'metal3', (min(xs), y), (max(xs), y))
    for net, y in RAIL.items():
        pts = anchors.get(net, [])
        xs = [p[0] for p in pts]
        wire(c, 'metal3', (-40.0, y), (max(xs), y), width=0.6)

    # ---- ports -------------------------------------------------------
    c.label('metal3', -14.0, -38.5, -12.8, -37.5, 'VIN', port='VIN')
    c.label('metal3', -14.0, -40.5, -12.8, -39.5, 'VSS', port='VSS')
    for net in ('PB', 'ENB', 'VREF', 'VFB'):
        y = TRACK[net]
        x = anchors[net][0][0]
        c.label('metal3', x - 0.6, y - 0.4, x + 0.6, y + 0.4, net, port=net)
    c.label('metal1', rm_r[0] - 0.3, rm_r[1] - 0.3,
            rm_r[0] + 0.3, rm_r[1] + 0.3, 'STBY', port='STBY')
    c.label('metal3', 99.9, -24.9, 100.7, -24.1, 'GATE', port='GATE')

    c.write(str(LAYOUT / 'ldo_error_amp.mag'))
    print('wrote layout/ldo_error_amp.mag')


if __name__ == '__main__':
    main()
