#!/bin/bash
#
# install_harness_pdklibs.sh
#
# The iic-osic-tools "gf180mcuD" PDK ships only the foundry "gf180mcu_fd_*"
# libraries, but the Chipalooza harness layout (gf180mcu_ocd_chipalooza)
# references three more, which open-pdks main installs under libs.ref/.
# The gf180mcuD.magicrc already inside the container has addpath lines for
# all three, so only the contents are missing.  Without them, magic fails
# the harness cell reads with e.g.
#
#     Failed on cell gf180mcu_as_sc_mcu7t3v3__tap_2
#
# and scripts/run_gen_wrapper_gds.sh leaves 0-byte GDS files.
#
# Each library is cloned at the commit pinned by open-pdks main
# (gf180mcu/gf180mcu.json, "reference" section) and installed into the
# CONTAINER PDK at /foss/pdks/gf180mcuD/libs.ref/.  The install is
# container-local: re-run this script after recreating the container.
#
# Staging (mirrors the open-pdks gf180mcu/Makefile.in targets):
#   gf180mcu_as_sc_mcu7t3v3  copied verbatim from the repo's
#                            pdk/libs.ref/ overlay  (digital-avalon-%)
#   gf180mcu_ocd_io           mag/ from the repo's magic/ and spice/ from
#                            netlist/schematic/  (open-pdks regenerates the
#                            mag views from cells/*_5lm.gds.gz via
#                            gds_import_io.tcl; the repo magic sources are
#                            the same geometry)
#   gf180mcu_ocd_ip_sram     mag/ from the repo's cells/*/magic/
#                            (open-pdks regenerates from cells/*/*.gds via
#                            gds_import_ocd_sram.tcl; equivalent geometry)
#
# Usage:
#     sh scripts/install_harness_pdklibs.sh [container-name]
#
# docker cp goes through the docker daemon as root, so no container-side
# permissions are needed (a "Permission denied" from a plain docker exec
# mkdir in libs.ref/ is expected; docker cp bypasses it).

set -e

CONTAINER=${1:-iic-osic-tools_xserver_uid_501}
PDKPATH=/foss/pdks/gf180mcuD/libs.ref

AS_SC_URL=https://github.com/AvalonSemiconductors/gf180mcu_as_sc_mcu7t3v3
AS_SC_COMMIT=aa30990f0d9f71d2966f27ffd5afd586efcfd05e
OCD_IO_URL=https://github.com/RTimothyEdwards/gf180mcu_ocd_io
OCD_IO_COMMIT=6e0e354a78793339a4a004a6d9c08990d0eee3e4
OCD_SRAM_URL=https://github.com/RTimothyEdwards/gf180mcu_ocd_ip_sram
OCD_SRAM_COMMIT=d41c7447d34d0c298158094378c8268560941724

STAGE=$(mktemp -d "${TMPDIR:-/tmp}/chipalooza-pdklibs.XXXXXX")
OUT="$STAGE/install"
mkdir -p "$OUT"
trap 'rm -rf "$STAGE"' EXIT

echo "== cloning libraries at open-pdks pinned commits into $STAGE"
git clone -q "$AS_SC_URL"   "$STAGE/gf180mcu_as_sc_mcu7t3v3"
git clone -q "$OCD_IO_URL"  "$STAGE/gf180mcu_ocd_io"
git clone -q "$OCD_SRAM_URL" "$STAGE/gf180mcu_ocd_ip_sram"
git -C "$STAGE/gf180mcu_as_sc_mcu7t3v3"   checkout -q "$AS_SC_COMMIT"
git -C "$STAGE/gf180mcu_ocd_io"          checkout -q "$OCD_IO_COMMIT"
git -C "$STAGE/gf180mcu_ocd_ip_sram"     checkout -q "$OCD_SRAM_COMMIT"

echo "== staging"

# --- gf180mcu_as_sc_mcu7t3v3: verbatim PDK overlay copy ------------------
mkdir -p "$OUT/gf180mcu_as_sc_mcu7t3v3"
cp -R "$STAGE/gf180mcu_as_sc_mcu7t3v3/pdk/libs.ref/gf180mcu_as_sc_mcu7t3v3/." \
      "$OUT/gf180mcu_as_sc_mcu7t3v3/"
cat > "$OUT/gf180mcu_as_sc_mcu7t3v3/PROVENANCE" <<EOF
Manually installed $(date +%Y-%m-%d) to match open-pdks main staging.
repo:   $AS_SC_URL
commit: $AS_SC_COMMIT (open-pdks gf180mcu/gf180mcu.json pin)
copied verbatim from the repo's pdk/libs.ref/gf180mcu_as_sc_mcu7t3v3
per the open-pdks gf180mcu/Makefile.in target digital-avalon-%.
EOF

# --- gf180mcu_ocd_io: magic + spice views --------------------------------
mkdir -p "$OUT/gf180mcu_ocd_io/mag" "$OUT/gf180mcu_ocd_io/spice"
cp -R "$STAGE/gf180mcu_ocd_io/magic/." "$OUT/gf180mcu_ocd_io/mag/"
cp -R "$STAGE/gf180mcu_ocd_io/netlist/schematic/." \
      "$OUT/gf180mcu_ocd_io/spice/" 2>/dev/null || true
cat > "$OUT/gf180mcu_ocd_io/PROVENANCE" <<EOF
Manually installed $(date +%Y-%m-%d).
repo:   $OCD_IO_URL
commit: $OCD_IO_COMMIT (open-pdks gf180mcu/gf180mcu.json pin)
mag/ from the repo's magic/ (the author's own magic sources).
open-pdks stages this library by importing cells/*_5lm.gds.gz with
gds_import_io.tcl instead; geometry is equivalent.
spice/ from the repo's netlist/schematic/.
EOF

# --- gf180mcu_ocd_ip_sram: magic views for all four macros ---------------
mkdir -p "$OUT/gf180mcu_ocd_ip_sram/mag"
for d in "$STAGE"/gf180mcu_ocd_ip_sram/cells/*/; do
    [ -d "$d/magic" ] && cp -R "$d/magic/." "$OUT/gf180mcu_ocd_ip_sram/mag/"
done
cat > "$OUT/gf180mcu_ocd_ip_sram/PROVENANCE" <<EOF
Manually installed $(date +%Y-%m-%d).
repo:   $OCD_SRAM_URL
commit: $OCD_SRAM_COMMIT (open-pdks gf180mcu/gf180mcu.json pin)
mag/ from the repo's cells/*/magic/ (top cell plus subcells).
open-pdks stages by importing cells/*/*.gds with gds_import_ocd_sram.tcl
instead; geometry is equivalent.
EOF

echo "== installing into container $CONTAINER:$PDKPATH"
docker cp "$OUT/gf180mcu_as_sc_mcu7t3v3/." "$CONTAINER:$PDKPATH/gf180mcu_as_sc_mcu7t3v3/"
docker cp "$OUT/gf180mcu_ocd_io/."          "$CONTAINER:$PDKPATH/gf180mcu_ocd_io/"
docker cp "$OUT/gf180mcu_ocd_ip_sram/."     "$CONTAINER:$PDKPATH/gf180mcu_ocd_ip_sram/"

echo "== verifying"
docker exec "$CONTAINER" bash -lc "
    ls $PDKPATH/gf180mcu_as_sc_mcu7t3v3/mag | grep -c mag &&
    ls $PDKPATH/gf180mcu_ocd_io/mag/gf180mcu_ocd_io__asig_5p0.mag &&
    ls $PDKPATH/gf180mcu_ocd_ip_sram/mag | grep -c mag"

echo "Done. If the wrapper GDS needs regenerating, run inside the container:"
echo "  cd <...>/gf180mcu_ocd_chipalooza && sh scripts/run_gen_wrapper_gds.sh"
