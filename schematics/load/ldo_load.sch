v {xschem version=3.4.8RC file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {On-die 0-100 mA load - NMOS mirror, 210:1. NAND3(PGOOD,STBYB,LDENB_B) drives LOAD_DIS: on only in RUN after PGOOD with LDENB low.} 0 -170 0 0 0.45 0.45 {}
C {iopin.sym} 0 -90 0 0 {name=p0 lab=VIN}
C {iopin.sym} 140 -90 0 0 {name=p1 lab=VSS}
C {iopin.sym} 280 -90 0 0 {name=p2 lab=VLOAD}
C {iopin.sym} 420 -90 0 0 {name=p3 lab=LDENB}
C {iopin.sym} 560 -90 0 0 {name=p4 lab=VOUT}
C {iopin.sym} 700 -90 0 0 {name=p5 lab=PGOOD}
C {iopin.sym} 840 -90 0 0 {name=p6 lab=STBY}
C {gf180mcu_fd_pr/pfet_03v3.sym} 200 150 0 0 {name=MPINV model=pfet_03v3 spiceprefix=X W=2u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 220 120 220 150 {lab=VIN}
C {lab_pin.sym} 220 120 0 0 {name=lp1 lab=VIN}
N 180 150 160 150 {lab=LOAD_DIS}
C {lab_pin.sym} 160 150 0 0 {name=lp2 lab=LOAD_DIS}
N 220 180 220 270 {lab=LDB}
N 220 210 250 210 {lab=LDB}
C {lab_pin.sym} 250 210 0 0 {name=lp3 lab=LDB}
C {gf180mcu_fd_pr/nfet_03v3.sym} 200 300 0 0 {name=MNINV model=nfet_03v3 spiceprefix=X W=1u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 180 300 160 300 {lab=LOAD_DIS}
C {lab_pin.sym} 160 300 0 0 {name=lp4 lab=LOAD_DIS}
N 220 330 220 360 {lab=VSS}
C {lab_pin.sym} 220 360 0 0 {name=lp5 lab=VSS}
C {gf180mcu_fd_pr/nfet_03v3.sym} 450 220 0 0 {name=MNSW model=nfet_03v3 spiceprefix=X W=50u L=0.5u nf=1 m=8 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 470 160 470 190 {lab=VLOAD}
C {lab_pin.sym} 470 160 0 0 {name=lp6 lab=VLOAD}
N 430 220 410 220 {lab=LDB}
C {lab_pin.sym} 410 220 0 0 {name=lp7 lab=LDB}
N 470 250 470 280 {lab=ISET}
N 470 280 520 280 {lab=ISET}
C {lab_pin.sym} 490 280 0 0 {name=lp8 lab=ISET}
C {gf180mcu_fd_pr/ppolyf_u.sym} 550 280 3 0 {name=RSET W=20u L=19.657u model=ppolyf_u spiceprefix=X m=1}
N 550 300 550 320 {lab=VSS}
C {lab_pin.sym} 550 320 0 0 {name=lp9 lab=VSS}
N 580 280 580 340 {lab=IREF}
N 580 340 930 340 {lab=IREF}
C {lab_pin.sym} 760 340 0 0 {name=lp10 lab=IREF}
C {gf180mcu_fd_pr/nfet_03v3.sym} 700 400 0 0 {name=MREF model=nfet_03v3 spiceprefix=X W=50u L=1u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 720 370 720 340 {lab=IREF}
N 680 400 640 400 {lab=IREF}
N 640 400 640 355 {lab=IREF}
N 640 355 720 355 {lab=IREF}
N 720 355 720 370 {lab=IREF}
N 720 430 720 460 {lab=VSS}
C {lab_pin.sym} 720 460 0 0 {name=lp11 lab=VSS}
C {gf180mcu_fd_pr/nfet_03v3.sym} 950 400 0 0 {name=MIR model=nfet_03v3 spiceprefix=X W=50u L=1u nf=1 m=210 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 930 340 930 400 {lab=IREF}
N 970 330 970 370 {lab=VOUT}
N 970 330 1000 330 {lab=VOUT}
C {lab_pin.sym} 1000 330 0 0 {name=lp12 lab=VOUT}
N 970 430 970 460 {lab=VSS}
C {lab_pin.sym} 970 460 0 0 {name=lp13 lab=VSS}
C {gf180mcu_fd_pr/nfet_03v3.sym} 600 520 0 0 {name=MNCL model=nfet_03v3 spiceprefix=X W=2u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 600 340 600 490 {lab=IREF}
N 600 490 620 490 {lab=IREF}
N 580 520 550 520 {lab=LOAD_DIS}
C {lab_pin.sym} 550 520 0 0 {name=lp14 lab=LOAD_DIS}
N 620 550 620 580 {lab=VSS}
C {lab_pin.sym} 620 580 0 0 {name=lp15 lab=VSS}
T {VLOAD sets the reference current through RSET: IREF = (VLOAD - VGS)/350 ohm.
VLOAD = 1.2 V gives ~0.47 mA reference and ~99.5 mA at VOUT.
LDENB is active-high disable. When LDENB is high, the inverter turns off the
series NMOS and MNCL clamps the mirror gate to VSS. When low, the series NMOS
gate is at VIN, so the switch stays low-resistance down to VLOAD = 0.
MIR is 210 x 50u/1u and adds about 6 pF of drain junction capacitance at VOUT.} 0 700 0 0 0.3 0.3 {}
N 220 300 220 330 {lab=VSS}
N 470 220 470 250 {lab=ISET}
N 720 400 720 430 {lab=VSS}
N 970 400 970 430 {lab=VSS}
N 620 520 620 550 {lab=VSS}
C {gf180mcu_fd_pr/cap_mim_analog.sym} 850 500 0 0 {name=CIREF W=20u L=12.2u model=cap_mim_2f0_m4m5_noshield spiceprefix=X m=205}
N 850 470 850 440 {lab=IREF}
C {lab_pin.sym} 850 440 0 0 {name=lc1 lab=IREF}
N 850 530 850 560 {lab=VSS}
C {lab_pin.sym} 850 560 0 0 {name=lc2 lab=VSS}

C {gf180mcu_fd_pr/pfet_03v3.sym} 1500 150 0 0 {name=MPSTB model=pfet_03v3 spiceprefix=X W=2u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
C {gf180mcu_fd_pr/nfet_03v3.sym} 1500 300 0 0 {name=MNSTB model=nfet_03v3 spiceprefix=X W=1u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 1520 120 1520 150 {lab=VIN}
C {lab_pin.sym} 1520 120 0 0 {name=ls1 lab=VIN}
N 1520 330 1520 360 {lab=VSS}
C {lab_pin.sym} 1520 360 0 0 {name=ls2 lab=VSS}
N 1480 150 1440 150 {lab=STBY}
C {lab_pin.sym} 1440 150 0 0 {name=ls3 lab=STBY}
N 1480 300 1440 300 {lab=STBY}
C {lab_pin.sym} 1440 300 0 0 {name=ls4 lab=STBY}
N 1520 180 1520 270 {lab=STBYB}
C {lab_pin.sym} 1520 210 0 0 {name=ls5 lab=STBYB}
C {gf180mcu_fd_pr/pfet_03v3.sym} 1800 150 0 0 {name=MPLDB model=pfet_03v3 spiceprefix=X W=2u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
C {gf180mcu_fd_pr/nfet_03v3.sym} 1800 300 0 0 {name=MNLDB model=nfet_03v3 spiceprefix=X W=1u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 1820 120 1820 150 {lab=VIN}
C {lab_pin.sym} 1820 120 0 0 {name=ls6 lab=VIN}
N 1820 330 1820 360 {lab=VSS}
C {lab_pin.sym} 1820 360 0 0 {name=ls7 lab=VSS}
N 1780 150 1740 150 {lab=LDENB}
C {lab_pin.sym} 1740 150 0 0 {name=ls8 lab=LDENB}
N 1780 300 1740 300 {lab=LDENB}
C {lab_pin.sym} 1740 300 0 0 {name=ls9 lab=LDENB}
N 1820 180 1820 270 {lab=LDENB_B}
C {lab_pin.sym} 1820 210 0 0 {name=ls10 lab=LDENB_B}
C {gf180mcu_fd_pr/pfet_03v3.sym} 2100 150 0 0 {name=MP1 model=pfet_03v3 spiceprefix=X W=4u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 2120 120 2120 150 {lab=VIN}
C {lab_pin.sym} 2120 120 0 0 {name=lMP1vin lab=VIN}
N 2120 180 2120 210 {lab=LOAD_DIS}
C {lab_pin.sym} 2120 210 0 0 {name=lMP1d lab=LOAD_DIS}
N 2080 150 2040 150 {lab=PGOOD}
C {lab_pin.sym} 2040 150 0 0 {name=lMP1g lab=PGOOD}
C {gf180mcu_fd_pr/pfet_03v3.sym} 2300 150 0 0 {name=MP2 model=pfet_03v3 spiceprefix=X W=4u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 2320 120 2320 150 {lab=VIN}
C {lab_pin.sym} 2320 120 0 0 {name=lMP2vin lab=VIN}
N 2320 180 2320 210 {lab=LOAD_DIS}
C {lab_pin.sym} 2320 210 0 0 {name=lMP2d lab=LOAD_DIS}
N 2280 150 2240 150 {lab=STBYB}
C {lab_pin.sym} 2240 150 0 0 {name=lMP2g lab=STBYB}
C {gf180mcu_fd_pr/pfet_03v3.sym} 2500 150 0 0 {name=MP3 model=pfet_03v3 spiceprefix=X W=4u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 2520 120 2520 150 {lab=VIN}
C {lab_pin.sym} 2520 120 0 0 {name=lMP3vin lab=VIN}
N 2520 180 2520 210 {lab=LOAD_DIS}
C {lab_pin.sym} 2520 210 0 0 {name=lMP3d lab=LOAD_DIS}
N 2480 150 2440 150 {lab=LDENB_B}
C {lab_pin.sym} 2440 150 0 0 {name=lMP3g lab=LDENB_B}
N 1520 300 1520 330 {lab=VSS}
N 1820 300 1820 330 {lab=VSS}

C {gf180mcu_fd_pr/nfet_03v3.sym} 2900 150 0 0 {name=MN1 model=nfet_03v3 spiceprefix=X W=4u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 2920 120 2920 90 {lab=LOAD_DIS}
C {lab_pin.sym} 2920 90 0 0 {name=lsd1 lab=LOAD_DIS}
N 2880 150 2840 150 {lab=PGOOD}
C {lab_pin.sym} 2840 150 0 0 {name=lsg1 lab=PGOOD}
N 2920 150 2920 180 {lab=NS1}
C {gf180mcu_fd_pr/nfet_03v3.sym} 2900 210 0 0 {name=MN2 model=nfet_03v3 spiceprefix=X W=4u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 2880 210 2840 210 {lab=STBYB}
C {lab_pin.sym} 2840 210 0 0 {name=lsg2 lab=STBYB}
N 2920 210 2920 240 {lab=NS2}
C {gf180mcu_fd_pr/nfet_03v3.sym} 2900 270 0 0 {name=MN3 model=nfet_03v3 spiceprefix=X W=4u L=0.5u nf=1 m=1 ad="'int((nf+1)/2)*W/nf*0.18u'" as="'int((nf+2)/2)*W/nf*0.18u'" pd="'2*int((nf+1)/2)*(W/nf+0.18u)'" ps="'2*int((nf+2)/2)*(W/nf+0.18u)'" nrd="'0.18u/W'" nrs="'0.18u/W'" sa=0 sb=0 sd=0}
N 2880 270 2840 270 {lab=LDENB_B}
C {lab_pin.sym} 2840 270 0 0 {name=lsg3 lab=LDENB_B}
N 2920 270 2920 330 {lab=VSS}
C {lab_pin.sym} 2920 330 0 0 {name=lss3 lab=VSS}
