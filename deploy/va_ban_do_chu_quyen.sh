#!/bin/bash
# Vá bản đồ Việt Nam trong GCompris cho có quần đảo Hoàng Sa và Trường Sa.
#
#   va_ban_do_chu_quyen.sh <đường/dẫn/geography.rcc>
#
# Chạy trên máy CÓ Qt (để dùng lệnh rcc). Với NEO One thì lấy tệp về máy này,
# vá, rồi chép ngược sang.
#
#   scp neo@<ip>:/usr/share/gcompris-qt/rcc/geography.rcc /tmp/
#   ./deploy/va_ban_do_chu_quyen.sh /tmp/geography.rcc
#   scp /tmp/geography-vi.rcc neo@<ip>:/tmp/
#   ssh neo@<ip> 'sudo cp -n /usr/share/gcompris-qt/rcc/geography.rcc{,.orig}; \
#                 sudo cp /tmp/geography-vi.rcc /usr/share/gcompris-qt/rcc/geography.rcc'
set -e
HERE="$(cd "$(dirname "$0")/.." && pwd)"
PY="$HERE/.venv/bin/python"; [ -x "$PY" ] || PY=python3
RCC="${1:?thiếu đường dẫn geography.rcc}"
OUT="$(dirname "$RCC")/geography-vi.rcc"
VER=$("$PY" -c "import struct,sys;print(struct.unpack_from('>I',open(sys.argv[1],'rb').read(),4)[0])" "$RCC")
WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT

"$PY" "$HERE/tools/rcc_extract.py" "$RCC" "$WORK/x"
# kiểm khứ hồi trước khi sửa: đóng lại y nguyên rồi bung ra phải khớp từng byte
"$PY" "$HERE/tools/rcc_repack.py" "$WORK/x" "$WORK/rt.rcc" --version "$VER" >/dev/null
"$PY" "$HERE/tools/rcc_extract.py" "$WORK/rt.rcc" "$WORK/rt" >/dev/null
diff -r "$WORK/x" "$WORK/rt" >/dev/null && echo "khứ hồi ĐẠT" || { echo "khứ hồi HỎNG, dừng"; exit 1; }

"$PY" "$HERE/tools/them_hoang_sa_truong_sa.py" "$WORK/x"
"$PY" "$HERE/tools/rcc_repack.py" "$WORK/x" "$OUT" --version "$VER"
echo "Xong: $OUT"
