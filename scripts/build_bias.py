#!/usr/bin/env python3
"""Build layout/ldo_bias.mag: bias generator, fully routed.

Devices (one row, gates up):
    XMPINV     pfet_03v3_w2_l05     S=VIN  D=ENB   G=EN
    XMNINV     nfet_03v3_w1_l05     S=VSS  D=ENB   G=EN
    XMPADEN    pfet_03v3_w4_l05     S=VIN  D=ADSUP G=ENB
    XMPADMODE  pfet_03v3_w4_l05     S=ADSUP D=ADSOURCE G=STBY
    XMPREPLICA pfet_03v3_w022_l028  S=ADSOURCE D=IBIAS G=GATE
    XMNREF     nfet_03v3_w2_l2      S=VSS  D=IBIAS G=IBIAS
    XMNCOPY    nfet_03v3_w2_l2      S=VSS  D=PB    G=IBIAS
    XMPREF     pfet_03v3_w4_l2      S=VIN  D=PB    G=PB

Routing: metal1 fan-bar pads -> via1 -> metal2 stubs; horizontal nets on
metal2; VIN/VSS rails on metal3 below the row.  Ports are labelled on the
top edge (metal2) and on the rail ends (metal3).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from magcanvas import Canvas, parse_mag

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / 'layout'

INV = 1.0 / 200.0
VIA_NAME = {('metal4', 'metal5'): 'via4', ('metal3', 'metal4'): 'via3',
            ('metal2', 'metal3'): 'via2', ('metal1', 'metal2'): 'via1'}


def um(rect):
    return tuple(v * INV for v in rect)


def wire(c, layer, a, b, width=0.4):
    (x0, y0), (x1, y1) = a, b
    h = width / 2.0
    if y0 == y1:
        c.rect(layer, min(x0, x1) - h, y0 - h, max(x0, x1) + h, y0 + h)
    elif x0 == x1:
        c.rect(layer, x0 - h, min(y0, y1) - h, x0 + h, max(y0, y1) + h)
    else:
        raise ValueError('wire must be Manhattan')


def via(c, x, y, lower, upper, size=0.26, enc=0.05):
    s = size / 2.0
    c.rect(lower, x - s - enc, y - s - enc, x + s + enc, y + s + enc)
    c.rect(upper, x - s - enc, y - s - enc, x + s + enc, y + s + enc)
    c.rect(VIA_NAME[(lower, upper)], x - s, y - s, x + s, y + s)


_TERMS = {}


def terms(cell):
    """Local (L, R, G, B) anchors of a generated device cell, in um."""
    if cell in _TERMS:
        return _TERMS[cell]
    layers, _, _ = parse_mag(LAYOUT / f'{cell}.mag')
    m1 = [um(r) for r in layers.get('metal1', [])]
    m2 = [um(r) for r in layers.get('metal2', [])]
    fans = [r for r in m1
            if abs((r[3] - r[1]) - 0.26) < 0.02 and (r[2] - r[0]) > 1.5]
    fans.sort(key=lambda r: r[0])
    lfan, rfan = fans[0], fans[1]
    left = (lfan[0] + 0.16, (lfan[1] + lfan[3]) / 2.0)
    right = (rfan[2] - 0.16, (rfan[1] + rfan[3]) / 2.0)
    gate = max(m2, key=lambda r: r[3])
    g = ((gate[0] + gate[2]) / 2.0, (gate[1] + gate[3]) / 2.0)
    bulk = min(m1, key=lambda r: (r[1], -(r[2] - r[0])))
    b = (bulk[0] + 0.22, (bulk[1] + bulk[3]) / 2.0)
    _TERMS[cell] = dict(L=left, R=right, G=g, B=b)
    return _TERMS[cell]


PLACE = [
    ('XMPINV', 'pfet_03v3_w2_l05', 0.0),
    ('XMNINV', 'nfet_03v3_w1_l05', 7.0),
    ('XMPADEN', 'pfet_03v3_w4_l05', 15.0),
    ('XMPADMODE', 'pfet_03v3_w4_l05', 22.5),
    ('XMPREPLICA', 'pfet_03v3_w022_l028', 29.5),
    ('XMNREF', 'nfet_03v3_w2_l2', 37.5),
    ('XMNCOPY', 'nfet_03v3_w2_l2', 47.0),
    ('XMPREF', 'pfet_03v3_w4_l2', 56.5),
]


def main():
    c = Canvas(library_dir=str(LAYOUT))
    P = {}
    for inst, cell, x in PLACE:
        c.flatten(cell, x, 0.0)
        t = terms(cell)
        P[inst] = {k: (x + v[0], v[1]) for k, v in t.items()}

    # ---- local S/D and gate nets -------------------------------------
    # ADSUP: XMPADEN.D -> XMPADMODE.S
    a, b = P['XMPADEN']['R'], P['XMPADMODE']['L']
    via(c, *a, 'metal1', 'metal2')
    via(c, *b, 'metal1', 'metal2')
    wire(c, 'metal2', a, (b[0], a[1]))
    wire(c, 'metal2', (b[0], a[1]), b)

    # ADSOURCE: XMPADMODE.D -> XMPREPLICA.S
    a, b = P['XMPADMODE']['R'], P['XMPREPLICA']['L']
    via(c, *a, 'metal1', 'metal2')
    via(c, *b, 'metal1', 'metal2')
    mid = (b[0], a[1])
    wire(c, 'metal2', a, mid)
    wire(c, 'metal2', mid, b)

    # EN: both gates on metal2, joined over the row on metal3
    a, b = P['XMPINV']['G'], P['XMNINV']['G']
    ybus = 6.6
    via(c, a[0], a[1], 'metal2', 'metal3')
    via(c, b[0], b[1], 'metal2', 'metal3')
    wire(c, 'metal3', (a[0], a[1]), (a[0], ybus))
    wire(c, 'metal3', (a[0], ybus), (b[0], ybus))
    wire(c, 'metal3', (b[0], ybus), (b[0], b[1]))
    wire(c, 'metal3', (a[0], ybus), (a[0], 8.5))
    c.label('metal3', a[0] - 0.5, 8.1, a[0] + 0.5, 8.9, 'EN', port='EN')

    # ENB: XMPINV.D, XMNINV.D, XMPADEN.G
    ybus = 5.0
    for inst in ('XMPINV', 'XMNINV'):
        p = P[inst]['R']
        via(c, *p, 'metal1', 'metal2')
        wire(c, 'metal2', p, (p[0], ybus))
    g = P['XMPADEN']['G']
    wire(c, 'metal2', (g[0], ybus), g)
    wire(c, 'metal2', (g[0], ybus), (g[0], 8.0))
    wire(c, 'metal2', (P['XMPINV']['R'][0], ybus), (g[0], ybus))
    c.label('metal2', g[0] - 0.5, 7.6, g[0] + 0.5, 8.4, 'ENB', port='ENB')

    # IBIAS: XMPREPLICA.D, XMNREF.D/G, XMNCOPY.G
    ybus = 4.0
    p = P['XMPREPLICA']['R']
    via(c, *p, 'metal1', 'metal2')
    wire(c, 'metal2', p, (p[0], ybus))
    p = P['XMNREF']['R']
    via(c, *p, 'metal1', 'metal2')
    wire(c, 'metal2', p, (p[0], ybus))
    for inst in ('XMNREF', 'XMNCOPY'):
        g = P[inst]['G']
        wire(c, 'metal2', (g[0], ybus), g)
    wire(c, 'metal2', (P['XMPREPLICA']['R'][0], ybus),
         (P['XMNCOPY']['G'][0], ybus))
    wire(c, 'metal2', (42.0, ybus), (42.0, 8.0))
    c.label('metal2', 41.5, 7.6, 42.5, 8.4, 'IBIAS', port='IBIAS')

    # PB: XMNCOPY.D, XMPREF.D/G
    ybus = 4.6
    p = P['XMNCOPY']['R']
    via(c, *p, 'metal1', 'metal2')
    wire(c, 'metal2', p, (p[0], ybus))
    p = P['XMPREF']['R']
    via(c, *p, 'metal1', 'metal2')
    wire(c, 'metal2', p, (p[0], ybus))
    g = P['XMPREF']['G']
    wire(c, 'metal2', (g[0], ybus), g)
    wire(c, 'metal2', (P['XMNCOPY']['R'][0], ybus), (P['XMPREF']['R'][0], ybus))
    wire(c, 'metal2', (g[0], ybus), (g[0], 8.0))
    c.label('metal2', g[0] - 0.5, 7.6, g[0] + 0.5, 8.4, 'PB', port='PB')

    # STBY: XMPADMODE.G up to the top edge
    g = P['XMPADMODE']['G']
    wire(c, 'metal2', g, (g[0], 8.0))
    c.label('metal2', g[0] - 0.5, 7.6, g[0] + 0.5, 8.4, 'STBY', port='STBY')

    # GATE: XMPREPLICA.G up to the top edge
    g = P['XMPREPLICA']['G']
    wire(c, 'metal2', g, (g[0], 8.0))
    c.label('metal2', g[0] - 0.5, 7.6, g[0] + 0.5, 8.4, 'GATE', port='GATE')

    # ---- VIN rail (metal3, below the row) ----------------------------
    yvin = -4.0
    vin_terms = [('XMPINV', 'L'), ('XMPINV', 'B'), ('XMPADEN', 'L'),
                 ('XMPADEN', 'B'), ('XMPADMODE', 'B'), ('XMPREPLICA', 'B'),
                 ('XMPREF', 'L'), ('XMPREF', 'B')]
    for inst, k in vin_terms:
        p = P[inst][k]
        via(c, *p, 'metal1', 'metal2')
        wire(c, 'metal2', p, (p[0], yvin))
        via(c, p[0], yvin, 'metal2', 'metal3')
    wire(c, 'metal3', (-5.0, yvin), (55.2, yvin), width=0.6)
    c.label('metal3', -5.0, yvin - 0.5, -4.0, yvin + 0.5, 'VIN', port='VIN')

    # ---- VSS rail (metal3, below the VIN rail) -----------------------
    yvss = -5.8
    vss_terms = [('XMNINV', 'L'), ('XMNINV', 'B'), ('XMNREF', 'L'),
                 ('XMNREF', 'B'), ('XMNCOPY', 'L'), ('XMNCOPY', 'B')]
    for inst, k in vss_terms:
        p = P[inst][k]
        via(c, *p, 'metal1', 'metal2')
        wire(c, 'metal2', p, (p[0], yvss))
        via(c, p[0], yvss, 'metal2', 'metal3')
    wire(c, 'metal3', (3.0, yvss), (46.0, yvss), width=0.6)
    c.label('metal3', 45.0, yvss - 0.5, 46.0, yvss + 0.5, 'VSS', port='VSS')

    c.write(str(LAYOUT / 'ldo_bias.mag'))
    print('wrote layout/ldo_bias.mag')


if __name__ == '__main__':
    main()
