# Layout baseline

`ldo_top.mag` + 7 child block cells + per-device gencell cells, generated
from `schematics/` with `scripts/import_layout.sh`. Everything is instanced
hierarchically: open `ldo_top` in Magic and every block is a real cell use
with its devices inside, all with port labels.

What imported as real layout:
- All `nfet_03v3` / `pfet_03v3` (gencell), including `m=` as vertical stacks
- `RBLEED` is now `pplus_u` 360 k (W=0.5, L=863.5 um): ~866 um straight, fits
  the slot unfolded, imported as real geometry. Its n-well body must tie to
  **VIN** (schematic already does) so the p+/n-well junctions stay
  reverse-biased. Same +1375 ppm/C TC as the old n+ stick, so the
  cold-heavy/hot-light bleed corners are preserved.
- All `nplus_u` and `ppolyf_u` (350 ohm/sq) resistors at true length
- All MIM caps via the `cap_mim_2p0fF` gencell (M4-M5, 2 fF/um^2); the
  schematic models them as `cap_mim_2f0_m4m5_noshield`, which is what Magic
  extraction will name them, so LVS matches

Still manual — the 3k-poly placeholder list (one shared empty cell
`ppolyf_u_3k.mag`; draw each folded/serpentine and give each instance its own
cell, or the first one you draw will be reused everywhere). After the
narrowing pass they are all short enough to fit the 1274 um slot width as one
straight run:

| Instance | Value | W | Drawn length |
| --- | --- | --- | --- |
| `RSS` | 1.02 M | 0.5 | 155 um |
| `RPRE_D` | 1.02 M | 0.5 | 155 um |
| `RMODE_D` | 1.02 M | 0.5 | 155 um |
| `RSWGC` | 1.02 M | 0.5 | 155 um |
| `RSWGCC` | 1.02 M | 0.5 | 155 um |
| `RBLEDPD1` | 256 k | 0.5 | 38.6 um |
| `RBLEDPD2` | 1.02 M | 0.5 | 155 um |
| `RTH` | 205 k | 1.0 | 65.0 um |
| `RLOW` | 1.84 M | 1.0 | 586 um |
| `RHYS` | 3.13 M | 1.0 | 996 um |
| `RTOP` | 614 k | 2.0 | 400 um (unchanged) |
| `RBOT` | 1.23 M | 2.0 | 800 um (unchanged) |

`RTOP`/`RBOT` stay at W=2 on purpose: they set the ±3% DC accuracy, and wider
is better for divider matching.

Also still manual:
- `MPASS` (m=400) imports as a single ~20.5 mm tall finger stack and
  `MIR` (m=210) as ~5.4 mm. Re-floorplan both into 2D arrays inside the
  1274 x 413 um slot; total area is fine, only the stacking is absurd.
- Device `use` transforms are a naive left-to-right row; this is a device
  source, not a floorplan.

Notes:
- `RPRE` is a single `W=200u L=68.229u m=1` resistor (119.4 ohm). The old
  `W=50u m=4` form made Magic stack 4 segments in series (~1.9 k) while
  SPICE treated them as parallel (119 ohm) — LVS would have failed.
- The narrow resistors (W=0.5/1.0) were re-targeted with the PDK model's
  `r_dw`/`r_dl` edge corrections so their nominal resistance is unchanged;
  the full PVT matrix re-run (`.amp/in/single-loop/pdk-fix9`) certifies it.
- The `error_s`/`checkpaint` rectangles in the generated cells are import
  feedback marks, not geometry; delete them as you go.
