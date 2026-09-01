#!/bin/bash
# Đóng kho giọng tiếng Việt thành .rcc + tệp Contents, đúng cách GCompris chờ đợi.
#   pack_voices.sh [ogg|aac|mp3]
# Kết quả: build/data3/voices-<fmt>/{Contents, voices-vi-<ngày giờ>.rcc}
set -e
cd "$(dirname "$0")/.."
FMT=${1:-ogg}
PY=.venv/bin/python
SRC="build/voices-$FMT"
OUT="build/data3/voices-$FMT"
STAMP=$(date +%Y-%m-%d-%H-%M-%S)
RCC="voices-vi-$STAMP.rcc"

[ -d "$SRC" ] || { echo "Chưa có $SRC — chạy tools/make_voices.py trước."; exit 1; }
mkdir -p "$OUT"
rm -f "$OUT"/voices-vi-*.rcc
$PY tools/rcc_repack.py "$SRC" "$OUT/$RCC" --version 2
( cd "$OUT" && md5 -q "$RCC" | awk -v f="$RCC" '{print $1"  "f}' > Contents )
echo "Contents: $(cat "$OUT/Contents")"
