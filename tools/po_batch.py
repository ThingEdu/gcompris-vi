#!/usr/bin/env python3
"""Xuất/nhập từng đợt dịch giữa file po và file JSON gọn để dịch.

  export <po> <out.json> --group core-ui --count 200
  import <po> <in.json>          (kiểm tra rồi ghi đè file po)

Khoá của mỗi mục là chỉ số dòng trong file po; lúc nhập có đối chiếu lại
nguyên văn tiếng Anh nên đặt nhầm chỗ là báo lỗi ngay chứ không ghi bừa.
"""
import argparse
import json
import sys

import polib

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from check_po import check_entry

GROUPS = ["core-ui", "title", "desc", "goal", "prereq", "activity-ui", "manual"]


def group_of(entry):
    cmt = (entry.comment or "").strip()
    occ = entry.occurrences[0][0] if entry.occurrences else ""
    if "Activity title" in cmt:
        return "title"
    if "Help title" in cmt:
        return "desc"
    if "Help goal" in cmt:
        return "goal"
    if "Help prerequisite" in cmt:
        return "prereq"
    if "Help manual" in cmt:
        return "manual"
    if occ.startswith("activities/"):
        return "activity-ui"
    return "core-ui"


SKIP_FILE = __file__.rsplit("/", 2)[0] + "/po/giu-nguyen.txt"


def load_skip():
    """Các chuỗi cố ý để nguyên tiếng Anh — tên riêng nước ngoài mà tiếng Việt
    vẫn viết y như vậy. Ghi ra đây để không phải xét lại ở mọi đợt dịch."""
    import os

    if not os.path.exists(SKIP_FILE):
        return set()
    return {
        line.strip() for line in open(SKIP_FILE, encoding="utf-8")
        if line.strip() and not line.startswith("#")
    }


def cmd_export(args):
    po = polib.pofile(args.po)
    skip = load_skip()
    out = []
    for i, e in enumerate(po):
        if e.translated() or (e.msgid_plural and any(e.msgstr_plural.values())):
            continue
        if args.group and group_of(e) != args.group:
            continue
        if e.msgid in skip:
            continue
        item = {
            "k": i,
            "ctx": (e.msgctxt or "").rstrip("|"),
            "en": e.msgid,
            "vi": "",
        }
        if e.msgid_plural:
            item["en_plural"] = e.msgid_plural
        note = (e.comment or "").strip()
        if note:
            item["note"] = note
        occ = e.occurrences[0][0] if e.occurrences else ""
        if occ:
            item["where"] = occ
        out.append(item)
        if args.count and len(out) >= args.count:
            break
    if args.format == "tsv":
        with open(args.out, "w", encoding="utf-8") as f:
            for x in out:
                en = x["en"].replace("\\", "\\\\").replace("\n", "\\n").replace("\t", "\\t")
                f.write(f"{x['k']}\t{x['ctx']}\t{en}\n")
    else:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
    words = sum(len(x["en"].split()) for x in out)
    print(f"xuất {len(out)} chuỗi ({words} từ) -> {args.out}")


def cmd_import(args):
    po = polib.pofile(args.po)
    if args.inp.endswith(".tsv"):
        items = []
        for lineno, line in enumerate(open(args.inp, encoding="utf-8"), 1):
            line = line.rstrip("\n")
            if not line.strip():
                continue
            if "\t" not in line:
                print(f"dòng {lineno} thiếu tab: {line[:60]!r}")
                return 1
            k, vi = line.split("\t", 1)
            vi = vi.replace("\\n", "\n").replace("\\t", "\t").replace("\\\\", "\\")
            items.append({"k": int(k), "vi": vi})
    else:
        items = json.load(open(args.inp, encoding="utf-8"))
    applied = skipped = 0
    errors = []
    for it in items:
        # KHÔNG cắt xuống dòng ở hai đầu: nhiều chuỗi của GCompris cố ý kết thúc
        # bằng \n hoặc khoảng trắng, cắt đi là sai lệch so với bản gốc.
        vi = it.get("vi") or ""
        if not vi.strip():
            skipped += 1
            continue
        e = po[it["k"]]
        if "en" in it and e.msgid != it["en"]:
            errors.append(f"lệch khoá {it['k']}: po có {e.msgid[:50]!r}, json có {it['en'][:50]!r}")
            continue
        probs = check_entry(e.msgid, vi)
        if probs:
            errors.append(f"[{it['k']}] {e.msgid[:50]!r} -> {vi[:50]!r}\n    " + "; ".join(map(str, probs)))
            continue
        if e.msgid_plural:
            e.msgstr_plural = {0: vi}
        else:
            e.msgstr = vi
        applied += 1

    if errors:
        print("KHÔNG ghi gì cả. Lỗi:")
        for x in errors:
            print(" -", x)
        return 1
    po.save(args.po)
    total = len([e for e in po if e.translated() or (e.msgid_plural and any(e.msgstr_plural.values()))])
    print(f"nhập {applied} chuỗi, bỏ qua {skipped} chuỗi trống. Tổng đã dịch: {total}/{len(po)}")
    return 0


def cmd_stats(args):
    po = polib.pofile(args.po)
    import collections

    done = collections.Counter()
    tot = collections.Counter()
    for e in po:
        g = group_of(e)
        tot[g] += 1
        if e.translated() or (e.msgid_plural and any(e.msgstr_plural.values())):
            done[g] += 1
    print(f"{'nhóm':<14}{'đã dịch':>9}{'tổng':>8}{'%':>7}")
    for g in GROUPS:
        if tot[g]:
            print(f"{g:<14}{done[g]:>9}{tot[g]:>8}{100*done[g]/tot[g]:>6.0f}%")
    print(f"{'TỔNG':<14}{sum(done.values()):>9}{sum(tot.values()):>8}{100*sum(done.values())/sum(tot.values()):>6.0f}%")


p = argparse.ArgumentParser()
sub = p.add_subparsers(dest="cmd", required=True)
e = sub.add_parser("export"); e.add_argument("po"); e.add_argument("out")
e.add_argument("--group", choices=GROUPS); e.add_argument("--count", type=int, default=0)
e.add_argument("--format", choices=["json", "tsv"], default="json")
e.set_defaults(func=cmd_export)
i = sub.add_parser("import"); i.add_argument("po"); i.add_argument("inp"); i.set_defaults(func=cmd_import)
s = sub.add_parser("stats"); s.add_argument("po"); s.set_defaults(func=cmd_stats)
a = p.parse_args()
sys.exit(a.func(a) or 0)
