#!/usr/bin/env python3
"""Soát kho giọng đã sinh: tệp thiếu, tệp cụt tiếng, tệp chạy loạn.

VieNeu-TTS không tất định — với câu ngắn nó thỉnh thoảng cho ra tệp 0,1 giây
hoặc dài hơn 10 giây. Bộ soát này bắt những tệp đó để sinh lại.

Usage: check_voices.py [--fmt ogg]
"""
import argparse
import contextlib
import glob
import os
import sys
import wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from make_voices import EXT, WAV_DIR, duration_band, out_dir  # noqa: E402


def manifest_entries():
    out = {}
    for m in sorted(glob.glob(os.path.join(ROOT, "voices", "manifest", "*.tsv"))):
        group = os.path.basename(m)[:-4]
        for line in open(m, encoding="utf-8"):
            if "\t" in line:
                k, t = line.rstrip("\n").split("\t", 1)
                out[f"{group}/{k}"] = t.strip()
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--fmt", default="ogg")
    a = p.parse_args()

    entries = manifest_entries()
    missing_wav, missing_enc, bad = [], [], []
    total = 0.0
    for key, text in sorted(entries.items()):
        wav = os.path.join(WAV_DIR, key + ".wav")
        enc = os.path.join(out_dir(a.fmt), key + "." + EXT[a.fmt])
        if not os.path.exists(wav):
            missing_wav.append(key)
            continue
        if not os.path.exists(enc):
            missing_enc.append(key)
        with contextlib.closing(wave.open(wav)) as w:
            d = w.getnframes() / w.getframerate()
        total += d
        lo, hi = duration_band(text)
        if not (lo <= d <= hi):
            bad.append((key, d, lo, hi, text))

    print(f"{len(entries)} mục trong bảng lời · tổng thời lượng {total / 60:.1f} phút")
    for label, items in (("thiếu wav", missing_wav), (f"thiếu {a.fmt}", missing_enc)):
        if items:
            print(f"{label}: {len(items)} — {', '.join(items[:8])}")
    if bad:
        print(f"\nlệch dải thời lượng: {len(bad)}")
        for k, d, lo, hi, t in bad:
            print(f"  {k}  {d:.2f}s (mong đợi {lo:.2f}–{hi:.2f})  {t[:45]!r}")
    ok = not (missing_wav or missing_enc or bad)
    print("\nĐẠT" if ok else "\nCHƯA ĐẠT — xoá các tệp wav hỏng rồi chạy lại make_voices.py")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
