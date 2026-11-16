#!/usr/bin/env python3
"""Cross-check selected LDO loop-gain cases using saved fresh-netlist run.py decks.

Checks unchanged DC, reversed Tian probe at 800 points/decade, and closed-loop
small load pulses of both signs. Halving amplitude and maximum timestep tests
linearity and numerical convergence. This is not a full-PVT transient signoff.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import re

import numpy as np

from check_loopgain import read, simulate
from loopgain import margins, tian
from run import replace_once

ROOT = Path(__file__).resolve().parents[1]


def check(row, source, out):
    name = row['name']
    net = (source / (name + '_voltage.spice')).read_text()
    net = re.sub(r'(?ims)^\.control\s*$.*?^\.endc\s*$', '', net)
    net = re.sub(r'(?im)^\.end\s*$', '', net)
    closed = replace_once(net, 'VTEST VFB_TEST VFB dc 0 ac 1\nITEST VSS VFB_TEST dc 0 ac 0\n', '')
    closed = replace_once(closed, 'VREF_SS VFB_TEST GATE ldo_error_amp',
                          'VREF_SS VFB GATE ldo_error_amp')
    opvars = 'v(vout) v(xdut.gate) v(xdut.pb) v(xdut.xea.ea)'
    simulate(out, name + '_closed', closed, f'op\nwrdata {out / (name + "_closed.dat")} {opvars}')
    op = read(out, name + '_closed')[0, 1:]
    np.testing.assert_allclose(op, read(source, name + '_voltage_op')[0, 1:], rtol=1e-6, atol=1e-8)
    responses = []
    for excitation in ['v', 'i']:
        reverse = replace_once(net, 'VTEST VFB_TEST VFB dc 0 ac 1\nITEST VSS VFB_TEST dc 0 ac 0',
                               f'VTEST VFB VFB_TEST dc 0 ac {int(excitation == "v")}\n'
                               f'ITEST VSS VFB dc 0 ac {int(excitation == "i")}')
        sample = name + '_reverse_' + excitation
        simulate(out, sample, reverse, f'op\nwrdata {out / (sample + "_op.dat")} {opvars}\n'
                 f'ac dec 800 1 1e9\nwrdata {out / (sample + ".dat")} '
                 'real(v(xdut.vfb)) imag(v(xdut.vfb)) real(i(v.xdut.vtest)) imag(i(v.xdut.vtest))')
        np.testing.assert_allclose(op, read(out, sample + '_op')[0, 1:], rtol=1e-6, atol=1e-8)
        d = read(out, sample)
        responses.append((d[:, 1] + 1j * d[:, 2], d[:, 3] + 1j * d[:, 4]))
    (vv, iv), (vi, ii) = responses
    loop = tian(vv, iv, vi, ii)
    original = read(source, name)
    reference = original[:, 1] + 1j * original[:, 2]
    np.testing.assert_allclose(d[::4, 0], original[:, 0], rtol=1e-10)
    np.testing.assert_allclose(loop[::4], reference, rtol=1e-6, atol=1e-8)
    refined = margins(d[:, 0], loop)
    np.testing.assert_allclose(refined['min_pm_deg'], row['min_pm_deg'], rtol=0, atol=.1)

    # Broad pulse around the dominant crossover. Begin at the solved operating
    # point, not a power-up transient, and leave every physical loop closed.
    fu = row['crossings_Hz_deg'][0][0]
    amplitude = max(row['load_A'], 5e-6) * .001
    delay, edge, width = 1 / fu, 1 / (50 * fu), 1 / (5 * fu)
    stop = max(30 / fu, 50e-6)
    # Resolve internal responses too, rather than choosing timestep only from
    # the outer crossover. Residual PB convergence errors remain reported.
    step = min(2e-9, 1 / (100 * fu))
    pulse_end = delay + 2 * edge + width
    waves, pulses = {}, []
    for scale, divisor in [(1, 1), (1, 2), (-1, 1), (-1, 2), (.5, 2)]:
        sample = f'{name}_pulse_{scale}_{divisor}'
        pulse = (f'\nIPERT VOUT 0 PWL(0 0 {delay} 0 {delay + edge} {scale * amplitude} '
                 f'{delay + edge + width} {scale * amplitude} {pulse_end} 0)\n'
                 # STANDBY PB excursions can be only a few nanovolts. Use
                 # tighter solver accuracy rather than relaxing agreement tests.
                 '.options reltol=1e-7 vntol=1e-11 abstol=1e-14 method=trap\n')
        dt = step / divisor
        simulate(out, sample, closed + pulse, f'op\nwrdata {out / (sample + "_op.dat")} {opvars}\n'
                 f'tran {dt} {stop} 0 {dt}\nwrdata {out / (sample + ".dat")} {opvars}')
        # The tighter transient tolerances can move the OP slightly. Reference
        # each waveform to its own converged DC, not the looser AC/DC solution.
        baseline = read(out, sample + '_op')[0, 1:]
        d = read(out, sample)
        delta = d[:, 1:] - baseline
        peak = np.max(abs(delta), axis=0)
        late = np.max(abs(delta[d[:, 0] > .75 * stop]), axis=0)
        ratio = late / np.maximum(peak, 1e-9)
        waves[(scale, divisor)] = (d[:, 0], delta)
        pulses.append(dict(name=sample, amplitude_A=scale * amplitude, max_step_s=dt,
                           peak_delta_V=peak.tolist(), late_to_peak=ratio.tolist(),
                           decayed=bool(np.all(late < np.maximum(.01 * peak, 1e-9)))))
    fine_time, fine = waves[(1, 2)]
    errors = {}
    for label, key, normalization in [('timestep', (1, 1), 1),
                                      ('opposite_sign', (-1, 2), -1),
                                      ('half_amplitude', (.5, 2), .5)]:
        time, delta = waves[key]
        aligned = np.column_stack([np.interp(fine_time, time, delta[:, i]) for i in range(4)]) / normalization
        error = np.max(abs(aligned - fine), axis=0) / np.maximum(np.max(abs(fine), axis=0), 1e-9)
        errors[label] = error.tolist()
    # Validation tolerance, not a product transient specification. Preserve
    # failed cases and every node's error in JSON instead of aborting the report.
    agreement_ok = all(error < .05 for values in errors.values() for error in values)
    result = dict(case=row, refined_pm_deg=refined['min_pm_deg'],
                  probe_reversal_error=float(np.max(abs(loop[::4] - reference) / np.maximum(1, abs(reference)))),
                  node_order=['VOUT', 'GATE', 'PB', 'EA'], pulse_end_s=pulse_end,
                  stop_s=stop, waveform_errors=errors, agreement_ok=agreement_ok, pulses=pulses)
    (out / (name + '_check.json')).write_text(json.dumps(result, indent=2) + '\n')
    print(name, 'PM:', refined['min_pm_deg'], 'all perturbations decayed:', all(p['decayed'] for p in pulses),
          'waveform agreement:', agreement_ok, flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('results', type=Path, help='Full results directory generated by run.py')
    parser.add_argument('--out', type=Path, default=ROOT / '.amp/in/stability-check')
    parser.add_argument('--jobs', type=int, default=3)
    args = parser.parse_args()
    source, out = args.results.resolve(), args.out.resolve()
    rows = json.loads((source / 'results.json').read_text())['ac']
    # Nominal endpoints plus actual worst valid RUN and STANDBY margins, and
    # the worst zero-load RUN point. Deduplicate if a case serves two purposes.
    selected = [r for r in rows if r['corner'] == 'typical' and r['temp_C'] == 27
                and r['vin_V'] == 3.3 and r['cap_F'] == 1e-10 and not r['standby']
                and r['load_A'] in [0, .1]]
    for mode, zero_load in [(False, False), (True, False), (False, True)]:
        candidates = [r for r in rows if r['valid'] and r['standby'] == mode
                      and (not zero_load or r['load_A'] == 0)]
        if candidates:
            selected.append(min(candidates, key=lambda r: r['min_pm_deg']))
    selected = list({r['name']: r for r in selected}.values())
    if not selected:
        raise ValueError('No usable cases; inspect the original AC failures')
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(lambda row: check(row, source, out), selected))
    (out / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    if not all(r['agreement_ok'] and all(p['decayed'] for p in r['pulses']) for r in results):
        raise SystemExit('FAIL: selected-case pulse decay or waveform agreement; inspect results.json and traces')
    print('PASS: selected-case DC, probe reversal, frequency refinement, pulse decay/linearity/timestep checks')


if __name__ == '__main__':
    main()
