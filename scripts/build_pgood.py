#!/usr/bin/env python3
"""Build layout/ldo_pgood.mag: power-good comparator + hysteresis.

Transistors (one row, gates up, S=left D=right):
    XMNBIAS n2/2  D=G=NB      S=VSS
    XMPBIAS p2/2  D=NB        G=PB      S=VP
    XMPMIR  p4/2  D=G=MIR     S=VP
    XMPOUT  p4/2  D=RAW       G=MIR     S=VP
    XMNREF  n8/1  D=MIR       G=THRESH  S=TAIL
    XMNFB   n8/1  D=RAW       G=VFB     S=TAIL
    XMNTAIL n2/2  D=TAIL      G=NB      S=VSS
    XMPEN   p8/0.5 D=VP       G=ENB     S=VIN
    XMPBUF  p2/0.5 D=PGOOD    G=RAW     S=VIN
    XMNBUF  n1/0.5 D=PGOOD    G=RAW     S=VSS
    XMPOFF  p2/0.5 D=RAW      G=EN      S=VIN
    XMNHYS  n2/0.5 D=HYS      G=PGOOD   S=VSS

Resistors (horizontal, rot=90): RHYS 1/996.352, RLOW 1/586.046,
RTH 1/65.022, left pads at x=2 on y=16/20/24.

Routing: metal1 pads -> via1 -> metal2 stubs -> via2 -> metal3 tracks
above the row; VIN/VSS on metal3 rails below.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from magcanvas import Canvas, parse_mag
from build_bias import um, wire, via, terms

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / 'layout'

PLACE = [
    ('XMNBIAS', 'nfet_03v3_w2_l2', 3.5),
    ('XMPBIAS', 'pfet_03v3_w2_l2', 12.0),
    ('XMPMIR', 'pfet_03v3_w4_l2', 20.5),
    ('XMPOUT', 'pfet_03v3_w4_l2', 29.0),
    ('XMNREF', 'nfet_03v3_w8_l1', 37.5),
    ('XMNFB', 'nfet_03v3_w8_l1', 45.5),
    ('XMNTAIL', 'nfet_03v3_w2_l2', 54.5),
    ('XMPEN', 'pfet_03v3_w8_l05', 62.5),
    ('XMPBUF', 'pfet_03v3_w2_l05', 70.5),
    ('XMNBUF', 'nfet_03v3_w1_l05', 78.5),
    ('XMPOFF', 'pfet_03v3_w2_l05', 86.5),
    ('XMNHYS', 'nfet_03v3_w2_l05', 94.5),
]

# (inst, cell, length, y, left_pad_x)
RES = [
    ('RHYS', 'ppolyf_u_3k_rhys', 996.352, 16.0, 2.0),
    ('RLOW', 'ppolyf_u_3k_rlow', 586.046, 20.0, 2.0),
    ('RTH', 'ppolyf_u_3k_rth', 65.022, 24.0, 2.0),
]


def main():
    c = Canvas(library_dir=str(LAYOUT))
    P = {}
    for inst, cell, x in PLACE:
        c.flatten(cell, x, 0.0)
        t = terms(cell)
        P[inst] = {k: (x + v[0], v[1]) for k, v in t.items()}

    pads = {}
    for inst, cell, length, y, xl in RES:
        hl = length / 2.0
        off = hl + 0.275
        X = xl + off
        c.flatten(cell, X, y, rot=90)
        pads[inst] = {'L': (X - off, y), 'R': (X + off, y)}

    def track(net, anchors, y, kinds=None, label=None, lx=None):
        """One metal3 horizontal track with a metal2 stub per anchor."""
        for i, a in enumerate(anchors):
            kind = kinds[i] if kinds else 'm1'
            if kind == 'm1':
                via(c, a[0], a[1], 'metal1', 'metal2')
            wire(c, 'metal2', a, (a[0], y))
            via(c, a[0], y, 'metal2', 'metal3')
        xs = [a[0] for a in anchors]
        wire(c, 'metal3', (min(xs), y), (max(xs), y))
        if label:
            c.label('metal3', lx - 0.6, y - 0.4, lx + 0.6, y + 0.4,
                    net, port=net)

    # ---- VIN / VSS rails on metal3 below the row ---------------------
    yvin, yvss = -5.8, -4.0
    vin = [('XMPBIAS', 'B'), ('XMPMIR', 'B'), ('XMPOUT', 'B'),
           ('XMPEN', 'L'), ('XMPEN', 'B'), ('XMPBUF', 'L'),
           ('XMPBUF', 'B'), ('XMPOFF', 'L'), ('XMPOFF', 'B')]
    for inst, k in vin:
        a = P[inst][k]
        via(c, a[0], a[1], 'metal1', 'metal2')
        wire(c, 'metal2', a, (a[0], yvin))
        via(c, a[0], yvin, 'metal2', 'metal3')
    wire(c, 'metal3', (-6.0, yvin), (84.5, yvin), width=0.6)
    c.label('metal3', -6.0, yvin - 0.5, -4.8, yvin + 0.5, 'VIN', port='VIN')

    vss = [('XMNBIAS', 'L'), ('XMNBIAS', 'B'), ('XMNREF', 'B'),
           ('XMNFB', 'B'), ('XMNTAIL', 'L'), ('XMNTAIL', 'B'),
           ('XMNBUF', 'L'), ('XMNBUF', 'B'), ('XMNHYS', 'L'),
           ('XMNHYS', 'B')]
    for inst, k in vss:
        a = P[inst][k]
        via(c, a[0], a[1], 'metal1', 'metal2')
        wire(c, 'metal2', a, (a[0], yvss))
        via(c, a[0], yvss, 'metal2', 'metal3')
    wire(c, 'metal3', (-1.5, yvss), (93.0, yvss), width=0.6)
    c.label('metal3', 92.0, yvss - 0.5, 93.2, yvss + 0.5, 'VSS', port='VSS')

    # RLOW left pad is VSS: go left and down to the VSS rail
    a = pads['RLOW']['L']
    via(c, a[0], a[1], 'metal1', 'metal2')
    wire(c, 'metal2', a, (-1.0, a[1]))
    via(c, -1.0, a[1], 'metal2', 'metal3')
    wire(c, 'metal3', (-1.0, a[1]), (-1.0, yvss), width=0.5)

    # ---- local nets ---------------------------------------------------
    track('VP', [P['XMPBIAS']['L'], P['XMPMIR']['L'],
                 P['XMPOUT']['L'], P['XMPEN']['R']], 7.0,
          kinds=['m1', 'm1', 'm1', 'm1'])
    track('NB', [P['XMNBIAS']['G'], P['XMNBIAS']['R'],
                 P['XMPBIAS']['R'], P['XMNTAIL']['G']], 7.8,
          kinds=['m2', 'm1', 'm1', 'm2'])
    track('MIR', [P['XMPMIR']['G'], P['XMPMIR']['R'],
                  P['XMPOUT']['G'], P['XMNREF']['R']], 8.6,
          kinds=['m2', 'm1', 'm2', 'm1'])
    track('RAW', [P['XMPOUT']['R'], P['XMNFB']['R'], P['XMPBUF']['G'],
                  P['XMNBUF']['G'], P['XMPOFF']['R']], 9.4,
          kinds=['m1', 'm1', 'm2', 'm2', 'm1'])
    track('TAIL', [P['XMNREF']['L'], P['XMNFB']['L'],
                   P['XMNTAIL']['R']], 10.2,
          kinds=['m1', 'm1', 'm1'])
    track('PGOOD', [P['XMPBUF']['R'], P['XMNBUF']['R'],
                    P['XMNHYS']['G']], 11.0,
          kinds=['m1', 'm1', 'm2'], label='PGOOD', lx=94.0)
    track('HYS', [pads['RHYS']['L'], P['XMNHYS']['R']], 11.8,
          kinds=['m1', 'm1'])
    track('THRESH', [P['XMNREF']['G'], pads['RTH']['R'],
                     pads['RLOW']['R'], pads['RHYS']['R']], 12.6,
          kinds=['m2', 'm1', 'm1', 'm1'])

    # ---- single-ended ports ------------------------------------------
    for inst, net in (('XMPBIAS', 'PB'), ('XMNFB', 'VFB'),
                      ('XMPEN', 'ENB'), ('XMPOFF', 'EN')):
        a = P[inst]['G']
        wire(c, 'metal2', a, (a[0], 14.2))
        c.label('metal2', a[0] - 0.6, 13.8, a[0] + 0.6, 14.6,
                net, port=net)

    # VREF: RTH left pad up on metal2
    a = pads['RTH']['L']
    via(c, a[0], a[1], 'metal1', 'metal2')
    wire(c, 'metal2', a, (a[0], 25.2))
    c.label('metal2', a[0] - 0.6, 24.8, a[0] + 0.6, 25.6,
            'VREF', port='VREF')

    c.write(str(LAYOUT / 'ldo_pgood.mag'))
    print('wrote layout/ldo_pgood.mag')


if __name__ == '__main__':
    main()
