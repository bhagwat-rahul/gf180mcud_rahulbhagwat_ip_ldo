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

## Slot 17 harness frame — generated and verified 2026-11-20

The Chipalooza slot-17 frame is generated and checked; layout can start
against it.

- **Wrapper**: `../gf180mcu_ocd_chipalooza/magic/slot17_wrapper.mag`
  (regenerated with the harness `scripts/run_gen_user_wrappers.sh` after
  initializing its three `dependencies/` submodules).  User area = the
  `FIXED_BBOX 0 0 254854 82542` property at 5 nm file units (magscale 1 10)
  = **1274.27 × 412.71 µm**, lower-left at the wrapper origin.  In the frame
  the slot sits at x 349.76–1624.01, y 1316.65–1729.36 µm (west column;
  slots 10–18 exit west, 1–9 exit east).
- **GDS**: `../gf180mcu_ocd_chipalooza/gds/slot17_wrapper.gds` (written by
  the harness `scripts/run_gen_wrapper_gds.sh`; all 18 slots now write).
  Top cell `slot17_wrapper`, bbox (0,0)–(1392.25, 412.71) µm — the user
  area plus the two harness power switches, which live beyond x = 1274.27
  and clip into the area by < 1 µm.  Checked with
  `scripts/check_slot_gds.py`.  The 82 magic feedback entries during the
  write are all "CIF error … NPLUS" inside the harness `power_stage` cells
  at x 1297–1368 µm — outside our area, harness-side, not blocking.
- **Keep-outs inside the user area are edge furniture only**: a 0–2 µm
  obsm1/obsm2 strip on the west edge, the west-edge pin straps
  (s17_an[0]/[1] metal3 at x 0.24–4.24 µm, vss3v3 metal5 at x 0.24–4.59 µm),
  ~2.3 µm-deep stubs on the east edge, and the 2.31 µm comment-layer
  border.  Everything else is ours to fill.
- **Pin map**: `layout/slot17.mag` — guide cell in the same coordinate frame
  as the wrapper (origin lower-left, 1274.25 × 412.71 µm): the 2.31 µm slot
  border plus a tick and label at every pin (10 µm ticks for the dedicated
  pads and power rails, 5 µm for the control/bias signals).  Instance it at
  0,0 while routing and delete it before GDS release (it is `comment` layer
  only and does not export).  Slot 17 exits west:
  `s17_an[1]` y 5.70–50.02 µm, `s17_an[0]` y 175.70–220.02 µm, `vss3v3`
  y 331.72–404.00 µm.  All slots share the east-edge rails and buses
  (`vdd_3v3`, `vss_3v3`, `vdd_5v0`, `vss_5v0`, `dig_in[23:0]`,
  `dig_out[11:0]`, `vbias`, `ibias0/1`, `analog_bus[3:0]`, `reset`,
  `enable`, `clk`).

LDO pin plan (slot 17):

| LDO pin | harness pin | position / note |
| --- | --- | --- |
| VIN | `vdd_3v3` | east metal5 rail entry, port y 50.6–96.2 µm (rail rect y 8.9–96.2).  Per-slot switched 3.3 V domain (SPI reg 0x51 bit 2); our 1.8–3.6 V VIN range fits |
| VSS | `vss_3v3` + `vss3v3` | east y 113.4–143.4 µm, plus the west-edge strap (local return for the dedicated pads).  The 3.3 V and 5.0 V ground returns are not physically separate on this chip |
| VREF | `s17_an[1]` (recommended) | west y 5.70–50.02 µm — dedicated 5 V analog pad; drive 1.2 V from the board (~0.46 mA incl. the on-die load reference).  Alternatives: `analog_bus[3:0]` (shared analog pad, needs the reg 0x51 analog-bus enable) or on-chip `vbias` (voltgen high-drive may not cover 0.46 mA) |
| IBIAS | — (leave unwired) | `ldo_bias` is on-die inside `ldo_top`; the pin is a test node |
| EN | `enable` | east y 172.7–173.0 µm — this is the housekeeping *project enable* (reg 0x50 bit 0, per `slot<N>_wrapper.v`); the LDO turns on only when slot 17 is selected |
| STBY | `dig_in[k]` | east, y 158.2–171.8 µm zone — sequencer-driven, held 0 when the slot is not selected |
| LDENB | `dig_in[m]` | same zone; 0 = load armed, and the load self-sequences on PGOOD |
| VOUT | `s17_an[0]` | west y 175.70–220.02 µm — dedicated 5 V analog pad |
| PGOOD | `dig_out[j]` | east, y 150.4–157.0 µm zone — sampled to SPI regs 0x38/0x39; the shared gpio pads can also bus it out when enabled |

Integration contract (harness `scripts/get_project_gds.sh`): the tapeout
deliverable is a file `slot_17.gds` (`.gds.gz` accepted) with a **top cell
named `slot_17`**, full hierarchy, in wrapper coordinates (origin at the
user-area lower-left).  The harness reads it read-only and `getcell`s it
over the slot-17 wrapper, so our pin straps must land exactly on the
wrapper pin metal at the positions marked by `layout/slot17.mag`.

### Harness PDK libraries (container-local install)

The iic-osic-tools `gf180mcuD` PDK ships only the `gf180mcu_fd_*` libraries;
the harness layout needs three more that open-pdks main installs under
`libs.ref/` (the container's `gf180mcuD.magicrc` already carries addpath
lines for all three — only the contents were missing).  Installed
2026-11-20 into the container at `/foss/pdks/gf180mcuD/libs.ref/`, each at
its open-pdks pinned commit (see the `PROVENANCE` file in each directory):

| library | commit | magic views taken from |
| --- | --- | --- |
| `gf180mcu_as_sc_mcu7t3v3` | `aa30990f` | repo `pdk/libs.ref/` overlay, verbatim |
| `gf180mcu_ocd_io` | `6e0e354a` | repo `magic/` (+ `netlist/schematic/` spice) |
| `gf180mcu_ocd_ip_sram` | `d41c7447` | repo `cells/*/magic/` |

The install is container-local — re-run after recreating the container:

    sh scripts/install_harness_pdklibs.sh [container]

Without these, `run_gen_wrapper_gds.sh` fails with "Failed on cell
gf180mcu_as_sc_mcu7t3v3__tap_2" and leaves 0-byte GDS files.

