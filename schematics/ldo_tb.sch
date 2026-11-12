v {xschem version=3.4.8RC file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {LDO simulation fixture - real GF180 MOS, ideal supplies and independent load} 0 -170 0 0 0.45 0.45 {}
C {ldo_top.sym} 250 50 0 0 {name=XDUT}
C {vsource.sym} 650 100 0 0 {name=VSUP value=3.3 m=1}
C {vsource.sym} 950 100 0 0 {name=VREF value=1.2 m=1}
C {vsource.sym} 1250 100 0 0 {name=VEN value=3.3 m=1}
C {vsource.sym} 1550 100 0 0 {name=VSTBY value=0 m=1}
C {isource.sym} 650 400 0 0 {name=IBIAS value=1u m=1}
C {isource.sym} 950 400 0 0 {name=ILOAD value=1m m=1}
C {capa.sym} 1250 400 0 0 {name=CLOAD value=100p m=1}
C {code_shown.sym} 0 650 0 0 {name=MODELS only_toplevel=true value=".lib /foss/pdks/gf180mcuD/libs.tech/ngspice/sm141064.spice typical
.include /foss/pdks/gf180mcuD/libs.tech/ngspice/design.ngspice
.param sw_stat_global=0
.param sw_stat_mismatch=0
.control
op
print v(vout) v(pgood) i(vsup)
.endc"}
T {Nominal: 3.3 V, 1.2 V reference, 1 uA bias, 100 pF output load.
Run sim/run.py for DC, AC return ratio, dropout, sequencing,
PGOOD and independent load-step characterization.
No behavioral regulator or preannounced load control is used.} 0 1050 0 0 0.3 0.3 {}
N 100 50 60 50 {lab=VIN}
C {lab_pin.sym} 60 50 0 0 {name=l1 lab=VIN}
N 100 80 60 80 {lab=0}
C {lab_pin.sym} 60 80 0 0 {name=l2 lab=0}
N 100 110 60 110 {lab=VREF}
C {lab_pin.sym} 60 110 0 0 {name=l3 lab=VREF}
N 100 140 60 140 {lab=IBIAS}
C {lab_pin.sym} 60 140 0 0 {name=l4 lab=IBIAS}
N 100 170 60 170 {lab=EN}
C {lab_pin.sym} 60 170 0 0 {name=l5 lab=EN}
N 100 200 60 200 {lab=STBY}
C {lab_pin.sym} 60 200 0 0 {name=l6 lab=STBY}
N 400 170 440 170 {lab=VOUT}
C {lab_pin.sym} 440 170 0 1 {name=l7 lab=VOUT}
N 400 200 440 200 {lab=PGOOD}
C {lab_pin.sym} 440 200 0 1 {name=l8 lab=PGOOD}
N 650 70 650 30 {lab=VIN}
C {lab_pin.sym} 650 30 0 0 {name=l9 lab=VIN}
N 650 130 650 170 {lab=0}
C {lab_pin.sym} 650 170 0 0 {name=l10 lab=0}
N 950 70 950 30 {lab=VREF}
C {lab_pin.sym} 950 30 0 0 {name=l11 lab=VREF}
N 950 130 950 170 {lab=0}
C {lab_pin.sym} 950 170 0 0 {name=l12 lab=0}
N 1250 70 1250 30 {lab=EN}
C {lab_pin.sym} 1250 30 0 0 {name=l13 lab=EN}
N 1250 130 1250 170 {lab=0}
C {lab_pin.sym} 1250 170 0 0 {name=l14 lab=0}
N 1550 70 1550 30 {lab=STBY}
C {lab_pin.sym} 1550 30 0 0 {name=l15 lab=STBY}
N 1550 130 1550 170 {lab=0}
C {lab_pin.sym} 1550 170 0 0 {name=l16 lab=0}
N 650 370 650 330 {lab=0}
C {lab_pin.sym} 650 330 0 0 {name=l17 lab=0}
N 650 430 650 470 {lab=IBIAS}
C {lab_pin.sym} 650 470 0 0 {name=l18 lab=IBIAS}
N 950 370 950 330 {lab=VOUT}
C {lab_pin.sym} 950 330 0 0 {name=l19 lab=VOUT}
N 950 430 950 470 {lab=0}
C {lab_pin.sym} 950 470 0 0 {name=l20 lab=0}
N 1250 370 1250 330 {lab=VOUT}
C {lab_pin.sym} 1250 330 0 0 {name=l21 lab=VOUT}
N 1250 430 1250 470 {lab=0}
C {lab_pin.sym} 1250 470 0 0 {name=l22 lab=0}
