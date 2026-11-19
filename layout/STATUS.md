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

## Remaining
- `ldo_load` (18 devices; 210-finger array, 205-unit cap, 2D small-device
  grid needs per-row routing channels), `ldo_error_amp` (20 devices),
  `ldo_startup` (12 devices, 80 x 50x50 + 205/62/40-unit cap arrays),
  `ldo_top` (99 instances).
- Top-level assembly and slot fit.

## Area budget warning
Reference MIM plate area: softstart 9.8k, load 50k, startup 275k um^2
(= 335k total).  At the current 63% array fill that is ~530k um^2, i.e.
already the whole 525.8k um^2 slot before FETs and routing.  The cap
arrays must be repacked to >=85% fill (tighter pitch, 50x50 unit arrays
for the startup caps) or the slot cannot hold the design.
