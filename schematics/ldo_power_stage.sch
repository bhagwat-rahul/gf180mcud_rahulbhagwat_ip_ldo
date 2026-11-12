v {xschem version=3.4.8RC file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Power stage - 3 logical MOS; repeated pass units dominate physical current routing} 0 -170 0 0 0.45 0.45 {}
C {iopin.sym} 0 -90 0 0 {name=p0 lab=VIN}
C {iopin.sym} 140 -90 0 0 {name=p1 lab=VSS}
C {iopin.sym} 280 -90 0 0 {name=p2 lab=EN}
C {iopin.sym} 420 -90 0 0 {name=p3 lab=ENB}
C {iopin.sym} 560 -90 0 0 {name=p4 lab=GATE}
C {iopin.sym} 700 -90 0 0 {name=p5 lab=VOUT}
C {gf180mcu_fd_pr/pfet_03v3.sym} 0 200 0 0 {name=MPASS model=pfet_03v3 spiceprefix=X W=50u L=0.28u nf=1 m=200 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 20 200 25 200 {lab=VIN}
N 25 200 25 250 {lab=VIN}
N 25 250 70 250 {lab=VIN}
C {lab_pin.sym} 70 250 0 1 {name=l1 lab=VIN}
C {gf180mcu_fd_pr/pfet_03v3.sym} 500 200 0 0 {name=MPOFF model=pfet_03v3 spiceprefix=X W=4u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 520 200 525 200 {lab=VIN}
N 525 200 525 250 {lab=VIN}
N 525 250 570 250 {lab=VIN}
C {lab_pin.sym} 570 250 0 1 {name=l2 lab=VIN}
C {res.sym} 1000 200 0 0 {name=RDIS value=2k m=1}
C {gf180mcu_fd_pr/nfet_03v3.sym} 980 450 0 0 {name=MNDIS model=nfet_03v3 spiceprefix=X W=4u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 1000 450 1005 450 {lab=VSS}
N 1005 450 1005 500 {lab=VSS}
N 1005 500 1050 500 {lab=VSS}
C {lab_pin.sym} 1050 500 0 1 {name=l3 lab=VSS}
N 1000 230 1000 420 {lab=DIS}
C {lab_pin.sym} 1000 320 0 0 {name=l4 lab=DIS}
T {MPASS: W=50 um, L=0.28 um, m=200 -> 10,000 um total width.
Multiplicity is not a finished finger/contact/metal layout. No reverse blocking or current limit.
RDIS=2 kohm limits OFF discharge; it does not actively clamp RUN overshoot.} 0 600 0 0 0.3 0.3 {}
N -20 200 -60 200 {lab=GATE}
C {lab_pin.sym} -60 200 0 0 {name=l5 lab=GATE}
N 20 170 20 130 {lab=VIN}
C {lab_pin.sym} 20 130 0 0 {name=l6 lab=VIN}
N 20 230 20 270 {lab=VOUT}
C {lab_pin.sym} 20 270 0 0 {name=l7 lab=VOUT}
N 480 200 440 200 {lab=EN}
C {lab_pin.sym} 440 200 0 0 {name=l8 lab=EN}
N 520 170 520 130 {lab=VIN}
C {lab_pin.sym} 520 130 0 0 {name=l9 lab=VIN}
N 520 230 520 270 {lab=GATE}
C {lab_pin.sym} 520 270 0 0 {name=l10 lab=GATE}
N 1000 170 1000 130 {lab=VOUT}
C {lab_pin.sym} 1000 130 0 0 {name=l11 lab=VOUT}
N 960 450 920 450 {lab=ENB}
C {lab_pin.sym} 920 450 0 0 {name=l12 lab=ENB}
N 1000 480 1000 520 {lab=VSS}
C {lab_pin.sym} 1000 520 0 0 {name=l13 lab=VSS}
