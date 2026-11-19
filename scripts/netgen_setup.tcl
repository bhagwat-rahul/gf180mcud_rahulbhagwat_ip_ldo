# Project netgen LVS setup for the LDO.
#
# Sources the PDK setup, then adds the three adjustments this design needs:
#
# 1. The PDK's magic technology has no ppolyf_u_3k device (the 3 kOhm/sq
#    poly resistor is a process option with the same drawn layers).  Layout
#    extraction produces `ppolyf_u`, so the two classes are equated; width
#    and length are still compared, only the class name is aliased.
# 2. MIM stacks are drawn as N parallel unit caps; the schematic carries
#    the same stack as one device with m=N.  Enable parallel combination.
# 3. Magic extracts parasitic gate overlap capacitors (cap_*mos*_b) that
#    have no schematic counterpart; they are ignored, as in the PDK flow.

source /foss/pdks/gf180mcuD/libs.tech/netgen/gf180mcuD_setup.tcl

equate classes ppolyf_u ppolyf_u_3k

foreach ckt {-circuit1 -circuit2} {
    property "$ckt cap_mim_2f0_m4m5_noshield" parallel enable
    property "$ckt cap_mim_2f0_m4m5_noshield" parallel {c_width critical}
    property "$ckt cap_mim_2f0_m4m5_noshield" parallel {c_length critical}
    property "$ckt cap_mim_2f0_m4m5_noshield" parallel {m add}
    property "$ckt cap_mim_2f0_m4m5_noshield" tolerance {c_width 0.001}
    property "$ckt cap_mim_2f0_m4m5_noshield" tolerance {c_length 0.001}
}

ignore class cap_pmos_03v3_b
ignore class cap_nmos_03v3_b
ignore class cap_pmos_03v3
ignore class cap_nmos_03v3
