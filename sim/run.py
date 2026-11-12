#!/usr/bin/env python3
"""Netlist the editable Xschem design and characterize it with real GF180 models.

Run inside IIC-OSIC after `iic-pdk gf180mcuD`. --full expands the DC/AC/PVT
matrix, not the transient matrix. All simulation inputs, logs, and data are kept.
No implementation netlist is maintained separately from the schematics.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
import hashlib
from itertools import product
import json
import os
from pathlib import Path
import re
import subprocess

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SCHEMATICS = ROOT / 'schematics'
LOW, HIGH = 1.8 * 0.97, 1.8 * 1.03


def replace_once(text, old, new):
    if text.count(old) != 1:
        raise ValueError(f'Expected one occurrence of {old!r}; recheck schematic interface')
    return text.replace(old, new)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full', action='store_true')
    parser.add_argument('--jobs', type=int, default=4)
    parser.add_argument('--out', type=Path, default=ROOT / '.amp/in/sim')
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    models = Path(os.environ['PDK_ROOT']) / 'gf180mcuD/libs.tech/ngspice'
    if not (models / 'sm141064.spice').exists():
        raise FileNotFoundError(f'GF180MCU-D not installed under {models}')
    with (out / 'netlist.log').open('w') as log:
        subprocess.run(['xschem', '-n', '-q', '-x', '-b', '--rcfile', './xschemrc',
                        '-o', str(out), '-N', 'ldo_tb.spice', 'ldo_tb.sch'],
                       cwd=SCHEMATICS, stdout=log, stderr=log, check=True)
    base = (out / 'ldo_tb.spice').read_text()
    base = re.sub(r'(?ims)^\.control\s*$.*?^\.endc\s*$', '', base)
    base = re.sub(r'(?im)^\.end\s*$', '', base)
    base = base.replace('/foss/pdks/gf180mcuD/libs.tech/ngspice', str(models))
    manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(SCHEMATICS.iterdir()) if p.is_file()}
    manifest['model_sha256'] = hashlib.sha256((models / 'sm141064.spice').read_bytes()).hexdigest()
    (out / 'sources.json').write_text(json.dumps(manifest, indent=2) + '\n')

    def run(name, net, commands):
        path = out / f'{name}.spice'
        path.write_text(net + '\n.control\nset wr_singlescale\nset wr_vecnames\n'
                        'set numdgt=12\n' + commands + '\n.endc\n.end\n')
        with (out / f'{name}.log').open('w') as log:
            subprocess.run(['ngspice', '-b', str(path)], cwd=SCHEMATICS,
                           stdout=log, stderr=log, check=True)
        log = (out / f'{name}.log').read_text()
        # ngspice can exit successfully after errors in a .control command.
        if re.search(r'(?im)^\s*(error\b|fatal\b)|timestep too small|analysis aborted', log):
            raise RuntimeError(f'Simulation error; inspect {name}.log')

    def data(name):
        values = np.loadtxt(out / f'{name}.dat', skiprows=1, ndmin=2)
        if not np.isfinite(values).all():
            raise RuntimeError(f'Non-finite results in {name}')
        return values

    def circuit(corner='typical', temp=27, vin=3.3, current=.001, cap=100e-12, standby=False):
        net = replace_once(base, 'sm141064.spice typical', f'sm141064.spice {corner}')
        net = replace_once(net, 'VSUP VIN 0 3.3', f'VSUP VIN 0 {vin}')
        net = replace_once(net, 'VEN EN 0 3.3', f'VEN EN 0 {vin}')
        net = replace_once(net, 'VSTBY STBY 0 0', f'VSTBY STBY 0 {vin if standby else 0}')
        net = replace_once(net, 'ILOAD VOUT 0 1m', f'ILOAD VOUT 0 {current}')
        net = replace_once(net, 'CLOAD VOUT 0 100p', f'CLOAD VOUT 0 {cap}')
        return net + f'\n.temp {temp}\n'

    corners = ['typical', 'ff', 'ss', 'fs', 'sf'] if args.full else ['typical']
    temps = [-40, 27, 125] if args.full else [27]
    volts = [3.0, 3.3, 3.6] if args.full else [3.3]
    caps = [10e-12, 100e-12, 1e-9] if args.full else [100e-12]
    loads = [0, 1e-5, 1e-4, .001, .01, .1]
    pvts = list(product(corners, temps, volts))

    def dc_case(case):
        corner, temp, vin, standby = case
        name = f'dc_{corner}_{temp}_{vin}_{int(standby)}'
        maximum, step = (.001, .00001) if standby else (.1, .001)
        run(name, circuit(corner, temp, vin, standby=standby),
            f'dc ILOAD 0 {maximum} {step}\nwrdata {out / (name + ".dat")} '
            'v(vout) i(vsup) i(vref) v(pgood) v(xdut.gate)')
        d = data(name)
        iq_vin = -d[:, 2] - d[:, 0]
        iq_total = iq_vin + 1e-6 - d[:, 3]  # imported bias and reference current
        return dict(name=name, corner=corner, temp_C=temp, vin_V=vin, standby=standby,
                    vout_min_V=float(d[:, 1].min()), vout_max_V=float(d[:, 1].max()),
                    iq_vin_max_A=float(iq_vin.max()), iq_total_max_A=float(iq_total.max()),
                    dc_ok=bool(np.all((d[:, 1] >= LOW) & (d[:, 1] <= HIGH))),
                    iq_ok=bool(not standby or iq_total.max() <= 20e-6))

    def ac_case(case):
        corner, temp, vin, cap, current, standby = case
        name = f'ac_{corner}_{temp}_{vin}_{cap}_{current}_{int(standby)}'
        net = circuit(corner, temp, vin, current, cap, standby)
        # Series voltage injection keeps the exact DC circuit closed. The
        # voltage return ratio assumes the feedback input is high impedance;
        # do not mistake it for extracted multiloop stability signoff.
        # An ideal full-load sink can make Newton converge to an unphysical
        # negative-output solution. A nodeset is a solver guess, not a clamp.
        # Startup tests below intentionally have no nodeset or forced IC.
        net += '\n.nodeset v(vout)=1.8\n'
        net = replace_once(net, 'VREF_SS VFB GATE ldo_error_amp',
                           'VREF_SS VFB_TEST GATE ldo_error_amp')
        net = replace_once(net, 'XEA VIN', 'VTEST VFB_TEST VFB dc 0 ac 1\nXEA VIN')
        run(name, net, f'op\nwrdata {out / (name + "_op.dat")} v(vout)\n'
            f'ac dec 100 1 1e9\nlet loop=-v(xdut.vfb)/v(xdut.vfb_test)\n'
            f'wrdata {out / (name + ".dat")} real(loop) imag(loop)')
        op = float(data(name + '_op')[0, 1])
        d = data(name)
        gain = 20 * np.log10(np.hypot(d[:, 1], d[:, 2]))
        phase = np.unwrap(np.arctan2(d[:, 2], d[:, 1])) * 180 / np.pi
        down = np.where((gain[:-1] > 0) & (gain[1:] <= 0))[0]
        crossings = []
        for i in down:
            fraction = gain[i] / (gain[i] - gain[i + 1])
            crossings.append((float(10 ** (np.log10(d[i, 0]) + fraction *
                               np.log10(d[i + 1, 0] / d[i, 0]))),
                              float(180 + phase[i] + fraction * (phase[i + 1] - phase[i]))))
        pm = min((x[1] for x in crossings), default=None)
        valid = bool(LOW <= op <= HIGH and gain[0] > 40 and pm is not None)
        return dict(name=name, corner=corner, temp_C=temp, vin_V=vin, cap_F=cap,
                    load_A=current, standby=standby, op_vout_V=op,
                    dc_loop_gain_dB=float(gain[0]), crossings_Hz_deg=crossings,
                    min_pm_deg=pm, valid=valid, pm_ok=bool(valid and pm >= 60))

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        dc = list(pool.map(dc_case, [(*pvt, mode) for pvt in pvts for mode in [False, True]]))
        cases = [(*pvt, cap, current, mode) for pvt in pvts for cap in caps
                 for mode in [False, True] for current in (loads if not mode else [0, .001])]
        ac = list(pool.map(ac_case, cases))

    # Dropout characterization uses a fresh DC sweep, not an AC operating point.
    dropout = []
    for corner, temp in product(corners, temps):
        name = f'drop_{corner}_{temp}'
        net = circuit(corner, temp, current=.1)
        # EN tracks VIN during the supply sweep instead of exceeding its rail.
        net = replace_once(net, 'VEN EN 0 3.3', 'EEN EN 0 VIN 0 1')
        net += '\n.nodeset v(vout)=1.8\n'
        run(name, net, f'dc VSUP 3.3 1.7 -0.005\nwrdata {out / (name + ".dat")} v(vout)')
        d = data(name)
        at_21 = float(d[np.argmin(abs(d[:, 0] - 2.1)), 1])
        good = d[(d[:, 1] >= LOW) & (d[:, 1] <= HIGH)]
        dropout.append(dict(corner=corner, temp_C=temp, vout_at_2p1V=at_21,
                            lowest_VIN_in_band=float(good[:, 0].min()) if len(good) else None,
                            headroom_300mV_ok=LOW <= at_21 <= HIGH))

    transient = []
    for name, edge in [('load_10us', 10e-6), ('load_100ns', 100e-9)]:
        points = [(0, 0), (.0002, 0), (.0002 + edge, .001), (.0005, .001),
                  (.0005 + edge, .1), (.0008, .1), (.0008 + edge, .001),
                  (.0011, .001), (.0011 + edge, 0)]
        pwl = ' '.join(f'{t:.9g} {i:.9g}' for t, i in points)
        net = replace_once(circuit(current=0), 'ILOAD VOUT 0 0',
                           f'VCMD LOAD_CMD 0 PWL({pwl})\n'
                           'VLOAD_SENSE VOUT LOAD_TOP 0\n'
                           'BLOAD LOAD_TOP 0 I=v(LOAD_CMD)*min(max(v(VOUT)/0.1,0),1)')
        run(name, net, f'tran 20n 1.5m\nwrdata {out / (name + ".dat")} '
            'v(vout) v(pgood) i(vload_sense) v(xdut.gate)')
        d = data(name)
        settled = [float(d[np.argmin(abs(d[:, 0] - t)), 1]) for t in [.00045, .00075, .00105, .00145]]
        transient.append(dict(name=name, min_V=float(d[:, 1].min()), max_V=float(d[:, 1].max()),
                              settled_V=settled, settled_ok=all(LOW <= v <= HIGH for v in settled)))

    startups = [('startup_no_load', 1e12, 'typical', 27),
                ('startup_1mA', 1800, 'typical', 27), ('startup_100mA', 18, 'typical', 27)]
    if args.full:
        startups += [('startup_hot_ff', 1e12, 'ff', 125),
                     ('startup_cold_tt', 18, 'typical', -40),
                     ('startup_ss_27', 18, 'ss', 27), ('startup_ss_125', 18, 'ss', 125)]
    for name, resistance, corner, temp in startups:
        net = replace_once(circuit(corner, temp), 'ILOAD VOUT 0 0.001', f'RLOAD VOUT 0 {resistance}')
        net = replace_once(net, 'VEN EN 0 3.3',
                           'VEN EN 0 PWL(0 0 10u 0 11u 3.3 800u 3.3 801u 0)')
        run(name, net, f'tran 20n 1.2m\nwrdata {out / (name + ".dat")} '
            'v(vout) v(pgood) v(en) v(xdut.vref_ss)')
        d = data(name)
        settled = float(d[np.argmin(abs(d[:, 0] - .00075)), 1])
        discharged = d[(d[:, 0] >= .000801) & (d[:, 1] < .18), 0]
        discharge_us = float((discharged[0] - .000801) * 1e6) if len(discharged) else None
        off_pgood = float(d[-1, 2])
        transient.append(dict(name=name, min_V=float(d[:, 1].min()), max_V=float(d[:, 1].max()),
                              settled_V=settled, off_V=float(d[-1, 1]),
                              off_pgood_V=off_pgood, discharge_90pct_us=discharge_us,
                              settled_ok=bool(LOW <= settled <= HIGH and d[-1, 1] < .01
                                              and off_pgood < .33 and discharge_us is not None
                                              and discharge_us < 10)))

    net = replace_once(circuit(), 'VSTBY STBY 0 0', 'VSTBY STBY 0 PWL(0 0 200u 0 201u 3.3 600u 3.3 601u 0)')
    run('modes', net, f'tran 20n 1m\nwrdata {out / "modes.dat"} v(vout) v(stby) i(vsup) v(pgood)')
    d = data('modes')
    transient.append(dict(name='modes', min_V=float(d[:, 1].min()), max_V=float(d[:, 1].max()),
                          settled_ok=bool(np.all((d[:, 1] >= LOW) & (d[:, 1] <= HIGH)))))

    # Comparator characterized separately with rising AND falling input.
    net = replace_once(circuit(), 'XDUT VIN 0 VREF IBIAS EN STBY VOUT PGOOD ldo_top',
                       'XBIAS VIN 0 IBIAS EN STBY GATE ENB PB ldo_bias\nVGATE GATE 0 3.3\n'
                       'XPG VIN 0 PB EN ENB VREF VFB PGOOD ldo_pgood\n'
                       'VFB VFB 0 PWL(0 .9 100u .9 1.1m 1.2 1.2m 1.2 2.2m .9)')
    net = replace_once(net, 'ILOAD VOUT 0 0.001', 'RLOAD VOUT 0 1k')
    run('pgood', net, f'tran 100n 2.3m\nwrdata {out / "pgood.dat"} v(vfb) v(pgood)')
    d = data('pgood')
    high = d[:, 2] > 1.65
    rises = np.where(~high[:-1] & high[1:])[0] + 1
    falls = np.where(high[:-1] & ~high[1:])[0] + 1
    pgood = dict(rising_equivalent_vout_V=[float(1.5 * d[i, 1]) for i in rises],
                 falling_equivalent_vout_V=[float(1.5 * d[i, 1]) for i in falls])
    pgood['ok'] = bool(len(rises) == len(falls) == 1 and
                       1.59 < pgood['rising_equivalent_vout_V'][0] < 1.65 and
                       1.50 < pgood['falling_equivalent_vout_V'][0] < 1.56)

    results = dict(full=args.full, dc=dc, ac=ac, dropout=dropout, transient=transient, pgood=pgood)
    results['failures'] = dict(dc=sum(not r['dc_ok'] for r in dc),
                              standby_iq=sum(not r['iq_ok'] for r in dc),
                              ac=sum(not r['pm_ok'] for r in ac),
                              dropout=sum(not r['headroom_300mV_ok'] for r in dropout),
                              transient=sum(not r['settled_ok'] for r in transient),
                              pgood=int(not pgood['ok']))
    (out / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    for name, rows in [('dc', dc), ('ac', ac), ('dropout', dropout)]:
        with (out / f'{name}.csv').open('w') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    print(json.dumps({k: results[k] for k in ['failures', 'transient', 'pgood']}, indent=2))
    print('DC range:', min(r['vout_min_V'] for r in dc), max(r['vout_max_V'] for r in dc))
    print('Max STANDBY Iq (VIN + imported bias/reference):', max(r['iq_total_max_A'] for r in dc if r['standby']))
    print('Worst valid voltage-return-ratio margin:', min((r for r in ac if r['valid']), key=lambda r: r['min_pm_deg']))
    print('Outputs:', out)
    raise SystemExit(1 if any(results['failures'].values()) else 0)


if __name__ == '__main__':
    main()
