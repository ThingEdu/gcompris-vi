"""Kiểm dữ liệu điểm chạm của các mini app Làng Maker.

Điểm chạm là hình tròn đặt trên bức tranh nền: tâm (x, y) tính theo phần của
bề rộng và chiều cao ảnh, bán kính r tính theo phần của BỀ RỘNG ảnh. Hai chỗ
sai hay gặp:

1. Điểm nằm tràn ra ngoài mép tranh — trẻ không chạm tới được.
2. Hai điểm chồng lên nhau — chạm vào chỗ này lại tính thành chỗ kia. Khi so
   khoảng cách phải quy cả hai trục về ĐƠN VỊ BỀ RỘNG, vì y tính theo chiều
   cao mà ảnh không vuông; quên đổi thì bài kiểm bỏ lọt chồng lấn thật.
"""
import os
import re

import pytest

GOC = os.path.join(os.path.dirname(__file__), "..", "mini-app")
APP = "lang_maker"
TI_LE_ANH = 512.0 / 286.0        # bề rộng chia chiều cao của tranh nền


def doc_diem(ten_app=APP):
    js = open(os.path.join(GOC, ten_app, "gcompris/src/activities", ten_app,
                           ten_app + ".js"), encoding="utf-8").read()
    khoi = js[js.index("var noiChon"):js.index("var soCap")]
    diem = re.findall(
        r'\{\s*ma:\s*"([^"]+)",\s*ten:\s*"([^"]+)",\s*mo:\s*"([^"]+)",\s*'
        r'x:\s*([\d.]+),\s*y:\s*([\d.]+),\s*r:\s*([\d.]+)\s*\}', khoi, re.S)
    return [(ma, ten, mo, float(x), float(y), float(r))
            for ma, ten, mo, x, y, r in diem]


DIEM = doc_diem()


def test_doc_du_muoi_hai_diem():
    assert len(DIEM) == 12


def test_ma_khong_trung():
    ma = [d[0] for d in DIEM]
    assert len(set(ma)) == len(ma)


def test_ten_khong_trung_va_khong_rong():
    ten = [d[1] for d in DIEM]
    assert len(set(ten)) == len(ten)
    assert all(t.strip() for t in ten)


@pytest.mark.parametrize("ma,ten,mo,x,y,r", DIEM)
def test_diem_nam_gon_trong_tranh(ma, ten, mo, x, y, r):
    ry = r * TI_LE_ANH          # bán kính quy về đơn vị chiều cao
    assert 0 <= x - r and x + r <= 1, ma
    assert 0 <= y - ry and y + ry <= 1, ma


@pytest.mark.parametrize("ma,ten,mo,x,y,r", DIEM)
def test_moi_diem_co_loi_mo_ta_ket_thuc_bang_dau_cham(ma, ten, mo, x, y, r):
    # cấp 3 ghép "Cáo đố: " + mô tả + " Đó là chỗ nào?" nên mô tả phải trọn câu
    assert mo.endswith("."), ma
    assert len(mo) >= 20, ma


def test_khong_hai_diem_nao_chong_nhau():
    xau = []
    for i, a in enumerate(DIEM):
        for b in DIEM[i + 1:]:
            dx = a[3] - b[3]
            dy = (a[4] - b[4]) / TI_LE_ANH   # quy y về đơn vị bề rộng
            kc = (dx * dx + dy * dy) ** 0.5
            if kc < a[5] + b[5]:
                xau.append(f"{a[0]} ↔ {b[0]} (cách {kc:.3f} < {a[5] + b[5]:.3f})")
    assert xau == [], "; ".join(xau)


def test_ban_kinh_du_to_de_tre_cham_trung():
    # dưới 0,03 bề rộng thì trên màn hình 1920 chỉ còn ~45 px, ngón tay khó trúng
    nho = [d[0] for d in DIEM if d[5] < 0.03]
    assert nho == [], nho


def test_co_du_tep_cua_hoat_dong():
    tm = os.path.join(GOC, APP, "gcompris/src/activities", APP)
    for tep in ["ActivityInfo.qml", "Lang_maker.qml", "lang_maker.js",
                "resource/lang-maker.png"]:
        assert os.path.exists(os.path.join(tm, tep)), tep


def test_nhan_vat_dung_chung_khong_kem_co_hay_logo():
    svg = open(os.path.join(GOC, "chung", "neo_tre.svg"), encoding="utf-8").read()
    assert "<text" not in svg, "nhân vật dùng chung không được có chữ hay logo"
    assert "image" not in svg, "nhân vật dùng chung phải là hình vẽ, không nhúng ảnh"
