#!/bin/bash
# Thêm bản đồ hành chính 34 tỉnh thành Việt Nam vào hoạt động "Tìm vùng trên
# bản đồ" (geo-country) của GCompris. Bản đồ vào bộ "Các nước châu Á".
#
#   va_ban_do_34_tinh.sh <đường/dẫn/geo-country.rcc>
#
#   scp neo@<ip>:/usr/share/gcompris-qt/rcc/geo-country.rcc /tmp/
#   ./deploy/va_ban_do_34_tinh.sh /tmp/geo-country.rcc
#   scp /tmp/geo-country-vi.rcc neo@<ip>:/tmp/
#   ssh neo@<ip> 'sudo cp -n /usr/share/gcompris-qt/rcc/geo-country.rcc{,.orig}; \
#                 sudo cp /tmp/geo-country-vi.rcc /usr/share/gcompris-qt/rcc/geo-country.rcc'
set -e
HERE="$(cd "$(dirname "$0")/.." && pwd)"
PY="$HERE/.venv/bin/python"; [ -x "$PY" ] || PY=python3
RCC="${1:?thiếu đường dẫn geo-country.rcc}"
OUT="$(dirname "$RCC")/geo-country-vi.rcc"
VER=$("$PY" -c "import struct,sys;print(struct.unpack_from('>I',open(sys.argv[1],'rb').read(),4)[0])" "$RCC")
WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT

"$PY" "$HERE/tools/rcc_extract.py" "$RCC" "$WORK/x"
# kiểm khứ hồi trước khi sửa: đóng lại y nguyên rồi bung ra phải khớp từng byte
"$PY" "$HERE/tools/rcc_repack.py" "$WORK/x" "$WORK/rt.rcc" --version "$VER" >/dev/null
"$PY" "$HERE/tools/rcc_extract.py" "$WORK/rt.rcc" "$WORK/rt" >/dev/null
diff -r "$WORK/x" "$WORK/rt" >/dev/null && echo "khứ hồi ĐẠT" || { echo "khứ hồi HỎNG, dừng"; exit 1; }

"$PY" "$HERE/tools/gan_ban_do_34_tinh.py" "$WORK/x"
"$PY" "$HERE/tools/rcc_repack.py" "$WORK/x" "$OUT" --version "$VER"
echo "Xong: $OUT"
