import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from check_po import check_entry


def kinds(msgid, msgstr):
    return sorted(p.kind for p in check_entry(msgid, msgstr))


def test_ban_dich_dung_thi_khong_bao_loi():
    assert kinds("Select the %1 button", "Chọn nút %1") == []


def test_mat_placeholder_bi_bat():
    assert kinds("Select the %1 button", "Chọn nút") == ["placeholder"]


def test_doi_so_thu_tu_placeholder_van_dat():
    # %1 %2 đổi chỗ là hợp lệ trong tiếng Việt
    assert kinds("%1 of %2", "%2 trong số %1") == []


def test_them_placeholder_la_bi_bat():
    assert kinds("Score", "Điểm %1") == ["placeholder"]


def test_mat_placeholder_dem_so_nhieu():
    assert kinds("%n level(s)", "vài cấp độ") == ["placeholder"]


def test_mat_the_rich_text_bi_bat():
    assert kinds("<b>Keyboard</b>", "Bàn phím") == ["tag"]


def test_giu_the_rich_text_thi_dat():
    assert kinds("<b>Keyboard</b>", "<b>Bàn phím</b>") == []


def test_the_br_thieu_bi_bat():
    assert kinds("A<br>B", "A B") == ["tag"]


def test_lech_so_dong_bi_bat():
    assert kinds("Dòng một\nDòng hai", "Một dòng thôi") == ["newline"]


def test_mat_khoang_trang_cuoi_bi_bat():
    assert kinds("Level ", "Cấp độ") == ["whitespace"]


def test_giu_khoang_trang_cuoi_thi_dat():
    assert kinds("Level ", "Cấp độ ") == []


def test_chuoi_chua_dich_bi_bat():
    assert kinds("Practice addition and subtraction", "Practice addition and subtraction") == [
        "untranslated"
    ]


def test_tu_ngan_giong_nhau_thi_bo_qua():
    # tên riêng như "Tux" giữ nguyên là đúng
    assert kinds("Tux", "Tux") == []


def test_chuoi_rong_khong_phai_loi():
    assert kinds("Anything at all", "") == []


def test_nhieu_loi_cung_luc():
    assert kinds("<b>%1</b>\nSecond line", "Dòng hai") == ["newline", "placeholder", "tag"]
