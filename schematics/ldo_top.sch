v {xschem version=3.4.8RC file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {3.3 V -> 1.8 V LDO - transistor-level prototype, not layout signoff} 0 -170 0 0 0.45 0.45 {}
C {iopin.sym} 0 -90 0 0 {name=p0 lab=VIN}
C {iopin.sym} 140 -90 0 0 {name=p1 lab=VSS}
C {iopin.sym} 280 -90 0 0 {name=p2 lab=VREF}
C {iopin.sym} 420 -90 0 0 {name=p3 lab=IBIAS}
C {iopin.sym} 560 -90 0 0 {name=p4 lab=EN}
C {iopin.sym} 700 -90 0 0 {name=p5 lab=STBY}
C {iopin.sym} 840 -90 0 0 {name=p6 lab=VOUT}
C {iopin.sym} 980 -90 0 0 {name=p7 lab=PGOOD}
C {ldo_softstart.sym} 200 160 0 0 {name=XSS}
C {ldo_error_amp.sym} 700 100 0 0 {name=XEA}
C {ldo_power_stage.sym} 1250 100 0 0 {name=XPWR}
C {ldo_bias.sym} 200 650 0 0 {name=XBIAS}
C {ldo_pgood.sym} 1250 700 0 0 {name=XPG}
N 350 220 550 220 {lab=VREF_SS}
C {lab_wire.sym} 450 220 0 0 {name=l1 lab=VREF_SS}
N 850 220 960 220 {lab=GATE}
N 960 220 1100 220 {lab=GATE}
C {lab_wire.sym} 1040 220 0 0 {name=l2 lab=GATE}
N 1400 220 1640 220 {lab=VOUT}
N 1640 220 1820 220 {lab=VOUT}
C {lab_pin.sym} 1820 220 0 1 {name=l3 lab=VOUT}
C {res.sym} 1640 400 0 0 {name=RTOP value=600k m=1}
C {res.sym} 1640 600 0 0 {name=RBOT value=1.2Meg m=1}
N 1640 220 1640 370 {lab=VOUT}
N 1640 430 1640 500 {lab=VFB}
N 1640 500 1640 570 {lab=VFB}
N 1640 500 500 500 {lab=VFB}
N 500 500 500 250 {lab=VFB}
N 500 250 550 250 {lab=VFB}
C {lab_pin.sym} 1640 500 0 1 {name=l4 lab=VFB}
C {res.sym} 1010 340 3 0 {name=RZERO value=5k m=1}
C {capa.sym} 1270 340 3 0 {name=CC value=200p m=1}
N 960 220 960 340 {lab=GATE}
N 960 340 980 340 {lab=GATE}
N 1040 340 1240 340 {lab=COMP}
C {lab_wire.sym} 1140 340 0 0 {name=l5 lab=COMP}
N 1300 340 1560 340 {lab=VOUT}
N 1560 340 1560 220 {lab=VOUT}
N 1560 220 1640 220 {lab=VOUT}
C {res.sym} 1800 600 0 0 {name=RBLEED value=360k m=1}
T {RUN: EN=1, STBY=0  |  STANDBY: EN=1, STBY=1  |  OFF: EN=0
Feedback: 600 kohm / 1.2 Mohm. Preload: 360 kohm (~5 uA).
Ideal R/C targets; internal programmable load and harness wrapper deferred.} 650 1040 0 0 0.3 0.3 {}
N 50 160 10 160 {lab=VSS}
C {lab_pin.sym} 10 160 0 0 {name=l6 lab=VSS}
N 50 190 10 190 {lab=ENB}
C {lab_pin.sym} 10 190 0 0 {name=l7 lab=ENB}
N 50 220 10 220 {lab=VREF}
C {lab_pin.sym} 10 220 0 0 {name=l8 lab=VREF}
N 550 100 510 100 {lab=VIN}
C {lab_pin.sym} 510 100 0 0 {name=l9 lab=VIN}
N 550 130 510 130 {lab=VSS}
C {lab_pin.sym} 510 130 0 0 {name=l10 lab=VSS}
N 550 160 510 160 {lab=PB}
C {lab_pin.sym} 510 160 0 0 {name=l11 lab=PB}
N 550 190 510 190 {lab=ENB}
C {lab_pin.sym} 510 190 0 0 {name=l12 lab=ENB}
N 1100 100 1060 100 {lab=VIN}
C {lab_pin.sym} 1060 100 0 0 {name=l13 lab=VIN}
N 1100 130 1060 130 {lab=VSS}
C {lab_pin.sym} 1060 130 0 0 {name=l14 lab=VSS}
N 1100 160 1060 160 {lab=EN}
C {lab_pin.sym} 1060 160 0 0 {name=l15 lab=EN}
N 1100 190 1060 190 {lab=ENB}
C {lab_pin.sym} 1060 190 0 0 {name=l16 lab=ENB}
N 50 650 10 650 {lab=VIN}
C {lab_pin.sym} 10 650 0 0 {name=l17 lab=VIN}
N 50 680 10 680 {lab=VSS}
C {lab_pin.sym} 10 680 0 0 {name=l18 lab=VSS}
N 50 710 10 710 {lab=IBIAS}
C {lab_pin.sym} 10 710 0 0 {name=l19 lab=IBIAS}
N 50 740 10 740 {lab=EN}
C {lab_pin.sym} 10 740 0 0 {name=l20 lab=EN}
N 50 770 10 770 {lab=STBY}
C {lab_pin.sym} 10 770 0 0 {name=l21 lab=STBY}
N 50 800 10 800 {lab=GATE}
C {lab_pin.sym} 10 800 0 0 {name=l22 lab=GATE}
N 350 740 390 740 {lab=ENB}
C {lab_pin.sym} 390 740 0 1 {name=l23 lab=ENB}
N 350 710 390 710 {lab=PB}
C {lab_pin.sym} 390 710 0 1 {name=l24 lab=PB}
N 1100 700 1060 700 {lab=VIN}
C {lab_pin.sym} 1060 700 0 0 {name=l25 lab=VIN}
N 1100 730 1060 730 {lab=VSS}
C {lab_pin.sym} 1060 730 0 0 {name=l26 lab=VSS}
N 1100 760 1060 760 {lab=PB}
C {lab_pin.sym} 1060 760 0 0 {name=l27 lab=PB}
N 1100 790 1060 790 {lab=EN}
C {lab_pin.sym} 1060 790 0 0 {name=l28 lab=EN}
N 1100 820 1060 820 {lab=ENB}
C {lab_pin.sym} 1060 820 0 0 {name=l29 lab=ENB}
N 1100 850 1060 850 {lab=VREF}
C {lab_pin.sym} 1060 850 0 0 {name=l30 lab=VREF}
N 1100 880 1060 880 {lab=VFB}
C {lab_pin.sym} 1060 880 0 0 {name=l31 lab=VFB}
N 1400 880 1440 880 {lab=PGOOD}
C {lab_pin.sym} 1440 880 0 1 {name=l32 lab=PGOOD}
N 1640 630 1640 670 {lab=VSS}
C {lab_pin.sym} 1640 670 0 0 {name=l33 lab=VSS}
N 1800 570 1800 530 {lab=VOUT}
C {lab_pin.sym} 1800 530 0 0 {name=l34 lab=VOUT}
N 1800 630 1800 670 {lab=VSS}
C {lab_pin.sym} 1800 670 0 0 {name=l35 lab=VSS}
