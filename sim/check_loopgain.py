#!/usr/bin/env python3
"""Validate the loop-gain calculation against analytically solvable SPICE circuits.

Requires ngspice and numpy. The loaded three-pole feedback fixture deliberately
violates the voltage-only probe's impedance assumption. Both probe orientations
must reproduce its known return ratio and nonzero DC point. Stable, unstable,
and wrong-feedback-sign controls prevent a plausible-looking plot from passing.
"""

import argparse
import json
from pathlib import Path
import re
import subprocess

import numpy as np

from loopgain import margins, tian

ROOT = Path(__file__).resolve().parents[1]


def simulate(out, name, net, commands):
    out.mkdir(parents=True, exist_ok=True)
    net = re.sub(r'(?ims)^\.control\s*$.*?^\.endc\s*$', '', net)
    net = re.sub(r'(?im)^\.end\s*$', '', net)
    deck = out / f'{name}.spice'
    # Parallelism is across cases, not across the few MOS in each circuit.
    deck.write_text(net + '\n.control\nset num_threads=1\nset wr_singlescale\nset wr_vecnames\n'
                    'set numdgt=17\n' + commands + '\n.endc\n.end\n')
    with (out / f'{name}.log').open('w') as log:
        subprocess.run(['ngspice', '-b', str(deck)], stdout=log, stderr=log, check=True)
    log = (out / f'{name}.log').read_text()
    if re.search(r'(?im)^\s*(error\b|fatal\b)|timestep too small|analysis aborted', log):
        raise RuntimeError(f'Simulation error; inspect {name}.log')


def read(out, name):
    d = np.loadtxt(out / f'{name}.dat', skiprows=1, ndmin=2)
    if not np.isfinite(d).all():
        raise ValueError(f'Non-finite output: {name}')
    return d


def fixture(out, label, gain, f1, f2):
    # A(s) = gain/((1+s/w1)(1+s/w2)); Rout=1k, Rin=10k, Cin=1nF.
    # Loaded loop = A(s)/(1.1+s*1us). Its CLOSED-loop characteristic is
    # (1.1+s*1us)(1+s/w1)(1+s/w2) + gain = 0, independently of any probe.
    w1, w2 = 2 * np.pi * f1, 2 * np.pi * f2
    net = f'''Analytical loaded feedback fixture: {label}
VREF ref 0 1
E1 drive1 0 sense ref {-gain}
R1 drive1 n1 1k
C1 n1 0 {1 / (1000 * w1):.17g}
E2 drive2 0 n1 0 1
R2 drive2 n2 1k
C2 n2 0 {1 / (1000 * w2):.17g}
EDRV drive 0 n2 0 1
ROUT drive ret 1k
RIN sense 0 10k
CIN sense 0 1n
'''
    opvars = 'v(ret) v(n1) v(n2)'
    baseline = net.replace('sense', 'ret')
    simulate(out, label + '_closed', baseline,
             f'op\nwrdata {out / (label + "_closed.dat")} {opvars}')
    op = read(out, label + '_closed')[0, 1:]
    np.testing.assert_allclose(op[0], gain / (gain + 1.1), rtol=1e-9)
    curves = []
    for reverse in [False, True]:
        positive, negative = ('ret', 'sense') if reverse else ('sense', 'ret')
        responses = []
        for excitation in ['v', 'i']:
            name = f'{label}_{int(reverse)}_{excitation}'
            injected = net + f'VTEST {positive} {negative} dc 0 ac {int(excitation == "v")}\n'
            injected += f'ITEST 0 {positive} dc 0 ac {int(excitation == "i")}\n'
            simulate(out, name, injected,
                     f'op\nwrdata {out / (name + "_op.dat")} {opvars}\n'
                     f'ac dec 200 1 1e9\nwrdata {out / (name + ".dat")} '
                     f'real(v({positive})) imag(v({positive})) '
                     'real(i(vtest)) imag(i(vtest))')
            np.testing.assert_allclose(read(out, name + '_op')[0, 1:], op, rtol=1e-9, atol=1e-12)
            d = read(out, name)
            responses.append((d[:, 1] + 1j * d[:, 2], d[:, 3] + 1j * d[:, 4]))
        (vv, iv), (vi, ii) = responses
        measured = tian(vv, iv, vi, ii)
        curves.append(measured)
        s = 2j * np.pi * d[:, 0]
        expected = gain / ((1 + s / w1) * (1 + s / w2) * (1.1 + s * 1e-6))
        np.testing.assert_allclose(measured, expected, rtol=1e-7, atol=1e-10)
    np.testing.assert_allclose(curves[0], curves[1], rtol=1e-7, atol=1e-10)
    coefficients = np.polymul(np.polymul([1 / w1, 1], [1 / w2, 1]), [1e-6, 1.1])
    coefficients[-1] += gain
    poles = np.roots(coefficients)
    rhp = int(sum(poles.real > 0))
    result = margins(d[:, 0], curves[0])
    if gain > 0:
        # Solve the analytical unity equation independently of the interpolation
        # implementation, and compute its phase from the three known pole angles.
        low, high = 1., 1e9
        for _ in range(80):
            f = np.sqrt(low * high)
            w = 2 * np.pi * f
            magnitude = gain / np.sqrt((1 + (w / w1)**2) * (1 + (w / w2)**2)
                                       * (1.1**2 + (w * 1e-6)**2))
            if magnitude > 1:
                low = f
            else:
                high = f
        pm = 180 - np.degrees(np.arctan(w / w1) + np.arctan(w / w2) + np.arctan(w * 1e-6 / 1.1))
        np.testing.assert_allclose(result['crossings_Hz_deg'][0], [f, pm], rtol=2e-4, atol=.002)
        assert (result['min_pm_deg'] > 0) == (rhp == 0), (result, poles)
    assert result['pm_ok'] == (label == 'stable'), result
    assert rhp == {'stable': 0, 'unstable': 2, 'positive_feedback': 1}[label], poles
    result.update(label=label, closed_loop_RHP_poles=rhp,
                  analytical_poles_rad_s=[[float(p.real), float(p.imag)] for p in poles],
                  max_normalized_error=float(np.max(abs(curves[0] - expected) / np.maximum(1, abs(expected)))))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT / '.amp/in/loopgain-check')
    args = parser.parse_args()
    out = args.out.resolve()
    results = [fixture(out, 'stable', 1000, 10, 1e6),
               fixture(out, 'unstable', 1000, 1e3, 1e5),
               fixture(out, 'positive_feedback', -1000, 10, 1e6)]
    # No crossover, truncated sweep and multiple crossings must not become passes.
    for f, loop in [(np.array([1., 10.]), np.array([1000., 100.])),
                    (np.array([1., 10.]), np.array([.1, .01])),
                    (np.array([1., 10., 100., 1000.]), np.array([1000., .1, 10., .01]))]:
        assert not margins(f, loop)['pm_ok']
    (out / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))
    print('PASS: analytical AC, nonzero DC preservation, reversal, stable/unstable/sign controls')


if __name__ == '__main__':
    main()
