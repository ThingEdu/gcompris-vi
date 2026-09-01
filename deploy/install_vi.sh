#!/bin/bash
# Cài tiếng Việt vào một bản GCompris đã cài sẵn, không cần biên dịch lại.
#
#   install_vi.sh <thư_mục_chứa_rcc_và_translations> [file.qm]
#
# Ví dụ macOS: install_vi.sh /Applications/gcompris-qt.app/Contents/Resources
# Ví dụ Linux: install_vi.sh /usr/share/GCompris
#
# Làm hai việc:
#   1. Chép file .qm tiếng Việt vào thư mục translations, đặt tên theo đúng
#      quy ước của bản GCompris đó.
#   2. Vá LanguageList.qml bên trong core.rcc để thêm mục "Tiếng Việt" —
#      nếu không, GCompris sẽ từ chối locale vi_VN và quay về ngôn ngữ hệ thống.
set -e
HERE="$(cd "$(dirname "$0")/.." && pwd)"
PY="$HERE/.venv/bin/python"
[ -x "$PY" ] || PY=python3

ROOT="${1:?thiếu thư mục GCompris}"
QM="${2:-$HERE/build/gcompris_qt_vi.qm}"
TRANS="$ROOT/translations"
CORE="$ROOT/rcc/core.rcc"

[ -f "$QM" ] || { echo "Chưa có $QM — chạy tools/build_qm.sh trước."; exit 1; }
[ -d "$TRANS" ] || { echo "Không thấy $TRANS"; exit 1; }
[ -f "$CORE" ] || { echo "Không thấy $CORE"; exit 1; }

# 1. Đặt tên .qm theo quy ước của bản đang cài
if ls "$TRANS"/gcompris_qt_*.qm >/dev/null 2>&1; then
    NAME=gcompris_qt_vi.qm
else
    NAME=gcompris_vi.qm
fi
cp "$QM" "$TRANS/$NAME"
echo "→ $TRANS/$NAME"

# 2. Vá core.rcc
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
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
# chèn ngay sau mục "system" đầu danh sách
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
echo "Xong. Bản gốc được giữ ở $CORE.orig"
