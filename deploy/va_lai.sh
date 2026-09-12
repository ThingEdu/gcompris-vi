#!/bin/sh
# Re-patch GCompris' .rcc files from the pristine copies dpkg-divert keeps at
# <file>.orig.
#
# Called from two places:
#   - postinst, when the gcompris-vi package is installed
#   - the dpkg trigger, every time gcompris-qt-data is upgraded: dpkg writes the
#     NEW pristine to <file>.orig and this script patches that, so the Vietnamese
#     localisation survives the upgrade
#
# Always patches from .orig, never on top of an already-patched file, so running
# it any number of times gives the same result.
#
# SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
# SPDX-License-Identifier: GPL-3.0-or-later
set -e

RCC=${RCC_DIR:-/usr/share/gcompris-qt/rcc}
TOOLS=${TOOLS_DIR:-/usr/share/gcompris-vi/tools}
MAPS=${MAPS_DIR:-/usr/share/gcompris-vi/maps}
PY=${PYTHON:-python3}

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

rcc_version() {
    $PY -c "import struct,sys;print(struct.unpack_from('>I',open(sys.argv[1],'rb').read(),4)[0])" "$1"
}

# patch_rcc <name.rcc> <patch command...>
# The patch command is called with the unpacked tree as its last argument.
patch_rcc() {
    name=$1
    shift
    orig="$RCC/$name.orig"
    if [ ! -f "$orig" ]; then
        echo "skipping $name: no $orig (diversion not set up?)" >&2
        return 0
    fi
    ver=$(rcc_version "$orig")
    tree="$TMP/tree"
    rm -rf "$tree" "$TMP/rt" "$TMP/rt.rcc"
    $PY "$TOOLS/rcc_extract.py" "$orig" "$tree" >/dev/null

    # Round-trip before changing anything: repack unmodified, unpack again, and
    # every file must match byte for byte. This is the check that catches an
    # .rcc generation the packer does not handle yet.
    $PY "$TOOLS/rcc_repack.py" "$tree" "$TMP/rt.rcc" --version "$ver" >/dev/null
    $PY "$TOOLS/rcc_extract.py" "$TMP/rt.rcc" "$TMP/rt" >/dev/null
    if ! diff -r "$tree" "$TMP/rt" >/dev/null; then
        echo "$name: round-trip FAILED, not patching" >&2
        exit 1
    fi

    "$@" "$tree"
    $PY "$TOOLS/rcc_repack.py" "$tree" "$RCC/$name" --version "$ver" >/dev/null
    chmod 644 "$RCC/$name"
    echo "patched $name (rcc v$ver)"
}

add_vietnamese()  { $PY "$TOOLS/them_tieng_viet.py" "$1"; }
add_village_tab() { $PY "$TOOLS/va_muc_lang.py" "$1"; }
add_sovereignty() { $PY "$TOOLS/them_hoang_sa_truong_sa.py" "$1"; }
add_province_map() { $PY "$TOOLS/gan_ban_do_34_tinh.py" "$1" "$MAPS/34-tinh"; }

# The mini app list comes from the lang_*.rcc files actually installed, so
# adding a third mini app needs no change here.
register_mini_apps() {
    list="$1/gcompris/src/activities/activities_out.txt"
    [ -f "$list" ] || { echo "no activities_out.txt inside activities.rcc" >&2; exit 1; }
    for rcc in "$RCC"/lang_*.rcc; do
        [ -e "$rcc" ] || continue
        app=$(basename "$rcc" .rcc)
        grep -qx "$app" "$list" || { printf '%s\n' "$app" >> "$list"; echo "  registered $app"; }
    done
}

patch_rcc core.rcc        add_vietnamese
patch_rcc activities.rcc  register_mini_apps
patch_rcc menu.rcc        add_village_tab
patch_rcc geography.rcc   add_sovereignty
patch_rcc geo-country.rcc add_province_map
