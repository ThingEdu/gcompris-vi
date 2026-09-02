#!/usr/bin/env python3
"""Bung 57 hình của Làng Maker khỏi tệp HTML một trang thành SVG rời.

Bẫy phải xử lý: Qt5 dựng SVG theo chuẩn SVG Tiny 1.2, không hiểu hai thứ mà
bộ hình gốc dùng:

  fill="currentColor"     màu thân hình, thừa hưởng từ class c-luc, c-son… của thẻ
  stroke="var(--vang)"    biến CSS của trình duyệt

Cả hai phải thay thành mã hex thật, nếu không hình ra trắng trơn trên máy thật
mà xem trên trình duyệt vẫn thấy đẹp.

    tach_57_hinh.py <tệp_html> <thư_mục_ra>

SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
SPDX-License-Identifier: GPL-3.0-or-later
"""
import json
import os
import re
import sys
import unicodedata

MAU = {
    "son": "#C4231F", "vang": "#E8A317", "luc": "#1F7A52", "lam": "#2B57A6",
    "tim": "#6B3FA0", "gian": "#8A4B24", "ngoc": "#12958E", "then": "#3A3A3A",
}
NHOM_THEO_SO = [("A", 1, 10), ("B", 11, 22), ("C", 23, 34),
                ("D", 35, 45), ("E", 46, 57)]

THE = re.compile(
    r'<div class="card c-(?P<mau>[\w-]+)"><span class="num">(?P<so>\d+)</span>\s*'
    r'(?P<svg><svg.*?</svg>)\s*'
    r'<div class="nm">(?P<ten>.*?)</div><div class="vi">(?P<nghia>.*?)</div>',
    re.S)


def khong_dau(s):
    """"Bảng đen & phấn" -> "bang_den_phan". Chỉ dùng cho tên tệp và mã."""
    s = s.replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_").lower()
    return s


def nhom_cua(so):
    for ten, dau, cuoi in NHOM_THEO_SO:
        if dau <= so <= cuoi:
            return ten
    raise ValueError(f"hình số {so} không thuộc nhóm nào")


def go_html(s):
    return (s.replace("&amp;", "&").replace("&lt;", "<")
             .replace("&gt;", ">").replace("&quot;", '"').strip())


def sua_mau(svg, mau_than):
    """Thay currentColor và var(--x) bằng mã hex thật."""
    svg = svg.replace("currentColor", mau_than)
    def thay(m):
        ten = m.group(1)
        if ten not in MAU:
            raise ValueError(f"biến màu lạ: var(--{ten})")
        return MAU[ten]
    return re.sub(r"var\(--([\w-]+)\)", thay, svg)


def tach(html, ra):
    thu_muc_hinh = os.path.join(ra, "hinh")
    os.makedirs(thu_muc_hinh, exist_ok=True)
    noi_dung = open(html, encoding="utf-8").read()

    danh_muc = []
    for m in THE.finditer(noi_dung):
        so = int(m.group("so"))
        ten = go_html(m.group("ten"))
        ma = khong_dau(ten)
        mau_than = MAU[m.group("mau")]
        svg = sua_mau(m.group("svg"), mau_than)
        if "var(--" in svg or "currentColor" in svg:
            raise ValueError(f"hình {so:02d} còn sót màu chưa thay")
        ten_tep = f"{so:02d}-{ma}.svg"
        with open(os.path.join(thu_muc_hinh, ten_tep), "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n' + svg + "\n")
        danh_muc.append({"so": so, "ma": ma, "ten": ten, "nhom": nhom_cua(so),
                         "mau": mau_than, "nghia": go_html(m.group("nghia"))})

    if len(danh_muc) != 57:
        raise SystemExit(f"chỉ tách được {len(danh_muc)} hình, phải đủ 57")
    danh_muc.sort(key=lambda h: h["so"])
    with open(os.path.join(ra, "hinh.json"), "w", encoding="utf-8") as f:
        json.dump(danh_muc, f, ensure_ascii=False, indent=1)
    return danh_muc


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    d = tach(sys.argv[1], sys.argv[2])
    print(f"tách được {len(d)} hình")


if __name__ == "__main__":
    main()
