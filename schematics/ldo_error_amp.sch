v {xschem version=3.4.8RC file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Balanced two-stage amplifier - experimental single global LDO loop} -200 -240 0 0 0.45 0.45 {}
C {iopin.sym} -200 -160 0 0 {name=p0 lab=VIN}
C {iopin.sym} -20 -160 0 0 {name=p1 lab=VSS}
C {iopin.sym} 160 -160 0 0 {name=p2 lab=PB}
C {iopin.sym} 340 -160 0 0 {name=p3 lab=ENB}
C {iopin.sym} 520 -160 0 0 {name=p4 lab=STBY}
C {iopin.sym} 700 -160 0 0 {name=p5 lab=VREF}
C {iopin.sym} 880 -160 0 0 {name=p6 lab=VFB}
C {iopin.sym} 1060 -160 0 0 {name=p7 lab=GATE}
C {gf180mcu_fd_pr/pfet_03v3.sym} 0 100 0 0 {name=MPEN model=pfet_03v3 spiceprefix=X W=50u L=0.5u nf=1 m=4 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 20 100 65 100 {lab=VIN}
C {lab_pin.sym} 65 100 0 1 {name=l1 lab=VIN}
N 20 70 20 0 {lab=VIN}
C {lab_pin.sym} 20 0 0 0 {name=l2 lab=VIN}
N -20 100 -65 100 {lab=ENB}
C {lab_pin.sym} -65 100 0 0 {name=l3 lab=ENB}
N 20 130 20 180 {lab=VP}
N 20 180 1460 180 {lab=VP}
C {lab_pin.sym} 20 180 0 0 {name=l4 lab=VP}
C {gf180mcu_fd_pr/pfet_03v3.sym} 0 280 0 0 {name=MPBIAS model=pfet_03v3 spiceprefix=X W=2u L=2u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 20 280 65 280 {lab=VIN}
C {lab_pin.sym} 65 280 0 1 {name=l5 lab=VIN}
N -20 280 -65 280 {lab=PB}
C {lab_pin.sym} -65 280 0 0 {name=l6 lab=PB}
N 20 180 20 250 {lab=VP}
N 20 310 20 400 {lab=NB}
N 20 400 20 510 {lab=NB}
C {lab_pin.sym} 20 400 0 0 {name=l7 lab=NB}
C {gf180mcu_fd_pr/nfet_03v3.sym} 0 540 0 0 {name=MNBIAS model=nfet_03v3 spiceprefix=X W=16u L=2u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 20 540 65 540 {lab=VSS}
C {lab_pin.sym} 65 540 0 1 {name=l8 lab=VSS}
N -20 540 -80 540 {lab=NB}
N -80 540 -80 400 {lab=NB}
N -80 400 20 400 {lab=NB}
N 20 570 20 760 {lab=VSS}
C {gf180mcu_fd_pr/pfet_03v3.sym} 200 280 0 0 {name=MPBOOST model=pfet_03v3 spiceprefix=X W=50u L=2u nf=1 m=2 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 220 280 265 280 {lab=VIN}
C {lab_pin.sym} 265 280 0 1 {name=l9 lab=VIN}
N 220 180 220 250 {lab=VP}
N 180 280 135 280 {lab=PB}
C {lab_pin.sym} 135 280 0 0 {name=l10 lab=PB}
N 220 310 220 400 {lab=RUN_BIAS}
C {gf180mcu_fd_pr/pfet_03v3.sym} 200 430 0 0 {name=MPMODE model=pfet_03v3 spiceprefix=X W=40u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 220 430 265 430 {lab=VIN}
C {lab_pin.sym} 265 430 0 1 {name=l11 lab=VIN}
N 180 430 135 430 {lab=MODEG}
C {lab_pin.sym} 135 430 0 0 {name=l12 lab=MODEG}
C {gf180mcu_fd_pr/ppolyf_u_3k.sym} 300 620 3 0 {name=RMODE_D W=0.8u L=257.311u model=ppolyf_u_3k spiceprefix=X m=1}
C {lab_pin.sym} 300 640 0 0 {name=lrb7 lab=VSS}
C {gf180mcu_fd_pr/cap_mim_analog.sym} 400 620 0 0 {name=CMODE_D W=20u L=12.2u model=cap_mim_2f0_m4m5_noshield spiceprefix=X m=10}
N 180 430 180 590 {lab=MODEG}
N 180 590 400 590 {lab=MODEG}
N 330 590 330 620 {lab=MODEG}
N 400 650 400 690 {lab=VSS}
C {lab_pin.sym} 400 690 0 1 {name=l43 lab=VSS}
N 270 620 270 660 {lab=STBY}
C {lab_pin.sym} 270 660 0 0 {name=l45 lab=STBY}
N 220 460 100 460 {lab=NB}
N 100 460 100 400 {lab=NB}
N 100 400 20 400 {lab=NB}
C {gf180mcu_fd_pr/pfet_03v3.sym} 400 260 0 0 {name=MPLA model=pfet_03v3 spiceprefix=X W=20u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 420 260 465 260 {lab=VIN}
C {lab_pin.sym} 465 260 0 1 {name=l13 lab=VIN}
N 420 180 420 230 {lab=VP}
N 380 260 335 260 {lab=CMAVG}
C {lab_pin.sym} 335 260 0 0 {name=l14 lab=CMAVG}
C {gf180mcu_fd_pr/pfet_03v3.sym} 800 260 0 0 {name=MPLB model=pfet_03v3 spiceprefix=X W=20u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 820 260 865 260 {lab=VIN}
C {lab_pin.sym} 865 260 0 1 {name=l15 lab=VIN}
N 820 180 820 230 {lab=VP}
N 780 260 735 260 {lab=CMAVG}
C {lab_pin.sym} 735 260 0 0 {name=l16 lab=CMAVG}
N 420 290 420 330 {lab=A}
N 420 330 420 450 {lab=A}
N 820 290 820 330 {lab=EA}
N 820 330 820 450 {lab=EA}
C {gf180mcu_fd_pr/ppolyf_u.sym} 520 330 3 0 {name=RA W=1u L=222.66u model=ppolyf_u spiceprefix=X m=1}
C {lab_pin.sym} 520 350 0 0 {name=lrb8 lab=VSS}
C {gf180mcu_fd_pr/ppolyf_u.sym} 720 330 3 0 {name=RB W=1u L=222.66u model=ppolyf_u spiceprefix=X m=1}
C {lab_pin.sym} 720 350 0 0 {name=lrb9 lab=VSS}
N 420 330 490 330 {lab=A}
N 550 330 620 330 {lab=CMAVG}
N 620 330 690 330 {lab=CMAVG}
C {lab_pin.sym} 620 330 0 0 {name=l17 lab=CMAVG}
N 750 330 820 330 {lab=EA}
C {gf180mcu_fd_pr/nfet_03v3.sym} 400 480 0 0 {name=MNREF model=nfet_03v3 spiceprefix=X W=40u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 420 480 465 480 {lab=VSS}
C {lab_pin.sym} 465 480 0 1 {name=l18 lab=VSS}
N 380 480 335 480 {lab=VREF}
C {lab_pin.sym} 335 480 0 0 {name=l19 lab=VREF}
C {gf180mcu_fd_pr/nfet_03v3.sym} 800 480 0 0 {name=MNFB model=nfet_03v3 spiceprefix=X W=40u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 820 480 865 480 {lab=VSS}
C {lab_pin.sym} 865 480 0 1 {name=l20 lab=VSS}
N 780 480 735 480 {lab=VFB}
C {lab_pin.sym} 735 480 0 0 {name=l21 lab=VFB}
N 420 510 420 560 {lab=TAIL}
N 820 510 820 560 {lab=TAIL}
N 420 560 620 560 {lab=TAIL}
N 620 560 820 560 {lab=TAIL}
N 620 560 620 620 {lab=TAIL}
C {gf180mcu_fd_pr/nfet_03v3.sym} 600 650 0 0 {name=MNTAIL model=nfet_03v3 spiceprefix=X W=32u L=2u nf=1 m=2 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 620 650 665 650 {lab=VSS}
C {lab_pin.sym} 665 650 0 1 {name=l22 lab=VSS}
N 580 650 535 650 {lab=NB}
C {lab_pin.sym} 535 650 0 0 {name=l23 lab=NB}
N 620 680 620 760 {lab=VSS}
C {gf180mcu_fd_pr/pfet_03v3.sym} 1120 260 0 0 {name=MPMIRDRV model=pfet_03v3 spiceprefix=X W=40u L=1u nf=1 m=2 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 1140 260 1185 260 {lab=VIN}
C {lab_pin.sym} 1185 260 0 1 {name=l24 lab=VIN}
C {gf180mcu_fd_pr/pfet_03v3.sym} 1440 260 0 0 {name=MPDRV model=pfet_03v3 spiceprefix=X W=40u L=1u nf=1 m=2 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 1460 260 1505 260 {lab=VIN}
C {lab_pin.sym} 1505 260 0 1 {name=l25 lab=VIN}
N 1140 180 1140 230 {lab=VP}
N 1460 180 1460 230 {lab=VP}
N 420 330 320 330 {lab=A}
N 320 330 320 60 {lab=A}
N 320 60 1080 60 {lab=A}
N 1080 60 1080 260 {lab=A}
N 1080 260 1100 260 {lab=A}
N 820 330 900 330 {lab=EA}
N 900 330 900 100 {lab=EA}
N 900 100 1400 100 {lab=EA}
N 1400 100 1400 260 {lab=EA}
N 1400 260 1420 260 {lab=EA}
N 1140 290 1140 400 {lab=Q}
N 1140 400 1140 510 {lab=Q}
C {gf180mcu_fd_pr/nfet_03v3.sym} 1120 540 0 0 {name=MNMIRDRV model=nfet_03v3 spiceprefix=X W=40u L=1u nf=1 m=2 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 1140 540 1185 540 {lab=VSS}
C {lab_pin.sym} 1185 540 0 1 {name=l26 lab=VSS}
N 1100 540 1080 540 {lab=Q}
N 1080 540 1080 400 {lab=Q}
N 1080 400 1140 400 {lab=Q}
N 1140 400 1360 400 {lab=Q}
N 1360 400 1360 540 {lab=Q}
N 1360 540 1420 540 {lab=Q}
C {gf180mcu_fd_pr/nfet_03v3.sym} 1440 540 0 0 {name=MNDRV model=nfet_03v3 spiceprefix=X W=40u L=1u nf=1 m=2 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 1460 540 1505 540 {lab=VSS}
C {lab_pin.sym} 1505 540 0 1 {name=l27 lab=VSS}
N 1460 290 1460 400 {lab=GATE}
N 1460 400 1460 510 {lab=GATE}
N 1460 400 1600 400 {lab=GATE}
C {lab_pin.sym} 1600 400 0 1 {name=l28 lab=GATE}
N 1140 570 1140 760 {lab=VSS}
N 1460 570 1460 760 {lab=VSS}
N 20 760 620 760 {lab=VSS}
N 620 760 1140 760 {lab=VSS}
N 1140 760 1460 760 {lab=VSS}
C {lab_pin.sym} 20 760 0 0 {name=l29 lab=VSS}
C {lab_wire.sym} 420 400 0 0 {name=l30 lab=A}
C {lab_wire.sym} 820 400 0 0 {name=l31 lab=EA}
C {lab_wire.sym} 1140 400 0 0 {name=l32 lab=Q}
C {lab_wire.sym} 620 560 0 0 {name=l33 lab=TAIL}
C {lab_wire.sym} 220 350 0 0 {name=l34 lab=RUN_BIAS}
C {gf180mcu_fd_pr/ppolyf_u.sym} 1000 620 3 0 {name=RZA W=10u L=28.229u model=ppolyf_u spiceprefix=X m=1}
C {lab_pin.sym} 1000 640 0 0 {name=lrb10 lab=VSS}
N 970 620 940 620 {lab=EA}
N 1030 620 1030 650 {lab=MC}
C {gf180mcu_fd_pr/cap_mim_analog.sym} 1030 680 0 0 {name=CM W=20u L=12.2u model=cap_mim_2f0_m4m5_noshield spiceprefix=X m=20}
N 1030 710 1030 740 {lab=GATE}
C {lab_wire.sym} 940 620 0 0 {name=l40 lab=EA}
C {lab_wire.sym} 1030 620 0 0 {name=l41 lab=MC}
C {lab_wire.sym} 1030 740 0 0 {name=l42 lab=GATE}
T {RUN: MPBOOST adds bias; STBY=1 disables it. PB adaptation remains active only in RUN.
A/EA average sets first-stage common mode. A drives mirrored sink; EA drives pull-up.
VFB rises -> A rises / EA falls -> less sink / more source -> GATE rises -> pass current falls.
External MPOFF holds GATE at VIN in OFF. Main compensation is in ldo_top; RZA/CM feed the
interstage zero across the driver. All R/C remain ideal.
MPMODE gate is delayed by RMODE_D/CMODE_D (1 Mohm, 5 pF, ~5 us) so the boost bias
turns on after the STANDBY compensation zero has re-opened on mode changes.} -180 840 0 0 0.3 0.3 {}
