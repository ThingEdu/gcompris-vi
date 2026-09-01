"""Kiểm bộ bản đồ 34 tỉnh thành ở maps/34-tinh/.

Điều cần bảo đảm: toạ độ x,y ghi trong board19_0.qml phải đặt đúng mảnh vào
chỗ của nó trên nền. GCompris đặt mảnh theo Babymatch.qml:

    x = posX * bề_rộng_nền - bề_rộng_mảnh / 2

nên posX phải bằng tâm khung bao của mảnh chia cho bề rộng nền. Bài kiểm này
tính ngược từ chính tệp .svgz (transform translate + width/height) rồi đối
chiếu với con số trong board.
"""
import gzip
import os
import re

import pytest

GOC = os.path.join(os.path.dirname(__file__), "..", "maps", "34-tinh")
NEN_W, NEN_H = 504.0, 520.0
SO_TINH = 34


def doc_board(duong_dan=None):
    src = open(duong_dan or os.path.join(GOC, "board19_0.qml"), encoding="utf-8").read()
    return src, re.findall(
        r'"pixmapfile" : "(vietnam/[^"]+)",\n[^\n]*\n\s*"toolTipText" : qsTr\("([^"]+)"\),'
        r'\n\s*"x" : "([\d.]+)",\n\s*"y" : "([\d.]+)"', src)


def khung_bao(tep):
    d = gzip.open(os.path.join(GOC, tep)).read().decode("utf-8")
    w, h = (float(v) for v in re.search(r'width="([\d.]+)" height="([\d.]+)"', d).groups())
    tx, ty = (float(v) for v in re.search(r'translate\(([-\d.]+) ([-\d.]+)\)', d).groups())
    return -tx, -ty, w, h


def test_du_mot_nen_va_34_manh():
    tep = [t for t in os.listdir(os.path.join(GOC, "vietnam")) if t.endswith(".svgz")]
    assert len(tep) == SO_TINH + 1
    assert "vietnam.svgz" in tep


def test_board_liet_ke_du_34_manh():
    _, muc = doc_board()
    assert len(muc) == SO_TINH


def test_nen_khai_bao_dung_kich_thuoc_khung():
    d = gzip.open(os.path.join(GOC, "vietnam/vietnam.svgz")).read().decode("utf-8")
    w, h = (float(v) for v in re.search(r'width="([\d.]+)" height="([\d.]+)"', d).groups())
    assert (w, h) == (NEN_W, NEN_H)


@pytest.mark.parametrize("tep,ten,x,y", doc_board()[1])
def test_toa_do_khop_khung_bao_cua_manh(tep, ten, x, y):
    mx, my, w, h = khung_bao(tep)
    # sai số 0,0001 là chỗ làm tròn 4 chữ số khi ghi board
    assert abs(float(x) - (mx + w / 2) / NEN_W) < 1e-4, ten
    assert abs(float(y) - (my + h / 2) / NEN_H) < 1e-4, ten


def test_manh_nam_gon_trong_khung_nen():
    for tep, ten, _, _ in doc_board()[1]:
        mx, my, w, h = khung_bao(tep)
        assert 0 <= mx and mx + w <= NEN_W, ten
        assert 0 <= my and my + h <= NEN_H, ten


def test_khong_manh_nao_chiem_qua_nua_ban_do():
    # quần đảo nằm ở lớp nền chứ không nhập vào mảnh; nếu lỡ nhập thì mảnh
    # Đà Nẵng và Khánh Hòa phình ra quá nửa bản đồ, trẻ không kéo thả nổi
    for tep, ten, _, _ in doc_board()[1]:
        _, _, w, h = khung_bao(tep)
        assert w < NEN_W / 2 and h < NEN_H / 2, f"{ten} to {w:.0f}x{h:.0f}"


def test_ten_khong_trung_va_co_hai_quan_dao():
    _, muc = doc_board()
    ten = [m[1] for m in muc]
    assert len(set(ten)) == SO_TINH
    assert "Đà Nẵng (quản lý quần đảo Hoàng Sa)" in ten
    assert "Khánh Hòa (quản lý quần đảo Trường Sa)" in ten


def test_nen_co_ve_hai_quan_dao():
    # chấm đảo nằm ở phía đông kinh tuyến 111, tức x > 290 trên khung 504
    d = gzip.open(os.path.join(GOC, "vietnam/vietnam.svgz")).read().decode("utf-8")
    x = [float(m) for m in re.findall(r'[ML](\d+\.\d+) ', d)]
    assert max(x) > 450, "thiếu Trường Sa ở phía đông nền"
    assert sum(1 for v in x if v > 290) > 100, "nền không có đủ chấm quần đảo"
