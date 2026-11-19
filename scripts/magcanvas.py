#!/usr/bin/env python3
"""Minimal Magic .mag writer for the gf180mcuD LDO layout.

All coordinates are in micrometres; they are written on the PDK's 5 nm
grid (magscale 1 10 => 200 file units per micron).  The writer supports
rectangles on named layers, cell instances with rotation/mirror, and
labels/ports, which is everything a hand-generated block needs.

Usage from a build script:

    from magcanvas import Canvas
    c = Canvas()
    c.use('nfet_03v3_K8XTZ5', 'M1', 10.0, 20.0)
    c.rect('metal1', 10.0, 20.0, 12.0, 22.0)
    c.label('metal1', 10.0, 20.0, 12.0, 22.0, 'VOUT', port=True)
    c.write('/path/to/cell.mag')
"""

import os
import re
import time

UNITS_PER_UM = 200          # magscale 1 10 at the gf180mcuD internal grid
TECH = 'gf180mcuD'

# Rotation -> (a, b, d, e) of the .mag transform:
#   x' = a*x + b*y + c_x,  y' = d*x + e*y + c_y
ROT = {
    0:   (1, 0, 0, 1),
    90:  (0, -1, 1, 0),
    180: (-1, 0, 0, -1),
    270: (0, 1, -1, 0),
}


def u(v):
    """Micrometres -> file units (5 nm grid)."""
    return int(round(v * UNITS_PER_UM))


def parse_mag(path):
    """Return (layers, uses, labels) for a .mag file.

    layers: {layer: [(x0,y0,x1,y1), ...]} in file units
    uses:   [(cell, (a,b,c,d,e,f), box)]
    labels: [(layer, x0,y0,x1,y1, text)]
    """
    layers, uses, labels = {}, [], []
    layer = None
    pending_use = None
    for line in open(path):
        line = line.rstrip('\n')
        m = re.match(r'<< (.+) >>', line)
        if m:
            layer = m.group(1)
            layers.setdefault(layer, [])
            continue
        m = re.match(r'rect (-?\d+) (-?\d+) (-?\d+) (-?\d+)$', line)
        if m and layer:
            layers[layer].append(tuple(int(x) for x in m.groups()))
            continue
        m = re.match(r'use (\S+) (\S+)$', line)
        if m:
            pending_use = [m.group(1), None, None]
            uses.append(pending_use)
            continue
        m = re.match(r'transform (.*)$', line)
        if m and pending_use is not None:
            pending_use[1] = tuple(int(v) for v in m.group(1).split())
            continue
        m = re.match(r'box (-?\d+) (-?\d+) (-?\d+) (-?\d+)$', line)
        if m and pending_use is not None:
            pending_use[2] = tuple(int(x) for x in m.groups())
            continue
        m = re.match(r'(?:f?r?)label (\S+) (-?\d+) (-?\d+) (-?\d+) (-?\d+) \d+ \S+ \d+'
                     r' -?\d+ -?\d+ -?\d+ (.+)$', line)
        if m:
            labels.append((m.group(1), int(m.group(2)), int(m.group(3)),
                           int(m.group(4)), int(m.group(5)), m.group(6)))
    return layers, uses, labels


def cell_bbox(path, cache=None):
    """Content bbox in file units, including used cells (recursively)."""
    cache = cache if cache is not None else {}
    if path in cache:
        return cache[path]
    layers, uses, _ = parse_mag(path)
    xs, ys = [], []
    for rects in layers.values():
        for x0, y0, x1, y1 in rects:
            xs += [x0, x1]
            ys += [y0, y1]
    base = os.path.dirname(path)
    for name, trans, box in uses:
        if box is not None:
            bx0, by0, bx1, by1 = box
        else:
            child = os.path.join(base, name + '.mag')
            bx0, by0, bx1, by1 = cell_bbox(child, cache) if os.path.isfile(child) else (0, 0, 0, 0)
        a, b, c, d, e, f = trans or (1, 0, 0, 0, 1, 0)
        for x, y in ((bx0, by0), (bx0, by1), (bx1, by0), (bx1, by1)):
            xs.append(a * x + b * y + c)
            ys.append(d * x + e * y + f)
    if not xs:
        result = (0, 0, 0, 0)
    else:
        result = (min(xs), min(ys), max(xs), max(ys))
    cache[path] = result
    return result


class Canvas:
    def __init__(self, library_dir=None):
        self.library_dir = library_dir
        self.rects = {}      # layer -> [(x0,y0,x1,y1)] in units
        self.uses = []       # [(cell, (a,b,c,d,e,f), box)]
        self.labels = []     # [(layer, x0,y0,x1,y1, text, port_name)]

    def rect(self, layer, x0, y0, x1, y1):
        x0, x1 = sorted((u(x0), u(x1)))
        y0, y1 = sorted((u(y0), u(y1)))
        if x0 == x1 or y0 == y1:
            raise ValueError(f'zero-area rect on {layer}')
        self.rects.setdefault(layer, []).append((x0, y0, x1, y1))

    def use(self, cell, inst, x, y, rot=0, mirror=False, bbox=None):
        a, b, d, e = ROT[rot]
        if mirror:
            b, d = -b, -d
        c, f = u(x), u(y)
        if bbox is None:
            if self.library_dir is None:
                raise ValueError('bbox required without library_dir')
            bbox = cell_bbox(os.path.join(self.library_dir, cell + '.mag'))
        self.uses.append((cell, (a, b, c, d, e, f), bbox))

    def remove_rect(self, layer, x0, y0, x1, y1):
        """Delete a rectangle previously added (matched on the 5 nm grid)."""
        target = (u(x0), u(y0), u(x1), u(y1))
        rects = self.rects.get(layer, [])
        for i, rect in enumerate(rects):
            if rect == target:
                del rects[i]
                return
        raise ValueError(f'rect {target} not found on {layer}')

    def flatten(self, cell, x, y, rot=0, mirror=False):
        """Inline a child cell's rectangles (devices have no ports, so a
        block must own their geometry to connect to them)."""
        if self.library_dir is None:
            raise ValueError('library_dir required for flatten')
        layers, uses, _ = parse_mag(os.path.join(self.library_dir, cell + '.mag'))
        if uses:
            raise ValueError(f'{cell} is not a leaf cell')
        a, b, d, e = ROT[rot]
        if mirror:
            b, d = -b, -d
        c, f = u(x), u(y)
        for layer, rects in layers.items():
            for x0, y0, x1, y1 in rects:
                pts = [(a * px + b * py + c, d * px + e * py + f)
                       for px, py in ((x0, y0), (x1, y1), (x0, y1), (x1, y0))]
                xs = [pt[0] for pt in pts]
                ys = [pt[1] for pt in pts]
                self.rects.setdefault(layer, []).append(
                    (min(xs), min(ys), max(xs), max(ys)))
        return self

    def label(self, layer, x0, y0, x1, y1, text, port=None, size=700):
        self.labels.append((layer, u(x0), u(y0), u(x1), u(y1), text, port))

    def bounds(self):
        xs, ys = [], []
        for rects in self.rects.values():
            for x0, y0, x1, y1 in rects:
                xs += [x0, x1]
                ys += [y0, y1]
        for cell, (a, b, c, d, e, f), (bx0, by0, bx1, by1) in self.uses:
            for x, y in ((bx0, by0), (bx0, by1), (bx1, by0), (bx1, by1)):
                xs.append(a * x + b * y + c)
                ys.append(d * x + e * y + f)
        return (min(xs), min(ys), max(xs), max(ys)) if xs else (0, 0, 0, 0)

    def write(self, path):
        lines = [f'magic\ntech {TECH}\nmagscale 1 10\ntimestamp {int(time.time())}']
        for layer, rects in self.rects.items():
            lines.append(f'<< {layer} >>')
            lines.extend(f'rect {x0} {y0} {x1} {y1}' for x0, y0, x1, y1 in rects)
        for cell, (a, b, c, d, e, f), (bx0, by0, bx1, by1) in self.uses:
            lines.append(f'use {cell} {cell}_{len([l for l in lines if l.startswith("use ")])}')
            lines.append('timestamp 0')
            lines.append(f'transform {a} {b} {c} {d} {e} {f}')
            lines.append(f'box {bx0} {by0} {bx1} {by1}')
        if self.labels:
            lines.append('<< labels >>')
            port = 0
            for layer, x0, y0, x1, y1, text, port_name in self.labels:
                lines.append(f'flabel {layer} {x0} {y0} {x1} {y1} 0 FreeSans 700 0 0 0 {text}')
                if port_name is not None:
                    lines.append(f'port {port} nsew')
                    port += 1
        lines += ['<< properties >>', '<< end >>']
        with open(path, 'w') as stream:
            stream.write('\n'.join(lines) + '\n')
        return path


def resistor_cell(width_um, length_um, path):
    """Emit a gf180MCU ppolyf_u style resistor .mag.

        body        ppolyres, width x length          (unsalicided poly)
        heads       polysilicon, 0.51 um beyond body
        contacts    polycontact + metal1 pad on each head
        isolation   pwell island (substrate is the global p-well)

    Extraction then reports r_width/r_length from the drawn body and a
    third terminal on VSUBS, the process substrate, which is the same net
    as VSS on this chip.  Body width must be >= 0.8 um (DRC PRES.1).
    """
    if width_um < 0.8:
        raise ValueError('PPOLYRES minimum width is 0.8 um (PRES.1)')
    hw = width_um / 2.0
    hl = length_um / 2.0
    c = Canvas()
    c.rect('ppolyres', -hw, -hl, hw, hl)
    for sign in (1, -1):
        c.rect('polysilicon', -hw, min(sign * hl, sign * (hl + 0.51)),
               hw, max(sign * hl, sign * (hl + 0.51)))
        c.rect('polycontact', -0.11, min(sign * (hl + 0.16), sign * (hl + 0.39)),
               0.11, max(sign * (hl + 0.16), sign * (hl + 0.39)))
        c.rect('metal1', -hw - 0.15, min(sign * (hl - 0.05), sign * (hl + 0.60)),
               hw + 0.15, max(sign * (hl - 0.05), sign * (hl + 0.60)))
    c.rect('pwell', -hw - 0.7, -hl - 1.21, hw + 0.7, hl + 1.21)
    c.write(path)
    return path


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 4:
        resistor_cell(float(sys.argv[1]), float(sys.argv[2]), sys.argv[3])
