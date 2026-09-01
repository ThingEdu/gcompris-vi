#!/usr/bin/env python3
"""Đóng gói lại một thư mục đã bung thành file .rcc bằng lệnh rcc của Qt.

Usage: rcc_repack.py <thư_mục> <out.rcc> [--rcc /đường/dẫn/rcc] [--version 2]
"""
import argparse
import os
import subprocess
import sys
import tempfile
from xml.sax.saxutils import escape

DEFAULT_RCC = "/opt/homebrew/opt/qt/share/qt/libexec/rcc"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("src_dir")
    p.add_argument("out")
    p.add_argument("--rcc", default=os.environ.get("RCC", DEFAULT_RCC))
    p.add_argument("--version", default="2", help="phiên bản định dạng rcc (2 cho Qt5, 3 cho Qt6)")
    a = p.parse_args()

    src_dir = os.path.abspath(a.src_dir)
    files = []
    for dp, _, fn in os.walk(src_dir):
        for f in fn:
            full = os.path.join(dp, f)
            alias = os.path.relpath(full, src_dir)
            files.append((full, alias))
    files.sort(key=lambda x: x[1])

    qrc = ["<!DOCTYPE RCC><RCC version=\"1.0\">", '<qresource prefix="/">']
    for full, alias in files:
        qrc.append(f'  <file alias="{escape(alias)}">{escape(full)}</file>')
    qrc += ["</qresource>", "</RCC>"]

    with tempfile.NamedTemporaryFile("w", suffix=".qrc", delete=False, encoding="utf-8") as f:
        f.write("\n".join(qrc))
        qrc_path = f.name

    cmd = [a.rcc, "--binary", "--format-version", a.version, "--no-zstd", "-o", a.out, qrc_path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    os.unlink(qrc_path)
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr)
        return r.returncode
    print(f"đóng gói {len(files)} tệp -> {a.out} ({os.path.getsize(a.out)} byte)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
