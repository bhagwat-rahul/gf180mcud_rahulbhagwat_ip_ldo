"""Two-excitation Tian return ratio and conservative crossover screening.

Probe: VTEST positive negative, ITEST ground positive. Both have DC=0.
Run AC with (VTEST, ITEST)=(1 V, 0 A), then (0 V, 1 A).
vv/iv are V(positive)/I(VTEST) from the voltage run; vi/ii from the current run.
Current follows SPICE's positive-to-negative voltage-source convention.

Reference and circuit: https://gotroot.ca/spectrum/www.spectrum-soft.com/news/
spring2011/loopgain.html (Tian/Wiedmann two-source method).
This removes the high-input-impedance assumption, not the need to check loops
which remain closed around the chosen probe. PM alone is not a stability proof.
"""

import numpy as np


def tian(vv, iv, vi, ii):
    # Algebraically -1/(1 - 1/m); this form also works when m=0.
    m = 2 * (iv * vi - vv * ii) + vv + ii
    return m / (1 - m)


def margins(frequency, loop):
    """Report every unity crossing, retaining the continuous phase branch.

The automatic >=60 degree gate is deliberately limited to one downward
crossing, positive low-frequency feedback, and a sweep ending below unity.
Multiple crossings are reported for review, never hidden by phase wrapping.
These are sampled/interpolated margins, not a pole count or Nyquist proof.
"""
    frequency, loop = np.asarray(frequency), np.asarray(loop)
    if (frequency.ndim != 1 or loop.shape != frequency.shape or len(frequency) < 2
            or not np.isfinite(frequency).all() or not np.isfinite(loop).all()
            or np.any(frequency <= 0) or np.any(np.diff(frequency) <= 0)):
        raise ValueError('Expected finite loop data on an increasing positive frequency grid')
    gain = 20 * np.log10(np.maximum(abs(loop), np.finfo(float).tiny))
    phase = np.unwrap(np.angle(loop)) * 180 / np.pi
    logf = np.log10(frequency)
    crossings = []
    for i in np.where((gain[:-1] > 0) != (gain[1:] > 0))[0]:
        fraction = gain[i] / (gain[i] - gain[i + 1])
        crossings.append(dict(frequency_Hz=float(10 ** (logf[i] + fraction * (logf[i + 1] - logf[i]))),
                              direction='down' if gain[i] > 0 else 'up',
                              phase_deg=float(phase[i] + fraction * (phase[i + 1] - phase[i])),
                              pm_deg=float(180 + phase[i] + fraction * (phase[i + 1] - phase[i]))))
    downward = [(c['frequency_Hz'], c['pm_deg']) for c in crossings if c['direction'] == 'down']
    pm = min((c[1] for c in downward), default=None)
    phase_crossings = []
    # All odd multiples of 180 degrees, not only the first -180 crossing.
    for critical in np.arange(-180 + 360 * np.floor((phase.min() + 180) / 360), phase.max() + 360, 360):
        for i in np.where((phase[:-1] > critical) != (phase[1:] > critical))[0]:
            fraction = (critical - phase[i]) / (phase[i + 1] - phase[i])
            phase_crossings.append(dict(
                frequency_Hz=float(10 ** (logf[i] + fraction * (logf[i + 1] - logf[i]))),
                gain_margin_dB=float(-(gain[i] + fraction * (gain[i + 1] - gain[i])))))
    simple = bool(len(crossings) == 1 and crossings[0]['direction'] == 'down'
                  and -180 < crossings[0]['pm_deg'] <= 180)
    valid = bool(gain[0] > 40 and abs(phase[0]) < 90 and gain[-1] < 0 and pm is not None)
    return dict(dc_loop_gain_dB=float(gain[0]), dc_phase_deg=float(phase[0]),
                crossings_Hz_deg=downward, unity_crossings=crossings,
                phase_crossings=phase_crossings, min_pm_deg=pm,
                min_return_difference=float(np.min(abs(1 + loop))),
                single_crossover=simple, valid=valid,
                pm_ok=bool(valid and simple and pm >= 60))
