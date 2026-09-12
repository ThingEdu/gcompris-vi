#!/usr/bin/env python3
"""Đóng gói một thư mục thành tệp .rcc của Qt — thuần Python, không cần lệnh rcc.

    rcc_repack.py <thư_mục> <out.rcc> [--version 2]

Trước đây tệp này gọi lệnh `rcc` của Qt. Bản đóng gói .deb phải vá .rcc ngay
trên NEO One nên không thể phụ thuộc vào bộ công cụ phát triển Qt: viết thẳng
định dạng ra thì postinst chỉ cần python3.

Định dạng (khớp rcc_extract.py; đối chiếu src/tools/rcc/rcc.cpp của Qt):

    header   "qres", u32 phiên bản, u32 tree_off, u32 data_off, u32 name_off
             [u32 cờ tổng — chỉ từ v3]
    data     mỗi tệp: u32 độ dài + payload
    names    mỗi tên: u16 số ký tự + u32 băm + tên UTF-16BE
    tree     mỗi nút 14 byte (v1) hoặc 22 byte (v2+, thêm mốc thời gian)

Hai bất biến mà tệp sai thì Qt vẫn nạp được nhưng KHÔNG tìm thấy nội dung, nên
rcc_extract.py không bắt được — `tests/test_rcc.py` kiểm riêng:

1. Nút con của mỗi thư mục phải xếp tăng dần theo băm: QResource tìm con bằng
   tìm kiếm nhị phân trên băm (qresource.cpp findNode).
2. Trường ngôn ngữ của nút tệp phải là QLocale::C = 1, không phải 0.
   findNode chỉ nhận tệp không theo ngôn ngữ khi `territory == AnyTerritory &&
   language == C`; ghi 0 thì mọi tệp thành vô hình.

SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
SPDX-License-Identifier: GPL-3.0-or-later
"""
import argparse
import os
import struct
import sys
import zlib

FLAG_COMPRESSED = 0x01
FLAG_DIRECTORY = 0x02

NGON_NGU_C = 1          # QLocale::C
VUNG_BAT_KY = 0         # QLocale::AnyTerritory
NGUONG_NEN = 70         # như rcc.cpp: chỉ giữ bản nén khi tiết kiệm >= 70%
MUC_NEN = 9


def ban_ghi_ten(ten):
    """Trả về (băm, bản ghi trong bảng tên) cho một thành phần đường dẫn.

    Băm của Qt (qhash.cpp qt_hash) chạy trên đơn vị mã UTF-16, không phải điểm
    mã, nên mã hoá trước rồi mới duyệt.
    """
    b = ten.encode("utf-16-be", "surrogatepass")
    h = 0
    for i in range(0, len(b), 2):
        h = ((h << 4) + int.from_bytes(b[i:i + 2], "big")) & 0xFFFFFFFF
        h ^= (h & 0xF0000000) >> 23
    h &= 0x0FFFFFFF
    return h, struct.pack(">HI", len(b) // 2, h) + b


class Nut:
    def __init__(self, ten, duong_dan=None):
        self.ten = ten
        self.duong_dan = duong_dan      # None => thư mục
        self.con = []
        self.bam, self.ban_ghi = ban_ghi_ten(ten)
        self.ten_off = 0
        self.data_off = 0
        self.con_off = 0
        self.co = 0


def dung_cay(goc):
    def di(d, ten):
        n = Nut(ten)
        for e in sorted(os.listdir(d)):
            p = os.path.join(d, e)
            n.con.append(di(p, e) if os.path.isdir(p) else Nut(e, p))
        return n
    return di(goc, "")


def dong_goi(goc, phien_ban):
    # 1. đánh chỉ số nút theo chiều rộng; con của mỗi thư mục xếp theo băm
    nuts = [goc]
    hang_doi = [goc]
    while hang_doi:
        d = hang_doi.pop(0)
        d.con_off = len(nuts)
        d.con.sort(key=lambda c: c.bam)
        nuts.extend(d.con)
        hang_doi.extend(c for c in d.con if c.duong_dan is None)

    # 2. khối dữ liệu
    data = bytearray()
    co_tong = 0
    so_tep = 0
    for n in nuts:
        if n.duong_dan is None:
            continue
        so_tep += 1
        with open(n.duong_dan, "rb") as f:
            tho = f.read()
        payload = tho
        if tho:
            # qCompress: 4 byte độ dài gốc (big endian) rồi tới luồng zlib
            nen = struct.pack(">I", len(tho)) + zlib.compress(tho, MUC_NEN)
            if 100 * (len(tho) - len(nen)) // len(tho) >= NGUONG_NEN:
                payload, n.co = nen, FLAG_COMPRESSED
        co_tong |= n.co
        n.data_off = len(data)
        data += struct.pack(">I", len(payload)) + payload

    # 3. bảng tên — tên trùng nhau dùng chung một bản ghi (rcc.cpp cũng vậy)
    names = bytearray()
    da_co = {}
    for n in nuts[1:]:      # nút gốc không có tên
        if n.ten in da_co:
            n.ten_off = da_co[n.ten]
        else:
            n.ten_off = da_co[n.ten] = len(names)
            names += n.ban_ghi

    # 4. cây
    tree = bytearray()
    for n in nuts:
        if n.duong_dan is None:
            tree += struct.pack(">IHII", n.ten_off, FLAG_DIRECTORY, len(n.con), n.con_off)
        else:
            tree += struct.pack(">IHHHI", n.ten_off, n.co, VUNG_BAT_KY, NGON_NGU_C, n.data_off)
        if phien_ban >= 2:
            tree += struct.pack(">Q", 0)    # mốc thời gian 0: dựng lại là ra y hệt

    dai_header = 20 + (4 if phien_ban >= 3 else 0)
    data_off = dai_header
    name_off = data_off + len(data)
    tree_off = name_off + len(names)
    ra = bytearray(b"qres" + struct.pack(">IIII", phien_ban, tree_off, data_off, name_off))
    if phien_ban >= 3:
        ra += struct.pack(">I", co_tong)
    ra += data + names + tree
    return bytes(ra), so_tep


def main():
    p = argparse.ArgumentParser()
    p.add_argument("src_dir")
    p.add_argument("out")
    p.add_argument("--version", type=int, default=2,
                   help="phiên bản định dạng rcc (2 cho Qt5, 3 cho Qt6)")
    a = p.parse_args()
    if not 1 <= a.version <= 3:
        raise SystemExit(f"phiên bản rcc chưa hỗ trợ: {a.version}")

    blob, so_tep = dong_goi(dung_cay(os.path.abspath(a.src_dir)), a.version)
    with open(a.out, "wb") as f:
        f.write(blob)
    print(f"đóng gói {so_tep} tệp -> {a.out} ({len(blob)} byte)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
