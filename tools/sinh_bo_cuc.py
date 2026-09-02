#!/usr/bin/env python3
"""Sinh sẵn các bố cục xếp hình trên thẻ tròn, không hình nào đè hình nào.

SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
SPDX-License-Identifier: GPL-3.0-or-later

Toạ độ tính trong ĐĨA ĐƠN VỊ: tâm thẻ (0, 0), mép thẻ bán kính 1. QML nhân với
bán kính thẻ thật để ra pixel, nên bố cục dùng được cho mọi cỡ màn.

Sinh lúc dựng thay vì lúc chạy: bất biến "không đè nhau" kiểm được bằng pytest,
và máy thật khỏi chạy vòng thử-và-sai giữa buổi chơi.

    sinh_bo_cuc.py <thư_mục_ra>
"""
import json
import math
import os
import random
import sys
from itertools import combinations

GIEO = 20260902        # gieo cố định để lần dựng nào cũng ra bộ bố cục y hệt
SO_BO_CUC = 24
KHE = 0.012

# (số hình ở vòng trong, bán kính gốc) — dò bằng thực nghiệm, 40/40 lần đạt
CAU_HINH = {6: (1, 0.255), 8: (2, 0.215)}


def mot_bo_cuc(so_hinh, rng, so_lan=600):
    trong, r_goc = CAU_HINH[so_hinh]
    ngoai = so_hinh - trong
    for _ in range(so_lan):
        diem = []
        for i in range(so_hinh):
            r = r_goc * rng.uniform(0.85, 1.15)
            if i < trong:
                if trong == 1:
                    x = y = 0.0
                else:
                    goc = 2 * math.pi * i / trong + rng.uniform(-0.3, 0.3)
                    x, y = 0.30 * math.cos(goc), 0.30 * math.sin(goc)
                x += rng.uniform(-0.05, 0.05)
                y += rng.uniform(-0.05, 0.05)
            else:
                k = i - trong
                goc = 2 * math.pi * k / ngoai + rng.uniform(-0.15, 0.15)
                bk = (1 - r) * rng.uniform(0.80, 0.95)
                x, y = bk * math.cos(goc), bk * math.sin(goc)
            diem.append((x, y, r))
        roi = any(math.hypot(x1 - x2, y1 - y2) < r1 + r2 + KHE
                  for (x1, y1, r1), (x2, y2, r2) in combinations(diem, 2))
        tran = any(math.hypot(x, y) + r > 1.0 for x, y, r in diem)
        if not roi and not tran:
            return [[round(x, 5), round(y, 5), round(r, 5)] for x, y, r in diem]
    return None


def sinh(ra):
    rng = random.Random(GIEO)
    ket = {}
    for so_hinh in sorted(CAU_HINH):
        ds = []
        while len(ds) < SO_BO_CUC:
            b = mot_bo_cuc(so_hinh, rng)
            if b is None:
                raise SystemExit(f"không dựng nổi bố cục {so_hinh} hình — "
                                 f"giảm bán kính gốc trong CAU_HINH")
            if b not in ds:
                ds.append(b)
        ket[str(so_hinh)] = ds
    with open(os.path.join(ra, "bo_cuc.json"), "w", encoding="utf-8") as f:
        json.dump(ket, f, ensure_ascii=False, indent=1)
    return ket


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    k = sinh(sys.argv[1])
    for so, ds in k.items():
        print(f"{so} hình: {len(ds)} bố cục")


if __name__ == "__main__":
    main()
