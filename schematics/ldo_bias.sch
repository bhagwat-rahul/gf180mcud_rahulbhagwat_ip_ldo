v {xschem version=3.4.8RC file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Bias entry and RUN adaptation - 8 MOS; externally SOURCED 1 uA} 0 -170 0 0 0.45 0.45 {}
C {iopin.sym} 0 -90 0 0 {name=p0 lab=VIN}
C {iopin.sym} 140 -90 0 0 {name=p1 lab=VSS}
C {iopin.sym} 280 -90 0 0 {name=p2 lab=IBIAS}
C {iopin.sym} 420 -90 0 0 {name=p3 lab=EN}
C {iopin.sym} 560 -90 0 0 {name=p4 lab=STBY}
C {iopin.sym} 700 -90 0 0 {name=p5 lab=GATE}
C {iopin.sym} 840 -90 0 0 {name=p6 lab=ENB}
C {iopin.sym} 980 -90 0 0 {name=p7 lab=PB}
C {gf180mcu_fd_pr/nfet_03v3.sym} 0 500 0 0 {name=MNREF model=nfet_03v3 spiceprefix=X W=2u L=2u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 20 500 25 500 {lab=VSS}
N 25 500 25 550 {lab=VSS}
N 25 550 70 550 {lab=VSS}
C {lab_pin.sym} 70 550 0 1 {name=l1 lab=VSS}
C {gf180mcu_fd_pr/nfet_03v3.sym} 350 500 0 0 {name=MNCOPY model=nfet_03v3 spiceprefix=X W=2u L=2u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 370 500 375 500 {lab=VSS}
N 375 500 375 550 {lab=VSS}
N 375 550 420 550 {lab=VSS}
C {lab_pin.sym} 420 550 0 1 {name=l2 lab=VSS}
C {gf180mcu_fd_pr/pfet_03v3.sym} 350 100 0 0 {name=MPREF model=pfet_03v3 spiceprefix=X W=4u L=2u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 370 100 375 100 {lab=VIN}
N 375 100 375 150 {lab=VIN}
N 375 150 420 150 {lab=VIN}
C {lab_pin.sym} 420 150 0 1 {name=l3 lab=VIN}
C {gf180mcu_fd_pr/pfet_03v3.sym} 800 100 0 0 {name=MPADEN model=pfet_03v3 spiceprefix=X W=4u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 820 100 825 100 {lab=VIN}
N 825 100 825 150 {lab=VIN}
N 825 150 870 150 {lab=VIN}
C {lab_pin.sym} 870 150 0 1 {name=l4 lab=VIN}
C {gf180mcu_fd_pr/pfet_03v3.sym} 800 300 0 0 {name=MPADMODE model=pfet_03v3 spiceprefix=X W=4u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 820 300 825 300 {lab=VIN}
N 825 300 825 350 {lab=VIN}
N 825 350 870 350 {lab=VIN}
C {lab_pin.sym} 870 350 0 1 {name=l5 lab=VIN}
C {gf180mcu_fd_pr/pfet_03v3.sym} 800 500 0 0 {name=MPREPLICA model=pfet_03v3 spiceprefix=X W=0.22u L=0.28u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 820 500 825 500 {lab=VIN}
N 825 500 825 550 {lab=VIN}
N 825 550 870 550 {lab=VIN}
C {lab_pin.sym} 870 550 0 1 {name=l6 lab=VIN}
C {gf180mcu_fd_pr/pfet_03v3.sym} 1150 100 0 0 {name=MPINV model=pfet_03v3 spiceprefix=X W=2u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 1170 100 1175 100 {lab=VIN}
N 1175 100 1175 150 {lab=VIN}
N 1175 150 1220 150 {lab=VIN}
C {lab_pin.sym} 1220 150 0 1 {name=l7 lab=VIN}
C {gf180mcu_fd_pr/nfet_03v3.sym} 1150 300 0 0 {name=MNINV model=nfet_03v3 spiceprefix=X W=1u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 1170 300 1175 300 {lab=VSS}
N 1175 300 1175 350 {lab=VSS}
N 1175 350 1220 350 {lab=VSS}
C {lab_pin.sym} 1220 350 0 1 {name=l8 lab=VSS}
N -20 500 -60 500 {lab=IBIAS}
N -60 500 -60 400 {lab=IBIAS}
N -60 400 20 400 {lab=IBIAS}
N 20 400 20 470 {lab=IBIAS}
C {lab_pin.sym} 20 400 0 1 {name=l9 lab=IBIAS}
N 370 130 370 220 {lab=PB}
N 370 220 370 470 {lab=PB}
N 330 100 310 100 {lab=PB}
N 310 100 310 220 {lab=PB}
N 310 220 370 220 {lab=PB}
C {lab_pin.sym} 370 220 0 1 {name=l10 lab=PB}
N 820 130 820 270 {lab=ADSUP}
C {lab_pin.sym} 820 220 0 1 {name=l11 lab=ADSUP}
N 820 330 820 470 {lab=ADSOURCE}
C {lab_pin.sym} 820 420 0 1 {name=l12 lab=ADSOURCE}
N 1170 130 1170 210 {lab=ENB}
N 1170 210 1170 270 {lab=ENB}
C {lab_pin.sym} 1170 210 0 1 {name=l13 lab=ENB}
N 1130 100 1090 100 {lab=EN}
N 1090 100 1090 300 {lab=EN}
N 1090 300 1130 300 {lab=EN}
C {lab_pin.sym} 1090 100 0 0 {name=l14 lab=EN}
T {STBY=0: small replica-pass current adds to the bias input as load rises.
STBY=1: replica branch disabled; external 1 uA sets the fixed bias.
EN=0 disables adaptation, but the bias-entry mirror remains powered.} 0 650 0 0 0.3 0.3 {}
N 20 530 20 570 {lab=VSS}
C {lab_pin.sym} 20 570 0 0 {name=l15 lab=VSS}
N 330 500 290 500 {lab=IBIAS}
C {lab_pin.sym} 290 500 0 0 {name=l16 lab=IBIAS}
N 370 530 370 570 {lab=VSS}
C {lab_pin.sym} 370 570 0 0 {name=l17 lab=VSS}
N 370 70 370 30 {lab=VIN}
C {lab_pin.sym} 370 30 0 0 {name=l18 lab=VIN}
N 780 100 740 100 {lab=ENB}
C {lab_pin.sym} 740 100 0 0 {name=l19 lab=ENB}
N 820 70 820 30 {lab=VIN}
C {lab_pin.sym} 820 30 0 0 {name=l20 lab=VIN}
N 780 300 740 300 {lab=STBY}
C {lab_pin.sym} 740 300 0 0 {name=l21 lab=STBY}
N 780 500 740 500 {lab=GATE}
C {lab_pin.sym} 740 500 0 0 {name=l22 lab=GATE}
N 820 530 820 570 {lab=IBIAS}
C {lab_pin.sym} 820 570 0 0 {name=l23 lab=IBIAS}
N 1170 70 1170 30 {lab=VIN}
C {lab_pin.sym} 1170 30 0 0 {name=l24 lab=VIN}
N 1170 330 1170 370 {lab=VSS}
C {lab_pin.sym} 1170 370 0 0 {name=l25 lab=VSS}
