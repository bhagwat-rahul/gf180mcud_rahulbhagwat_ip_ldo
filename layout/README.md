# Layout baseline

`ldo_top.mag` + 7 child block cells + per-device gencell cells, generated
from `schematics/` with `scripts/import_layout.sh`. Everything is instanced
hierarchically: open `ldo_top` in Magic and every block is a real cell use
with its devices inside, all with port labels.

What imported as real layout:
- All `nfet_03v3` / `pfet_03v3` (gencell), including `m=` as vertical stacks
- All `nplus_u` and `ppolyf_u` (350 ohm/sq) resistors, drawn at true length
- All MIM caps via the `cap_mim_2p0fF` gencell (M4-M5, 2 fF/um^2); the
  schematic models them as `cap_mim_2f0_m4m5_noshield`, which is what Magic
  extraction will name them, so LVS matches

What is still a placeholder — the manual layout list:
1. `ppolyf_u_3k` has no Magic gencell. All twelve 3k-poly resistors reference
   one shared empty cell `ppolyf_u_3k.mag`. Draw each folded/serpentine and
   give each instance its own cell (copy + rename), or the first one you draw
   will be reused everywhere:
   `RTOP 600k`, `RBOT 1.2M`, `RBLEED 360k n+ (3.6 mm — fold)`, `RSS 1M`,
   `RTH 200k`, `RLOW 1.8M (1.2 mm)`, `RHYS 3.06M (2.0 mm)`,
   `RSWGC 1M`, `RSWGCC 1M`, `RBLEDPD1 250k`, `RBLEDPD2 1M`,
   `RPRE_D 1M`, `RMODE_D 1M`
2. `MPASS` (m=400) imports as a single ~20.5 mm tall finger stack and
   `MIR` (m=210) as ~5.4 mm. Re-floorplan both into 2D arrays inside the
   1274 x 413 um slot; total area is fine, only the stacking is absurd.
3. Device `use` transforms are a naive left-to-right row; this is a device
   source, not a floorplan.

Notes:
- `RPRE` is fixed in the schematic as a single `W=200u L=68.229u m=1`
  resistor (119.4 ohm). The old `W=50u m=4` form made Magic stack 4 segments
  in series (~1.9 k) while SPICE treated them as parallel (119 ohm) — LVS
  would have failed.
- The `error_s`/`checkpaint` rectangles in the generated cells are import
  feedback marks, not geometry; delete them as you go.
