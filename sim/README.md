# Regulator-only schematic characterization

This is a working transistor-level prototype, not a layout-ready design or a
claim that every README target is met. The programmable on-die load is deferred;
independently commanded testbench loads exercise the regulator without telling
its adaptive-bias circuit when a load change will happen.

## Run in IIC-OSIC

From this repository's root inside the running container:

```sh
iic-pdk gf180mcuD
python3 sim/run.py --out .amp/in/sim
python3 sim/run.py --full --jobs 6 --out .amp/in/full-sim
python3 sim/plot.py .amp/in/full-sim --out .amp/in/artifacts
python3 sim/render.py --out .amp/in/artifacts
```

On the host, the full simulation command is:

```sh
docker exec \
  -w /foss/designs/current-designs/chipalooza3/gf180mcud_rahulbhagwat_ip_ldo \
  iic-osic-tools_xserver_uid_501 \
  bash -ic 'iic-pdk gf180mcuD; python3 sim/run.py --full --jobs 6 --out .amp/in/full-sim'
```

The tools use Python/numpy/matplotlib/CairoSVG already installed in that
container, Xschem, and ngspice. No packages were added. `xschemrc` loads the
installed GF180MCU-D configuration from `PDK_ROOT`. The interactive testbench's
model paths use the container's `/foss/pdks`; the runner substitutes `PDK_ROOT`
when generating test decks.

Run `xschem --rcfile schematics/xschemrc schematics/ldo_top.sch` from the
repository root to open the hierarchy, or open `ldo_tb.sch` for the nominal
operating point. Each reusable block has an editable schematic and matching
symbol. The runner always netlists these sheets; no second implementation in
handwritten SPICE needs to be kept in sync.

Each result directory contains `ldo_tb.spice`, one deck/log/data file per case,
source hashes, `results.json`, and DC/AC/dropout CSVs. A nonzero exit status means
a numerical error or an implemented check failed; inspect the logs/JSON rather
than treating a generated plot as a pass. Outputs default to ignored
`.amp/in/`; add `/.amp/in/` to `.git/info/exclude` in a fresh checkout.

## Implemented blocks and interfaces

| Sheet | Logical MOS | Function |
| --- | ---: | --- |
| `ldo_top.sch` | 0 additional | Divider, compensation and ~5 µA preload; hierarchy |
| `ldo_bias.sch` | 8 | Sourced-current entry, EN inverter, replica-pass adaptation in RUN |
| `ldo_error_amp.sch` | 11 | NMOS input pair, PMOS mirror, common-source gate driver, OFF clamp |
| `ldo_power_stage.sch` | 3 | 10,000 µm total-width PMOS pass device, gate OFF clamp, output discharge |
| `ldo_softstart.sch` | 1 | 1 MΩ / 20 pF reference ramp and reset switch |
| `ldo_pgood.sch` | 12 | Final-reference comparator, hysteresis, VIN-domain buffer, OFF masking |

Total: 35 logical MOS, 10 ideal resistors, 3 ideal capacitors. Multiplicity,
matching, isolation, contacts and power routing are additional layout work.
There is no control decoder, SPI, sequencer, oscillator or Verilog in this slice.

| Pin | Meaning |
| --- | --- |
| `VIN`, `VSS` | Local 3.3 V supply and return; controls remain powered when VOUT is disabled |
| `VREF` | Nominal 1.2 V voltage input; assume valid before enabling; not 3.3/5 V tolerant |
| `IBIAS` | Externally **sourced** 1 µA into the bias-entry diode; not a voltage supply |
| `EN` | VIN-domain active-high regulator enable; low clamps the pass gate and discharges VOUT |
| `STBY` | VIN-domain high disables replica adaptation; EN remains high to regulate |
| `VOUT` | Nominal 1.8 V regulated output; full current stays on die, pad is sense/light-load only |
| `PGOOD` | VIN-domain status, not a package-pad driver; final-reference threshold, low in OFF |

EN=1/STBY=0 is RUN; EN=1/STBY=1 is STANDBY; EN=0 is OFF. STANDBY does not
limit the external load to 1 mA: the future load controller must enforce that.
OFF is not zero supply current; the bias-entry mirror remains active.
Missing reference/bias, supply removal and externally driven VOUT are not safe
operating modes established by these tests.

## Tests and interpretation

The full matrix uses typical/ff/ss/fs/sf MOS models, −40/27/125 °C and
3.0/3.3/3.6 V. These are characterization points, not an automotive qualification.
Reference and bias accuracy, resistor/capacitor corners and mismatch are excluded.
The model's actual statistical switches `sw_stat_global` and `sw_stat_mismatch`
are both zero.

- DC: 101 loads in RUN (0–100 mA) and 101 in STANDBY (0–1 mA) per PVT.
  Checks 1.746–1.854 V. Quiescent current is VIN current minus external load;
  a separately reported conservative sum also includes imported 1 µA bias and
  reference current. It excludes consumption inside the harness generators.
- AC: 1,080 voltage-return-ratio sweeps in full mode: 10 pF/100 pF/1 nF;
  RUN loads 0/10 µA/100 µA/1 mA/10 mA/100 mA and STANDBY 0/1 mA.
  A zero-DC, AC-1 V source sits between the divider and amplifier feedback input.
  It preserves the closed DC circuit. The return-ratio approximation assumes
  a high-impedance amplifier input; multiple high-frequency crossings and
  interaction with the adaptive loop require proper multiloop analysis.
  Check every downward unity crossing; missing crossings or invalid operating
  points are failures, never automatic passes.
- Dropout: 100 mA, VIN swept 3.3→1.7 V in 5 mV steps with EN tracking VIN.
  Checks regulation at VIN=2.1 V (300 mV nominal headroom), and reports the lowest
  sampled VIN in the DC accuracy band. This is not an exact dropout extraction
  under a different definition, nor does it include harness-switch voltage loss.
- AC/dropout use `.nodeset v(vout)=1.8` to guide Newton away from unphysical
  negative-output solutions caused by the ideal current sink. It is an initial
  guess, not a forced voltage. Startup tests have **no nodeset, forced IC or UIC**.
- Transients: typical 3.3 V / 27 °C / 100 pF, independently applied
  0→1→100→1→0 mA with 10 µs and 100 ns edges. The testbench sink tapers below
  100 mV output so it cannot pull constant current from an unpowered rail.
  Check settled regulation and report excursions; no transient excursion limit
  was agreed, so a settlement pass does not mean acceptable domain powering.
- Startup/OFF: no external load, 1.8 kΩ and 18 Ω; selected hot/slow/cold corners
  in full mode. Reference/bias and VIN are established before EN. Checks settled
  output, PGOOD low in OFF, and 90% discharge within 10 µs at 100 pF (an engineering
  check added here, not a negotiated spec). Shutdown minima are reported too.
- RUN→STANDBY→RUN at 1 mA; nominal comparator up/down ramp checks PGOOD at
  approximately 1.62/1.53 V equivalent output. Comparator checks are not a full
  PVT/mismatch or propagation-delay characterization.

## Known limitations before layout

The MOS DC results do not establish stability or transient suitability. The
current compensation still fails portions of the capacitance/PVT sweep. Fast
100 mA steps produce substantial droop/overshoot, and unloaded startup can
briefly drive VOUT negative. Do not call this
safe for a powered digital domain yet.

The current 200 pF + 200 pF + 20 pF capacitor targets total 420 pF. At the
installed GF180MCU-D Magic MIM density of 2 fF/µm², that is about 0.21 mm² of
bare plate area, roughly 40% of a 1274.27 × 412.71 µm slot, before boundaries,
contacts and routing. Resistors and capacitors must be replaced with PDK devices,
sized and re-simulated; the area estimate is not a floorplan or fit proof.

No current limit, UVLO, thermal protection, reference selector/buffer,
reverse-current blocking, ESD, package/harness impedance, EM/IR checks or extracted
layout are included. The harness `vbias`/`ibias` interfaces are not yet connected
to this prototype. The upstream reference discrepancy mentioned in the design
discussion remains unresolved. 100 mA on-die loading still needs organizer
approval for supply/return, harness switches, package and ~330 mW thermal load.
