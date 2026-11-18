# LDO design for chipalooza #3 on wafer.space (gf180mcuD)

## Draft target specification

1. Supply and output: Single-slot power-domain LDO, nominal 3.3 V input → 1.8 V output, ±3% DC accuracy, targeting 0–100 mA with an internal load.
2. Modes: Adaptive-bias RUN; 1.8 V STANDBY supporting ≤1 mA with ≤20 µA quiescent current; OFF with controlled output discharge.
3. Sequencing: Harness-controlled enable/mode, soft-start and 3.3 V-domain power-good for downstream reset/isolation; keep the controller powered while the regulated domain is off.
4. Regulation: Target ≤300 mV dropout at 100 mA, ≥60° phase margin across PVT/load/capacitance corners, and RUN 0↔100 mA load transitions with 100 ns rise/fall times; no large external output capacitor assumed. Capacitance range and transient excursion/recovery limits remain provisional.
5. Test access and limits: Disableable programmable 0–100 mA on-die load; unchanged analog pad for sensing/light loading within its 10 mA DC rating, with transient currents checked separately; 100 mA operation requires harness supply/return, switch, package and thermal approval (~330 mW total at nominal full on-die load).

## Schematic prototype

The editable hierarchy starts at [schematics/ldo_top.sch](schematics/ldo_top.sch).
It contains a two-stage error amplifier, PMOS pass stage with a mode-switched
compensation zero, soft-start, power-good and a sequenced startup block. The
pass device represents 400 parallel 50 µm-wide units (20 mm total), not a
completed physical layout. No Verilog is needed for this regulator-only
prototype; the internal load and harness wrapper are deferred.

Real GF180MCU-D MOS models and PDK poly/MIM passives are used; the external
1.2 V reference and sourced 1 µA bias remain ideal. **The five lines above are
targets, not achieved specifications.** On the editable sheets the redesign
meets the provisional DC, ≥60° AC and 100 ns step gates (see below), but that is
schematic-level evidence only: no layout, mismatch, EM/IR or package model is
included. Do not start layout from these values as though they are signed off.

See [simulation instructions and limitations](sim/README.md) to regenerate the
SPICE netlist, run the characterization, and render the actual Xschem sheets.

## Single-loop redesign — November 18, PDK passives

The redesign is implemented in `schematics/`; the latest full matrix is
`.amp/in/single-loop/pdk-fix3/`. It keeps the single balanced two-stage
amplifier and adds a mode-switched compensation zero (400 Ω in RUN, 18 kΩ in
STANDBY), sequenced preload/boost mode transitions and the new sequenced
startup block. Characterization of the editable sheets gives:

- **AC, 1080 cases**: every case has one unity crossing; worst phase margin
  **62.08°** (STANDBY 0 A, `ss`/−40 °C/3.6 V/1 nF), worst RUN **79.03°**.
- **DC, 90 cases**: RUN 1.80030–1.80090 V, STANDBY 1.80348–1.82260 V, inside
  the ±3% band 1.746–1.854 V; worst STANDBY `IQ` 19.625 µA.
- **Transient, 10 cases**: all settle inside the band; the 100 ns load-step
  peak is 1.877 V (no transient excursion limit has been agreed). The separate
  exact 0↔100 mA / 100 ns 270-case matrix still needs to be re-run on the
  PDK-passive design.
- **Startup, 7 cases**: minimum **−1.457 mV**, maximum **1.800782 V**; all pass
  the −50 mV/1.854 V gate, including the cold/10 pF corner.
- **Dropout, 15 cases**: 15/15 pass; VOUT at VIN=2.1 V is 1.80012–1.80033 V.
- **PGOOD**: rising 1.6249 V, falling 1.5342 V; **RUN↔STANDBY↔RUN** modes
  settle 1.7720–1.8327 V.

All 1080 AC cases are valid. The pass device is still a schematic composite,
not a layout; no mismatch, EM/IR or package model is included. Full evidence and
limits are in [sim/README.md](sim/README.md).

## Sequenced startup — November 18

The startup fix is in `schematics/ldo_startup.sch`, instantiated from
`ldo_top.sch`. `CC` and `CGF` are disconnected while the pass-device gate falls,
then reconnect through PMOS soft switches driven by two `ENB` RC ramps:
`CGF` first (40 pF, ~30 pF effective) to stabilize the loop, and `CC` later
(100 pF) once the loop can absorb its charge. A 2 kΩ switched bleed holds
`VOUT` at zero during the gate transition and turns off after the `CC` switch
is on. The bleed is set by a 250 kΩ/1 MΩ divider from the `CC` ramp, so it
turns off only after the compensation is restored.

Worst measured startup at `ss`, −40 °C, 3.6 V, 10 pF: `VOUT` minimum
**−3.15 mV**, maximum **1.80042 V**, no overshoot or PGOOD chatter. Typical
startup into 0/1 mA/100 mA: minimum **−1.5/−0.6/−0.01 mV**, maximum
**1.80058/1.80057/1.80049 V**. The full PVT matrix is being re-run from these
sheets.

## What's an LDO?

A Low Dropout Regulator (LDO) is a voltage regulator that will supply variable amounts of current to the cpu at whatever voltage it wants that current at.
Eg. If your computer is not doing much you might need very little energy, but when its doing a lot of work you need to provide a lot more current (still maintaining the same voltage levels), so the ldo varies its resistance to supply whatever current the CPU needs while keeping voltage stable (within a limit).
