#!/usr/bin/env python3
"""Build layout/ldo_power_stage.mag: pass FET + gate pull-up + discharge.

    XMPASS  pfet 400 x W50/L0.28  S=VIN G=GATE D=VOUT B=VIN   (array)
    XMPOFF  pfet W40/L0.5         S=VIN D=GATE G=EN  B=VIN
    XMNDIS  nfet W20/L0.5         D=DIS G=ENB S=VSS  B=VSS
    XRDIS   ppolyf_u W20/L28.229  DIS-VOUT
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from magcanvas import Canvas
from build_bias import wire, via, terms
from build_devices import array_fet

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / 'layout'


def arr_terms(w, l, n, x, y):
    """Terminal anchors of an array_fet cell placed at (x, y)."""
    P = l + 0.64
    hw = w / 2.0
    dl = -0.55
    dr = (n - 1) * P + l + 0.55
    return {
        'G': (x + dl, y + hw + 0.87),
        'S': (x + dr - 0.6, y - hw - 3.35),
        'D': (x + dr - 0.6, y - hw - 4.55),
        'B': (x + dl - 0.725, y),
    }


def main():
    c = Canvas(library_dir=str(LAYOUT))
    # pass array: 400 fingers of W=50, L=0.28 at (0,100)
    c.flatten('arr_p50_l028_n400', 0.0, 100.0)
    PA = arr_terms(50.0, 0.28, 400, 0.0, 100.0)
    # gate pull-up pfet W=40 L=0.5 at (380,100)
    c.flatten('arr_p40_l05_n1', 380.0, 100.0)
    PO = arr_terms(40.0, 0.5, 1, 380.0, 100.0)
    # discharge nfet W=20 L=0.5 at (390,50)
    c.flatten('arr_n20_l05_n1', 390.0, 50.0)
    ND = arr_terms(20.0, 0.5, 1, 390.0, 50.0)
    # discharge resistor W=20 L=28.229 at (410,55), vertical
    c.flatten('ppolyf_u_xrdis', 410.0, 55.0)
    r_hi = (410.0, 55.0 + 28.229 / 2.0 + 0.275)
    r_lo = (410.0, 55.0 - 28.229 / 2.0 - 0.275)

    # ---- VIN: short end-taps only (no metal3 along the bus row) ------
    # pass source bus left end; ring tied to it
    via(c, *PA['B'], 'metal1', 'metal2')
    wire(c, 'metal2', PA['B'], (PA['B'][0], PA['S'][1]))
    via(c, PA['B'][0], PA['S'][1], 'metal2', 'metal3', enc=0.07)
    c.rect('metal3', -1.40, 71.40, -0.50, 71.90)
    via(c, -1.15, 71.65, 'metal2', 'metal3', enc=0.07)
    wire(c, 'metal2', (-1.15, 71.65), (-1.15, 64.0))
    via(c, -1.15, 64.0, 'metal2', 'metal3', enc=0.07)
    # pull-up source bus left end: one metal3 tongue, two well-separated
    # metal2 drops (source rail and guard-ring tie)
    c.rect('metal3', 377.00, 76.40, 379.05, 76.90)
    via(c, 377.60, 76.65, 'metal2', 'metal3', enc=0.07)
    wire(c, 'metal2', (377.60, 76.65), (377.60, 64.0))
    via(c, 377.60, 64.0, 'metal2', 'metal3', enc=0.07)
    via(c, *PO['B'], 'metal1', 'metal2')
    wire(c, 'metal2', PO['B'], (PO['B'][0], PO['S'][1]))
    via(c, PO['B'][0], PO['S'][1], 'metal2', 'metal3', enc=0.07)
    # VIN rail
    wire(c, 'metal3', (-1.15, 64.0), (383.0, 64.0), width=0.6)
    wire(c, 'metal3', (377.60, 64.0), (377.60, 76.65))
    c.label('metal3', 382.4, 63.4, 383.6, 64.8, 'VIN', port='VIN')

    # ---- GATE: pass gate + pull-up drain (right end tap) ------------
    c.rect('metal3', 381.45, 75.20, 382.00, 75.70)
    via(c, 381.75, 75.45, 'metal2', 'metal3', enc=0.07)
    wire(c, 'metal2', (381.75, 75.45), (381.75, 140.0))
    wire(c, 'metal2', (381.75, 140.0), (-3.0, 140.0))
    wire(c, 'metal2', (-3.0, 140.0), (-3.0, PA['G'][1]))
    wire(c, 'metal2', (-3.0, PA['G'][1]), PA['G'])
    c.label('metal2', -3.6, 139.0, -2.4, 141.0, 'GATE', port='GATE')

    # ---- EN: pull-up gate -------------------------------------------
    wire(c, 'metal2', PO['G'], (PO['G'][0], 132.0))
    c.label('metal2', PO['G'][0] - 0.6, 131.6, PO['G'][0] + 0.6, 132.4,
            'EN', port='EN')

    # ---- VOUT: pass drain right end + resistor top ------------------
    c.rect('metal3', 368.20, 70.20, 369.10, 70.70)
    via(c, 368.80, 70.45, 'metal2', 'metal3', enc=0.07)
    wire(c, 'metal2', (368.80, 70.45), (368.80, 62.0))
    via(c, 368.80, 62.0, 'metal2', 'metal3', enc=0.07)
    wire(c, 'metal3', (368.80, 62.0), (r_hi[0], 62.0))
    wire(c, 'metal3', (r_hi[0], 62.0), (r_hi[0], r_hi[1]))
    via(c, *r_hi, 'metal1', 'metal2')
    via(c, r_hi[0], r_hi[1], 'metal2', 'metal3', enc=0.07)
    c.label('metal3', r_hi[0] - 0.6, 61.4, r_hi[0] + 0.6, 62.6,
            'VOUT', port='VOUT')

    # ---- DIS: resistor bottom + nfet drain --------------------------
    via(c, *ND['D'], 'metal2', 'metal3', enc=0.07)
    wire(c, 'metal2', ND['D'], (ND['D'][0], 33.0))
    via(c, ND['D'][0], 33.0, 'metal2', 'metal3', enc=0.07)
    via(c, *r_lo, 'metal1', 'metal2')
    wire(c, 'metal2', r_lo, (r_lo[0], 33.0))
    via(c, r_lo[0], 33.0, 'metal2', 'metal3', enc=0.07)
    wire(c, 'metal3', (ND['D'][0], 33.0), (r_lo[0], 33.0))

    # ---- ENB: nfet gate ---------------------------------------------
    wire(c, 'metal2', ND['G'], (ND['G'][0], 66.0))
    c.label('metal2', ND['G'][0] - 0.6, 65.6, ND['G'][0] + 0.6, 66.4,
            'ENB', port='ENB')

    # ---- VSS: nfet source + bulk ring -------------------------------
    via(c, *ND['B'], 'metal1', 'metal2')
    wire(c, 'metal2', ND['B'], (ND['B'][0], ND['S'][1]))
    via(c, ND['B'][0], ND['S'][1], 'metal2', 'metal3', enc=0.07)
    wire(c, 'metal3', (ND['B'][0], ND['S'][1]),
         (ND['S'][0] + 1.0, ND['S'][1]))
    wire(c, 'metal3', (ND['S'][0] - 1.0, ND['S'][1]), (ND['S'][0] + 1.0,
                                                      ND['S'][1]))
    wire(c, 'metal3', (ND['S'][0] - 1.0, ND['S'][1]), (375.0, ND['S'][1]))
    # label on the guard-ring tie's metal2 (definitely the VSS net)
    c.label('metal2', ND['B'][0] - 0.6, 43.0, ND['B'][0] + 0.6, 44.0,
            'VSS', port='VSS')

    c.write(str(LAYOUT / 'ldo_power_stage.mag'))
    print('wrote layout/ldo_power_stage.mag')


if __name__ == '__main__':
    main()
