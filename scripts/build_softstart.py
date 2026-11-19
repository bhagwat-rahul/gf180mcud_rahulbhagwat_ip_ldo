#!/usr/bin/env python3
"""Build layout/ldo_softstart.mag: RSS + CSS + MNRESET, fully routed.

Nets:  VSS (cap bottom plate, nfet source/bulk), VREF_SS (cap top plate,
resistor end, nfet drain), VREF (resistor other end), ENB (nfet gate).

Terminal access (probed on the gencell geometry):
  cap top plate      parent metal5 over a `mimcapcontact` band
  cap bottom plate   parent metal4 over the cell's metal4 edge
  nfet S/D           parent metal1 on the cell's metal1 end sliver
  nfet gate          parent polysilicon extension + polycontact + metal1
  nfet bulk          parent metal1 on the cell's bulk bar or tap strip
Each escape is a local pad -> via1 -> metal2 (long routes on metal2/metal3).
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
        via(c, x, y, VIA_ORDER[i + 1], VIA_ORDER[i])
        i += 1


def main():
    c = Canvas(library_dir=str(LAYOUT))

    # ---- CSS: 40 x (20 x 12.2) MIM stack, rotated to 560 x 22.4 ----
    # Cell -> block (rot 270): x' = y + 290, y' = -x + 30.
    c.use('cap_mim_2p0fF_UFNFZK', 'C1', 290.0, 30.0, rot=270)
    # top plate: metal5 over the mimcapcontact band near the left end
    c.rect('metal5', 12.0, 29.0, 21.0, 37.0)
    wire(c, 'metal5', (12.0, 33.0), (5.0, 33.0), width=1.2)
    down_to(c, 5.0, 33.0, 'metal5', 'metal2')
    # bottom plate: metal4 over the cell's metal4 at the edge
    c.rect('metal4', 12.0, 40.62, 21.0, 41.18)
    down_to(c, 16.5, 40.90, 'metal4', 'metal2')

    # ---- RSS: 0.8 x 257.311 resistor, rotated horizontal at y=60 ----
    c.use('ppolyf_u_3k_rss', 'R1', 150.0, 60.0, rot=90)
    # metal1 pads at (21.07, 60) and (278.93, 60)

    # ---- MNRESET: nfet_03v3 W=2 L=0.5 ----
    # Flattened so the top bulk bar can be removed; it seals the drain,
    # source and gate metal inside the cell.  The bottom bar still ties the
    # p-well taps together.
    c.flatten('nfet_03v3_K8XTZ5', 350.0, 50.0)
    c.remove_rect('metal1', 348.685, 51.635, 351.315, 51.865)
    # Redundant metal1 end-caps on the contact bars: the cell alone flags
    # them on M1.1/M1.3 (narrow dangling strips).  Our pads cover the bars.
    for x0, x1 in ((349.375, 349.605), (350.395, 350.625)):
        c.remove_rect('metal1', x0, 50.935, x1, 50.99)
        c.remove_rect('metal1', x0, 49.01, x1, 49.065)
    for x0, x1 in ((349.76, 349.815), (350.185, 350.24)):
        c.remove_rect('metal1', x0, 51.165, x1, 51.395)
        c.remove_rect('metal1', x0, 48.605, x1, 48.835)

    # nfet escapes (cell-relative -> absolute).  Metal1 pads may cross
    # poly/COMP; only contacts need enclosure.  Rails are spaced >= 0.28.
    c.rect('metal1', 350.43, 50.88, 350.81, 51.35)      # drain pad
    via(c, 350.67, 51.15, 'metal1', 'metal2')
    c.rect('metal1', 349.19, 50.88, 349.57, 51.35)      # source pad
    via(c, 349.33, 51.15, 'metal1', 'metal2')
    c.rect('metal1', 349.82, 50.90, 350.18, 51.60)      # gate pad on contact
    via(c, 350.0, 51.15, 'metal1', 'metal2')
    c.rect('metal1', 351.10, 48.80, 351.60, 50.40)      # bulk pad on tap strip
    via(c, 351.40, 49.60, 'metal1', 'metal2')

    # ---- VREF_SS: cap top plate -> RSS pad1 -> nfet drain ----
    wire(c, 'metal2', (5.0, 33.0), (5.0, 62.5))
    wire(c, 'metal2', (5.0, 62.5), (21.07, 62.5))
    wire(c, 'metal2', (21.07, 62.5), (21.07, 60.0))
    via(c, 21.07, 60.0, 'metal1', 'metal2')
    wire(c, 'metal2', (21.07, 62.5), (350.67, 62.5))
    wire(c, 'metal2', (350.67, 62.5), (350.67, 51.15))
    c.label('metal2', 80.2, 62.35, 81.8, 62.65, 'VREF_SS', port='VREF_SS')

    # ---- VSS: cap bottom plate -> nfet source + bulk ----
    wire(c, 'metal2', (16.5, 40.9), (16.5, 58.0))
    wire(c, 'metal2', (16.5, 58.0), (349.33, 58.0))
    wire(c, 'metal2', (349.33, 58.0), (349.33, 51.15))
    wire(c, 'metal2', (351.4, 49.6), (351.4, 46.5))
    wire(c, 'metal2', (351.4, 46.5), (345.0, 46.5))
    wire(c, 'metal2', (345.0, 46.5), (345.0, 58.0))
    c.label('metal2', 150.2, 57.85, 151.8, 58.15, 'VSS', port='VSS')

    # ---- VREF: RSS pad 2 (metal3 to clear the VREF_SS run) ----
    via(c, 278.93, 60.0, 'metal1', 'metal2')
    wire(c, 'metal2', (278.93, 60.0), (278.93, 61.0))
    via(c, 278.93, 61.0, 'metal2', 'metal3')
    wire(c, 'metal3', (278.93, 61.0), (278.93, 80.0))
    wire(c, 'metal3', (278.93, 80.0), (300.0, 80.0))
    c.label('metal3', 298.2, 79.85, 299.8, 80.15, 'VREF', port='VREF')

    # ---- ENB: nfet gate on metal3 ----
    wire(c, 'metal2', (350.0, 51.15), (350.0, 53.0), width=0.28)
    via(c, 350.0, 53.0, 'metal2', 'metal3')
    wire(c, 'metal3', (350.0, 53.0), (340.0, 53.0))
    wire(c, 'metal3', (340.0, 53.0), (340.0, 56.0))
    c.label('metal3', 339.85, 55.7, 340.15, 56.1, 'ENB', port='ENB')

    c.write(str(LAYOUT / 'ldo_softstart.mag'))
    print('wrote layout/ldo_softstart.mag')


if __name__ == '__main__':
    main()
