#!/bin/bash
# Gắn các mini app của Làng Maker vào một bản GCompris đã cài.
#
#   gan_mini_app.sh <đường/dẫn/activities.rcc> [tên_app ...]
#
# GCompris nạp hoạt động từ .rcc bên ngoài nên KHÔNG cần biên dịch lại. Chỗ duy
# nhất đụng vào phần của GCompris là thêm dòng tên vào activities_out.txt bên
# trong activities.rcc — chạy lại được nhiều lần, không nhân đôi dòng. Nâng đời
# GCompris xong chỉ cần chạy lại lệnh này.
#
#   scp neo@<ip>:/usr/share/gcompris-qt/rcc/activities.rcc /tmp/
#   ./deploy/gan_mini_app.sh /tmp/activities.rcc
#   scp /tmp/activities-vi.rcc /tmp/lang_*.rcc neo@<ip>:/tmp/
#   ssh neo@<ip> 'sudo cp -n /usr/share/gcompris-qt/rcc/activities.rcc{,.orig}; \
#                 sudo cp /tmp/lang_*.rcc /usr/share/gcompris-qt/rcc/; \
#                 sudo cp /tmp/activities-vi.rcc /usr/share/gcompris-qt/rcc/activities.rcc'
set -e
HERE="$(cd "$(dirname "$0")/.." && pwd)"
PY="$HERE/.venv/bin/python"; [ -x "$PY" ] || PY=python3
RCC="${1:?thiếu đường dẫn activities.rcc}"; shift
RA="$(dirname "$RCC")"
OUT="$RA/activities-vi.rcc"
VER=$("$PY" -c "import struct,sys;print(struct.unpack_from('>I',open(sys.argv[1],'rb').read(),4)[0])" "$RCC")
WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT

"$PY" "$HERE/tools/rcc_extract.py" "$RCC" "$WORK/x"
"$PY" "$HERE/tools/rcc_repack.py" "$WORK/x" "$WORK/rt.rcc" --version "$VER" >/dev/null
"$PY" "$HERE/tools/rcc_extract.py" "$WORK/rt.rcc" "$WORK/rt" >/dev/null
diff -r "$WORK/x" "$WORK/rt" >/dev/null && echo "khứ hồi ĐẠT" || { echo "khứ hồi HỎNG, dừng"; exit 1; }

TENS=$("$PY" "$HERE/tools/dong_goi_mini_app.py" "$RA" "$@" | tail -1 | sed 's/^[^:]*: //')
DS="$WORK/x/gcompris/src/activities/activities_out.txt"
for t in $TENS; do
    if grep -qx "$t" "$DS"; then
        echo "$t đã có trong danh sách"
    else
        printf '%s\n' "$t" >> "$DS"
        echo "thêm $t vào activities_out.txt"
    fi
done
"$PY" "$HERE/tools/rcc_repack.py" "$WORK/x" "$OUT" --version "$VER"
echo "Xong: $OUT và $RA/{$(echo $TENS | tr ' ' ',')}.rcc"
