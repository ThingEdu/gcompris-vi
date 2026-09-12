"""Kiểm deploy/va_lai.sh — đường vá mà postinst và trigger của gói .deb dùng.

Bài kiểm dựng một bộ .rcc giả giống gcompris-qt-data (bản gốc đã nằm ở tên
.orig như sau khi dpkg-divert đẩy sang), chạy đúng script mà máy thật chạy, rồi
bung kết quả ra soát.

Hai điều phải đúng, vì cả hai đều hỏng âm thầm:

1. Vá luôn đi từ .orig, không vá chồng lên bản đã vá. Trigger gọi lại script
   này mỗi lần gcompris-qt-data nâng đời, chạy hai lần phải ra y hệt một lần —
   không nhân đôi mục ngôn ngữ, không nhân đôi dòng trong activities_out.txt.
2. Danh sách mini app suy ra từ chính các tệp lang_*.rcc đã cài, nên thêm mini
   app thứ ba không phải sửa script.

SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
SPDX-License-Identifier: GPL-3.0-or-later
"""
import os
import subprocess
import sys

import pytest

from tests.test_va_muc_lang import MENU_MAU
from tools import rcc_repack

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VA_LAI = os.path.join(GOC, "deploy", "va_lai.sh")
BUNG = os.path.join(GOC, "tools", "rcc_extract.py")

LANGLIST = '''import QtQuick 2.12
QtObject {
    property var languages: [
        { "text": "System", "locale": "system" },
        { "text": "English", "locale": "en_US.UTF-8" },
        { "text": "Français", "locale": "fr_FR.UTF-8" }
    ]
}
'''
NOI_DUNG = {
    "core.rcc": {"gcompris/src/core/LanguageList.qml": LANGLIST},
    "menu.rcc": {"gcompris/src/activities/menu/Menu.qml": MENU_MAU},
    "activities.rcc": {"gcompris/src/activities/activities_out.txt":
                       "".join(f"activity{i:03d}\n" for i in range(183))},
}
DUONG_DAN = {t: list(v)[0] for t, v in NOI_DUNG.items()}


@pytest.fixture
def may(tmp_path):
    """Máy giả: bản gốc đã ở tên .orig, hai mini app đã cài trong rcc/."""
    rcc = tmp_path / "rcc"
    rcc.mkdir()
    for ten, tep in NOI_DUNG.items():
        cay = tmp_path / "mk" / ten
        for p, noi in tep.items():
            f = cay / p
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(noi, encoding="utf-8")
        blob = rcc_repack.dong_goi(rcc_repack.dung_cay(str(cay)), 3)[0]
        (rcc / (ten + ".orig")).write_bytes(blob)
    for t in ("lang_maker", "lang_doidoi"):
        (rcc / (t + ".rcc")).write_bytes(b"gia")
    return rcc


def chay(rcc):
    return subprocess.run(
        [VA_LAI], check=True, capture_output=True, text=True,
        env={**os.environ, "RCC_DIR": str(rcc), "TOOLS_DIR": os.path.join(GOC, "tools"),
             "MAPS_DIR": os.path.join(GOC, "maps")})


def doc(rcc, tmp_path, ten):
    dich = tmp_path / "bung" / ten
    subprocess.run([sys.executable, BUNG, str(rcc / ten), str(dich)],
                   check=True, capture_output=True)
    return (dich / DUONG_DAN[ten]).read_text(encoding="utf-8")


def test_va_du_ba_tep_co_ban_goc(may):
    ra = chay(may).stdout
    for ten in NOI_DUNG:
        assert f"patched {ten}" in ra
        assert (may / ten).exists()


def test_bo_qua_tep_chua_duoc_chuyen_huong(may):
    """Thiếu .orig thì bỏ qua và nói rõ, không được dựng .rcc rỗng."""
    ra = chay(may)
    assert "skipping geography.rcc" in ra.stderr
    assert not (may / "geography.rcc").exists()


def test_them_dung_mot_muc_tieng_viet(may, tmp_path):
    chay(may)
    s = doc(may, tmp_path, "core.rcc")
    assert s.count("vi_VN.UTF-8") == 1
    assert s.count('"locale": "system"') == 1      # mục cũ còn nguyên


def test_dang_ky_mini_app_tim_thay_tu_thu_muc_rcc(may, tmp_path):
    chay(may)
    dong = doc(may, tmp_path, "activities.rcc").splitlines()
    assert len(dong) == 185
    assert dong[-2:] == ["lang_doidoi", "lang_maker"]
    assert dong[:183] == [f"activity{i:03d}" for i in range(183)]


def test_mini_app_moi_khong_phai_sua_script(may, tmp_path):
    """Thả thêm lang_abc.rcc vào thư mục rcc/ là script tự đăng ký."""
    (may / "lang_abc.rcc").write_bytes(b"gia")
    chay(may)
    assert "lang_abc" in doc(may, tmp_path, "activities.rcc").splitlines()


def test_them_muc_lang_maker_vao_menu(may, tmp_path):
    chay(may)
    s = doc(may, tmp_path, "menu.rcc")
    assert s.count('tag: "langmaker"') == 1
    assert s.count("sections.length * 1.15") == 4   # chừa chỗ tính chiều cao


def test_chay_lai_ra_y_het(may, tmp_path):
    """Trigger gọi lại sau mỗi lần gcompris-qt-data nâng đời."""
    chay(may)
    lan1 = {t: (may / t).read_bytes() for t in NOI_DUNG}
    chay(may)
    assert {t: (may / t).read_bytes() for t in NOI_DUNG} == lan1


def test_dung_khi_ban_goc_hong(may):
    """Bản gốc không đọc được thì dừng, tuyệt đối không ghi ra tệp dở dang."""
    (may / "core.rcc.orig").write_bytes(b"qres" + b"\x00" * 40)
    with pytest.raises(subprocess.CalledProcessError):
        chay(may)
    assert not (may / "core.rcc").exists()
