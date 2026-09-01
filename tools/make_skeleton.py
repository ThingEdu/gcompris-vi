#!/usr/bin/env python3
"""Dựng file po tiếng Việt rỗng từ một bản dịch thượng nguồn đã đầy đủ.

GCompris không phát hành file .pot trong repo, nhưng mọi file po trong poqm/
đều sinh ra từ cùng một pot nên tập msgid giống hệt nhau. Ta lấy bản tiếng
Pháp (đầy đủ nhất) làm khuôn, xoá sạch phần dịch và đặt lại header cho vi.

Usage: make_skeleton.py <upstream.po> <out-vi.po>
"""
import sys
import polib

HEADER = {
    "Project-Id-Version": "gcompris_qt",
    "Report-Msgid-Bugs-To": "https://bugs.kde.org",
    "Language-Team": "Vietnamese",
    "Language": "vi",
    "MIME-Version": "1.0",
    "Content-Type": "text/plain; charset=UTF-8",
    "Content-Transfer-Encoding": "8bit",
    "Plural-Forms": "nplurals=1; plural=0;",
    "X-Accelerator-Marker": "&",
    "X-Environment": "kde",
    "X-Language": "vi",
    "X-Qt-Contexts": "true",
    "X-Text-Markup": "qtrich",
}


def main(src_path, out_path):
    src = polib.pofile(src_path)
    out = polib.POFile()
    out.header = "Bản dịch tiếng Việt cho GCompris.\nSPDX-License-Identifier: GPL-3.0-or-later"
    out.metadata = dict(HEADER)
    out.metadata["POT-Creation-Date"] = src.metadata.get("POT-Creation-Date", "")

    for e in src:
        if e.obsolete:
            continue
        entry = polib.POEntry(
            msgid=e.msgid,
            msgstr="",
            msgctxt=e.msgctxt,
            occurrences=e.occurrences,
            comment=e.comment,
            tcomment="",
            flags=[f for f in e.flags if f != "fuzzy"],
        )
        if e.msgid_plural:
            entry.msgid_plural = e.msgid_plural
            entry.msgstr_plural = {0: ""}
        out.append(entry)

    out.save(out_path)
    print(f"{len(out)} chuỗi -> {out_path}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
