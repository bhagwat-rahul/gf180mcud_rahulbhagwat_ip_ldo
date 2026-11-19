#!/usr/bin/env python3
"""Assemble ldo_top from the seven blocks and measure the real bbox.

Shelf packing into the 1274.27 um slot width (first-fit, tallest first).
The placement is hierarchical (`use`); inter-block routing is not drawn.
The purpose is the measured assembled bounding box.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from magcanvas import Canvas, parse_mag

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / 'layout'
WIDTH = 1274.27 - 8.0          # keep 4 um margin each side

BLOCKS = ['ldo_startup', 'ldo_pgood', 'ldo_softstart', 'ldo_load',
          'ldo_error_amp', 'ldo_power_stage', 'ldo_bias']


def bbox(cell):
    layers, _, _ = parse_mag(LAYOUT / f'{cell}.mag')
    xs, ys = [], []
    for rs in layers.values():
        for r in rs:
            xs += [r[0], r[2]]
            ys += [r[1], r[3]]
    inv = 1.0 / 200.0
    return (min(xs) * inv, min(ys) * inv, max(xs) * inv, max(ys) * inv)


def main():
    boxes = {b: bbox(b) for b in BLOCKS}
    order = sorted(BLOCKS, key=lambda b: boxes[b][3] - boxes[b][1], reverse=True)
    c = Canvas(library_dir=str(LAYOUT))
    x = y = 0.0
    row_h = 0.0
    placed = {}
    for b in order:
        x0, y0, x1, y1 = boxes[b]
        w, h = x1 - x0, y1 - y0
        if x > 0 and x + w > WIDTH:
            x = 0.0
            y += row_h + 4.0
            row_h = 0.0
        placed[b] = (x - x0, y - y0)
        c.use(b, b.upper(), x - x0, y - y0)
        x += w + 4.0
        row_h = max(row_h, h)
    total_h = y + row_h
    print('placement:')
    for b in order:
        x0, y0, x1, y1 = boxes[b]
        print(f'  {b:16s} {x1-x0:8.2f} x {y1-y0:7.2f} at ({placed[b][0]:.2f},{placed[b][1]:.2f})')
    print(f'assembled bbox: {WIDTH:.1f} x {total_h:.1f} um = {WIDTH*total_h/1e3:.1f}k um2')
    print(f'slot: 1274.27 x 412.71 um = {1274.27*412.71/1e3:.1f}k um2')
    c.write(str(LAYOUT / 'ldo_top.mag'))
    print('wrote layout/ldo_top.mag')


if __name__ == '__main__':
    main()
