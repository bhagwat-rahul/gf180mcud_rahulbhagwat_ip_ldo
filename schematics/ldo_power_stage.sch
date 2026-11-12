v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {Power stage - 3 logical MOS; repeated pass units dominate physical current routing} -480 -190 0 0 0.45 0.45 {}
T {MPASS: W=50 um, L=0.28 um, m=200 -> 10,000 um total width.
Multiplicity is not a finished finger/contact/metal layout. No reverse blocking or current limit.
RDIS=2 kohm limits OFF discharge; it does not actively clamp RUN overshoot.} -330 270 0 0 0.3 0.3 {}
N -110 -80 -110 -40 {lab=ENB}
N -180 0 -140 0 {lab=VSS}
N 240 0 240 60 {lab=VOUT}
N 240 60 240 120 {lab=VOUT}
N 140 0 240 0 {lab=VOUT}
N -80 0 80 0 {lab=DIS}
N -140 0 -110 0 {lab=VSS}
N 80 120 110 120 {lab=VIN}
N 140 120 240 120 {lab=VOUT}
N -80 120 -80 150 {lab=VIN}
N -80 120 80 120 {lab=VIN}
N 110 160 110 180 {lab=GATE}
N -80 180 110 180 {lab=GATE}
N -180 150 -120 150 {lab=EN}
C {iopin.sym} 0 120 3 0 {name=p0 lab=VIN}
C {iopin.sym} -180 0 0 1 {name=p1 lab=VSS}
C {iopin.sym} -180 150 0 1 {name=p2 lab=EN}
C {iopin.sym} -110 -80 3 0 {name=p3 lab=ENB}
C {iopin.sym} 0 180 1 0 {name=p4 lab=GATE}
C {iopin.sym} 240 60 0 0 {name=p5 lab=VOUT}
C {gf180mcu_fd_pr/pfet_03v3.sym} 110 140 3 0 {name=MPASS model=pfet_03v3 spiceprefix=X W=50u L=0.28u nf=1 m=200 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
C {gf180mcu_fd_pr/pfet_03v3.sym} -100 150 0 0 {name=MPOFF model=pfet_03v3 spiceprefix=X W=4u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
C {res.sym} 110 0 1 1 {name=RDIS value=2k m=1}
C {gf180mcu_fd_pr/nfet_03v3.sym} -110 -20 1 0 {name=MNDIS model=nfet_03v3 spiceprefix=X W=4u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
C {lab_wire.sym} 0 0 1 0 {name=l4 lab=DIS}
