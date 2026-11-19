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

## 2. nfet_03v3_w2_l05_wide -- 3 markers, device-internal

`layout/nfet_03v3_w2_l05_wide.mag` is the PDK `nfet_03v3` W=2 L=0.5 cell
with routing-friendly terminal metal (S/D risers, gate pad, bulk pad; the
bulk bars and contact-bar end-caps are removed).  Extraction parameters
are unchanged (`w=2u l=0.5u`).

Remaining markers, all inside the cell:

* **M1.2a x2** -- the PDK contact enclosures leave only **0.21 um**
  between the S/D contact metal and the gate contact metal (rule: 0.23).
  The channel is 1.02 um wide and three 0.28 um escapes plus spacing need
  1.40 um, so no escape geometry at this width can satisfy it.
* **M1.3 x1** -- the bottom gate contact's metal island is 0.37 x 0.23 um
  (0.085 um^2, minimum 0.09).  Removing the contact makes magic's
  poly/polycontact extraction produce PL.* errors, so it stays.

**Resolution plan:** draw the nfet from primitives (pwell, ndiff, poly,
contacts, metal1) as a custom cell with the gate contact moved >= 0.23 um
from the S/D bars (e.g. staggered landing pads above the tap strips).
W/L and the extracted model stay `nfet_03v3 w=2u l=0.5u`.
