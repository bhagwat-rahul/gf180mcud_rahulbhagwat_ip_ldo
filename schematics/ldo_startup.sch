v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {Startup sequencing: CC/CGF soft-connect and switched minimum load} -600 -220 0 0 0.45 0.45 {}
T {CC and CGF are disconnected while the pass-device gate falls.  After EN, the
PMOS switches close slowly through the ENB-RC ramp, and the 5 kohm bleed holds
VOUT at zero until PGOOD.  The bleed turns off at PGOOD.} -600 380 0 0 0.3 0.3 {}
C {iopin.sym} -600 0 0 1 {name=p0 lab=VIN}
C {iopin.sym} -600 30 0 1 {name=p1 lab=VSS}
C {iopin.sym} -600 60 0 1 {name=p2 lab=COMP2}
C {iopin.sym} -600 90 0 1 {name=p3 lab=GATE}
C {iopin.sym} 600 60 0 0 {name=p4 lab=VOUT}
C {iopin.sym} 600 90 0 0 {name=p5 lab=PGOOD}
C {iopin.sym} 600 120 0 0 {name=p6 lab=ENB}

C {gf180mcu_fd_pr/cap_mim_analog.sym} -200 60 3 0 {name=CC W=50u L=50u model=cap_mim_2f0_m4m5_noshield spiceprefix=X m=80}
N -230 60 -280 60 {lab=COMP2}
C {lab_pin.sym} -280 60 0 0 {name=lp1 lab=COMP2}
N -170 60 -120 60 {lab=CCF}
C {lab_pin.sym} -120 60 0 0 {name=lp2 lab=CCF}

C {gf180mcu_fd_pr/cap_mim_analog.sym} -200 120 3 0 {name=CGF W=20u L=12.2u model=cap_mim_2f0_m4m5_noshield spiceprefix=X m=40}
N -230 120 -280 120 {lab=GATE}
C {lab_pin.sym} -280 120 0 0 {name=lp3 lab=GATE}
N -170 120 -120 120 {lab=CGFF}
C {lab_pin.sym} -120 120 0 0 {name=lp4 lab=CGFF}

C {gf180mcu_fd_pr/pfet_03v3.sym} 300 100 0 0 {name=MPCC model=pfet_03v3 spiceprefix=X W=50u L=0.28u nf=1 m=10 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 320 100 360 100 {lab=VOUT}
C {lab_pin.sym} 360 100 0 0 {name=lp5 lab=VOUT}
N 280 100 240 100 {lab=SWGCC}
C {lab_pin.sym} 240 100 0 0 {name=lp6 lab=SWGCC}
N 320 130 320 170 {lab=CCF}
C {lab_pin.sym} 320 170 0 0 {name=lp7 lab=CCF}

C {gf180mcu_fd_pr/pfet_03v3.sym} 300 220 0 0 {name=MPCG model=pfet_03v3 spiceprefix=X W=50u L=0.28u nf=1 m=4 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 320 220 360 220 {lab=VOUT}
C {lab_pin.sym} 360 220 0 0 {name=lp8 lab=VOUT}
N 280 220 240 220 {lab=SWGC}
C {lab_pin.sym} 240 220 0 0 {name=lp9 lab=SWGC}
N 320 250 320 290 {lab=CGFF}
C {lab_pin.sym} 320 290 0 0 {name=lp10 lab=CGFF}

C {gf180mcu_fd_pr/ppolyf_u_3k.sym} -450 -100 3 0 {name=RSWGC W=0.5u L=154.978u model=ppolyf_u_3k spiceprefix=X m=1}
N -480 -100 -540 -100 {lab=ENB}
C {lab_pin.sym} -540 -100 0 0 {name=lp11 lab=ENB}
N -420 -100 -360 -100 {lab=SWGC}
C {lab_pin.sym} -360 -100 0 0 {name=lp12 lab=SWGC}
C {lab_pin.sym} -450 -80 0 0 {name=lp13 lab=VSS}

C {gf180mcu_fd_pr/cap_mim_analog.sym} -250 -100 3 0 {name=CSWGC W=20u L=12.2u model=cap_mim_2f0_m4m5_noshield spiceprefix=X m=62}
N -280 -100 -340 -100 {lab=SWGC}
C {lab_pin.sym} -340 -100 0 0 {name=lp14 lab=SWGC}
N -220 -100 -160 -100 {lab=VIN}
C {lab_pin.sym} -160 -100 0 0 {name=lp15 lab=VIN}

C {gf180mcu_fd_pr/ppolyf_u_3k.sym} -450 -180 3 0 {name=RSWGCC W=0.5u L=154.978u model=ppolyf_u_3k spiceprefix=X m=1}
N -480 -180 -540 -180 {lab=ENB}
C {lab_pin.sym} -540 -180 0 0 {name=lp26 lab=ENB}
N -420 -180 -360 -180 {lab=SWGCC}
C {lab_pin.sym} -360 -180 0 0 {name=lp27 lab=SWGCC}
C {lab_pin.sym} -450 -160 0 0 {name=lp28 lab=VSS}

C {gf180mcu_fd_pr/cap_mim_analog.sym} -250 -180 3 0 {name=CSWGCC W=20u L=12.2u model=cap_mim_2f0_m4m5_noshield spiceprefix=X m=205}
N -280 -180 -340 -180 {lab=SWGCC}
C {lab_pin.sym} -340 -180 0 0 {name=lp29 lab=SWGCC}
N -220 -180 -160 -180 {lab=VIN}
C {lab_pin.sym} -160 -180 0 0 {name=lp30 lab=VIN}

C {gf180mcu_fd_pr/ppolyf_u.sym} -450 260 3 0 {name=RBLD W=10u L=57.143u model=ppolyf_u spiceprefix=X m=1}
N -480 260 -540 260 {lab=VOUT}
C {lab_pin.sym} -540 260 0 0 {name=lp16 lab=VOUT}
N -420 260 -360 260 {lab=BLD}
C {lab_pin.sym} -360 260 0 0 {name=lp17 lab=BLD}
C {lab_pin.sym} -450 280 0 0 {name=lp18 lab=VSS}

C {gf180mcu_fd_pr/nfet_03v3.sym} 300 500 0 0 {name=MNBLD model=nfet_03v3 spiceprefix=X W=10u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 280 500 240 500 {lab=BLED}
C {lab_pin.sym} 240 500 0 0 {name=lp19 lab=BLED}
N 320 500 360 500 {lab=VSS}
C {lab_pin.sym} 360 500 0 0 {name=lp20 lab=VSS}
N 320 470 320 430 {lab=BLD}
C {lab_pin.sym} 320 430 0 0 {name=lp21 lab=BLD}


N 320 70 320 100 {lab=VOUT}
C {lab_pin.sym} 320 70 0 0 {name=lp26 lab=VOUT}
N 320 190 320 220 {lab=VOUT}
C {lab_pin.sym} 320 190 0 0 {name=lp27 lab=VOUT}
N 320 530 320 500 {lab=VSS}
C {lab_pin.sym} 320 530 0 0 {name=lp28 lab=VSS}
C {gf180mcu_fd_pr/ppolyf_u_3k.sym} 700 300 3 0 {name=RBLEDPD1 W=0.5u L=38.637u model=ppolyf_u_3k spiceprefix=X m=1}
N 670 300 620 300 {lab=SWGCC}
C {lab_pin.sym} 620 300 0 0 {name=lp31 lab=SWGCC}
N 730 300 780 300 {lab=BLED}
C {lab_pin.sym} 780 300 0 0 {name=lp32 lab=BLED}
C {gf180mcu_fd_pr/ppolyf_u_3k.sym} 700 420 3 0 {name=RBLEDPD2 W=0.5u L=154.978u model=ppolyf_u_3k spiceprefix=X m=1}
N 670 420 620 420 {lab=BLED}
C {lab_pin.sym} 620 420 0 0 {name=lp33 lab=BLED}
N 730 420 780 420 {lab=VSS}
C {lab_pin.sym} 780 420 0 0 {name=lp34 lab=VSS}
N 700 320 700 340 {lab=VSS}
C {lab_pin.sym} 700 340 0 0 {name=lp35 lab=VSS}
N 700 440 700 460 {lab=VSS}
C {lab_pin.sym} 700 460 0 0 {name=lp36 lab=VSS}
