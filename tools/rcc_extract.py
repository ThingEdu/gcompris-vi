#!/usr/bin/env python3
"""Bung một file .rcc của Qt ra thư mục.

Dùng để vá LanguageList.qml trong core.rcc mà không cần biên dịch lại
GCompris: bung ra, sửa, rồi đóng gói lại bằng lệnh rcc của Qt.

Usage: rcc_extract.py <file.rcc> <thư_mục_đích>
"""
import os
import struct
import sys
import zlib

FLAG_COMPRESSED = 0x01
FLAG_DIRECTORY = 0x02
FLAG_COMPRESSED_ZSTD = 0x04


class Rcc:
    def __init__(self, blob):
        self.b = blob
        if blob[:4] != b"qres":
            raise ValueError("không phải file .rcc (thiếu chữ ký 'qres')")
        self.version, self.tree_off, self.data_off, self.name_off = struct.unpack_from(">IIII", blob, 4)
        if self.version < 1 or self.version > 3:
            raise ValueError(f"phiên bản rcc chưa hỗ trợ: {self.version}")
        # v1: 14 byte/nút; từ v2 thêm 8 byte thời gian sửa đổi
        self.node_size = 14 if self.version < 2 else 22

    def node(self, i):
        o = self.tree_off + i * self.node_size
        name_off, flags = struct.unpack_from(">IH", self.b, o)
        if flags & FLAG_DIRECTORY:
            child_count, first_child = struct.unpack_from(">II", self.b, o + 6)
            return dict(name=self.name(name_off), flags=flags, count=child_count, first=first_child)
        data_off = struct.unpack_from(">I", self.b, o + 10)[0]
        return dict(name=self.name(name_off), flags=flags, data=data_off)

    def name(self, off):
        length = struct.unpack_from(">H", self.b, self.name_off + off)[0]
        start = self.name_off + off + 6  # bỏ qua 2 byte độ dài + 4 byte hash
        return self.b[start : start + length * 2].decode("utf-16-be")

    def payload(self, data_off, flags):
        o = self.data_off + data_off
        size = struct.unpack_from(">I", self.b, o)[0]
        raw = self.b[o + 4 : o + 4 + size]
        if flags & FLAG_COMPRESSED:
            return zlib.decompress(raw[4:])
        if flags & FLAG_COMPRESSED_ZSTD:
            import zstandard  # chỉ cần khi gặp rcc nén zstd

            return zstandard.ZstdDecompressor().decompress(raw)
        return raw

    def walk(self, index=0, path="", is_root=True):
        n = self.node(index)
        name = "" if is_root else n["name"]
        here = f"{path}/{name}" if name else path
        if n["flags"] & FLAG_DIRECTORY:
            for c in range(n["first"], n["first"] + n["count"]):
                yield from self.walk(c, here, is_root=False)
        else:
            yield here, self.payload(n["data"], n["flags"])


def main(rcc_path, out_dir):
    rcc = Rcc(open(rcc_path, "rb").read())
    count = 0
    for path, data in rcc.walk():
        target = os.path.join(out_dir, path.lstrip("/"))
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wb") as f:
            f.write(data)
        count += 1
    print(f"bung {count} tệp (rcc v{rcc.version}) -> {out_dir}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
