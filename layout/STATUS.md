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

## Remaining (4 blocks + top)
- `ldo_load`: finish LVS connectivity (see above), then commit.
- `ldo_error_amp` (20 devices; needs new sizes p50/0.5, p50/2, n16/2,
  p40/0.5, p20/0.5, n40/0.5, n32/2, p40/1, n40/1, R 222.66/1, caps
  10+20 units).  Single-row track router applies.
- `ldo_startup` (12 devices; 80 x 50x50 cap units + 205/62/40-unit
  20x12.2 arrays + 996/257/64/57 um resistors).  Needs a 50x50-unit MIM
  array generator; the 20x12.2 `cap_array` is reusable.
- `ldo_top` (99 instances) and full-chip slot assembly.

## Area budget warning
Reference MIM plate area: softstart 9.8k, load 50k, startup 275k um^2
(= 335k total).  At the current 63% array fill that is ~530k um^2, i.e.
already the whole 525.8k um^2 slot before FETs and routing.  The cap
arrays must be repacked to >=85% fill (tighter pitch, 50x50 unit arrays
for the startup caps) or the slot cannot hold the design.
