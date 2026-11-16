# LDO design for chipalooza #3 on wafer.space (gf180mcuD)

## Draft target specification

1. Supply and output: Single-slot power-domain LDO, nominal 3.3 V input → 1.8 V output, ±3% DC accuracy, targeting 0–100 mA with an internal load.
2. Modes: Adaptive-bias RUN; 1.8 V STANDBY supporting ≤1 mA with ≤20 µA quiescent current; OFF with controlled output discharge.
3. Sequencing: Harness-controlled enable/mode, soft-start and 3.3 V-domain power-good for downstream reset/isolation; keep the controller powered while the regulated domain is off.
4. Regulation: Target ≤300 mV dropout at 100 mA, ≥60° phase margin across PVT/load/capacitance corners, and RUN 0↔100 mA load transitions with 100 ns rise/fall times; no large external output capacitor assumed. Capacitance range and transient excursion/recovery limits remain provisional.
5. Test access and limits: Disableable programmable 0–100 mA on-die load; unchanged analog pad for sensing/light loading within its 10 mA DC rating, with transient currents checked separately; 100 mA operation requires harness supply/return, switch, package and thermal approval (~330 mW total at nominal full on-die load).

## Schematic prototype

The editable hierarchy starts at [schematics/ldo_top.sch](schematics/ldo_top.sch).
It contains 41 logical MOS devices across bias/adaptation, a two-stage error
amplifier, PMOS pass stage with a mode-switched compensation zero, soft-start
and power-good. The pass device represents 800 parallel 50 µm-wide units
(40 mm total), not a completed physical layout. No Verilog is needed for this
regulator-only prototype; the internal load and harness wrapper are deferred.

Real GF180MCU-D MOS models are used, but resistors/capacitors and the external
1.2 V reference / sourced 1 µA bias remain ideal. **The five lines above are
targets, not achieved specifications.** On the editable sheets the redesign
meets the provisional DC, ≥60° AC and 100 ns step gates (see below), but that is
schematic-level evidence only: no layout, mismatch, EM/IR or package model is
included. Do not start layout from these values as though they are signed off.

See [simulation instructions and limitations](sim/README.md) to regenerate the
SPICE netlist, run the characterization, and render the actual Xschem sheets.

## Single-loop redesign — November 15

The redesign is implemented in `schematics/`; a byte-identical copy of the
sheets and the characterization outputs are kept under
`.amp/in/single-loop/candidate/`. It keeps the single balanced two-stage
amplifier and adds a mode-switched compensation zero (400 Ω in RUN, ~10 kΩ in
STANDBY) plus sequenced preload/boost mode transitions. Characterization of the
editable sheets gives:

- **AC, 1080 cases**: every case has one unity crossing; worst phase margin
  **72.1°** (STANDBY 0 A, `fs`/125 °C/3.6 V/1 nF), worst RUN **77.1°**.
- **DC, 90 cases**: RUN 1.8002–1.8007 V, STANDBY 1.8042–1.8287 V, inside the
  ±3% band 1.746–1.854 V; worst STANDBY `IQ` 17.6 µA.
- **Exact 0↔100 mA / 100 ns steps**: **270/270** pass the provisional
  1.62–1.98 V and 20 µs gates (worst excursions 1.6849 V and 1.9515 V, recovery
  ≤0.041 µs) over 5 corners, 3 temperatures, 3 supplies and 10/100/1000 pF.
- Startup, 300 mV dropout at 100 mA, PGOOD and RUN↔STANDBY↔RUN
  (**1.7601–1.8298 V**) also pass.

Nine STANDBY 0 A cases at `ff`/125 °C are rejected by the 40 dB loop-gain
validity heuristic (their measured gain is 32–36 dB) although their phase margin
is 78–91° and a reversed-probe re-measurement reproduces it exactly. Resistors,
capacitors, the reference and the bias are still ideal, and the pass device is a
schematic composite, not a layout. Full evidence and limits are in
[sim/README.md](sim/README.md#single-loop-redesign--november-15).

## What's an LDO?

A Low Dropout Regulator (LDO) is a voltage regulator that will supply variable amounts of current to the cpu at whatever voltage it wants that current at.
Eg. If your computer is not doing much you might need very little energy, but when its doing a lot of work you need to provide a lot more current (still maintaining the same voltage levels), so the ldo varies its resistance to supply whatever current the CPU needs while keeping voltage stable (within a limit).
