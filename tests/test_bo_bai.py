"""Kiểm bộ bài Dobble sinh từ mặt phẳng xạ ảnh hữu hạn.

Bất biến của cả trò chơi: HAI THẺ BẤT KỲ TRÙNG ĐÚNG MỘT HÌNH. Hỏng bất biến
này thì trò chơi vô nghĩa — có lượt không ai gọi được, hoặc có lượt gọi kiểu
gì cũng đúng. Vì vậy kiểm ở đây, lúc dựng, chứ không kiểm lúc chạy trên máy.

SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
SPDX-License-Identifier: GPL-3.0-or-later
"""
from collections import Counter
from itertools import combinations

import pytest

from tools.sinh_bo_bai import sinh_bo_bai

CAP = [(5, 31, 6), (7, 57, 8)]


@pytest.mark.parametrize("q,so_the,moi_the", CAP)
def test_dung_so_the_va_so_hinh(q, so_the, moi_the):
    bai = sinh_bo_bai(q)
    assert len(bai) == so_the
    assert all(len(t) == moi_the for t in bai)


@pytest.mark.parametrize("q,so_the,moi_the", CAP)
def test_moi_cap_the_trung_dung_mot_hinh(q, so_the, moi_the):
    bai = sinh_bo_bai(q)
    sai = [(a, b) for a, b in combinations(range(len(bai)), 2)
           if len(set(bai[a]) & set(bai[b])) != 1]
    assert sai == []


@pytest.mark.parametrize("q,so_the,moi_the", CAP)
def test_moi_hinh_xuat_hien_dung_so_lan(q, so_the, moi_the):
    bai = sinh_bo_bai(q)
    dem = Counter(h for t in bai for h in t)
    assert set(dem.values()) == {moi_the}


@pytest.mark.parametrize("q,so_the,moi_the", CAP)
def test_khong_the_nao_co_hinh_lap(q, so_the, moi_the):
    bai = sinh_bo_bai(q)
    assert all(len(set(t)) == len(t) for t in bai)


@pytest.mark.parametrize("q,so_the,moi_the", CAP)
def test_dung_dung_cac_hinh_tu_0_den_n_tru_1(q, so_the, moi_the):
    bai = sinh_bo_bai(q)
    assert set(h for t in bai for h in t) == set(range(so_the))


def test_bo_de_chi_dung_hinh_01_den_31():
    """Cấp Dễ dùng hình số 01-31 của bộ gốc: trọn nhóm A + trọn nhóm B +
    chín hình đầu nhóm C. Chỉ số 0-based nên là 0..30."""
    bai = sinh_bo_bai(5)
    assert max(h for t in bai for h in t) == 30


def test_tu_choi_bac_khong_phai_so_nguyen_to():
    with pytest.raises(ValueError):
        sinh_bo_bai(6)
