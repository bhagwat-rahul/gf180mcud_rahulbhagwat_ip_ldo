v {xschem version=3.4.8RC file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Reference soft-start - 1 MOS; 20 us nominal RC time constant} 0 -170 0 0 0.45 0.45 {}
C {iopin.sym} 0 -90 0 0 {name=p0 lab=VSS}
C {iopin.sym} 140 -90 0 0 {name=p1 lab=ENB}
C {iopin.sym} 280 -90 0 0 {name=p2 lab=VREF}
C {iopin.sym} 420 -90 0 0 {name=p3 lab=VREF_SS}
C {res.sym} 0 200 3 0 {name=RSS value=1Meg m=1}
C {capa.sym} 350 400 0 0 {name=CSS value=20p m=1}
C {gf180mcu_fd_pr/nfet_03v3.sym} 650 400 0 0 {name=MNRESET model=nfet_03v3 spiceprefix=X W=2u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 670 400 675 400 {lab=VSS}
N 675 400 675 450 {lab=VSS}
N 675 450 720 450 {lab=VSS}
C {lab_pin.sym} 720 450 0 1 {name=l1 lab=VSS}
N 30 200 350 200 {lab=VREF_SS}
N 350 200 350 300 {lab=VREF_SS}
N 350 300 670 300 {lab=VREF_SS}
N 670 300 670 370 {lab=VREF_SS}
N 350 300 350 370 {lab=VREF_SS}
C {lab_pin.sym} 350 300 0 0 {name=l2 lab=VREF_SS}
T {The capacitor resets in OFF; the input reference is assumed valid before EN.
NMOS-input amplifier operation begins only after the ramp enters its input range.} 0 600 0 0 0.3 0.3 {}
N -30 200 -70 200 {lab=VREF}
C {lab_pin.sym} -70 200 0 0 {name=l3 lab=VREF}
N 350 430 350 470 {lab=VSS}
C {lab_pin.sym} 350 470 0 0 {name=l4 lab=VSS}
N 630 400 590 400 {lab=ENB}
C {lab_pin.sym} 590 400 0 0 {name=l5 lab=ENB}
N 670 430 670 470 {lab=VSS}
C {lab_pin.sym} 670 470 0 0 {name=l6 lab=VSS}
