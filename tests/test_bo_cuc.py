"""Kiểm bố cục xếp hình trên thẻ tròn.

SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
SPDX-License-Identifier: GPL-3.0-or-later

Xếp hình lúc DỰNG chứ không lúc chạy: nhờ vậy bất biến "không hai hình nào đè
nhau" kiểm được bằng pytest, và máy thật không phải chạy vòng lặp thử-và-sai
giữa buổi chơi. QML chỉ chọn ngẫu nhiên một bố cục rồi xoay từng hình quanh
tâm của chính nó — xoay không đổi đường tròn bao nên bất biến vẫn còn.
"""
import json
import math
import os
from itertools import combinations

import pytest

GOC = os.path.join(os.path.dirname(__file__), "..")
RA = os.path.join(GOC, "mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/resource")

KHE = 0.012        # khe hở tối thiểu giữa hai hình, theo bán kính thẻ


@pytest.fixture(scope="module")
def bo_cuc():
    with open(os.path.join(RA, "bo_cuc.json"), encoding="utf-8") as f:
        return json.load(f)


def test_co_du_hai_cap(bo_cuc):
    assert set(bo_cuc) == {"6", "8"}


def test_moi_cap_co_it_nhat_20_bo_cuc(bo_cuc):
    for so, ds in bo_cuc.items():
        assert len(ds) >= 20, f"cấp {so} chỉ có {len(ds)} bố cục"


def test_moi_bo_cuc_dung_so_hinh(bo_cuc):
    for so, ds in bo_cuc.items():
        assert all(len(b) == int(so) for b in ds)


def test_khong_hai_hinh_nao_de_nhau(bo_cuc):
    for so, ds in bo_cuc.items():
        for i, b in enumerate(ds):
            for (x1, y1, r1), (x2, y2, r2) in combinations(b, 2):
                d = math.hypot(x1 - x2, y1 - y2)
                assert d >= r1 + r2 + KHE, f"cấp {so} bố cục {i}: đè nhau"


def test_moi_hinh_nam_tron_trong_the(bo_cuc):
    for so, ds in bo_cuc.items():
        for i, b in enumerate(ds):
            for x, y, r in b:
                assert math.hypot(x, y) + r <= 1.0, f"cấp {so} bố cục {i}: tràn mép"


def test_co_lech_co_giua_cac_hinh(bo_cuc):
    """Giống thẻ giấy: hình to nhỏ lệch nhau, không đều tăm tắp."""
    for so, ds in bo_cuc.items():
        for b in ds:
            bk = [r for _, _, r in b]
            assert max(bk) / min(bk) > 1.05


def test_lech_co_khong_qua_15_phan_tram(bo_cuc):
    for so, ds in bo_cuc.items():
        for b in ds:
            bk = [r for _, _, r in b]
            assert max(bk) / min(bk) <= 1.15 / 0.85 + 1e-9


def test_cac_bo_cuc_khac_nhau(bo_cuc):
    for so, ds in bo_cuc.items():
        khoa = {json.dumps(b) for b in ds}
        assert len(khoa) == len(ds)
