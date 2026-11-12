#!/usr/bin/env python3
"""Export the actual editable Xschem sheets, not a separate block diagram."""
import argparse
from pathlib import Path
import re
import subprocess

import cairosvg

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT / '.amp/in/artifacts')
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    for sheet in sorted((ROOT / 'schematics').glob('*.sch')):
        svg = out / (sheet.stem + '.svg')
        # Batch zoom_full excludes some off-canvas text in this Xschem build.
        # Include explicit bounds for components AND multiline annotations.
        positions = [(float(x), float(y)) for x, y in re.findall(
            r'(?ms)^[CT] \{.*?\} (-?[\d.]+) (-?[\d.]+) \d \d ', sheet.read_text())]
        x1 = min(x for x, y in positions) - 250
        y1 = min(y for x, y in positions) - 100
        x2 = max(x for x, y in positions) + 400
        y2 = max(y for x, y in positions) + 260
        height = round(2200 * (y2 - y1) / (x2 - x1))
        command = (f'set dark_colorscheme 0; xschem build_colors; '
                   f'xschem print svg {{{svg}}} 2200 {height} {x1} {y1} {x2} {y2}')
        subprocess.run(['xschem', '-q', '-x', '-b', '--rcfile', './xschemrc',
                        '--command', command, sheet.name], cwd=sheet.parent, check=True)
        cairosvg.svg2png(url=str(svg), write_to=str(svg.with_suffix('.png')), output_width=2200)
    print(out)


if __name__ == '__main__':
    main()
