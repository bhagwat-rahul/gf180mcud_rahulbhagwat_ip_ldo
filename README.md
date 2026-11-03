# LDO design for chipalooza #3 on wafer.space (gf180mcuD)

## What's an LDO?

A Low Dropout Regulator (LDO) is a voltage regulator that will supply variable amounts of current to the cpu at whatever voltage it wants that current at.
Eg. If your computer is not doing much you might need very little energy, but when its doing a lot of work you need to provide a lot more current (still maintaining the same voltage levels), so the ldo varies its resistance to supply whatever current the CPU needs while keeping voltage stable (within a limit).
