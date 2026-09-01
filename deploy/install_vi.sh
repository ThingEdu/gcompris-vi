#!/bin/bash
# Cài tiếng Việt vào một bản GCompris đã cài sẵn — KHÔNG cần biên dịch lại.
# Đích chính: NEO One (Linux ARM64). Bản macOS chỉ dùng để thử nghiệm.
#
#   install_vi.sh [--root <thư_mục_dữ_liệu_GCompris>] [--format ogg|aac]
#
# Trên NEO One thường là:  install_vi.sh --root /usr/share/GCompris
# Nếu không có quyền ghi vào /usr/share, kho giọng vẫn cài được vào
# ~/.cache/gcompris-qt — GCompris tìm ở đó nữa.
#
# Ba việc:
#   1. Chép .qm tiếng Việt vào thư mục translations (đặt tên theo bản đang cài).
#   2. Vá LanguageList.qml trong core.rcc để thêm mục "Tiếng Việt" — thiếu bước
#      này thì GCompris từ chối locale vi_VN và quay về ngôn ngữ hệ thống.
#   3. Cài kho giọng .rcc + tệp Contents vào data3/voices-<format>/.
set -e
HERE="$(cd "$(dirname "$0")/.." && pwd)"
PY="$HERE/.venv/bin/python"
[ -x "$PY" ] || PY=python3

ROOT=""
FMT=ogg
while [ $# -gt 0 ]; do
    case "$1" in
        --root) ROOT="$2"; shift 2 ;;
        --format) FMT="$2"; shift 2 ;;
        *) echo "Tham số lạ: $1"; exit 1 ;;
    esac
done

# Tự dò thư mục dữ liệu nếu không được chỉ định
if [ -z "$ROOT" ]; then
    for c in /usr/share/GCompris /usr/share/gcompris-qt /usr/local/share/GCompris \
             /Applications/gcompris-qt.app/Contents/Resources; do
        [ -d "$c/rcc" ] && ROOT="$c" && break
    done
fi
[ -n "$ROOT" ] || { echo "Không tìm thấy thư mục dữ liệu GCompris, hãy dùng --root"; exit 1; }
echo "Thư mục dữ liệu: $ROOT"

QM="$HERE/build/gcompris_qt_vi.qm"
TRANS="$ROOT/translations"
CORE="$ROOT/rcc/core.rcc"
[ -f "$QM" ] || { echo "Chưa có $QM — chạy tools/build_qm.sh trước."; exit 1; }
[ -f "$CORE" ] || { echo "Không thấy $CORE"; exit 1; }

# --- 1. bản dịch giao diện ---
if [ -d "$TRANS" ]; then
    if ls "$TRANS"/gcompris_qt_*.qm >/dev/null 2>&1; then NAME=gcompris_qt_vi.qm; else NAME=gcompris_vi.qm; fi
    cp "$QM" "$TRANS/$NAME"
    echo "→ $TRANS/$NAME"
else
    # Bản đóng gói kiểu KDE đặt .qm trong /usr/share/locale
    LOC="${ROOT%/share/*}/share/locale/vi/LC_MESSAGES"
    mkdir -p "$LOC"; cp "$QM" "$LOC/gcompris_qt.qm"
    echo "→ $LOC/gcompris_qt.qm"
fi

# --- 2. thêm Tiếng Việt vào danh sách ngôn ngữ ---
WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT
[ -f "$CORE.orig" ] || cp "$CORE" "$CORE.orig"
"$PY" "$HERE/tools/rcc_extract.py" "$CORE.orig" "$WORK/x" >/dev/null
LL=$(find "$WORK/x" -name LanguageList.qml | head -1)
[ -n "$LL" ] || { echo "Không tìm thấy LanguageList.qml trong core.rcc"; exit 1; }
if grep -q 'vi_VN.UTF-8' "$LL"; then
    echo "→ LanguageList.qml đã có tiếng Việt, giữ nguyên"
else
    "$PY" - "$LL" <<'PYEOF'
import re, sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
line = '            { "text": "Tiếng Việt", "locale": "vi_VN.UTF-8" },\n'
m = re.search(r'^.*"locale":\s*"system"\s*\},\n', s, re.M)
if not m:
    sys.exit("không tìm thấy mục 'system' trong LanguageList.qml")
open(p, "w", encoding="utf-8").write(s[:m.end()] + line + s[m.end():])
PYEOF
    echo "→ đã thêm 'Tiếng Việt' vào LanguageList.qml"
fi
VER=$("$PY" - "$CORE.orig" <<'PYEOF'
import struct, sys
print(struct.unpack_from(">I", open(sys.argv[1], "rb").read(), 4)[0])
PYEOF
)
"$PY" "$HERE/tools/rcc_repack.py" "$WORK/x" "$CORE" --version "$VER"

# --- 3. kho giọng ---
SRC="$HERE/build/data3/voices-$FMT"
if [ -d "$SRC" ]; then
    if [ -w "$ROOT/rcc" ]; then
        DST="$ROOT/rcc/data3/voices-$FMT"
    else
        DST="${XDG_CACHE_HOME:-$HOME/.cache}/gcompris-qt/data3/voices-$FMT"
        echo "  (không ghi được vào $ROOT/rcc, dùng thư mục cache của người dùng)"
    fi
    mkdir -p "$DST"; rm -f "$DST"/voices-vi-*.rcc
    cp "$SRC"/Contents "$SRC"/voices-vi-*.rcc "$DST/"
    echo "→ kho giọng ($FMT): $DST"
    echo "  Nhớ đặt enableAutomaticDownloads=false trong gcompris-qt.conf,"
    echo "  nếu không GCompris sẽ tải đè tệp Contents từ cdn.kde.org."
else
    echo "→ bỏ qua kho giọng (chưa có $SRC)"
fi

echo "Xong. Bản core.rcc gốc giữ ở $CORE.orig"
