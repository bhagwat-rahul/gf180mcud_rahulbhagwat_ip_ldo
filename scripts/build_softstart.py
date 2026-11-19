#!/usr/bin/env python3
"""Build layout/ldo_softstart.mag: RSS + CSS + MNRESET, fully routed.

Devices:
    CSS      layout/cap_mim_array.mag          4 x 10 MIM unit array (40)
    RSS      layout/ppolyf_u_3k_rss.mag        0.8 x 257.311
    MNRESET  layout/nfet_03v3_w2_l05_wide.mag  nfet_03v3 W=2 L=0.5

Nets: VSS (cap bottom, nfet source/bulk), VREF_SS (cap top, resistor end,
nfet drain), VREF (resistor other end), ENB (nfet gate).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from magcanvas import Canvas

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / 'layout'

VIA_ORDER = ['metal5', 'metal4', 'metal3', 'metal2', 'metal1']
VIA_NAME = {('metal4', 'metal5'): 'via4', ('metal3', 'metal4'): 'via3',
            ('metal2', 'metal3'): 'via2', ('metal1', 'metal2'): 'via1'}


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
    s, e = size / 2.0, enc
    c.rect(lower, x - s - e, y - s - e, x + s + e, y + s + e)
    c.rect(upper, x - s - e, y - s - e, x + s + e, y + s + e)
    c.rect(VIA_NAME[(lower, upper)], x - s, y - s, x + s, y + s)


def down_to(c, x, y, top, bottom):
    i = VIA_ORDER.index(top)
    j = VIA_ORDER.index(bottom)
    while i < j:
        c.rect(VIA_ORDER[i], x - 0.21, y - 0.21, x + 0.21, y + 0.21)
        c.rect(VIA_ORDER[i + 1], x - 0.21, y - 0.21, x + 0.21, y + 0.21)
        c.rect(VIA_NAME[(VIA_ORDER[i + 1], VIA_ORDER[i])],
               x - 0.13, y - 0.13, x + 0.13, y + 0.13)
        i += 1


def main():
    c = Canvas(library_dir=str(LAYOUT))

    # ---- CSS: 4 x 10 MIM array (40 unit caps) ----
    # local bbox x -8..86, y -12..151.5; placed at (30, 20)
    c.use('cap_mim_array', 'C1', 30.0, 20.0)
    top_pad = (24.0, 170.5)      # top-plate landing pad (metal5)
    bot_pad = (24.0, 9.5)        # bottom-plate landing pad (metal5)

    # ---- RSS: horizontal at y = 200, pads at 150.8 and 409.2 ----
    c.use('ppolyf_u_3k_rss', 'R1', 280.0, 200.0, rot=90)

    # ---- MNRESET: wide nfet at (450, 200) ----
    c.use('nfet_03v3_w2_l05_wide', 'M1', 450.0, 200.0)
    # terminals: D(452.4,201.7) S(447.6,201.7) G(450.0,201.3) B(448.75,198.9)

    # ---- VREF_SS: cap top -> RSS pad1 -> nfet drain ----
    wire(c, 'metal5', top_pad, (top_pad[0], 184.0), width=0.8)
    wire(c, 'metal5', (top_pad[0], 184.0), (130.0, 184.0), width=0.8)
    down_to(c, 130.0, 184.0, 'metal5', 'metal2')
    wire(c, 'metal2', (130.0, 184.0), (130.0, 204.0))
    wire(c, 'metal2', (130.0, 204.0), (452.4, 204.0))
    via(c, 150.8, 204.0, 'metal1', 'metal2')
    wire(c, 'metal1', (150.8, 204.0), (150.8, 200.0))     # RSS pad 1
    wire(c, 'metal2', (452.4, 204.0), (452.4, 201.7))
    via(c, 452.4, 201.7, 'metal1', 'metal2')              # nfet drain
    c.label('metal2', 200.0, 203.6, 202.0, 204.4, 'VREF_SS', port='VREF_SS')

    # ---- VSS: cap bottom -> nfet source + bulk ----
    wire(c, 'metal5', bot_pad, (bot_pad[0], 4.0), width=0.8)
    wire(c, 'metal5', (bot_pad[0], 4.0), (430.0, 4.0), width=0.8)
    down_to(c, 430.0, 4.0, 'metal5', 'metal2')
    wire(c, 'metal2', (430.0, 4.0), (430.0, 201.7))
    wire(c, 'metal2', (430.0, 201.7), (447.6, 201.7))
    via(c, 447.6, 201.7, 'metal1', 'metal2')              # source
    wire(c, 'metal2', (430.0, 190.0), (448.75, 190.0))
    wire(c, 'metal2', (448.75, 190.0), (448.75, 198.9))
    via(c, 448.75, 198.9, 'metal1', 'metal2')             # bulk
    c.label('metal5', 200.0, 3.6, 202.0, 4.4, 'VSS', port='VSS')

    # ---- VREF: RSS pad 2, on metal3 to clear the rails ----
    via(c, 409.2, 200.0, 'metal1', 'metal2')
    wire(c, 'metal2', (409.2, 200.0), (409.2, 202.0))
    via(c, 409.2, 202.0, 'metal2', 'metal3')
    wire(c, 'metal3', (409.2, 202.0), (409.2, 215.0))
    wire(c, 'metal3', (409.2, 215.0), (420.0, 215.0))
    c.label('metal3', 418.0, 214.6, 420.0, 215.4, 'VREF', port='VREF')

    # ---- ENB: nfet gate (poly contacted at the top), down on metal2 ----
    wire(c, 'metal2', (450.0, 202.25), (450.0, 199.0))
    via(c, 450.0, 199.0, 'metal2', 'metal3')
    wire(c, 'metal3', (450.0, 199.0), (462.0, 199.0))
    wire(c, 'metal3', (462.0, 199.0), (462.0, 210.0))
    c.label('metal3', 461.6, 208.0, 462.4, 210.0, 'ENB', port='ENB')

    c.write(str(LAYOUT / 'ldo_softstart.mag'))
    print('wrote layout/ldo_softstart.mag')


if __name__ == '__main__':
    main()
