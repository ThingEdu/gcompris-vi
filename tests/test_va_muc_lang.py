"""Kiểm bộ vá thêm mục "Làng Maker" vào hàng biểu tượng của GCompris.

Hai cái bẫy đã mắc phải khi làm, bài kiểm dựng ra để không mắc lại:

1. Công thức bề rộng ô mục xuất hiện ở NĂM chỗ trong Menu.qml — một chỗ khai
   mặc định, ba chỗ trong các state ghi đè lại, và một chỗ tính chiều cao. Vá
   mỗi chỗ khai mặc định thì state ghi đè lên, mục thứ 11 vẫn bị cắt khỏi màn
   hình. Chỉ được vá đúng bốn chỗ tính bề rộng biểu tượng, chừa chỗ tính chiều cao.
2. Chạy vá hai lần không được nhân đôi mục.
"""
import os
import shutil
import subprocess
import sys
import tempfile

import pytest

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONG_CU = os.path.join(GOC, "tools", "va_muc_lang.py")

MENU_MAU = '''import QtQuick 2.12
ActivityBase {
    property var sections: [
        {
            icon: activity.url + "all.svg",
            tag: "favorite"
        },
        {
            icon: activity.url + "computer.svg",
            tag: "computer"
        },
        {
            icon: activity.url + "search-icon.svg",
            tag: "search"
        }
    ]
    property int sectionIconWidth: Math.min(100 * ApplicationInfo.ratio, main.width / (sections.length + 1))
    property int sectionCellWidth: sectionIconWidth * 1.1
    states: [
        State { PropertyChanges {
            sectionIconWidth: Math.min(100 * ApplicationInfo.ratio, main.width / (sections.length + 1))
        } },
        State { PropertyChanges {
            sectionIconWidth: Math.min(100 * ApplicationInfo.ratio, (background.height - bar.height) / (sections.length + 1))
        } },
        State { PropertyChanges {
            sectionIconWidth: Math.min(100 * ApplicationInfo.ratio, (background.height - (bar.height+keyboard.height)) / (sections.length + 1))
            height: sectionCellWidth (sections.length + 1)
        } }
    ]
}
'''


def dung_cay(noi_dung=MENU_MAU):
    goc = tempfile.mkdtemp()
    tm = os.path.join(goc, "gcompris/src/activities/menu")
    os.makedirs(tm)
    open(os.path.join(tm, "Menu.qml"), "w", encoding="utf-8").write(noi_dung)
    return goc, os.path.join(tm, "Menu.qml")


def chay(goc):
    return subprocess.run([sys.executable, CONG_CU, goc], capture_output=True, text=True)


def test_them_muc_va_noi_be_rong():
    goc, qml = dung_cay()
    try:
        r = chay(goc)
        assert r.returncode == 0, r.stderr
        s = open(qml, encoding="utf-8").read()
        assert 'tag: "langmaker"' in s
        assert s.count("/ (sections.length * 1.15))") == 4
        assert "/ (sections.length + 1))" not in s
    finally:
        shutil.rmtree(goc)


def test_chua_lai_cho_tinh_chieu_cao():
    goc, qml = dung_cay()
    try:
        chay(goc)
        s = open(qml, encoding="utf-8").read()
        # dòng này tính chiều cao chứ không phải bề rộng biểu tượng, phải giữ nguyên
        assert "height: sectionCellWidth (sections.length + 1)" in s
    finally:
        shutil.rmtree(goc)


def test_muc_dat_ngay_sau_muc_yeu_thich():
    goc, qml = dung_cay()
    try:
        chay(goc)
        s = open(qml, encoding="utf-8").read()
        assert s.index('tag: "favorite"') < s.index('tag: "langmaker"') < s.index('tag: "computer"')
    finally:
        shutil.rmtree(goc)


def test_chay_lai_khong_nhan_doi():
    goc, qml = dung_cay()
    try:
        chay(goc)
        lan1 = open(qml, encoding="utf-8").read()
        r = chay(goc)
        assert r.returncode == 0
        assert open(qml, encoding="utf-8").read() == lan1
        assert lan1.count('tag: "langmaker"') == 1
    finally:
        shutil.rmtree(goc)


def test_dung_lai_khi_so_cho_be_rong_khong_dung():
    # Menu.qml đời sau đổi công thức thì phải dừng, không được vá mù
    goc, _ = dung_cay(MENU_MAU.replace(
        "main.width / (sections.length + 1))", "main.width / (sections.length + 2))", 1))
    try:
        r = chay(goc)
        assert r.returncode != 0
        assert "bề rộng ô mục" in r.stderr
    finally:
        shutil.rmtree(goc)


def test_dung_lai_khi_khong_thay_mang_muc():
    goc, _ = dung_cay(MENU_MAU.replace('tag: "favorite"', 'tag: "yeu-thich"'))
    try:
        r = chay(goc)
        assert r.returncode != 0
        assert "mảng mục" in r.stderr
    finally:
        shutil.rmtree(goc)
