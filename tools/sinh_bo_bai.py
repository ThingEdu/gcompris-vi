#!/usr/bin/env python3
"""Sinh bộ bài Dobble từ mặt phẳng xạ ảnh hữu hạn bậc q.

Với q là số nguyên tố: số thẻ = số hình = q² + q + 1, mỗi thẻ q + 1 hình, và
hai thẻ bất kỳ trùng ĐÚNG MỘT hình. Bộ 57 hình của làng khớp chính xác bậc 7.

    sinh_bo_bai.py <thư_mục_ra>      # ghi bo_bai_31.json và bo_bai_57.json

Bộ bài tính sẵn rồi nhúng vào .rcc, QML chỉ đọc. Hai lý do: máy NEO One 1,9 GB
không nên tính lúc khởi động, và bất biến trên kiểm được bằng pytest.

SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
SPDX-License-Identifier: GPL-3.0-or-later
"""
import json
import os
import sys

NGUYEN_TO = (2, 3, 5, 7, 11, 13)


def sinh_bo_bai(q):
    """Trả về danh sách thẻ, mỗi thẻ là danh sách chỉ số hình 0-based."""
    if q not in NGUYEN_TO:
        raise ValueError(f"bậc {q} phải là số nguyên tố, đã biết: {NGUYEN_TO}")
    # Thẻ đầu là "đường vô tận": q+1 hình đầu tiên.
    the = [list(range(q + 1))]
    # q thẻ đi qua hình 0.
    for i in range(q):
        the.append([0] + [q + 1 + q * i + j for j in range(q)])
    # q² thẻ còn lại, mỗi thẻ đi qua đúng một hình vô tận 1+i.
    for i in range(q):
        for j in range(q):
            the.append([1 + i] + [q + 1 + q * k + ((i * k + j) % q)
                                  for k in range(q)])
    return the


def ghi_json(q, duong_dan):
    """Ghi bộ bài ra file JSON."""
    bai = sinh_bo_bai(q)
    du_lieu = {"q": q, "so_the": len(bai), "so_hinh_moi_the": q + 1, "the": bai}
    with open(duong_dan, "w", encoding="utf-8") as f:
        json.dump(du_lieu, f, ensure_ascii=False, indent=1)
    return du_lieu


def main():
    """Chương trình chính."""
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    ra = sys.argv[1]
    os.makedirs(ra, exist_ok=True)
    for q in (5, 7):
        d = ghi_json(q, os.path.join(ra, f"bo_bai_{q * q + q + 1}.json"))
        print(f"bậc {q}: {d['so_the']} thẻ × {d['so_hinh_moi_the']} hình")


if __name__ == "__main__":
    main()
