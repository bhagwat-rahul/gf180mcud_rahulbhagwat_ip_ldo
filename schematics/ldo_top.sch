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
C {gf180mcu_fd_pr/ppolyf_u_3k.sym} 1640 400 0 0 {name=RTOP W=2u L=399.978u model=ppolyf_u_3k spiceprefix=X m=1}
C {lab_pin.sym} 1620 400 0 0 {name=lrb0 lab=VSS}
C {gf180mcu_fd_pr/ppolyf_u_3k.sym} 1640 600 0 0 {name=RBOT W=2u L=799.978u model=ppolyf_u_3k spiceprefix=X m=1}
C {lab_pin.sym} 1620 600 0 0 {name=lrb1 lab=VSS}
N 1640 220 1640 370 {lab=VOUT}
N 1640 430 1640 500 {lab=VFB}
N 1640 500 1640 570 {lab=VFB}
N 1640 500 500 500 {lab=VFB}
N 500 500 500 250 {lab=VFB}
N 500 250 550 250 {lab=VFB}
C {lab_pin.sym} 1640 500 0 1 {name=l4 lab=VFB}
N 850 130 900 130 {lab=STBY}
C {lab_pin.sym} 900 130 0 1 {name=l36 lab=STBY}
C {gf180mcu_fd_pr/cap_mim_analog.sym} 1800 400 0 0 {name=CFF W=20u L=12.2u model=cap_mim_2f0_m3m4_noshield spiceprefix=X m=2}
N 1800 220 1800 370 {lab=VOUT}
N 1800 430 1800 500 {lab=VFB}
N 1800 500 1640 500 {lab=VFB}
C {gf180mcu_fd_pr/ppolyf_u.sym} 1010 340 3 0 {name=RZERO W=20u L=22.514u model=ppolyf_u spiceprefix=X m=1}
C {lab_pin.sym} 1010 360 0 0 {name=lrb2 lab=VSS}
C {gf180mcu_fd_pr/nplus_u.sym} 1160 340 3 0 {name=RZB W=0.5u L=179.5u model=nplus_u spiceprefix=X m=1}
C {lab_pin.sym} 1160 360 0 0 {name=lrb3 lab=VSS}
C {gf180mcu_fd_pr/pfet_03v3.sym} 1280 420 3 0 {name=MSWZ model=pfet_03v3 spiceprefix=X W=50u L=0.5u nf=1 m=16 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 960 220 960 340 {lab=GATE}
N 960 340 980 340 {lab=GATE}
N 1040 340 1130 340 {lab=COMP}
C {lab_wire.sym} 1085 340 0 0 {name=l46 lab=COMP}
N 1190 340 1370 340 {lab=COMP2}
C {lab_wire.sym} 1305 340 0 0 {name=l47 lab=COMP2}
N 1100 340 1100 400 {lab=COMP}
N 1100 400 1280 400 {lab=COMP}
N 1370 340 1370 400 {lab=COMP2}
N 1370 400 1310 400 {lab=COMP2}
N 1280 440 1280 480 {lab=STBY}
C {lab_pin.sym} 1280 480 0 1 {name=l48 lab=STBY}
C {gf180mcu_fd_pr/nplus_u.sym} 1800 600 0 0 {name=RBLEED W=0.5u L=3590u model=nplus_u spiceprefix=X m=1}
C {lab_pin.sym} 1780 600 0 0 {name=lrb4 lab=VSS}
C {gf180mcu_fd_pr/pfet_03v3.sym} 2150 300 3 0 {name=MPPRE model=pfet_03v3 spiceprefix=X W=50u L=0.5u nf=1 m=30 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 2120 280 2090 280 {lab=VOUT}
N 2120 280 2150 280 {lab=VOUT}
N 2180 280 2210 280 {lab=PRE}
N 2150 320 2150 340 {lab=PREG}
C {gf180mcu_fd_pr/ppolyf_u.sym} 2210 370 0 0 {name=RPRE W=50u L=68.229u model=ppolyf_u spiceprefix=X m=4}
C {lab_pin.sym} 2190 370 0 0 {name=lrb5 lab=VSS}
N 2210 280 2210 340 {lab=PRE}
N 2210 400 2210 430 {lab=VSS}
C {gf180mcu_fd_pr/pfet_03v3.sym} 2400 300 0 0 {name=MPDIO model=pfet_03v3 spiceprefix=X W=10u L=1u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 2380 300 2380 330 {lab=PREG}
N 2380 330 2420 330 {lab=PREG}
N 2420 330 2450 330 {lab=PREG}
N 2420 270 2450 270 {lab=STBY}
N 2420 300 2450 300 {lab=VIN}
C {gf180mcu_fd_pr/ppolyf_u_3k.sym} 2600 370 0 0 {name=RPRE_D W=2u L=666.645u model=ppolyf_u_3k spiceprefix=X m=1}
C {lab_pin.sym} 2580 370 0 0 {name=lrb6 lab=VSS}
N 2600 340 2600 320 {lab=PREG}
N 2600 400 2600 420 {lab=VSS}
C {gf180mcu_fd_pr/cap_mim_analog.sym} 2700 370 0 0 {name=CPRE_D W=20u L=12.2u model=cap_mim_2f0_m3m4_noshield spiceprefix=X m=12}
N 2700 340 2700 320 {lab=PREG}
N 2700 400 2700 420 {lab=VSS}
C {lab_wire.sym} 2450 270 0 0 {name=l50 lab=STBY}
C {lab_wire.sym} 2450 300 0 0 {name=l51 lab=VIN}
C {lab_wire.sym} 2450 330 0 0 {name=l52 lab=PREG}
C {lab_wire.sym} 2600 320 0 0 {name=l53 lab=PREG}
C {lab_wire.sym} 2600 420 0 0 {name=l54 lab=VSS}
C {lab_wire.sym} 2700 320 0 0 {name=l55 lab=PREG}
C {lab_wire.sym} 2700 420 0 0 {name=l56 lab=VSS}
C {lab_wire.sym} 2000 340 0 0 {name=l40 lab=GATE}
C {lab_wire.sym} 2000 460 0 0 {name=l41 lab=VOUT}
C {lab_wire.sym} 2090 280 0 0 {name=l42 lab=VOUT}
C {lab_wire.sym} 2210 280 0 0 {name=l43 lab=PRE}
C {lab_wire.sym} 2150 340 0 0 {name=l44 lab=PREG}
C {lab_wire.sym} 2210 430 0 0 {name=l45 lab=VSS}
T {RUN: EN=1, STBY=0  |  STANDBY: EN=1, STBY=1  |  OFF: EN=0
Feedback: 600 kohm / 1.2 Mohm. RUN preload: MPPRE + 120 ohm, ~14 mA nominal and ~9 mA hot/slow, off in STANDBY.
RBLEED 360 kohm (~5 uA) keeps VOUT defined when the pass device is off.
Compensation zero: RZERO 400 ohm in RUN; STANDBY opens MSWZ so RZB 18 kohm
sets a ~20 kHz zero (STANDBY crossover is ~20 kHz, RUN crossover ~10 MHz).
Mode sequencing: preload gate PREG turns off fast through MPDIO but returns slowly
through RPRE_D/CPRE_D (1 Mohm, 6 pF); the amp delays the boost bias similarly.
PDK R/C devices; harness and package wrapper deferred.} 650 1040 0 0 0.3 0.3 {}
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
C {ldo_startup.sym} 2600 500 0 0 {name=XCS}
N 2450 500 2400 500 {lab=VIN}
C {lab_pin.sym} 2400 500 0 0 {name=lxvin lab=VIN}
N 2450 530 2400 530 {lab=VSS}
C {lab_pin.sym} 2400 530 0 0 {name=lxvss lab=VSS}
N 2450 560 2400 560 {lab=COMP2}
C {lab_pin.sym} 2400 560 0 0 {name=lxcomp2 lab=COMP2}
N 2450 590 2400 590 {lab=GATE}
C {lab_pin.sym} 2400 590 0 0 {name=lxgate lab=GATE}
N 2750 560 2800 560 {lab=VOUT}
C {lab_pin.sym} 2800 560 0 1 {name=lxvout lab=VOUT}
N 2750 590 2800 590 {lab=PGOOD}
C {lab_pin.sym} 2800 590 0 1 {name=lxpgood lab=PGOOD}
N 2750 620 2800 620 {lab=ENB}
C {lab_pin.sym} 2800 620 0 1 {name=lxenb lab=ENB}
C {iopin.sym} 1120 -90 0 0 {name=p8 lab=LDENB}
C {ldo_load.sym} 3200 500 0 0 {name=XLOAD}
N 3050 500 3000 500 {lab=VIN}
C {lab_pin.sym} 3000 500 0 0 {name=lxlvin lab=VIN}
N 3050 530 3000 530 {lab=VSS}
C {lab_pin.sym} 3000 530 0 0 {name=lxlvss lab=VSS}
N 3050 560 3000 560 {lab=VREF}
C {lab_pin.sym} 3000 560 0 0 {name=lxlvref lab=VREF}
N 3050 590 3000 590 {lab=LDENB}
C {lab_pin.sym} 3000 590 0 0 {name=lxldenb lab=LDENB}
N 3050 620 3000 620 {lab=PGOOD}
C {lab_pin.sym} 3000 620 0 0 {name=lxlpgood lab=PGOOD}
N 3050 650 3000 650 {lab=STBY}
C {lab_pin.sym} 3000 650 0 0 {name=lxlstby lab=STBY}
N 3350 560 3400 560 {lab=VOUT}
C {lab_pin.sym} 3400 560 0 0 {name=lxlvout lab=VOUT}
