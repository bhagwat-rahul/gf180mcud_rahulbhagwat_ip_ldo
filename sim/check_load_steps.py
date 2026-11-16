#!/usr/bin/env python3
"""Test independent 0<->100 mA / 100 ns steps from settled RUN operating points.

Netlists the actual Xschem hierarchy. No load-command feedforward, forced initial
conditions or startup exemption: each step starts with a DC-regulated output.
The 1.62--1.98 V / 20 us limits are provisional engineering acceptance targets.
Use --step-ns 1 to check numerical refinement against the default 2 ns maximum.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
from itertools import product
import json
from pathlib import Path
import re

import numpy as np

from check_loopgain import read, simulate
from run import HIGH, LOW, ROOT, SCHEMATICS, netlist, replace_once

EDGE = 100e-9
START = 5e-6
STOP = 100e-6
RECOVERY = 20e-6
TRANSIENT_LOW, TRANSIENT_HIGH = 1.62, 1.98


def check(base, out, corner, temp, vin, cap_pf, direction, step_ns):
    name = f'step_{corner}_{temp}_{vin}_{cap_pf}_{direction}'
    initial, final = (0, .1) if direction == 'up' else (.1, 0)
    net = replace_once(base, 'sm141064.spice typical', f'sm141064.spice {corner}')
    net = replace_once(net, 'VSUP VIN 0 3.3', f'VSUP VIN 0 {vin}')
    net = replace_once(net, 'VEN EN 0 3.3', f'VEN EN 0 {vin}')
    net = replace_once(net, 'CLOAD VOUT 0 100p', f'CLOAD VOUT 0 {cap_pf * 1e-12}')
    net = replace_once(net, 'ILOAD VOUT 0 1m',
                       f'VCMD LOAD_CMD 0 PWL(0 {initial} {START} {initial} '
                       f'{START + EDGE} {final} {STOP} {final})\n'
                       'VLOAD_SENSE VOUT LOAD_TOP 0\n'
                       'BLOAD LOAD_TOP 0 I=v(LOAD_CMD)*min(max(v(VOUT)/0.1,0),1)')
    # Insert ammeters at named drains, without assuming how the gate driver
    # is controlled. This preserves both the original and balanced topology.
    for device, drain, monitor, source in [
            ('XMPASS', 'VOUT', 'PASS_MON', 'VPASS PASS_MON VOUT 0'),
            ('XMPDRV', 'GATE', 'UP_MON', 'VUP UP_MON GATE 0'),
            ('XMNDRV', 'GATE', 'DOWN_MON', 'VDOWN GATE DOWN_MON 0')]:
        pattern = rf'(?m)^({device}) {drain} '
        net, count = re.subn(pattern, source + rf'\n\1 {monitor} ', net)
        if count != 1:
            raise ValueError(f'Expected exactly one {device} drain at {drain}')
    net += (f'\n.temp {temp}\n.nodeset v(vout)=1.8\n'
            '.options reltol=1e-5 vntol=1e-8 abstol=1e-12 method=trap\n')
    dt = step_ns * 1e-9
    variables = ('v(vout) v(xdut.gate) v(xdut.xea.ea) v(xdut.pb) '
                 'i(vload_sense) i(v.xdut.xpwr.vpass) '
                 'i(v.xdut.xea.vup) i(v.xdut.xea.vdown) i(vsup) v(pgood) v(xdut.vfb)')
    simulate(out, name, net, f'op\nwrdata {out / (name + "_op.dat")} {variables}\n'
             f'tran {dt} {STOP} 0 {dt}\nwrdata {out / (name + ".dat")} {variables}')
    op = read(out, name + '_op')[0]
    d = read(out, name)
    if (not np.isclose(d[0, 0], 0, atol=1e-15) or d[-1, 0] < STOP * .999
            or not np.all(np.diff(d[:, 0]) > 0)):
        raise RuntimeError(f'Truncated/nonmonotonic transient: {name}')
    active = d[d[:, 0] >= START]
    after = d[d[:, 0] >= START + EDGE]
    outside = np.flatnonzero((after[:, 1] < LOW) | (after[:, 1] > HIGH))
    recovery = 0.0
    if len(outside):
        next_sample = outside[-1] + 1
        recovery = (float(after[next_sample, 0] - START - EDGE)
                    if next_sample < len(after) else None)
    # Check the measured ramp, not just its endpoints: a slow/wrong/tapered
    # current sink must not count as a successful 100 mA / 100 ns stimulus.
    before = d[d[:, 0] < START]
    expected_current = initial + (final - initial) * np.clip((d[:, 0] - START) / EDGE, 0, 1)
    stimulus_ok = bool(np.isclose(op[5], initial, atol=1e-9, rtol=1e-5)
                       and np.allclose(d[:, 5], expected_current, atol=1e-9, rtol=1e-5))
    result = dict(name=name, corner=corner, temp_C=temp, vin_V=vin, cap_pF=cap_pf,
                  direction=direction, edge_ns=EDGE * 1e9, max_step_ns=step_ns,
                  initial_V=float(op[1]), min_V=float(active[:, 1].min()),
                  max_V=float(active[:, 1].max()), final_V=float(d[-1, 1]),
                  recovery_us=None if recovery is None else recovery * 1e6,
                  peak_gate_source_A=float(active[:, 7].max()),
                  peak_gate_sink_A=float(active[:, 8].max()),
                  peak_supply_A=float((-active[:, 9]).max()),
                  stimulus_ok=stimulus_ok,
                  initial_ok=bool(LOW <= op[1] <= HIGH and
                                  np.all((before[:, 1] >= LOW) & (before[:, 1] <= HIGH))),
                  excursion_ok=bool(np.all((active[:, 1] >= TRANSIENT_LOW) &
                                            (active[:, 1] <= TRANSIENT_HIGH))),
                  recovery_ok=bool(recovery is not None and recovery <= RECOVERY))
    result['ok'] = all(result[k] for k in ['stimulus_ok', 'initial_ok', 'excursion_ok', 'recovery_ok'])
    print(json.dumps(result), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT / '.amp/in/load-steps')
    parser.add_argument('--jobs', type=int, default=4)
    parser.add_argument('--schematics', type=Path, default=SCHEMATICS)
    parser.add_argument('--corners', nargs='+', choices=['typical', 'ff', 'ss', 'fs', 'sf'], default=['typical'])
    parser.add_argument('--temps', nargs='+', type=float, default=[27])
    parser.add_argument('--volts', nargs='+', type=float, default=[3.3])
    parser.add_argument('--caps-pf', nargs='+', type=float, default=[100])
    parser.add_argument('--step-ns', type=float, default=2)
    args = parser.parse_args()
    if args.step_ns <= 0 or args.step_ns > 10 or min(args.caps_pf) <= 0:
        parser.error('Require 0 < maximum timestep <= 10 ns and positive capacitances')
    out = args.out.resolve()
    base = netlist(out, args.schematics)
    cases = list(product(args.corners, args.temps, args.volts, args.caps_pf, ['up', 'down']))
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(lambda case: check(base, out, *case, args.step_ns), cases))
    (out / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    raise SystemExit(0 if all(r['ok'] for r in results) else 1)


if __name__ == '__main__':
    main()
