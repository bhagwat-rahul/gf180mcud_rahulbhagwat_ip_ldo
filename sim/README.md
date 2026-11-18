# Regulator-only schematic characterization

This is a working transistor-level prototype, not a layout-ready design or a
claim that every README target is met. The programmable on-die load is deferred;
independently commanded testbench loads exercise the regulator without telling
its adaptive-bias circuit when a load change will happen.

## Run in IIC-OSIC

From this repository's root inside the running container:

```sh
iic-pdk gf180mcuD
python3 sim/check_loopgain.py --out .amp/in/loopgain-check
python3 sim/run.py --out .amp/in/sim
python3 sim/run.py --full --jobs 6 --out .amp/in/full-sim
python3 sim/check_stability.py .amp/in/full-sim --out .amp/in/stability-check
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

Each result directory contains `ldo_tb.spice`, decks/logs/data for each case
(two excitations per AC case), source hashes, `results.json`, and DC/AC/dropout
CSVs. A nonzero exit status means
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
| `ldo_startup.sch` | 3 | CC/CGF soft-connect switches, 2 kΩ switched bleed, ENB-RC sequencing |
| `load/ldo_load.sch` | 6 | On-die 0–100 mA NMOS mirror load, 210:1 output, 100 pF mirror-gate cap |

Total: 44 logical MOS; the load's output mirror alone is 210 unit fingers
(222 unit devices in the load). The on-die resistors are GF180MCU-D poly devices and the
on-die capacitors are MIM devices; only the external 1.2 V reference and the
sourced 1 µA bias remain ideal. Multiplicity, matching, isolation, contacts and
power routing are additional layout work.
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
| `LDENB` | VIN-domain active-high disable for the on-die load; 0 = load enabled, VIN = disabled |

EN=1/STBY=0 is RUN; EN=1/STBY=1 is STANDBY; EN=0 is OFF. STANDBY does not
limit the external load to 1 mA: the future load controller must enforce that.
OFF is not zero supply current; the bias-entry mirror remains active.
Missing reference/bias, supply removal and externally driven VOUT are not safe
operating modes established by these tests.

The on-die load's `VLOAD` reference is tied to `VREF` inside `ldo_top`, so the
external 1.2 V reference must also supply the load's ~0.46 mA reference current.
The load is intended to be enabled after PGOOD (or after the LDO is in
regulation), not during startup. With `LDENB=0` from t=0 the LDO still starts,
but the output overshoots to ~1.88 V; with the load enabled after PGOOD the
0↔97 mA step stays within the provisional 1.62–1.98 V gate (1.713–1.858 V
typical, 100 pF output).

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
- AC: 1,080 two-excitation Tian return-ratio measurements in full mode:
  10 pF/100 pF/1 nF;
  RUN loads 0/10 µA/100 µA/1 mA/10 mA/100 mA and STANDBY 0/1 mA.
  Zero-DC voltage and current sources preserve the closed DC circuit. The
  two AC excitations account for bidirectional loading; the old voltage-only
  approximation is retained for comparison, not used to pass a case. Sweep
  1 Hz–1 GHz at 200 points/decade. `dc_loop_gain_dB` retains its old field name
  but measures the 1 Hz endpoint, not literal zero-frequency gain.
  Report every upward/downward unity crossing, continuous phase and gain
  margins. The automatic >=60° gate conservatively requires one downward
  crossing, a valid regulated OP, positive low-frequency feedback, >40 dB at
  1 Hz and gain below unity at the upper endpoint. Multiple crossings require
  review, never an automatic pass. Local compensation and adaptive-bias loops
  remain closed: this is an outer-loop measurement, not full multiloop signoff.
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

## Loop-gain validation

`loopgain.py` implements the [Tian/Wiedmann two-source method](https://gotroot.ca/spectrum/www.spectrum-soft.com/news/spring2011/loopgain.html).
`VTEST` points from amplifier input to divider; `ITEST` injects from VSS into
the amplifier-input side. Run (AC voltage, AC current) = (1 V, 0 A), then
(0 V, 1 A). These are linearized AC excitations, not large-signal supply demands.
With positive-terminal voltage/source current `(vv, iv)` from the voltage run
and `(vi, ii)` from the current run, calculate `m = 2*(iv*vi - vv*ii) + vv + ii`
and `T = m/(1-m)`. The feedback convention is `1 + T = 0`.

`check_loopgain.py` runs real ngspice fixtures whose loop transfer and
closed-loop characteristic polynomial are analytically known. It checks both
probe orientations, nonzero DC preservation, a stable loop, an unstable loop,
and reversed feedback polarity. Missing/truncated/multiple unity crossings
cannot produce an automatic pass. No PDK is needed for these reference fixtures.

`check_stability.py` reads the saved decks from a full `run.py` result. It checks
nominal 0/100 mA plus the worst RUN, STANDBY and unloaded RUN cases (deduplicated).
For each, it removes the probe and checks DC, reverses the probe and quadruples
frequency resolution, then applies small load pulses with **all physical loops
closed**. It monitors VOUT, GATE, PB and EA, uses both pulse signs, halves the
amplitude, and halves maximum timestep with trapezoidal integration. The 5%
waveform-agreement and 1%-of-peak late-tail limits are numerical validation
checks, not newly negotiated large-signal product specifications. A bounded
perturbation run only covers its nodes, excitation and finite observation time.

On the unchanged schematic, the corrected full matrix has **122/1,080 cases
below 60°**, versus 154 flagged by the old approximation: 3 at 10 pF, 6 at
100 pF and 113 at 1 nF. All 1,080 OP/sweep checks are valid and have one unity
crossing. The changed count is a measurement correction, not a circuit fix;
13 old passes become failures and 45 old failures become passes.
The worst case is ff / −40 °C / 3.6 V / RUN / 100 mA / 1 nF:
12.80° at 12.32 MHz, with approximately 1.01 dB gain margin. Nominal
3.3 V / 27 °C / 100 pF gives 68.93° at no load, 117.22° at 1 mA and
76.77° at 100 mA. The full characterization therefore still exits nonzero.

The five selected LDO cases preserve DC and agree under probe reversal and
200→800 points/decade refinement (largest margin change <0.0007°). All 25
small-pulse runs decay within their observation windows. Four cases pass all
waveform comparisons; **the worst STANDBY case still fails** the PB-node
agreement check: its ~2 nV response differs by 17% under timestep refinement
and 21% under amplitude halving, despite VOUT/GATE/EA agreeing within 0.2%.
Reducing the maximum timestep from 20 ns to 2 ns did not resolve it. The check
retains this failure and returns nonzero; do not call the complete validation
suite green. Overly tight solver tolerances also caused aborted runs and were
not accepted as evidence. The final settings are reltol=1e-7, vntol=1e-11 V,
abstol=1e-14 A, trapezoidal integration, and one ngspice thread per case.

## Exact 100 ns full-load steps and rejected driver experiment — November 13

`check_load_steps.py` independently tests 0→100 mA and 100→0 mA, each starting
from a settled RUN operating point, not from startup or the old 1 mA intermediate
load. The linear ramp's total duration is 100 ns (not its 10–90% duration).
The transition starts at 5 µs, and the trace ends at 100 µs. A VOUT nodeset guides
DC only; there is no forced initial condition or load-command feedforward.
The sink has the same near-zero-voltage taper as the existing transient bench.

The checker verifies the initial operating point and pre-step regulation, the
actual 100 ns load-current waveform, every sampled output excursion, and return to **and remaining
in** the ±3% band. It rejects truncated/non-finite traces. The provisional
engineering gates are 1.62–1.98 V throughout the disturbance and ≤20 µs recovery
after the ramp ends; these are not claimed achieved or final application limits.
It captures VOUT, GATE, EA, PB, VFB, PGOOD, pass/driver currents and supply current.
Zero-volt ammeters preserve loading. This is a regulator-only behavioral-load
test, not validation of a built internal load generator or package.

```sh
iic-pdk gf180mcuD
python3 sim/check_load_steps.py --out .amp/in/load-steps
python3 sim/check_load_steps.py --step-ns 1 --out .amp/in/load-steps-fine
# Expand only as needed; the rejected candidate already fails nominal tests.
python3 sim/check_load_steps.py --corners typical ff ss fs sf --temps -40 27 125 --volts 3.0 3.3 3.6 --caps-pf 10 100 300 --out .amp/in/load-steps-pvt
```

Both runners accept `--schematics DIRECTORY` to freshly netlist a saved Xschem
variant without replacing the main hierarchy. Source hashes accompany each run.
A complete, **rejected** candidate is saved locally under
`.amp/in/driver-candidate/schematics/`: MNDRV W2→4 µm at L4 µm, a three-MOS
RUN-only additional 1:1 bias-copy branch, and RZ 330→120 kΩ. Capacitor values and
pass-device dimensions are unchanged. The main schematics were restored to the
before-run hashes; no driver/bias modification is accepted by this experiment.

At typical / 27 °C / 3.3 V / 100 pF with a 1 ns maximum timestep:

| Measurement | Baseline | Rejected stronger-driver candidate |
| --- | ---: | ---: |
| 0→100 mA minimum VOUT | 0.34572 V | 0.34125 V |
| Rise-step recovery after ramp | 5.821 µs | 11.725 µs |
| 100→0 mA maximum VOUT | 3.00535 V | 3.29890 V |
| Release-step recovery | Not within 94.9 µs observation after ramp | Not within 94.9 µs observation after ramp |
| Worst sampled nominal RUN IQ, imported bias/reference included | 47.06 µA | 81.12 µA |
| Worst sampled nominal STANDBY IQ, same accounting | 17.105 µA | 17.107 µA |
| Minimum of eight nominal outer-loop PM checks | 67.09° | 61.13° |

Both exact-step tests fail, despite valid initial regulation and full applied
current. The larger excursions than the earlier 1.113–2.530 V result are caused
by testing **zero** load directly rather than 1↔100 mA; the earlier numbers are
not measurements of these new scenarios. A control changing only the minimum
load to 1 mA in the new bench gives 1.11010 V on the rising step and 2.54449 V
on release, confirming the importance of the minimum load. In the rising step, both versions cross
below 1.62 V about 6.5 ns after the ramp starts: load is 6.5 mA while pass-terminal
current is only about 0.445 mA. Raising driver capacity did not make the complete
feedback path respond sufficiently early. This is not proof that every possible
single-loop design fails.

The candidate's nominal DC, dropout, static-PGOOD and eight outer-loop checks
pass. Its existing mode-transition check fails: VOUT reaches 1.87088 V, above that
check's 1.854 V ceiling. Startup negative excursion also worsens to −0.200 V.
A first 20x-bias / 10x-width trial oscillated with the old compensation; it was
rejected. Further netlist-only sizing/compensation and complementary-driver trials
are exploratory, not validated replacements for the main hierarchy.

Halving maximum timestep from 2 ns to 1 ns changes extrema by at most about
1.1 mV across the baseline/candidate exact-step comparisons, without changing
any verdict. Snapshot re-netlisting reproduces the candidate results. Independent
checker controls accept an ideal regulated rail and reject a brief overvoltage,
late recovery and a deliberately slow load ramp separately. The analytical
loop-gain fixtures still pass.
The restored baseline passes the **nominal existing** control suite, not the
new exact-step gates or the previously failing full PVT stability matrix.

Local evidence: `.amp/in/driver-baseline-final/`,
`.amp/in/driver-candidate-final/`, `.amp/in/driver-after-controls/`,
`.amp/in/driver-restored-controls/` and `.amp/in/load-checker-controls/`.
The rejected candidate was not advanced to full-PVT, mismatch or layout tests.

## Final PDK-passive design — November 18

The final design uses GF180MCU-D poly resistors and MIM capacitors throughout.
The startup block is `schematics/ldo_startup.sch`; the latest full matrix is
`.amp/in/single-loop/pdk-fix3/`, generated from the current sheets.

| Item | Value |
| --- | --- |
| `MPASS` | 50 µm × 0.28 µm, m=400 (20 mm total) |
| Feedback `RTOP`/`RBOT` | 80 kΩ / 160 kΩ |
| `RZERO` / `RZB` | 400 Ω / 18 kΩ |
| `CC` / `CGF` | 400 pF / 19.5 pF |
| Preload `MPPRE` | 50 µm × 0.5 µm, m=30, 120 Ω |
| OFF clamp | `RDIS` 500 Ω, `MNDIS` 20 µm, `MPOFF` 40 µm |
| Startup | CC/CGF PMOS soft-connect, 2 kΩ bleed, ENB RC ramps |

`CC` and `CGF` are disconnected while the pass gate falls, then reconnect on
separate `ENB` ramps: `CGF` first (30 pF, stabilizes the loop) and `CC` later
(100 pF). A 2 kΩ switched bleed holds `VOUT` at zero; a 250 kΩ/1 MΩ divider
from the `CC` ramp turns the bleed off only after compensation is restored.

### Results from the editable sheets

```sh
python3 sim/run.py --full --jobs 4 --out .amp/in/single-loop/pdk-fix3
```

- **AC, 1080 cases**: every case has one unity crossing and is valid. Worst
  phase margin **62.08°** (`ss`, −40 °C, 3.6 V, 1 nF, STANDBY 0 A); worst RUN
  **79.03°** (`ss`, −40 °C, 3.6 V, 1 nF, RUN 0 A).
- **DC, 90 cases**: RUN 1.80030–1.80090 V, STANDBY 1.80348–1.82260 V, inside
  ±3% (1.746–1.854 V). Worst STANDBY `IQ` **19.625 µA** including imported
  bias/reference current.
- **Startup, 7 cases**: minimum **−1.457 mV**, maximum **1.800782 V**. Every
  case passes the −50 mV minimum and 1.854 V maximum gate, including
  `ss`/−40 °C/3.6 V/10 pF.
- **Dropout, 15 cases**: VOUT at VIN=2.1 V is 1.80012–1.80033 V; all pass the
  300 mV headroom check.
- **Transient, 10 cases**: all settle inside ±3%; the 100 ns load-step peak is
  1.877 V. No transient excursion limit has been agreed.
- **PGOOD**: rising 1.6249 V, falling 1.5342 V.
- **RUN↔STANDBY↔RUN**: output stays within 1.7720–1.8327 V and settles.

The separate exact 0↔100 mA / 100 ns 270-case matrix has not been re-run on the
PDK-passive design; the 10-case in-run transient set passes. The 1.2 V reference
and sourced 1 µA bias remain ideal. This is schematic evidence only: no layout,
mismatch, EM/IR or package model is included.

### Reproduction

```sh
iic-pdk gf180mcuD
python3 sim/run.py --full --jobs 4 --out .amp/in/single-loop/pdk-fix3
# pending: re-run the 270-case exact-step matrix on the current sheets
python3 sim/check_load_steps.py --schematics schematics \
  --corners typical ff ss fs sf --temps -40 27 125 --volts 3.0 3.3 3.6 \
  --caps-pf 10 100 1000 --out .amp/in/single-loop/steps-final --jobs 8
python3 sim/check_stability.py .amp/in/single-loop/candidate3-full \
  --out .amp/in/single-loop/stability3 --jobs 4
```

### Limits of this evidence

- Resistors, capacitors, the 1.2 V reference and the 1 µA bias are ideal; the
  pass device is a schematic composite, not a layout.
- The nine `ff`/125 °C zero-load STANDBY rows are rejected by the gain-validity
  heuristic (see above); they are reported, not hidden, and `run.py` exits
  nonzero on them.
- The supplementary pulse check aborts in `trap` integration on the nominal
  zero-load RUN case: the transient stalls at t = 4.59 µs with every node flat
  to 1e-10 V (LTE limit with a pA-scale `vstby#branch`). Gear integration
  completes 50 µs and agrees with the trap solution to 1.6e-8 V over the common
  window, but the 5 nA pulse response is only 166 nV peak, near the solver
  noise floor, so the late-tail and linearity ratios are not meaningful at that
  amplitude. This is a harness-resolution issue, not an observed oscillation.

## Known limitations before layout

The redesign section above supersedes the earlier stability and transient
limitations: the MOS PVT matrix, the 10/100/1000 pF capacitance envelope and the
exact 100 ns steps pass the provisional gates on the editable sheets. What
remains is still substantial: ideal R/C/reference/bias, the nine `ff`/125 °C
zero-load validity flags, no mismatch, no layout parasitics, and the
supplementary pulse check's numerical limit documented above. Do not call this
safe for a powered digital domain yet.

The redesign's capacitor targets total 841 pF (CC 800 pF, CGF 20 pF, CM 10 pF,
CPRE_D 6 pF, CMODE_D 5 pF). At the installed GF180MCU-D Magic MIM density of
2 fF/µm² that is about 0.42 mm² of bare plate area, roughly 80% of a
1274.27 × 412.71 µm slot, before boundaries, contacts and routing. The 800 pF
`CC` is the dominant item; it must be reduced or the slot/area renegotiated.
The sequencing resistors `RPRE_D`/`RMODE_D` (1 MΩ each) and `RZB` (9.6 kΩ) are
also large in poly and need PDK device selection and sizing. The area estimate
is not a floorplan or fit proof.

No current limit, UVLO, thermal protection, reference selector/buffer,
reverse-current blocking, ESD, package/harness impedance, EM/IR checks or extracted
layout are included. The harness `vbias`/`ibias` interfaces are not yet connected
to this prototype. The upstream reference discrepancy mentioned in the design
discussion remains unresolved. 100 mA on-die loading still needs organizer
approval for supply/return, harness switches, package and ~330 mW thermal load.
