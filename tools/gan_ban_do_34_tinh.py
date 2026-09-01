#!/usr/bin/env python3
"""Gắn bộ bản đồ 34 tỉnh thành Việt Nam vào cây tệp đã bung từ geo-country.rcc.

Chỉ dùng thư viện chuẩn để chạy được ở mọi nơi, kể cả trên NEO One.
Tài nguyên do tools/tao_ban_do_34_tinh.py sinh sẵn, nằm ở maps/34-tinh/.

    gan_ban_do_34_tinh.py <thư_mục_đã_bung> [thư_mục_tài_nguyên]
"""
import os
import re
import shutil
import sys

BOARD = "board19_0.qml"
DK = ('        ],\n        [\n            //Vietnam\n'
      '            "qrc:/gcompris/src/activities/geo-country/resource/board/'
      + BOARD + '"\n        ]\n    ]')


def main():
    if not 2 <= len(sys.argv) <= 3:
        raise SystemExit(__doc__)
    goc = sys.argv[1]
    tn = sys.argv[2] if len(sys.argv) == 3 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "maps", "34-tinh")
    res = os.path.join(goc, "gcompris/src/activities/geo-country/resource")
    if not os.path.isdir(res):
        raise SystemExit(f"không thấy {res} — đây có phải cây bung từ geo-country.rcc?")

    nguon = os.path.join(tn, "vietnam")
    dich = os.path.join(res, "vietnam")
    os.makedirs(dich, exist_ok=True)
    n = 0
    for tep in sorted(os.listdir(nguon)):
        if tep.endswith(".svgz"):
            shutil.copy2(os.path.join(nguon, tep), os.path.join(dich, tep))
            n += 1
    print(f"chép {n} tệp bản đồ vào {dich}")
    if n != 35:
        raise SystemExit(f"phải có 1 nền + 34 mảnh, đang có {n}")

    shutil.copy2(os.path.join(tn, BOARD), os.path.join(res, "board", BOARD))
    print(f"chép {BOARD}")

    dt = os.path.join(res, "2/Data.qml")          # bộ "Các nước châu Á"
    src = open(dt, encoding="utf-8").read()
    if BOARD.split(".")[0] in src:
        print("2/Data.qml đã có Việt Nam, bỏ qua")
        return
    m = re.search(r"\n        \]\n    \]", src)
    if not m:
        raise SystemExit("không nhận ra cấu trúc 2/Data.qml")
    open(dt, "w", encoding="utf-8").write(src[:m.start()] + "\n" + DK + src[m.end():])
    print(f"đăng ký Việt Nam vào {dt}")


if __name__ == "__main__":
    main()
