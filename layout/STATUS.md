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

## ldo_startup wiring plan (next session, coordinates)
Placement (committed d2ee1c4, DRC 0, 1267.4 x 404.2):
- caps: cap_80 (0,80) T(-23,328.5) B(27,51.5); cap_62 (0,-40)
  T(-6,17) B(-6,-50.5); cap_40 (450,-40) T(444,32.5) B(444,-50.5);
  cap_205 (880,80) T(874,292) B(874,69.5).  All metal5 -> down_to
  metal3.
- resistors rot90: RSWGC (880/1137.86,300), RSWGCC (...,306),
  RBLEDPD2 (...,312); RBLEDPD1 must move to (1200,360) vertical
  pads (1200,388.4)/(1200,331.6) to free the long verticals.
  RBLD at (861,300) pads (861,328.85)/(861,271.15) -- move to
  horizontal (1071..1129,340) to avoid the cap_205 body and the
  SWGCC vertical at x=874.
- switches: MPCC (1150,325) G(1149.45,350.87) S(1149.68,296.65)
  D(1157.96,295.45) B(1148.55,325); MPCG (1165,325)
  G(1164.45,350.87) S(1164.68,296.65) D(1167.44,295.45) B(1163.55,325);
  MNBLD (1180,325) G(1179.45,330.87) S(1179.68,316.65) D(1180.82,315.45)
  B(1178.55,325).
Lanes (metal3): CCF y=40, CGFF y=-45, VIN y=-56, SWGC y=365,
SWGCC y=372, BLED y=345; verticals x=1120 (CCF), 1130 (CGFF),
1172 (VSS), 1164 (SWGC), 1149 (SWGCC).  Ports COMP2 (-23,335),
GATE (444,44), ENB (1138,303), VIN, VSS, VOUT, PGOOD (1200,60).
Known collision to solve: RBLD/VOUT horizontal at y=296.65 vs the
SWGCC cap vertical at x=874 -- move RBLD right of x~1140 or route
VOUT at y=285 from the left end of the S buses.
