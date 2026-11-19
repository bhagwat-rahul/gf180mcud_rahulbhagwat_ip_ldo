#!/usr/bin/env python3
"""Build layout/ldo_startup.mag (wired).

Placement: cap_80, cap_62, cap_40, cap_205; RSWGC/RSWGCC/RBLEDPD2 on
y=300/306/312; RBLEDPD1 vertical at x=1200; RBLD horizontal at y=365;
switches MPCC (1150), MPCG (1165), MNBLD (1180).

Routing: cap plates metal5 -> metal3 -> metal2 verticals in the middle
band; metal3 horizontals at y=280/290/315/340/345/350/355/388; device
gates drop on metal2.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from magcanvas import Canvas
from build_bias import wire, via
from build_softstart import down_to

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / 'layout'


def main():
    c = Canvas(library_dir=str(LAYOUT))
    c.flatten('cap_80', 0.0, 80.0)
    c.flatten('cap_62', 0.0, -40.0)
    c.flatten('cap_40', 450.0, -40.0)
    c.flatten('cap_205', 880.0, 80.0)
    for y in (300.0, 306.0, 312.0):
        c.flatten('ppolyf_u_3k_rswgc', 1008.93, y, rot=90)
    c.flatten('ppolyf_u_3k_rbledpd1', 1200.0, 360.0)
    c.flatten('ppolyf_u_rbld', 1099.85, 365.0, rot=90)
    c.flatten('amp_p50_l028_n10', 1150.0, 325.0)
    c.flatten('amp_p50_l028_n4', 1165.0, 325.0)
    c.flatten('amp_n10_l05', 1180.0, 325.0)

    def m1(x, y):
        via(c, x, y, 'metal1', 'metal2', enc=0.07)
        via(c, x, y, 'metal2', 'metal3', enc=0.07)

    def m2(x, y):
        via(c, x, y, 'metal2', 'metal3', enc=0.07)

    def m5(x, y):
        down_to(c, x, y, 'metal5', 'metal3')

    # COMP2
    m5(-23.0, 328.5)
    wire(c, 'metal3', (-23.0, 328.5), (-23.0, 338.0))
    c.label('metal3', -23.6, 337.6, -22.4, 338.4, 'COMP2', port='COMP2')

    # CCF: cap_80 BOT -> metal2 x=27 -> metal3 y=290 -> XMPCC.D
    m5(27.0, 51.5)
    m2(27.0, 51.5)
    wire(c, 'metal2', (27.0, 51.5), (27.0, 290.0))
    m2(27.0, 290.0)
    wire(c, 'metal3', (27.0, 290.0), (1158.0, 290.0))
    wire(c, 'metal3', (1158.0, 290.0), (1158.0, 295.45))
    wire(c, 'metal3', (1158.0, 295.45), (1157.96, 295.45))

    # CGFF: cap_40 BOT -> metal2 x=444 -> y=280 -> XMPCG.D
    m5(444.0, -50.5)
    m2(444.0, -50.5)
    wire(c, 'metal2', (444.0, -50.5), (444.0, 280.0))
    m2(444.0, 280.0)
    wire(c, 'metal3', (444.0, 280.0), (1167.0, 280.0))
    wire(c, 'metal3', (1167.0, 280.0), (1167.0, 295.45))
    wire(c, 'metal3', (1167.0, 295.45), (1167.44, 295.45))

    # SWGC: cap_62 TOP -> metal2 -6 -> y=340 -> gate 1164.45; branch 870->880
    m5(-6.0, 17.0)
    m2(-6.0, 17.0)
    wire(c, 'metal2', (-6.0, 17.0), (-6.0, 340.0))
    m2(-6.0, 340.0)
    wire(c, 'metal3', (-6.0, 340.0), (1164.45, 340.0))
    m2(1164.45, 340.0)
    m1(880.0, 300.0)
    wire(c, 'metal3', (870.0, 340.0), (870.0, 300.0))
    wire(c, 'metal3', (870.0, 300.0), (880.0, 300.0))

    # SWGCC: cap_205 TOP -> metal2 874 -> y=345 -> gate 1149.45;
    # branch to RSWGCC 880,306; metal2 to 388 -> RBLEDPD1 top 1200,388.4
    m5(874.0, 292.0)
    m2(874.0, 292.0)
    wire(c, 'metal2', (874.0, 292.0), (874.0, 388.4))
    m2(874.0, 345.0)
    wire(c, 'metal3', (874.0, 345.0), (1149.45, 345.0))
    m2(1149.45, 345.0)
    m1(880.0, 306.0)
    m2(874.0, 306.0)
    wire(c, 'metal3', (874.0, 306.0), (880.0, 306.0))
    m2(874.0, 388.4)
    wire(c, 'metal3', (874.0, 388.4), (1200.0, 388.4))
    m1(1200.0, 388.4)

    # ENB
    m1(1137.86, 300.0)
    m1(1137.86, 306.0)
    wire(c, 'metal3', (1137.86, 300.0), (1137.86, 306.0))
    c.label('metal3', 1137.3, 302.6, 1138.4, 303.4, 'ENB', port='ENB')

    # VIN
    m5(-6.0, -50.5)
    m5(874.0, 69.5)
    wire(c, 'metal3', (-6.0, -50.5), (-6.0, -56.0))
    wire(c, 'metal3', (-6.0, -56.0), (860.0, -56.0))
    wire(c, 'metal3', (860.0, -56.0), (860.0, 69.5))
    wire(c, 'metal3', (860.0, 69.5), (874.0, 69.5))
    c.label('metal3', 860.4, -56.6, 861.4, -55.4, 'VIN', port='VIN')

    # VSS: RBLEDPD2 pad -> metal2 870 -> y=-10 -> x=1192 -> up -> taps
    m1(880.0, 312.0)
    wire(c, 'metal3', (880.0, 312.0), (870.0, 312.0))
    m2(870.0, 312.0)
    wire(c, 'metal2', (870.0, 312.0), (870.0, -10.0))
    m2(870.0, -10.0)
    wire(c, 'metal3', (870.0, -10.0), (1192.0, -10.0))
    wire(c, 'metal3', (1192.0, -10.0), (1192.0, 320.0))
    wire(c, 'metal3', (1192.0, 320.0), (1178.55, 320.0))
    wire(c, 'metal3', (1178.55, 320.0), (1178.55, 325.0))
    m1(1178.55, 325.0)
    wire(c, 'metal3', (1185.0, 320.0), (1185.0, 316.65))
    c.label('metal3', 1189.0, -10.6, 1190.0, -9.6, 'VSS', port='VSS')

    # VOUT: S buses -> metal3 x=1145 -> metal2 up to 365 -> RBLD left pad
    wire(c, 'metal3', (1149.68, 296.65), (1164.68, 296.65))
    wire(c, 'metal3', (1149.68, 296.65), (1145.0, 296.65))
    m2(1145.0, 296.65)
    wire(c, 'metal2', (1145.0, 296.65), (1145.0, 365.0))
    m2(1145.0, 365.0)
    wire(c, 'metal3', (1145.0, 365.0), (1128.7, 365.0))
    m1(1128.7, 365.0)
    # bulk rings to VOUT
    m1(1148.55, 325.0)
    m1(1163.55, 325.0)
    wire(c, 'metal3', (1148.55, 325.0), (1163.55, 325.0))
    wire(c, 'metal3', (1148.55, 325.0), (1148.55, 296.65))
    c.label('metal3', 1150.0, 296.25, 1151.0, 297.05, 'VOUT', port='VOUT')

    # BLD: RBLD left pad -> metal2 1071 -> y=315.45 -> XMNBLD.D
    m1(1071.0, 365.0)
    wire(c, 'metal2', (1071.0, 365.0), (1071.0, 315.45))
    m2(1071.0, 315.45)
    wire(c, 'metal3', (1071.0, 315.45), (1180.82, 315.45))

    # BLED: XMNBLD gate -> metal2 up to 355 -> metal3 -> RBLEDPD1 bottom
    m2(1179.45, 330.87)
    wire(c, 'metal2', (1179.45, 355.0), (1179.45, 330.87))
    m2(1179.45, 355.0)
    wire(c, 'metal3', (1179.45, 355.0), (1200.0, 355.0))
    wire(c, 'metal3', (1200.0, 355.0), (1200.0, 331.6))
    m1(1200.0, 331.6)

    # GATE port
    m5(444.0, 32.5)
    wire(c, 'metal3', (444.0, 32.5), (444.0, 44.0))
    c.label('metal3', 443.4, 43.6, 444.6, 44.4, 'GATE', port='GATE')

    # PGOOD stub
    wire(c, 'metal3', (1230.0, 60.0), (1240.0, 60.0))
    c.label('metal3', 1238.8, 59.6, 1240.0, 60.4, 'PGOOD', port='PGOOD')

    c.write(str(LAYOUT / 'ldo_startup.mag'))
    print('wrote layout/ldo_startup.mag')


if __name__ == '__main__':
    main()
