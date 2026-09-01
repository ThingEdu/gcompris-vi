#!/bin/bash
# Dựng gcompris_qt_vi.qm đúng như cách GCompris tự dựng (cmake/translation.cmake):
#   msgattrib --no-obsolete  ->  lconvert po->ts  ->  lrelease -removeidentical -nounfinished
set -e
cd "$(dirname "$0")/.."
PO=${1:-po/gcompris_qt.po}
OUT=${2:-build/gcompris_qt_vi.qm}
mkdir -p build tmp
msgattrib --no-obsolete "$PO" -o tmp/gcompris_qt_vi.ts
lconvert -if po -of ts -i tmp/gcompris_qt_vi.ts -o tmp/gcompris_qt_vi.ts
lrelease -removeidentical -nounfinished tmp/gcompris_qt_vi.ts -qm "$OUT"
ls -la "$OUT"
