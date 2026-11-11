# LDO design for chipalooza #3 on wafer.space (gf180mcuD)

## Draft target specification

1. Supply and output: Single-slot power-domain LDO, nominal 3.3 V input → 1.8 V output, ±3% DC accuracy, targeting 0–100 mA with an internal load.
2. Modes: Adaptive-bias RUN; 1.8 V STANDBY supporting ≤1 mA with ≤20 µA quiescent current; OFF with controlled output discharge.
3. Sequencing: Harness-controlled enable/mode, soft-start and 3.3 V-domain power-good for downstream reset/isolation; keep the controller powered while the regulated domain is off.
4. Regulation: Target ≤300 mV dropout at 100 mA and ≥60° phase margin across PVT/load/capacitance corners; no large external output capacitor assumed, with capacitance and transient limits TBD.
5. Test access and limits: Disableable programmable 0–100 mA on-die load; unchanged analog pad for sensing/light loading within its 10 mA DC rating, with transient currents checked separately; 100 mA operation requires harness supply/return, switch, package and thermal approval (~330 mW total at nominal full on-die load).

## What's an LDO?

A Low Dropout Regulator (LDO) is a voltage regulator that will supply variable amounts of current to the cpu at whatever voltage it wants that current at.
Eg. If your computer is not doing much you might need very little energy, but when its doing a lot of work you need to provide a lot more current (still maintaining the same voltage levels), so the ldo varies its resistance to supply whatever current the CPU needs while keeping voltage stable (within a limit).
