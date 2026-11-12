v {xschem version=3.4.8RC file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Power-good comparator - 12 MOS; final reference, hysteresis, OFF masking} 0 -170 0 0 0.45 0.45 {}
C {iopin.sym} 0 -90 0 0 {name=p0 lab=VIN}
C {iopin.sym} 140 -90 0 0 {name=p1 lab=VSS}
C {iopin.sym} 280 -90 0 0 {name=p2 lab=PB}
C {iopin.sym} 420 -90 0 0 {name=p3 lab=EN}
C {iopin.sym} 560 -90 0 0 {name=p4 lab=ENB}
C {iopin.sym} 700 -90 0 0 {name=p5 lab=VREF}
C {iopin.sym} 840 -90 0 0 {name=p6 lab=VFB}
C {iopin.sym} 980 -90 0 0 {name=p7 lab=PGOOD}
C {gf180mcu_fd_pr/pfet_03v3.sym} 0 100 0 0 {name=MPEN model=pfet_03v3 spiceprefix=X W=8u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 20 100 25 100 {lab=VIN}
N 25 100 25 150 {lab=VIN}
N 25 150 70 150 {lab=VIN}
C {lab_pin.sym} 70 150 0 1 {name=l1 lab=VIN}
C {gf180mcu_fd_pr/pfet_03v3.sym} 200 260 0 0 {name=MPBIAS model=pfet_03v3 spiceprefix=X W=2u L=2u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 220 260 225 260 {lab=VIN}
N 225 260 225 310 {lab=VIN}
N 225 310 270 310 {lab=VIN}
C {lab_pin.sym} 270 310 0 1 {name=l2 lab=VIN}
C {gf180mcu_fd_pr/nfet_03v3.sym} 200 450 0 0 {name=MNBIAS model=nfet_03v3 spiceprefix=X W=2u L=2u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 220 450 225 450 {lab=VSS}
N 225 450 225 500 {lab=VSS}
N 225 500 270 500 {lab=VSS}
C {lab_pin.sym} 270 500 0 1 {name=l3 lab=VSS}
C {gf180mcu_fd_pr/pfet_03v3.sym} 600 180 0 0 {name=MPMIR model=pfet_03v3 spiceprefix=X W=4u L=2u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 620 180 625 180 {lab=VIN}
N 625 180 625 230 {lab=VIN}
N 625 230 670 230 {lab=VIN}
C {lab_pin.sym} 670 230 0 1 {name=l4 lab=VIN}
C {gf180mcu_fd_pr/pfet_03v3.sym} 900 180 0 0 {name=MPOUT model=pfet_03v3 spiceprefix=X W=4u L=2u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 920 180 925 180 {lab=VIN}
N 925 180 925 230 {lab=VIN}
N 925 230 970 230 {lab=VIN}
C {lab_pin.sym} 970 230 0 1 {name=l5 lab=VIN}
C {gf180mcu_fd_pr/nfet_03v3.sym} 600 360 0 0 {name=MNREF model=nfet_03v3 spiceprefix=X W=8u L=1u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 620 360 625 360 {lab=VSS}
N 625 360 625 410 {lab=VSS}
N 625 410 670 410 {lab=VSS}
C {lab_pin.sym} 670 410 0 1 {name=l6 lab=VSS}
C {gf180mcu_fd_pr/nfet_03v3.sym} 900 360 0 0 {name=MNFB model=nfet_03v3 spiceprefix=X W=8u L=1u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 920 360 925 360 {lab=VSS}
N 925 360 925 410 {lab=VSS}
N 925 410 970 410 {lab=VSS}
C {lab_pin.sym} 970 410 0 1 {name=l7 lab=VSS}
C {gf180mcu_fd_pr/nfet_03v3.sym} 750 530 0 0 {name=MNTAIL model=nfet_03v3 spiceprefix=X W=2u L=2u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 770 530 775 530 {lab=VSS}
N 775 530 775 580 {lab=VSS}
N 775 580 820 580 {lab=VSS}
C {lab_pin.sym} 820 580 0 1 {name=l8 lab=VSS}
N 20 130 20 200 {lab=VP}
N 20 200 220 200 {lab=VP}
N 220 200 220 230 {lab=VP}
C {lab_pin.sym} 20 200 0 0 {name=l9 lab=VP}
N 220 290 220 360 {lab=NB}
N 220 360 220 420 {lab=NB}
N 180 450 160 450 {lab=NB}
N 160 450 160 360 {lab=NB}
N 160 360 220 360 {lab=NB}
C {lab_pin.sym} 160 360 0 0 {name=l10 lab=NB}
N 620 150 620 120 {lab=VP}
N 620 120 920 120 {lab=VP}
N 920 120 920 150 {lab=VP}
C {lab_pin.sym} 620 120 0 0 {name=l11 lab=VP}
N 620 210 620 260 {lab=MIR}
N 620 260 620 330 {lab=MIR}
N 580 180 560 180 {lab=MIR}
N 560 180 560 260 {lab=MIR}
N 560 260 620 260 {lab=MIR}
C {lab_pin.sym} 560 260 0 0 {name=l12 lab=MIR}
N 920 210 920 280 {lab=RAW}
N 920 280 920 330 {lab=RAW}
C {lab_wire.sym} 1010 280 0 0 {name=l13 lab=RAW}
N 620 390 620 440 {lab=TAIL}
N 620 440 770 440 {lab=TAIL}
N 770 440 920 440 {lab=TAIL}
N 920 440 920 390 {lab=TAIL}
N 770 440 770 500 {lab=TAIL}
C {lab_wire.sym} 770 440 0 0 {name=l14 lab=TAIL}
C {gf180mcu_fd_pr/pfet_03v3.sym} 1250 180 0 0 {name=MPBUF model=pfet_03v3 spiceprefix=X W=2u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 1270 180 1275 180 {lab=VIN}
N 1275 180 1275 230 {lab=VIN}
N 1275 230 1320 230 {lab=VIN}
C {lab_pin.sym} 1320 230 0 1 {name=l15 lab=VIN}
C {gf180mcu_fd_pr/nfet_03v3.sym} 1250 360 0 0 {name=MNBUF model=nfet_03v3 spiceprefix=X W=1u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 1270 360 1275 360 {lab=VSS}
N 1275 360 1275 410 {lab=VSS}
N 1275 410 1320 410 {lab=VSS}
C {lab_pin.sym} 1320 410 0 1 {name=l16 lab=VSS}
N 1270 210 1270 280 {lab=PGOOD}
N 1270 280 1270 330 {lab=PGOOD}
N 1270 280 1510 280 {lab=PGOOD}
C {lab_pin.sym} 1510 280 0 1 {name=l17 lab=PGOOD}
N 1230 360 1130 360 {lab=RAW}
N 1130 360 1130 280 {lab=RAW}
N 1130 280 920 280 {lab=RAW}
N 1230 180 1130 180 {lab=RAW}
N 1130 180 1130 280 {lab=RAW}
C {gf180mcu_fd_pr/pfet_03v3.sym} 1050 570 0 0 {name=MPOFF model=pfet_03v3 spiceprefix=X W=2u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 1070 570 1075 570 {lab=VIN}
N 1075 570 1075 620 {lab=VIN}
N 1075 620 1120 620 {lab=VIN}
C {lab_pin.sym} 1120 620 0 1 {name=l18 lab=VIN}
C {res.sym} 0 800 0 0 {name=RTH value=200k m=1}
C {res.sym} 0 1000 0 0 {name=RLOW value=1.8Meg m=1}
N 0 830 0 900 {lab=THRESH}
N 0 900 0 970 {lab=THRESH}
C {lab_pin.sym} 0 900 0 0 {name=l19 lab=THRESH}
C {res.sym} 500 800 0 0 {name=RHYS value=3.06Meg m=1}
C {gf180mcu_fd_pr/nfet_03v3.sym} 480 1000 0 0 {name=MNHYS model=nfet_03v3 spiceprefix=X W=2u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 500 1000 505 1000 {lab=VSS}
N 505 1000 505 1050 {lab=VSS}
N 505 1050 550 1050 {lab=VSS}
C {lab_pin.sym} 550 1050 0 1 {name=l20 lab=VSS}
N 500 830 500 970 {lab=HYS}
C {lab_pin.sym} 500 900 0 0 {name=l21 lab=HYS}
T {Initial threshold targets: 1.62 V rising / 1.53 V falling
(equivalent VOUT). PGOOD is VIN-domain, not a pad driver.
No reference-valid detection or UVLO.} 750 850 0 0 0.3 0.3 {}
N -20 100 -60 100 {lab=ENB}
C {lab_pin.sym} -60 100 0 0 {name=l22 lab=ENB}
N 20 70 20 30 {lab=VIN}
C {lab_pin.sym} 20 30 0 0 {name=l23 lab=VIN}
N 180 260 140 260 {lab=PB}
C {lab_pin.sym} 140 260 0 0 {name=l24 lab=PB}
N 220 480 220 520 {lab=VSS}
C {lab_pin.sym} 220 520 0 0 {name=l25 lab=VSS}
N 880 180 840 180 {lab=MIR}
C {lab_pin.sym} 840 180 0 0 {name=l26 lab=MIR}
N 580 360 540 360 {lab=THRESH}
C {lab_pin.sym} 540 360 0 0 {name=l27 lab=THRESH}
N 880 360 840 360 {lab=VFB}
C {lab_pin.sym} 840 360 0 0 {name=l28 lab=VFB}
N 730 530 690 530 {lab=NB}
C {lab_pin.sym} 690 530 0 0 {name=l29 lab=NB}
N 770 560 770 600 {lab=VSS}
C {lab_pin.sym} 770 600 0 0 {name=l30 lab=VSS}
N 1270 150 1270 110 {lab=VIN}
C {lab_pin.sym} 1270 110 0 0 {name=l31 lab=VIN}
N 1270 390 1270 430 {lab=VSS}
C {lab_pin.sym} 1270 430 0 0 {name=l32 lab=VSS}
N 1030 570 990 570 {lab=EN}
C {lab_pin.sym} 990 570 0 0 {name=l33 lab=EN}
N 1070 540 1070 500 {lab=VIN}
C {lab_pin.sym} 1070 500 0 0 {name=l34 lab=VIN}
N 1070 600 1070 640 {lab=RAW}
C {lab_pin.sym} 1070 640 0 0 {name=l35 lab=RAW}
N 0 770 0 730 {lab=VREF}
C {lab_pin.sym} 0 730 0 0 {name=l36 lab=VREF}
N 0 1030 0 1070 {lab=VSS}
C {lab_pin.sym} 0 1070 0 0 {name=l37 lab=VSS}
N 500 770 500 730 {lab=THRESH}
C {lab_pin.sym} 500 730 0 0 {name=l38 lab=THRESH}
N 460 1000 420 1000 {lab=PGOOD}
C {lab_pin.sym} 420 1000 0 0 {name=l39 lab=PGOOD}
N 500 1030 500 1070 {lab=VSS}
C {lab_pin.sym} 500 1070 0 0 {name=l40 lab=VSS}
