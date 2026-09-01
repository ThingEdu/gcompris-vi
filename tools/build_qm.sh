#!/bin/bash
# Dựng gcompris_qt_vi.qm đúng như cách GCompris tự dựng (cmake/translation.cmake):
#   msgattrib --no-obsolete  ->  lconvert po->ts  ->  lrelease -removeidentical -nounfinished
set -e
cd "$(dirname "$0")/.."
PO=${1:-po/gcompris_qt.po}
OUT=${2:-build/gcompris_qt_vi.qm}
OLD=po/gcompris_qt_doi-cu.po
mkdir -p build tmp
msgattrib --no-obsolete "$PO" -o tmp/moi.ts
lconvert -if po -of ts -i tmp/moi.ts -o tmp/moi.ts
# Catalog cho các đời GCompris cũ (3.x, 4.x): những chuỗi đã bị đổi lời ở bản 26.1
# nhưng máy đang chạy bản cũ vẫn dùng. Gộp vào cùng một .qm.
if [ -f "$OLD" ]; then
    msgattrib --no-obsolete "$OLD" -o tmp/cu.ts
    lconvert -if po -of ts -i tmp/cu.ts -o tmp/cu.ts
    lconvert -i tmp/moi.ts tmp/cu.ts -o tmp/gcompris_qt_vi.ts
else
    cp tmp/moi.ts tmp/gcompris_qt_vi.ts
fi
lrelease -removeidentical -nounfinished tmp/gcompris_qt_vi.ts -qm "$OUT"
ls -la "$OUT"
