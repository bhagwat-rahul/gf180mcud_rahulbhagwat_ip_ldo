#!/usr/bin/env python3
"""Build layout/ldo_load.mag: load switch, current mirror, bias, logic.

Small devices in one row at y=0 (gates up, S=left D=right):
  XMPINV p2/.5  LDB/LOAD_DIS/VIN      XMNINV n1/.5  LDB/LOAD_DIS/VSS
  XMNCL  n2/.5  IREF/LOAD_DIS/VSS     XMPSTB p2/.5  STBYB/STBY/VIN
  XMNSTB n1/.5  STBYB/STBY/VSS        XMPLDB p2/.5  LDENB_B/LDENB/VIN
  XMNLDB n1/.5  LDENB_B/LDENB/VSS     XMP1   p4/.5  LOAD_DIS/PGOOD/VIN
  XMP2   p4/.5  LOAD_DIS/STBYB/VIN    XMP3   p4/.5  LOAD_DIS/LDENB_B/VIN
  XMN1   n4/.5  LOAD_DIS/PGOOD/net1   XMN2   n4/.5  net1/STBYB/net2
  XMN3   n4/.5  net2/LDENB_B/VSS

Wide devices to the right:
  XMIR   array 210 x W50/L1    VOUT/IREF/VSS
  XMNSW  array   8 x W50/L.5   VLOAD/LDB/ISET
  XMREF  array   1 x W50/L1    IREF/IREF/VSS
  XRSET  ppolyf 20/19.657      IREF-ISET
  XCIREF 205-unit MIM          IREF-VSS

Routing: row nets on metal3 tracks y=8..17 with metal2 stubs; four
metal2 vertical lanes (x=88,89.5,91,92.5) carry IREF/VSS/LDB/ISET to the
wide devices, crossing the row tracks as metal3 jogs; VIN/VSS rails on
metal3 below the row.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from magcanvas import Canvas
from build_bias import wire, via, terms
from build_power import arr_terms
from build_softstart import down_to

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / 'layout'

# (inst, cell, x, {terminal: net})
ROW = [
    ('XMPINV', 'pfet_03v3_w2_l05', 0.0,
     {'L': 'VIN', 'R': 'LOAD_DIS', 'G': 'LDB', 'B': 'VIN'}),
    ('XMNINV', 'nfet_03v3_w1_l05', 7.0,
     {'L': 'VSS', 'R': 'LOAD_DIS', 'G': 'LDB', 'B': 'VSS'}),
    ('XMNCL', 'nfet_03v3_w2_l05', 14.0,
     {'L': 'VSS', 'R': 'IREF', 'G': 'LOAD_DIS', 'B': 'VSS'}),
    ('XMPSTB', 'pfet_03v3_w2_l05', 21.0,
     {'L': 'VIN', 'R': 'STBYB', 'G': 'STBY', 'B': 'VIN'}),
    ('XMNSTB', 'nfet_03v3_w1_l05', 28.0,
     {'L': 'VSS', 'R': 'STBYB', 'G': 'STBY', 'B': 'VSS'}),
    ('XMPLDB', 'pfet_03v3_w2_l05', 35.0,
     {'L': 'VIN', 'R': 'LDENB_B', 'G': 'LDENB', 'B': 'VIN'}),
    ('XMNLDB', 'nfet_03v3_w1_l05', 42.0,
     {'L': 'VSS', 'R': 'LDENB_B', 'G': 'LDENB', 'B': 'VSS'}),
    ('XMP1', 'pfet_03v3_w4_l05', 49.0,
     {'L': 'VIN', 'R': 'LOAD_DIS', 'G': 'PGOOD', 'B': 'VIN'}),
    ('XMP2', 'pfet_03v3_w4_l05', 56.0,
     {'L': 'VIN', 'R': 'LOAD_DIS', 'G': 'STBYB', 'B': 'VIN'}),
    ('XMP3', 'pfet_03v3_w4_l05', 63.0,
     {'L': 'VIN', 'R': 'LOAD_DIS', 'G': 'LDENB_B', 'B': 'VIN'}),
    ('XMN1', 'nfet_03v3_w4_l05', 70.0,
     {'L': 'net1', 'R': 'LOAD_DIS', 'G': 'PGOOD', 'B': 'VSS'}),
    ('XMN2', 'nfet_03v3_w4_l05', 77.0,
     {'L': 'net2', 'R': 'net1', 'G': 'STBYB', 'B': 'VSS'}),
    ('XMN3', 'nfet_03v3_w4_l05', 84.0,
     {'L': 'VSS', 'R': 'net2', 'G': 'LDENB_B', 'B': 'VSS'}),
]

# metal3 track y for each row net
TRACK_Y = {'LOAD_DIS': 8.0, 'LDB': 9.0, 'STBYB': 10.0, 'LDENB_B': 11.0,
           'net1': 12.0, 'net2': 13.0, 'STBY': 14.0, 'LDENB': 15.0,
           'PGOOD': 16.0, 'IREF': 17.0}

# lanes (metal2 verticals in the channel x=88..92.5)
LANE = {'IREF': 88.0, 'VSS': 89.5, 'LDB': 91.0, 'ISET': 92.5}


def main():
    c = Canvas(library_dir=str(LAYOUT))
    P = {}
    for inst, cell, x, nets in ROW:
        c.flatten(cell, x, 0.0)
        t = terms(cell)
        P[inst] = {k: (x + v[0], v[1]) for k, v in t.items()}

    # wide devices
    c.flatten('arr_n50_l1_n210', 95.0, 0.0)
    MRI = arr_terms(50.0, 1.0, 210, 95.0, 0.0)
    c.flatten('arr_n50_l05_n8', 95.0, 60.0)
    MSW = arr_terms(50.0, 0.5, 8, 95.0, 60.0)
    c.flatten('arr_n50_l1_n1', 120.0, 60.0)
    MRF = arr_terms(50.0, 1.0, 1, 120.0, 60.0)
    c.flatten('ppolyf_u_xrset', 140.0, 60.0)
    res_hi, res_lo = (140.0, 70.1), (140.0, 49.9)
    c.flatten('cap_205', 95.0, 110.0)
    cap_top, cap_bot = (88.0, 322.0), (89.5, 99.5)

    # ---- row tracks --------------------------------------------------
    for net, y in TRACK_Y.items():
        anchors, kinds = [], []
        for inst, cell, x, nets in ROW:
            for k, n in nets.items():
                if n == net:
                    anchors.append(P[inst][k])
                    kinds.append('m2' if k == 'G' else 'm1')
        if not anchors:
            continue
        for a, kind in zip(anchors, kinds):
            if kind == 'm1':
                via(c, *a, 'metal1', 'metal2')
            wire(c, 'metal2', a, (a[0], y))
            via(c, a[0], y, 'metal2', 'metal3')
        xs = [a[0] for a in anchors]
        x1 = max(xs)
        if net in ('LDB', 'IREF'):
            x1 = LANE[net]
        elif net in ('STBY', 'LDENB', 'PGOOD'):
            x1 = 75.0
        wire(c, 'metal3', (min(xs), y), (x1, y))

    # ---- VIN / VSS rails below the row -------------------------------
    yvin, yvss = -4.0, -5.5
    for inst, cell, x, nets in ROW:
        for k, n in nets.items():
            if k == 'G':
                continue
            a = P[inst][k]
            if n == 'VIN':
                via(c, *a, 'metal1', 'metal2')
                wire(c, 'metal2', a, (a[0], yvin))
                via(c, a[0], yvin, 'metal2', 'metal3')
            elif n == 'VSS':
                via(c, *a, 'metal1', 'metal2')
                wire(c, 'metal2', a, (a[0], yvss))
                via(c, a[0], yvss, 'metal2', 'metal3')
    wire(c, 'metal3', (-6.0, yvin), (87.0, yvin), width=0.6)
    c.label('metal3', -6.0, yvin - 0.5, -4.8, yvin + 0.5, 'VIN', port='VIN')
    wire(c, 'metal3', (-6.0, yvss), (LANE['VSS'], yvss), width=0.6)
    c.label('metal3', -6.0, yvss - 0.5, -4.8, yvss + 0.5, 'VSS', port='VSS')

    # ---- wide-device bulk ties (ring -> own S bus) -------------------
    for p in (MRI, MSW, MRF):
        via(c, *p['B'], 'metal1', 'metal2')
        wire(c, 'metal2', p['B'], (p['B'][0], p['S'][1]))
        via(c, p['B'][0], p['S'][1], 'metal2', 'metal3', enc=0.07)
        wire(c, 'metal3', (p['B'][0], p['S'][1]),
             (p['S'][0] + 0.9, p['S'][1]))

    # ---- IREF lane: row track -> XMIR gate -> XMREF gate -> XRSET ->
    #      cap top.  Lane is metal2 at x=88; hop to metal3 at each target.
    via(c, LANE['IREF'], 17.0, 'metal2', 'metal3')
    wire(c, 'metal2', (LANE['IREF'], 17.0), (LANE['IREF'], cap_top[1]))
    # XMIR gate
    via(c, LANE['IREF'], MRI['G'][1], 'metal2', 'metal3')
    wire(c, 'metal3', (LANE['IREF'], MRI['G'][1]), (MRI['G'][0], MRI['G'][1]))
    via(c, *MRI['G'], 'metal2', 'metal3')
    # XMREF gate (approach at y=83 so the hop clears the XMNSW gate pad)
    via(c, LANE['IREF'], 83.0, 'metal2', 'metal3')
    wire(c, 'metal3', (LANE['IREF'], 83.0), (MRF['G'][0], 83.0))
    wire(c, 'metal3', (MRF['G'][0], 83.0), MRF['G'])
    via(c, *MRF['G'], 'metal2', 'metal3')
    # XRSET top pad
    via(c, LANE['IREF'], res_hi[1], 'metal2', 'metal3')
    wire(c, 'metal3', (LANE['IREF'], res_hi[1]), (res_hi[0], res_hi[1]))
    via(c, *res_hi, 'metal1', 'metal2')
    via(c, res_hi[0], res_hi[1], 'metal2', 'metal3', enc=0.07)
    # cap top plate
    down_to(c, cap_top[0], cap_top[1], 'metal5', 'metal2')

    # ---- LDB lane: row track -> XMNSW gate ---------------------------
    via(c, LANE['LDB'], 9.0, 'metal2', 'metal3')
    wire(c, 'metal2', (LANE['LDB'], 9.0), (LANE['LDB'], MSW['G'][1]))
    via(c, LANE['LDB'], MSW['G'][1], 'metal2', 'metal3', enc=0.07)
    wire(c, 'metal3', (LANE['LDB'], MSW['G'][1]),
         (MSW['G'][0], MSW['G'][1]))
    via(c, *MSW['G'], 'metal2', 'metal3')

    # ---- ISET lane: XMNSW source bus -> XRSET bottom pad ------------
    wire(c, 'metal3', (MSW['S'][0] - 0.9, MSW['S'][1]),
         (LANE['ISET'], MSW['S'][1]))
    via(c, LANE['ISET'], MSW['S'][1], 'metal2', 'metal3')
    wire(c, 'metal2', (LANE['ISET'], MSW['S'][1]),
         (LANE['ISET'], res_lo[1]))
    via(c, LANE['ISET'], res_lo[1], 'metal2', 'metal3', enc=0.07)
    wire(c, 'metal3', (LANE['ISET'], res_lo[1]), (res_lo[0], res_lo[1]))
    via(c, *res_lo, 'metal1', 'metal2')
    via(c, res_lo[0], res_lo[1], 'metal2', 'metal3', enc=0.07)

    # ---- VSS lane: rail -> XMIR source bus; XMREF source; cap bottom -
    via(c, LANE['VSS'], yvss, 'metal2', 'metal3')
    wire(c, 'metal2', (LANE['VSS'], yvss), (LANE['VSS'], -28.35))
    via(c, LANE['VSS'], -28.35, 'metal2', 'metal3', enc=0.07)
    wire(c, 'metal3', (LANE['VSS'], -28.35), (MRI['S'][0], -28.35))
    wire(c, 'metal3', (MRF['S'][0], MRF['S'][1]), (125.0, MRF['S'][1]))
    wire(c, 'metal3', (125.0, MRF['S'][1]), (125.0, -28.35))
    wire(c, 'metal2', (LANE['VSS'], yvss), (LANE['VSS'], cap_bot[1]))
    down_to(c, cap_bot[0], cap_bot[1], 'metal5', 'metal2')

    # ---- ports on the wide devices / tracks -------------------------
    c.label('metal3', MSW['D'][0] - 0.6, MSW['D'][1] - 0.5,
            MSW['D'][0] + 0.6, MSW['D'][1] + 0.5, 'VLOAD', port='VLOAD')
    c.label('metal3', MRI['D'][0] - 0.6, MRI['D'][1] - 0.5,
            MRI['D'][0] + 0.6, MRI['D'][1] + 0.5, 'VOUT', port='VOUT')
    for net in ('STBY', 'LDENB', 'PGOOD'):
        y = TRACK_Y[net]
        c.label('metal3', 74.0, y - 0.4, 75.0, y + 0.4, net, port=net)

    c.write(str(LAYOUT / 'ldo_load.mag'))
    print('wrote layout/ldo_load.mag')


if __name__ == '__main__':
    main()
