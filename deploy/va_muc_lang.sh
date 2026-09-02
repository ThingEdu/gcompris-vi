#!/bin/bash
# Thêm mục "Làng Maker" vào hàng biểu tượng đầu màn hình chính.
#
#   va_muc_lang.sh <đường/dẫn/menu.rcc>
#
#   scp neo@<ip>:/usr/share/gcompris-qt/rcc/menu.rcc /tmp/
#   ./deploy/va_muc_lang.sh /tmp/menu.rcc
#   scp /tmp/menu-vi.rcc neo@<ip>:/tmp/
#   ssh neo@<ip> 'sudo cp -n /usr/share/gcompris-qt/rcc/menu.rcc{,.orig}; \
#                 sudo cp /tmp/menu-vi.rcc /usr/share/gcompris-qt/rcc/menu.rcc'
#
# Biểu tượng của mục lấy từ lang_maker.rcc nên phải cài mini app trước.
set -e
HERE="$(cd "$(dirname "$0")/.." && pwd)"
PY="$HERE/.venv/bin/python"; [ -x "$PY" ] || PY=python3
RCC="${1:?thiếu đường dẫn menu.rcc}"
OUT="$(dirname "$RCC")/menu-vi.rcc"
VER=$("$PY" -c "import struct,sys;print(struct.unpack_from('>I',open(sys.argv[1],'rb').read(),4)[0])" "$RCC")
WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT

"$PY" "$HERE/tools/rcc_extract.py" "$RCC" "$WORK/x"
"$PY" "$HERE/tools/rcc_repack.py" "$WORK/x" "$WORK/rt.rcc" --version "$VER" >/dev/null
"$PY" "$HERE/tools/rcc_extract.py" "$WORK/rt.rcc" "$WORK/rt" >/dev/null
diff -r "$WORK/x" "$WORK/rt" >/dev/null && echo "khứ hồi ĐẠT" || { echo "khứ hồi HỎNG, dừng"; exit 1; }

"$PY" "$HERE/tools/va_muc_lang.py" "$WORK/x"
"$PY" "$HERE/tools/rcc_repack.py" "$WORK/x" "$OUT" --version "$VER"
echo "Xong: $OUT"
