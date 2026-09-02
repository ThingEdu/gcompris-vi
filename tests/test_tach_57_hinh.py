"""Kiểm 57 hình bung ra từ tệp HTML nguồn.

Bẫy lớn nhất: Qt5 trong GCompris 3.1 dựng SVG theo chuẩn SVG Tiny 1.2, KHÔNG
hiểu `fill="currentColor"` lẫn `stroke="var(--vang)"` — mà bộ hình gốc dùng cả
hai. Không thay hết thành mã hex thì hình ra trắng trơn trên máy thật, mà trên
trình duyệt lại nhìn vẫn đẹp. Vì vậy phải kiểm ở đây.

SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
SPDX-License-Identifier: GPL-3.0-or-later
"""
import json
import os
import re
import xml.etree.ElementTree as ET

import pytest

GOC = os.path.join(os.path.dirname(__file__), "..")
RA = os.path.join(GOC, "mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/resource")
THU_MUC_HINH = os.path.join(RA, "hinh")

MAU_HOP_LE = {
    "#C4231F", "#E8A317", "#1F7A52", "#2B57A6",
    "#6B3FA0", "#8A4B24", "#12958E", "#3A3A3A",
    "#FBF8F1", "#141414",
}
NHOM_HOP_LE = set("ABCDE")


@pytest.fixture(scope="module")
def danh_muc():
    with open(os.path.join(RA, "hinh.json"), encoding="utf-8") as f:
        return json.load(f)


def tep_svg():
    return sorted(t for t in os.listdir(THU_MUC_HINH) if t.endswith(".svg"))


def test_du_57_tep_svg():
    assert len(tep_svg()) == 57


def test_moi_tep_svg_doc_duoc_bang_bo_doc_xml():
    for t in tep_svg():
        ET.parse(os.path.join(THU_MUC_HINH, t))


def test_khong_con_bien_css_hay_currentcolor():
    hong = []
    for t in tep_svg():
        noi_dung = open(os.path.join(THU_MUC_HINH, t), encoding="utf-8").read()
        if "var(--" in noi_dung or "currentColor" in noi_dung:
            hong.append(t)
    assert hong == []


def test_moi_ma_mau_nam_trong_bang_da_biet():
    la = {}
    for t in tep_svg():
        noi_dung = open(os.path.join(THU_MUC_HINH, t), encoding="utf-8").read()
        for m in re.findall(r"#[0-9A-Fa-f]{6}", noi_dung):
            if m.upper() not in MAU_HOP_LE:
                la.setdefault(t, set()).add(m)
    assert la == {}


def test_danh_muc_du_57_muc(danh_muc):
    assert len(danh_muc) == 57


def test_danh_muc_khong_trung_ma_khong_trung_ten(danh_muc):
    ma = [h["ma"] for h in danh_muc]
    ten = [h["ten"] for h in danh_muc]
    assert len(set(ma)) == 57
    assert len(set(ten)) == 57


def test_danh_muc_du_truong_va_nhom_hop_le(danh_muc):
    for h in danh_muc:
        assert set(h) == {"so", "ma", "ten", "nhom", "mau", "nghia"}
        assert h["nhom"] in NHOM_HOP_LE
        assert h["mau"].upper() in MAU_HOP_LE
        assert h["ten"].strip()


def test_so_chay_lien_tuc_tu_1_den_57(danh_muc):
    assert [h["so"] for h in danh_muc] == list(range(1, 58))


def test_moi_muc_danh_muc_co_dung_mot_tep_svg(danh_muc):
    co = set(tep_svg())
    thieu = [h for h in danh_muc
             if f"{h['so']:02d}-{h['ma']}.svg" not in co]
    assert thieu == []


def test_dung_so_luong_tung_nhom(danh_muc):
    from collections import Counter
    assert Counter(h["nhom"] for h in danh_muc) == {
        "A": 10, "B": 12, "C": 12, "D": 11, "E": 12}


def test_ma_khong_dau_va_khong_khoang_trang(danh_muc):
    for h in danh_muc:
        assert re.fullmatch(r"[a-z0-9_]+", h["ma"]), h["ma"]
