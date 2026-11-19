# Known DRC exceptions (block-level KLayout runs)

Two classes of KLayout DRC markers come from **device-cell geometry**, not
from block routing.  They are recorded here so a block check can be judged
on its own routing; they must be resolved before tapeout (see
"Resolution plan").

## 1. MIM cap array -- RESOLVED

The PDK `cap_mim_2p0fF` gencell violates **MIMTM.1** in its 40-unit stack
(78 markers on the cell alone; unit pitch 14 um leaves 1.14 um instead of
the required 1.2 um to the next virtual top plate).

`scripts/build_devices.py` now generates `layout/cap_mim_array.mag`:
4 x 10 unit caps at 25.0 x 15.5 um pitch, top plates strapped on metal5
through the mimcapcontact regions, bottom plates through the cells' via4
edge bars, buses on opposite sides so the two metal5 networks never cross.
The array is **KLayout DRC clean** and extraction gives 40 parallel caps
(`c_width=20u c_length=12.2u`) between the BOT and TOP ports.

## 2. nfet_03v3_w2_l05_wide -- 2 markers, device-internal

`layout/nfet_03v3_w2_l05_wide.mag` re-ports the PDK `nfet_03v3` W=2 L=0.5:
both gate heads, bulk bars/links and S/D end-caps are removed; the gate
poly is re-drawn as a stripe extending over field with p-well notches
under the extensions, contacted at the top; S/D fan out above the tap
strips.  Extraction is unchanged (`nfet_03v3 w=2u l=0.5u`); magic also
extracts a gate-to-well parasitic (`cap_pmos_03v3_b`) which the project
netgen setup ignores.

Remaining markers:

* **DF.1c x2** -- magic's CIF writes the MOS-capacitor marker (166/5) on
  the 0.5 um-wide field poly extension, and the deck then requires a
  1 um COMP width there.  The extension is real field poly (not a
  capacitor), so this is a marker-layer false positive, but it must be
  cleared rather than waived.

**Resolution plan:** draw the transistor from primitives as a single cell
whose gate contact sits over field *outside* the p-well (e.g. shift the
well boundary so the poly landing is on field oxide outside it, or use a
1 um-wide poly landing with the S/D fan-out routed around it).  W/L and
the extracted model must stay `nfet_03v3 w=2u l=0.5u`.

## Current block status (ldo_softstart)

* LVS (netgen) PASS, antenna 0 markers, PEX PASS, GDS export PASS.
* KLayout DRC: 2 markers, both DF.1c inside the nfet cell (above).
