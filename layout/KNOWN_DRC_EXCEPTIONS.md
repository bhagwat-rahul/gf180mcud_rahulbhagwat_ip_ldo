# Known DRC exceptions (block-level KLayout runs)

Two classes of KLayout DRC markers come from **PDK-supplied device cells**,
not from our routing.  They are recorded here so a block check can be
judged on its own geometry; they must be resolved before tapeout (see
"Resolution plan").

## 1. MIM cap gencell vs MIMTM.1

The PDK's `cap_mim_2p0fF` gencell (used for every MIM cap in the design)
violates **MIMTM.1** ("MiM bottom plate spacing to bottom plate metal,
1.2 µm") all by itself: 78 markers on a single 40-unit stack
(`layout/cap_mim_2p0fF_UFNFZK.mag`).  The stack pitch leaves 1.14 µm
between the metal4 bottom plate of one unit and the virtual bottom plate
(top plate +1.06 µm) of the next, i.e. 0.06 µm short.

Evidence: running the foundry deck on the cap cell alone gives
`{'MIMTM.1': 78}`; on the nfet cell alone `{'M1.3': 2, ...}`.

**Resolution plan:** draw a custom MIM array (same electrical stack:
mimcap / mimcapcontact / metal4 / via4 / metal5) with a pitch that leaves
>= 1.2 µm between unit caps, then re-run LVS/DRC.  The cap cell is a leaf
cell, so this does not change the netlist.

## 2. nfet/pfet gencell contact-bar metal

The PDK MOSFET gencells draw narrow metal1 end-caps on their contact bars
(0.23 x 0.055 um).  In isolation they violate **M1.1** (min metal1 width
0.23) and **M1.3** (min metal1 area).  In a block they additionally sit
0.20-0.22 um from neighbouring pads (M1.2a 0.23) because the cell is only
2.4 um wide while its drain/source/gate need three escaping rails.

Current handling in `scripts/build_softstart.py`: the redundant end-caps
are removed after flattening (the contact bars remain, and the block's own
metal pads cover them), which removes the PDK-inherent M1.1/M1.3 markers.

**Resolution plan:** for blocks where the escapes still crowd the cell
(e.g. ldo_softstart's MNRESET), draw a wider transistor cell at the same
W/L (extra source/drain/gate landing pads) or use a mirrored/rotated
placement with more channel.  Only the geometry changes; extraction and
LVS parameters stay identical.
