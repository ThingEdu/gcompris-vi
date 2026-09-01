#!/usr/bin/env python3
"""Kiểm tra bản dịch tiếng Việt của GCompris.

Bắt những lỗi làm hỏng lúc chạy hoặc làm lrelease loại chuỗi đi:
placeholder %1/%n, thẻ rich-text của Qt, xuống dòng, khoảng trắng đầu/cuối.
"""
import re
import sys
from collections import Counter

PLACEHOLDER = re.compile(r"%(?:L?\d|n)")
TAG = re.compile(r"</?([a-zA-Z]+)(?:\s[^>]*)?/?>")

# Thẻ mở/đóng không cân bằng trong nguồn của GCompris là chuyện bình thường
# (chuỗi bị cắt giữa chừng rồi nối lại trong QML), nên chỉ so bội số thẻ.


class Problem:
    def __init__(self, kind, detail):
        self.kind = kind
        self.detail = detail

    def __repr__(self):
        return f"{self.kind}: {self.detail}"

    def __eq__(self, other):
        return (self.kind, self.detail) == (other.kind, other.detail)


def check_entry(msgid, msgstr):
    """Trả về danh sách Problem. Rỗng nghĩa là đạt."""
    problems = []
    if not msgstr:
        return problems  # chưa dịch, không phải lỗi

    src_ph = Counter(PLACEHOLDER.findall(msgid))
    dst_ph = Counter(PLACEHOLDER.findall(msgstr))
    if src_ph != dst_ph:
        missing = src_ph - dst_ph
        extra = dst_ph - src_ph
        detail = []
        if missing:
            detail.append("thiếu " + " ".join(sorted(missing.elements())))
        if extra:
            detail.append("thừa " + " ".join(sorted(extra.elements())))
        problems.append(Problem("placeholder", ", ".join(detail)))

    src_tag = Counter(t.lower() for t in TAG.findall(msgid))
    dst_tag = Counter(t.lower() for t in TAG.findall(msgstr))
    if src_tag != dst_tag:
        missing = src_tag - dst_tag
        extra = dst_tag - src_tag
        detail = []
        if missing:
            detail.append("thiếu <" + "> <".join(sorted(missing.elements())) + ">")
        if extra:
            detail.append("thừa <" + "> <".join(sorted(extra.elements())) + ">")
        problems.append(Problem("tag", ", ".join(detail)))

    if msgid.count("\n") != msgstr.count("\n"):
        problems.append(
            Problem("newline", f"nguồn {msgid.count(chr(10))} dòng, dịch {msgstr.count(chr(10))} dòng")
        )

    if (msgid[:1].isspace(), msgid[-1:].isspace()) != (
        msgstr[:1].isspace(),
        msgstr[-1:].isspace(),
    ):
        problems.append(Problem("whitespace", "khoảng trắng đầu/cuối không khớp"))

    if msgid == msgstr and len(msgid.split()) > 2:
        problems.append(Problem("untranslated", "y hệt bản tiếng Anh, lrelease sẽ loại"))

    return problems


def main(path):
    import polib

    po = polib.pofile(path)
    total = failed = 0
    for entry in po:
        if entry.obsolete:
            continue
        strs = [entry.msgstr] if not entry.msgid_plural else list(entry.msgstr_plural.values())
        for s in strs:
            if not s:
                continue
            total += 1
            for p in check_entry(entry.msgid, s):
                failed += 1
                ctx = entry.msgctxt or ""
                print(f"[{p.kind}] {ctx}{entry.msgid[:60]!r}\n    {p.detail}\n    -> {s[:80]!r}")
    print(f"\nĐã kiểm {total} chuỗi đã dịch, {failed} lỗi.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "po/gcompris_qt.po"))
