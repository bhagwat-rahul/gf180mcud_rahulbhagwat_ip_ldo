v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {Reference soft-start - 1 MOS; 20 us nominal RC time constant} -350 -170 0 0 0.45 0.45 {}
T {The capacitor resets in OFF; the input reference is assumed valid before EN.
NMOS-input amplifier operation begins only after the ramp enters its input range.} -330 190 0 0 0.3 0.3 {}
N -320 0 -280 0 {lab=VREF}
N -220 0 -130 0 {lab=VREF_SS}
N -130 -60 -130 0 {lab=VREF_SS}
N -130 0 -130 60 {lab=VREF_SS}
N -130 -60 -30 -60 {lab=VREF_SS}
N 30 -60 110 -60 {lab=VSS}
N -130 60 -30 60 {lab=VREF_SS}
N 30 60 110 60 {lab=VSS}
N 110 -60 110 60 {lab=VSS}
N 110 -0 220 -0 {lab=VSS}
N -320 40 -180 40 {lab=VREF_SS}
N -180 0 -180 40 {lab=VREF_SS}
N -0 100 -0 130 {lab=ENB}
N -0 50 0 60 {lab=VSS}
N 0 50 30 50 {lab=VSS}
N 30 50 30 60 {lab=VSS}
C {iopin.sym} 220 0 0 0 {name=p0 lab=VSS}
C {iopin.sym} 0 130 1 0 {name=p1 lab=ENB}
C {iopin.sym} -320 0 0 1 {name=p2 lab=VREF}
C {iopin.sym} -320 40 2 0 {name=p3 lab=VREF_SS}
C {res.sym} -250 0 3 0 {name=RSS value=1Meg m=1}
C {capa.sym} 0 -60 3 0 {name=CSS value=20p m=1}
C {gf180mcu_fd_pr/nfet_03v3.sym} 0 80 3 0 {name=MNRESET model=nfet_03v3 spiceprefix=X W=2u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
