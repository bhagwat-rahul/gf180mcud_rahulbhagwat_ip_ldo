#!/usr/bin/env python3
#
# gen_slot_guides.py
#
# Generates magic layout guide cells "slot<N>_guide.mag" (N = 1 to 18) and a
# reference sheet "magic/SLOT_GUIDES.md" for the LDO project, one per slot of
# the Chipalooza 3 harness (gf180mcu_ocd_chipalooza).
#
# Each guide cell is drawn in the same coordinate frame as the harness slot
# wrapper (lower-left corner at 0, 0) and contains:
#
#   - The slot "square":  the wrapper's comment-layer border, exactly as the
#     wrapper draws it (0 to 1274.25 um x 0 to 412.71 um, border 2.31 um).
#   - A tick mark + label on the non-mask "comment" layer at every pin the
#     designer needs to take a wire out to:
#       * the slot's dedicated pads (sN_an[x])       10 um ticks
#       * the shared-edge power rails                10 um ticks
#       * the shared-edge control/bias signal pins    5 um ticks
#
# The comment layer is not a mask layer:  it does not affect DRC, netlist
# extraction, or GDS output.  Instances of the guide cell should be removed
# from the layout before release, but leaving one in is harmless.
#
# Guide positions come from the port (flabel) bounding boxes of the wrapper
# cells, which are the authoritative pin positions used by the chip top-level
# assembly.  Usage:
#
#     python3 scripts/gen_slot_guides.py [path/to/gf180mcu_ocd_chipalooza/magic]
#
# If the harness magic directory is not given, the script assumes it is the
# sibling directory "../gf180mcu_ocd_chipalooza/magic" of this repository.
#
# Results are written to "<repo>/magic/".

import os
import re
import sys
import time
from pathlib import Path

# Number of file units per micron in the wrapper .mag files ("magscale 1 10"
# with the gf180mcuD internal scale factor:  1 file unit = 5 nm).
UNITS_PER_UM = 200

# How deep, in microns, guide ticks extend inward from the slot border inner
# edge, by pin class.
TICK_DEDICATED_UM = 10.0
TICK_RAIL_UM = 10.0
TICK_SIGNAL_UM = 5.0

# The harness currently defines this many dedicated pads per slot (read from
# the wrapper cells).  If a wrapper is regenerated with different pad counts,
# this list must be updated (or the check relaxed).
EXPECTED_PADS = [2, 2, 2, 2, 2, 2, 2, 1, 3, 3, 1, 2, 2, 2, 2, 2, 2, 2]

FLABEL_RE = re.compile(
    r"^flabel (\S+) (-?\d+) (-?\d+) (-?\d+) (-?\d+) \S+ (\S+) (\d+) (-?\d+) "
    r"(\d+) (\d+) (.+)$"
)
RECT_RE = re.compile(r"^rect (-?\d+) (-?\d+) (-?\d+) (-?\d+)$")


def um(v):
    """Convert a file-unit coordinate string to microns (rounded to nm)."""
    return round(int(v) / UNITS_PER_UM, 3)


def parse_wrapper(path):
    """Parse a slot wrapper .mag file.

    Returns a dict with the border comment-layer rects and one record per
    label:  (name, layer, x1, y1, x2, y2, size, rotation) in file units.
    """
    borders = []
    labels = []
    section = None
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("<< "):
                section = line.strip("<> ")
                continue
            if line.startswith(("<<", "flabel", "port", "magic", "tech",
                                "magscale", "timestamp", "property")):
                pass
            m = RECT_RE.match(line) if section == "comment" else None
            if m:
                borders.append(tuple(int(x) for x in m.groups()))
                continue
            m = FLABEL_RE.match(line)
            if m:
                layer, x1, y1, x2, y2, font, size, rot, flags, justify, name = \
                    m.groups()
                labels.append({
                    "name": name,
                    "layer": layer,
                    "x1": int(x1), "y1": int(y1), "x2": int(x2), "y2": int(y2),
                    "font": font, "size": int(size),
                    "rot": int(rot), "flags": int(flags), "justify": int(justify),
                })
    return borders, labels


def classify(slot, labels):
    """Split labels into (dedicated, exit_extra, shared)."""
    east_re = re.compile(rf"s{slot}_an\[\d+\]$")
    dedicated, extra, shared = [], [], []
    for lab in labels:
        on_east = lab["x1"] >= 250000
        exit_side = (slot <= 9 and on_east) or (slot > 9 and not on_east)
        if exit_side and east_re.match(lab["name"]):
            dedicated.append(lab)
        elif exit_side:
            extra.append(lab)
        else:
            shared.append(lab)
    for group in (dedicated, extra, shared):
        group.sort(key=lambda l: (l["y1"], l["name"]))
    return dedicated, extra, shared


def guide_rects_and_labels(slot, borders, dedicated, extra, shared):
    """Build the guide cell content.

    Returns (comment_rects, flabel_lines) with coordinates in file units.
    """
    rects = [f"rect {x1} {y1} {x2} {y2}" for x1, y1, x2, y2 in borders]
    flabels = []

    def tick(lab, length_units):
        on_east = lab["x1"] >= 250000
        if on_east:
            x1, x2 = 254388 - length_units, 254388
        else:
            x1, x2 = 462, 462 + length_units
        y1, y2 = lab["y1"], lab["y2"]
        rects.append(f"rect {x1} {y1} {x2} {y2}")
        flabels.append(
            f"flabel comment {x1} {y1} {x2} {y2} 0 {lab['font']} {lab['size']} "
            f"{lab['rot']} {lab['flags']} {lab['justify']} {lab['name']}"
        )


    # Dedicated pads and any padframe power rails sharing the exit edge get
    # long ticks;  the shared-edge control/bias pins get short ones.
    for lab in dedicated:
        tick(lab, int(TICK_DEDICATED_UM * UNITS_PER_UM))
    for lab in extra:
        tick(lab, int(TICK_RAIL_UM * UNITS_PER_UM))
    for lab in shared:
        is_rail = lab["layer"] == "metal5"
        tick(lab, int(TICK_RAIL_UM * UNITS_PER_UM if is_rail
                      else TICK_SIGNAL_UM * UNITS_PER_UM))
    return rects, flabels


def write_guide(path, rects, flabels):
    body = ["magic", "tech gf180mcuD", "magscale 1 10",
            f"timestamp {int(time.time())}", "<< comment >>"]
    body += rects
    body.append("<< labels >>")
    body += flabels
    body += ["<< properties >>",
             "string FIXED_BBOX 0 0 254850 82542",
             "<< end >>"]
    path.write_text("\n".join(body) + "\n")


def write_reference(md_path, per_slot):
    """Write the SLOT_GUIDES.md reference sheet."""
    lines = []
    add = lines.append
    add("# Slot layout guides (slot1..slot18_guide.mag)")
    add("")
    add("Guide cells for laying out the LDO inside one Chipalooza 3 harness "
        "slot.  Each cell is the slot square plus tick marks and labels on "
        "the non-mask `comment` layer at every point where a wire must come "
        "out of the slot to reach the harness.")
    add("")
    add("Generated by `scripts/gen_slot_guides.py` from the harness slot "
        "wrappers (`gf180mcu_ocd_chipalooza/magic/slot<N>_wrapper.mag`).  "
        "Regenerate after any wrapper change with:")
    add("")
    add("    python3 scripts/gen_slot_guides.py")
    add("")
    add("## Using a guide in magic")
    add("")
    add("1. Open magic with the gf180mcuD tech loaded.")
    add("2. In your LDO layout cell, place the guide for your slot:  "
        "`getcell slot9_guide` (instance it at position 0 0;  the guide uses "
        "the same origin and size as the harness slot wrapper).")
    add("3. Route against the ticks:  a wire for pin X must end overlapping "
        "the harness wrapper's pin metal at that edge position (the wrapper "
        "cell carries the actual pad metal;  your GDS is overlaid on it by "
        "the top-level assembly).")
    add("4. Remove the guide instance before final GDS.  (Even if left in, "
        "the `comment` layer is not a mask layer and is not exported.)")
    add("")
    add("## Geometry common to every slot")
    add("")
    add("- Slot area:  0 to 1274.25 um (x) by 0 to 412.71 um (y);  the border "
        "square is 2.31 um thick.")
    add("- Slots 1 to 9:  dedicated pads exit the **east (right)** edge;  "
        "slots 10 to 18:  the **west (left)** edge.")
    add("- The shared-edge (control/bias/power) pins sit at the same "
        "positions in every slot.")
    add("- Positions below are the wrapper port (label) bounding boxes in "
        "um, origin at the slot's lower-left corner.")
    add("")
    add("### Shared edge (identical in all slots)")
    add("")
    add("Power rails (metal5):")
    add("")
    add("| pin | y low | y high |")
    add("|---|---|---|")
    common_rails = per_slot[0]["shared_rails"]
    for name, y1, y2 in common_rails:
        add(f"| {name} | {y1:.3f} | {y2:.3f} |")
    add("")
    add("Control/bias signals (metal3, hairline pins):")
    add("")
    add("| pin | y low | y high |")
    add("|---|---|---|")
    for name, y1, y2 in per_slot[0]["shared_signals"]:
        add(f"| {name} | {y1:.3f} | {y2:.3f} |")
    add("")
    add("### Dedicated pads per slot (the part that differs)")
    add("")
    add("| slot | exit edge | dedicated pads (y low..y high, um) | "
        "exit-edge extras |")
    add("|---|---|---|---|")
    for info in per_slot:
        pads = ", ".join(f"{n} {y1:.3f}..{y2:.3f}" for n, y1, y2 in info["pads"])
        extras = ", ".join(f"{n} {y1:.3f}..{y2:.3f}"
                           for n, y1, y2 in info["extras"]) or "-"
        add(f"| {info['slot']} | {info['edge']} | {pads} | {extras} |")
    add("")
    add("Note:  `config.txt` in the harness lists 2 dedicated pads for slots "
        "8 and 11, but the wrappers currently in the harness contain only "
        "one for each.  The tables and guides above reflect the wrappers "
        "as-is;  confirm with the harness owner before choosing slot 8 or 11.")
    add("")
    md_path.write_text("\n".join(lines))


def main():
    repo = Path(__file__).resolve().parent.parent
    if len(sys.argv) > 1:
        harness_magic = Path(sys.argv[1]).resolve()
    else:
        harness_magic = repo.parent / "gf180mcu_ocd_chipalooza" / "magic"
    if not harness_magic.is_dir():
        sys.exit(f"Harness magic directory not found:  {harness_magic}\n"
                 "Give it as the first argument.")
    out_dir = repo / "magic"
    out_dir.mkdir(exist_ok=True)

    per_slot = []
    for slot in range(1, 19):
        wrapper = harness_magic / f"slot{slot}_wrapper.mag"
        borders, labels = parse_wrapper(wrapper)
        if len(borders) != 4:
            sys.exit(f"slot{slot}_wrapper.mag:  expected 4 comment border "
                     f"rects, found {len(borders)}")
        dedicated, extra, shared = classify(slot, labels)
        if len(dedicated) != EXPECTED_PADS[slot - 1]:
            sys.exit(f"slot{slot}_wrapper.mag:  expected "
                     f"{EXPECTED_PADS[slot - 1]} dedicated pads, found "
                     f"{len(dedicated)} ({[l['name'] for l in dedicated]}).  "
                     "Wrapper changed?  Update EXPECTED_PADS.")
        rails = [(l["name"], um(l["y1"]), um(l["y2"])) for l in shared
                 if l["layer"] == "metal5"]
        signals = [(l["name"], um(l["y1"]), um(l["y2"])) for l in shared
                   if l["layer"] != "metal5"]
        per_slot.append({
            "slot": slot,
            "edge": "east (right)" if slot <= 9 else "west (left)",
            "pads": [(l["name"], um(l["y1"]), um(l["y2"])) for l in dedicated],
            "extras": [(l["name"], um(l["y1"]), um(l["y2"])) for l in extra],
            "shared_rails": rails,
            "shared_signals": signals,
        })

        rects, flabels = guide_rects_and_labels(slot, borders,
                                                dedicated, extra, shared)
        write_guide(out_dir / f"slot{slot}_guide.mag", rects, flabels)
        print(f"slot {slot:2d}:  {len(rects)} comment rects, "
              f"{len(flabels)} labels, {len(dedicated)} dedicated pads, "
              f"{len(extra)} exit-edge extras")

    write_reference(out_dir / "SLOT_GUIDES.md", per_slot)
    print(f"\nWrote {out_dir}/slot1..18_guide.mag and "
          f"{out_dir}/SLOT_GUIDES.md")


if __name__ == "__main__":
    main()
