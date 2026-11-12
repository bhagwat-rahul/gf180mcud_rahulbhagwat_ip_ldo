#!/usr/bin/env python3
"""Plot captured ngspice data without modifying or filtering the measurements."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('results', type=Path, help='Directory written by run.py')
    parser.add_argument('--out', type=Path, default=ROOT / '.amp/in/artifacts')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    results = json.loads((args.results / 'results.json').read_text())
    def read(name):
        return np.loadtxt(args.results / (name + '.dat'), skiprows=1)

    plt.rcParams.update({'font.size': 11, 'axes.grid': True, 'grid.alpha': .2})
    fig, axes = plt.subplots(2, 2, figsize=(13, 8), constrained_layout=True)
    for name, ax in zip(['load_10us', 'load_100ns'], axes[0]):
        d = read(name)
        ax.plot(d[:, 0] * 1e6, d[:, 1], color='#1c638c', label='VOUT')
        ax.axhspan(1.746, 1.854, color='#47a877', alpha=.15, label='±3% DC band (not transient limit)')
        ax.set(xlabel='Time (µs)', ylabel='VOUT (V)', title=f'{name.replace("_", " ")} — {d[:, 1].min():.3f} to {d[:, 1].max():.3f} V')
        other = ax.twinx()
        other.plot(d[:, 0] * 1e6, d[:, 3] * 1e3, color='#ae6226', alpha=.45, label='Applied load')
        other.set_ylabel('Applied load (mA)', color='#ae6226')
        other.grid(False)
        ax.set_zorder(other.get_zorder() + 1)
        ax.patch.set_visible(False)
        ax.legend(loc='lower right', fontsize=8)
    d = read('startup_no_load')
    axes[1, 0].plot(d[:, 0] * 1e6, d[:, 1], label='VOUT')
    axes[1, 0].plot(d[:, 0] * 1e6, d[:, 2], label='PGOOD', alpha=.7)
    axes[1, 0].plot(d[:, 0] * 1e6, d[:, 3], label='EN', linestyle='--', alpha=.7)
    axes[1, 0].set(xlabel='Time (µs)', ylabel='Voltage (V)', title='Startup and OFF discharge — no external DC load')
    axes[1, 0].legend()
    for row in results['dc']:
        d = read(row['name'])
        axes[1, 1].plot(d[:, 0] * 1e3, d[:, 1], alpha=.45, linewidth=.7)
    axes[1, 1].axhspan(1.746, 1.854, color='#47a877', alpha=.12, label='±3% DC target band')
    axes[1, 1].set(xlabel='External load (mA)', ylabel='VOUT (V)', title='DC sweep — all simulated PVT cases / both modes')
    axes[1, 1].legend(loc='lower right', fontsize=8)
    fig.suptitle('GF180MCU-D schematic simulations — ideal reference, bias and passives\nTransient plots: typical / 27 °C / 3.3 V / 100 pF; load generator not implemented')
    fig.savefig(args.out / 'ldo_results.png', dpi=170)
    plt.close(fig)

    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True, constrained_layout=True)
    selected = [r for r in results['ac'] if r['corner']=='typical' and r['temp_C']==27
                and r['vin_V']==3.3 and r['cap_F']==1e-10 and not r['standby']
                and r['load_A'] in [0, .001, .1]]
    for row in selected:
        d = read(row['name'])
        axes[0].semilogx(d[:, 0], 20*np.log10(np.hypot(d[:, 1], d[:, 2])), label=f'{row["load_A"]*1e3:g} mA')
        axes[1].semilogx(d[:, 0], np.unwrap(np.arctan2(d[:, 2], d[:, 1]))*180/np.pi)
    axes[0].axhline(0, color='gray', linewidth=.8)
    axes[0].set(ylabel='Voltage return ratio (dB)', title='Typical / 27 °C / 3.3 V / 100 pF\nFeedback-input series injection — preliminary, not multiloop signoff')
    axes[0].legend()
    axes[1].axhline(-120, color='gray', linestyle='--', label='60° margin phase at unity crossing')
    axes[1].set(xlabel='Frequency (Hz)', ylabel='Phase (degrees)')
    axes[1].legend()
    fig.savefig(args.out / 'ldo_loopgain.png', dpi=170)
    plt.close(fig)


if __name__ == '__main__':
    main()
