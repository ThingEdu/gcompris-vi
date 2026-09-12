"""Kiểm bộ đóng gói .rcc thuần Python.

rcc_extract.py không đọc hai trường quyết định việc Qt có TÌM THẤY tệp hay
không, nên khứ hồi một mình là chưa đủ — tệp sai vẫn bung ra đúng mà Qt mở lên
thì rỗng. Hai trường đó:

1. Thứ tự nút con theo băm. QResource tìm con bằng tìm kiếm nhị phân trên băm
   (qresource.cpp findNode), xếp sai là tra không ra.
2. Trường ngôn ngữ của nút tệp. findNode chỉ nhận tệp không theo ngôn ngữ khi
   `territory == QLocale::AnyTerritory && language == QLocale::C`, mà C bằng 1
   chứ không phải 0.

Nên ngoài khứ hồi, bài kiểm dựng lại đúng phép tra của QResource trên byte thô
và đòi tra ra được mọi tệp.

SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
SPDX-License-Identifier: GPL-3.0-or-later
"""
import os
import random
import struct
import subprocess
import sys

import pytest

from tools import rcc_repack

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUNG = os.path.join(GOC, "tools", "rcc_extract.py")

FLAG_COMPRESSED = 0x01
FLAG_DIRECTORY = 0x02

# Cây mẫu: có thư mục lồng nhau, tên trùng ở hai nhánh (bảng tên dùng chung bản
# ghi), tệp nén được, tệp không nén được, tệp rỗng, và tên có dấu tiếng Việt.
CAY = {
    "gcompris/src/activities/menu/Menu.qml": b"import QtQuick 2.12\n" * 500,
    "gcompris/src/activities/menu/resource/all.svg": b"<svg/>",
    "gcompris/src/activities/lang_doidoi/Menu.qml": b"khac hoan toan",
    "gcompris/src/activities/lang_doidoi/resource/hinh/ong_tre.svg": b"<svg>tre</svg>",
    "gcompris/src/core/LanguageList.qml": b'{ "locale": "system" },\n' * 200,
    "gcompris/rong.txt": b"",
    "gcompris/nhieu-dau-tiE1BABFng-viE1BB87t.txt": "chào bạn nhỏ".encode(),
    "ngau_nhien.bin": random.Random(0).randbytes(10000),   # đặc, nén không ăn thua
}


@pytest.fixture
def cay(tmp_path):
    for duong_dan, noi_dung in CAY.items():
        p = tmp_path / "src" / duong_dan
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(noi_dung)
    return tmp_path / "src"


class Doc:
    """Đọc .rcc từ byte thô, theo đúng cách QResource đọc."""

    def __init__(self, blob):
        assert blob[:4] == b"qres"
        self.b = blob
        self.phien_ban, self.tree, self.data, self.names = struct.unpack_from(">IIII", blob, 4)
        self.co_nut = 14 if self.phien_ban < 2 else 22

    def nut(self, i):
        o = self.tree + i * self.co_nut
        ten_off, co = struct.unpack_from(">IH", self.b, o)
        return o, ten_off, co

    def bam(self, i):
        return struct.unpack_from(">I", self.b, self.names + self.nut(i)[1] + 2)[0]

    def ten(self, i):
        ten_off = self.nut(i)[1]
        n = struct.unpack_from(">H", self.b, self.names + ten_off)[0]
        dau = self.names + ten_off + 6
        return self.b[dau:dau + n * 2].decode("utf-16-be")

    def con(self, i):
        o, _, co = self.nut(i)
        assert co & FLAG_DIRECTORY
        so, dau = struct.unpack_from(">II", self.b, o + 6)
        return range(dau, dau + so)

    def vung_ngon_ngu(self, i):
        o = self.nut(i)[0]
        return struct.unpack_from(">HH", self.b, o + 6)

    def noi_dung(self, i):
        o, _, co = self.nut(i)
        assert not co & FLAG_DIRECTORY
        off = struct.unpack_from(">I", self.b, o + 10)[0]
        d = self.data + off
        dai = struct.unpack_from(">I", self.b, d)[0]
        tho = self.b[d + 4:d + 4 + dai]
        return __import__("zlib").decompress(tho[4:]) if co & FLAG_COMPRESSED else tho

    def tim(self, duong_dan):
        """Tra một đường dẫn đúng phép của findNode: nhị phân trên băm rồi so tên."""
        nut = 0
        for doan in duong_dan.strip("/").split("/"):
            o, _, co = self.nut(nut)
            if not co & FLAG_DIRECTORY:
                return None
            so, dau = struct.unpack_from(">II", self.b, o + 6)
            h = rcc_repack.ban_ghi_ten(doan)[0]
            trai, phai, thay = dau, dau + so - 1, None
            while trai <= phai:
                giua = (trai + phai) // 2
                if self.bam(giua) < h:
                    trai = giua + 1
                elif self.bam(giua) > h:
                    phai = giua - 1
                else:
                    thay = giua
                    break
            if thay is None:
                return None
            while thay > dau and self.bam(thay - 1) == h:        # lùi lại khi băm đụng nhau
                thay -= 1
            while thay < dau + so and self.bam(thay) == h and self.ten(thay) != doan:
                thay += 1
            if thay >= dau + so or self.ten(thay) != doan:
                return None
            nut = thay
        return nut

    def moi_nut(self, i=0):
        yield i
        if self.nut(i)[2] & FLAG_DIRECTORY:
            for c in self.con(i):
                yield from self.moi_nut(c)


def goi(cay, phien_ban=2):
    return Doc(rcc_repack.dong_goi(rcc_repack.dung_cay(str(cay)), phien_ban)[0])


@pytest.mark.parametrize("phien_ban", [1, 2, 3])
def test_khu_hoi_qua_bo_bung(cay, tmp_path, phien_ban):
    """Đóng gói rồi bung ra bằng rcc_extract.py phải khớp từng byte."""
    ra = tmp_path / f"x{phien_ban}.rcc"
    blob, so_tep = rcc_repack.dong_goi(rcc_repack.dung_cay(str(cay)), phien_ban)
    ra.write_bytes(blob)
    assert so_tep == len(CAY)

    dich = tmp_path / f"bung{phien_ban}"
    subprocess.run([sys.executable, BUNG, str(ra), str(dich)], check=True,
                   capture_output=True)
    assert subprocess.run(["diff", "-r", str(cay), str(dich)],
                          capture_output=True).returncode == 0


def test_tra_duoc_moi_tep_dung_phep_cua_qresource(cay):
    """Phép tra nhị phân trên băm của Qt phải ra đúng nội dung từng tệp."""
    d = goi(cay)
    for duong_dan, noi_dung in CAY.items():
        i = d.tim(duong_dan)
        assert i is not None, f"tra không ra {duong_dan}"
        assert d.noi_dung(i) == noi_dung


def test_tra_hong_khi_nut_con_xep_sai(cay):
    """Chứng minh phép tra ở trên biết fail: đảo hai nút anh em là tra không ra."""
    blob = bytearray(rcc_repack.dong_goi(rcc_repack.dung_cay(str(cay)), 2)[0])
    d = Doc(bytes(blob))
    cha = d.tim("gcompris/src/activities")
    a, b = list(d.con(cha))[:2]
    assert d.bam(a) != d.bam(b)
    oa, ob = d.tree + a * d.co_nut, d.tree + b * d.co_nut
    blob[oa:oa + d.co_nut], blob[ob:ob + d.co_nut] = blob[ob:ob + d.co_nut], blob[oa:oa + d.co_nut]
    assert Doc(bytes(blob)).tim("gcompris/src/activities/menu/Menu.qml") is None


def test_nut_con_xep_tang_dan_theo_bam(cay):
    d = goi(cay)
    for i in d.moi_nut():
        if d.nut(i)[2] & FLAG_DIRECTORY:
            bams = [d.bam(c) for c in d.con(i)]
            assert bams == sorted(bams)


def test_nut_tep_ghi_dung_vung_va_ngon_ngu(cay):
    """language phải là QLocale::C = 1; ghi 0 thì findNode bỏ qua tệp."""
    d = goi(cay)
    tep = [i for i in d.moi_nut() if not d.nut(i)[2] & FLAG_DIRECTORY]
    assert len(tep) == len(CAY)
    for i in tep:
        assert d.vung_ngon_ngu(i) == (0, 1)


def test_chi_nen_khi_dang_nen(cay):
    """Ngưỡng 70% như rcc.cpp: QML lặp thì nén, tệp nhị phân đặc thì thôi."""
    d = goi(cay)
    assert d.nut(d.tim("gcompris/src/activities/menu/Menu.qml"))[2] & FLAG_COMPRESSED
    assert not d.nut(d.tim("ngau_nhien.bin"))[2] & FLAG_COMPRESSED
    assert not d.nut(d.tim("gcompris/rong.txt"))[2] & FLAG_COMPRESSED


def test_bang_ten_dung_chung_ban_ghi_cho_ten_trung(cay):
    """Hai nhánh cùng có "Menu.qml" và "resource" — mỗi tên chỉ một bản ghi."""
    d = goi(cay)
    theo_ten = {}
    for i in d.moi_nut():
        if i:
            theo_ten.setdefault(d.ten(i), set()).add(d.nut(i)[1])
    assert theo_ten["Menu.qml"] and len(theo_ten["Menu.qml"]) == 1
    assert theo_ten["resource"] and len(theo_ten["resource"]) == 1


@pytest.mark.parametrize("phien_ban,co_nut,dai_header", [(1, 14, 20), (2, 22, 20), (3, 22, 24)])
def test_kich_thuoc_theo_phien_ban(cay, phien_ban, co_nut, dai_header):
    d = goi(cay, phien_ban)
    assert d.co_nut == co_nut
    assert d.data == dai_header
    assert d.data < d.names < d.tree     # thứ tự khối như rcc.cpp ghi ra


def test_co_tong_chi_co_tu_v3(cay):
    """Cờ tổng ở byte 20 chỉ tồn tại từ v3; v2 không có chỗ cho nó."""
    blob3 = rcc_repack.dong_goi(rcc_repack.dung_cay(str(cay)), 3)[0]
    assert struct.unpack_from(">I", blob3, 20)[0] == FLAG_COMPRESSED
