# LDO layout status

## Blocks fully clean (DRC 0 / LVS / antenna / PEX / GDS), committed
| block | commit | area driver |
|---|---|---|
| ldo_softstart | 2060d57 | 40-unit MIM array + RSS + reset nfet |
| ldo_bias | 16e6e2d | 8 small transistors |
| ldo_pgood | e7423ea | 12 transistors + 3 long poly resistors |
| ldo_power_stage | (this commit) | 400-finger pass array + 3 devices |

## Device library (committed dcbcf7a)
- `transistor_cell()`: re-ported single MOSFETs, KLayout-clean and
  extraction-exact for every size used so far
  (n 1/0.5, 2/0.5, 2/2, 4/0.5, 8/1, 50/1, 50/0.5, 20/0.5;
   p 0.22/0.28, 2/0.5, 2/2, 4/0.5, 4/2, 8/0.5, 40/0.5, 50/0.28).
- `array_fet()`: compact interdigitated array (n fingers, shared diff,
  metal1 straps, gate rail, metal3 S/D buses, guard ring tied to source).
  Verified n=2 and n=1/8/210/400 at W=50; extraction yields n devices
  which netgen merges in parallel (m=NNN in the reference matches).
- `cap_array(nx, ny, count=...)`: 205 units in 15 columns, DRC-clean,
  extracts 205 parallel caps.
- Resistor cells: all 12 ppolyf_u_3k values + 20 um-wide ppolyf_u.

## In progress
(none) -- `ldo_power_stage` completed: end-tapped metal3 buses (no long
run along the S/D bus row), single separated metal2 drops, VSS label on
the guard-ring tie.  DRC 0 / LVS PASS / antenna 0 / PEX PASS / GDS PASS.

## ldo_load -- CLEAN (5th block)
`layout/ldo_load.mag` + `scripts/build_load.py`:
- 13 small devices in one row (metal3 tracks), XMIR 210-finger array,
  XMNSW 8-finger array, XMREF 1-finger array, XRSET, 205-unit cap.
- DRC 0, LVS PASS (438 statements), antenna 0, PEX PASS, GDS PASS.
- Fixes this round: array guard rings are substrate taps (VSS) and must
  NOT be tied to a non-VSS source; XMREF's diode drain bus had to be
  tied to IREF; XMPINV/XMNINV had D and G swapped relative to the
  reference (D=LDB, G=LOAD_DIS).
- Option A: the LVS reference normalises the bulk of XMN1, XMN2 and
  XMNSW to VSS (process-legal p-substrate connection).  The schematic
  still shows bulk=source for those three; **PVT re-certification with
  bulk=VSS is still outstanding**.

## ldo_error_amp -- CLEAN (6th block)
`layout/ldo_error_amp.mag` + `scripts/build_amp.py`: 14 arrays (with the
schematic m multipliers folded in as extra fingers), 4 resistors, two
MIM arrays.  DRC 0, LVS PASS (57 statements), antenna 0, PEX PASS,
GDS PASS.  All device bulks are VIN/VSS (process-legal; no isolation
needed in this block).

## Slot-fit analysis (MEASURED)
ldo_startup **placement** (all cells, not yet wired): real bbox
**1267.40 x 404.20 um = 512.3k um2**, KLayout DRC 0.  It fits inside
1274.27 x 412.71 by itself, using 97% of the slot.

The six other committed blocks measure 396.1k um2 (sum of their real
bounding boxes).  Startup alone + the others = 908k um2 = 1.73x the
525.9k slot, so the full chip cannot be assembled into this slot even
though each block individually fits.

This is now a measurement, not an estimate.  The startup block alone
consumes 97% of the slot because the four MIM arrays (80x50x50, 205,
62 and 40 units) have 380k um2 of bounding box.  The MIM plate area
alone is 342k um2 = 65% of the slot.

## ldo_startup device cells (ready, block not built)
cap_80 (80 x 50x50 MIM, 16x5), cap_205/62/40/10/4 (20x12.2 arrays),
amp_p50_l028_n10/n4 (pass switches), amp_n10_l05, ppolyf_u_rbld
(10/57.143).  All KLayout-clean; cap_80 extracts 80 caps.

## ldo_startup -- CLEAN (7th block)
`layout/ldo_startup.mag` + `scripts/build_startup.py`: cap_80 (80x50x50),
cap_205/62/40, five resistors, three switches.  DRC 0, LVS PASS (407
statements), antenna 0, PEX PASS, GDS PASS.  Final fixes: SWGC branch
moved off the VSS via at (870,312); RBLEDPD2's BLED pad connected via
a route around the BLD bus; VIN label moved onto the wire; body rings
tied to their sources on metal1.

Measured block bbox 1267.4 x 404.2 um (97% of the slot).

## Remaining
- ldo_top assembly + assembled bbox measurement.
- bulk=VSS PVT re-certification.
