#!/bin/sh
# Regenerate the Magic layout baseline in layout/ from the current schematics.
#
# Usage (from the repo root, inside the iic-osic-tools container):
#   iic-pdk gf180mcuD
#   sh scripts/import_layout.sh
#
# What this does:
#   1. Netlists schematics/ldo_tb.sch with xschem into a scratch dir.
#   2. Splits the design into one SPICE file per subckt (ldo_top + 7 children).
#   3. Renames cap_mim_2f0_m4m5_noshield -> cap_mim_2p0fF in the import
#      copies: "cap_mim_2p0fF" is the name of the PDK's Magic gencell that
#      draws a 2 fF/um^2 M4-M5 MIM cap.  The schematic keeps the true model
#      name cap_mim_2f0_m4m5_noshield so extraction/LVS match.
#   4. Runs "magic::netlist_to_layout" per block, then the top, then
#      "writeall force", producing the hierarchical .mag baseline in layout/.
#
# Known import limits (also see layout/README.md):
#   - ppolyf_u_3k has NO Magic gencell: every 3k poly resistor imports as an
#     empty placeholder cell. Draw them by hand (serpentine/folded).
#   - Multi-finger MOS (m>1) come in as one tall vertical stack; re-floorplan
#     MPASS (m=400) and MIR (m=210) into 2D arrays.

set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
SCRATCH="$ROOT/.amp/in/magic-import-run"
MAGICRC=/foss/pdks/gf180mcuD/libs.tech/magic/gf180mcuD.magicrc

rm -rf "$SCRATCH"; mkdir -p "$SCRATCH"

# ppolyf_u_3k has no gencell: pre-seed an empty placeholder cell BEFORE any
# import so the first block that references it (ldo_softstart/RSS) reads it
# and places the use line instead of silently dropping the instance.
cat > "$SCRATCH/ppolyf_u_3k.mag" <<'MEOF'
magic
tech gf180mcuD
timestamp 1795029197
<< end >>
MEOF

# 1. netlist
( cd "$ROOT/schematics" && xschem -n -q -x -b --rcfile ./xschemrc \
    -o "$SCRATCH" -N ldo_tb.spice ldo_tb.sch )

# 2. split into per-subckt import copies (+ cap gencell rename)
python3 - "$SCRATCH" <<'PYEOF'
import sys
from pathlib import Path
out = Path(sys.argv[1])
src = (out / 'ldo_tb.spice').read_text()
blocks, cur = {}, None
for ln in src.splitlines(keepends=True):
    st = ln.strip()
    if st.startswith('.subckt '):
        cur = st.split()[1]; blocks[cur] = [ln]
    elif cur:
        blocks[cur].append(ln)
        if st.startswith('.ends'): cur = None
for n, b in blocks.items():
    (out / f'{n}.spice').write_text(
        ''.join(b).replace('cap_mim_2f0_m4m5_noshield', 'cap_mim_2p0fF'))
print('import netlists:', ', '.join(blocks))
PYEOF

# 3. import children, then top
cd "$SCRATCH"
for n in ldo_softstart ldo_error_amp ldo_power_stage ldo_bias \
         ldo_pgood ldo_startup ldo_load ldo_top; do
    magic -dnull -noconsole -rcfile "$MAGICRC" <<EOF
magic::netlist_to_layout $n.spice gf180mcu
writeall force
quit -noprompt
EOF
done

# 4. publish (true netlist + all generated cells)
cp "$SCRATCH"/*.mag "$ROOT/layout/"
python3 - "$SCRATCH" "$ROOT" <<'PYEOF'
import sys
from pathlib import Path
src = Path(sys.argv[1]) / 'ldo_tb.spice'
dst = Path(sys.argv[2]) / 'layout' / 'ldo_top.spice'
lines = src.read_text().splitlines(keepends=True)
out = ['* gf180mcud_rahulbhagwat_ip_ldo - ldo_top design hierarchy (true netlist, for LVS)\n',
       '* regenerated from schematics/ via xschem; see scripts/import_layout.sh\n']
keep = False
for ln in lines:
    st = ln.strip()
    if st.startswith('.subckt'): keep = True
    if keep: out.append(ln)
    if keep and st.startswith('.ends'): keep = False
dst.write_text(''.join(out))
PYEOF
rm -f "$SCRATCH/ldo_tb.spice"

echo "layout baseline refreshed: $(ls "$ROOT/layout"/*.mag | wc -l) .mag files in layout/"
