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

## 2. nfet_03v3_w2_l05_wide -- RESOLVED

`layout/nfet_03v3_w2_l05_wide.mag` re-ports the PDK `nfet_03v3` W=2 L=0.5
from its own geometry: both gate heads, bulk bars/links and S/D end-caps
removed; gate poly re-drawn as a stripe over field; the p-well extended
under the poly landing and the p-substrate ring notched where the poly
crosses it (this is what created magic's substrate MOS-capacitor marker
and the DF.1c error); gate contacted at the top; S/D fanned out above the
tap strips.  The cell is **KLayout DRC clean** and extracts as a single
`nfet_03v3 w=2u l=0.5u` with no parasitic devices.

## Current block status

* `ldo_softstart`: **clean** -- KLayout DRC 0 markers, LVS PASS, antenna
  0 markers, PEX PASS, GDS export PASS.
