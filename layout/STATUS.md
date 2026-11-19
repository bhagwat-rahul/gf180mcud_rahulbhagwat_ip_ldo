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

## Slot-fit analysis (blocking)
Reference MIM plate area: softstart 9.8k + load 50.0k + error_amp
7.3k + startup 274.9k = **342,008 um^2**.  Even at 85% array fill
that is 402k of the 525.8k slot (76%), before any transistors,
resistors or routing.  Sum of the six existing block bounding boxes is
already ~822k um^2 (load alone 745x300, startup caps 880x280+375x220).
The full chip therefore does **not** fit the assigned slot at the
certified capacitance values with the current block floorplans; a
design decision is required (reduce capacitance with re-certification,
increase the slot, or use a denser MIM option).

## ldo_startup device cells (ready, block not built)
cap_80 (80 x 50x50 MIM, 16x5), cap_205/62/40/10/4 (20x12.2 arrays),
amp_p50_l028_n10/n4 (pass switches), amp_n10_l05, ppolyf_u_rbld
(10/57.143).  All KLayout-clean; cap_80 extracts 80 caps.
