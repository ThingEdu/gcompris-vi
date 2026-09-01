#!/usr/bin/env python3
"""Sinh kho giọng đọc tiếng Việt cho GCompris bằng VieNeu-TTS.

Đọc voices/manifest/<nhóm>.tsv (tên_tệp <tab> lời đọc), tổng hợp giọng một lần
vào kho wav rồi mã hoá ra đúng định dạng mà nền tảng đích dùng:

    Linux  -> ogg (vorbis)      build/voices-ogg/gcompris/data/voices-ogg/vi/...
    macOS  -> aac               build/voices-aac/gcompris/data/voices-aac/vi/...

Giữ wav lại nên đổi định dạng không phải chạy lại TTS.

Usage: make_voices.py [--only misc,colors] [--format ogg,aac] [--force] [--ref ref.wav]
"""
import argparse
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_DIR = os.path.join(ROOT, "voices", "manifest")
WAV_DIR = os.path.join(ROOT, "build", "voices-wav")
# Giọng chuẩn nam miền Bắc "Bình" đi kèm gói vieneu.
# Đổi giọng: truyền --ref tới một tệp wav khác rồi chạy lại với --force.
_VIENEU_SAMPLES = os.path.expanduser(
    "~/Ai-Code/NeoTeach/voice-studio/.venv/lib/python3.14/site-packages/vieneu/assets/samples"
)
DEFAULT_REF = os.path.join(_VIENEU_SAMPLES, "Bình (nam miền Bắc).wav")
SAMPLE_RATE = 24000
EXT = {"ogg": "ogg", "aac": "aac", "mp3": "mp3"}


def out_dir(fmt):
    return os.path.join(ROOT, "build", f"voices-{fmt}", "gcompris", "data", f"voices-{fmt}", "vi")


def load_manifests(only):
    jobs = []
    for name in sorted(os.listdir(MANIFEST_DIR)):
        if not name.endswith(".tsv"):
            continue
        group = name[:-4]
        if only and group not in only:
            continue
        for lineno, line in enumerate(open(os.path.join(MANIFEST_DIR, name), encoding="utf-8"), 1):
            line = line.rstrip("\n")
            if not line.strip():
                continue
            if "\t" not in line:
                sys.exit(f"{name}:{lineno} thiếu tab: {line[:60]!r}")
            key, text = line.split("\t", 1)
            if not text.strip():
                sys.exit(f"{name}:{lineno} thiếu lời đọc cho {key!r}")
            jobs.append((group, key, text.strip()))
    return jobs


def trim_silence(audio, sr=SAMPLE_RATE, thresh=0.015, pad=0.06):
    """Cắt bớt phần lặng hai đầu, chừa lại một chút cho đỡ cụt tiếng."""
    import numpy as np

    loud = np.abs(audio) > thresh
    if not loud.any():
        return audio
    i, j = loud.argmax(), len(loud) - loud[::-1].argmax()
    p = int(pad * sr)
    return audio[max(0, i - p):min(len(audio), j + p)]


def duration_band(text):
    """Dải thời lượng hợp lý cho một câu tiếng Việt, tính theo số âm tiết.

    VieNeu-TTS không tất định: với câu ngắn nó thỉnh thoảng cho ra tệp cụt
    (0,1 giây) hoặc chạy loạn (hơn 10 giây). Dải này để phát hiện và sinh lại.
    """
    syl = max(len(text.split()), 1)
    # Hiệu chuẩn trên 116 câu dài đã sinh: 0,19-0,32 giây mỗi âm tiết.
    # Câu ngắn đọc chậm hơn tính theo âm tiết nên cận dưới nới ra.
    return 0.15 * syl + 0.10, 0.55 * syl + 1.2


# Nhiệt độ lấy mẫu cho từng lần thử. Bộ sinh của VieNeu gieo số ngẫu nhiên cố
# định nên gọi lại y hệt sẽ ra y hệt — muốn thử lại có ích thì phải đổi nhiệt độ.
TEMPERATURES = [0.4, 0.30, 0.55, 0.22, 0.70, 0.45, 0.35, 0.60]


def synthesize(tts, ref, text, tries=len(TEMPERATURES)):
    """Sinh giọng, thử lại tới khi thời lượng nằm trong dải hợp lý."""
    import numpy as np

    lo, hi = duration_band(text)
    best = None
    for attempt in range(tries):
        temp = TEMPERATURES[attempt % len(TEMPERATURES)]
        audio = np.squeeze(np.asarray(
            tts.infer(text=text, voice=ref, temperature=temp, show_progress=False)))
        if audio.dtype == np.int16:
            audio = audio.astype(np.float32) / 32768.0
        audio = trim_silence(audio)
        d = len(audio) / SAMPLE_RATE
        if lo <= d <= hi:
            return audio, d, True
        # giữ lại lần gần dải nhất để dùng nếu thử hết vẫn hỏng
        miss = lo - d if d < lo else d - hi
        if best is None or miss < best[1]:
            best = (audio, miss, d)
    return best[0], best[2], False


def encode(wav_path, dst, fmt):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if fmt == "ogg":
        # oggenc của vorbis-tools: ffmpeg bản Homebrew không kèm bộ mã hoá Vorbis
        cmd = ["oggenc", "-Q", "-q", "3", "--resample", "44100", "-o", dst, wav_path]
    else:
        codec = {"aac": "aac", "mp3": "libmp3lame"}[fmt]
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", wav_path,
               "-c:a", codec, "-b:a", "96k", "-ar", "44100", "-ac", "1", dst]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"mã hoá {fmt} lỗi: {(r.stderr or r.stdout)[:300]}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--only", help="chỉ làm vài nhóm, ngăn cách bằng dấu phẩy")
    p.add_argument("--format", default="ogg,aac", help="định dạng cần xuất")
    p.add_argument("--force", action="store_true", help="tổng hợp lại cả tệp đã có")
    p.add_argument("--ref", default=DEFAULT_REF, help="tệp giọng mẫu cho VieNeu-TTS")
    a = p.parse_args()

    only = set(a.only.split(",")) if a.only else None
    formats = [f.strip() for f in a.format.split(",") if f.strip()]
    for f in formats:
        if f not in EXT:
            sys.exit(f"định dạng lạ: {f}")

    jobs = load_manifests(only)
    need_tts = [j for j in jobs
                if a.force or not os.path.exists(os.path.join(WAV_DIR, j[0], j[1] + ".wav"))]
    print(f"{len(jobs)} tệp trong bảng lời · cần tổng hợp giọng: {len(need_tts)}")

    if need_tts:
        if not os.path.exists(a.ref):
            sys.exit(f"Không thấy giọng mẫu {a.ref}")
        import soundfile as sf
        from vieneu import Vieneu

        tts = Vieneu(mode="turbo")
        ref = tts.encode_reference(a.ref)
        bad = []
        for i, (group, key, text) in enumerate(need_tts, 1):
            audio, dur, ok = synthesize(tts, ref, text)
            if not ok:
                bad.append((group, key, dur, text))
            dst = os.path.join(WAV_DIR, group, key + ".wav")
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            sf.write(dst, audio, SAMPLE_RATE)
            if i % 50 == 0 or i == len(need_tts):
                print(f"  giọng {i}/{len(need_tts)}")
        if bad:
            print(f"\n{len(bad)} tệp thử hết lượt vẫn lệch dải, cần nghe lại:")
            for g, k, d, t in bad:
                print(f"  {g}/{k}  {d:.2f}s  {t[:50]!r}")

    for fmt in formats:
        made = 0
        for group, key, _ in jobs:
            wav = os.path.join(WAV_DIR, group, key + ".wav")
            dst = os.path.join(out_dir(fmt), group, key + "." + EXT[fmt])
            stale = os.path.exists(dst) and os.path.getmtime(dst) < os.path.getmtime(wav)
            if a.force or stale or not os.path.exists(dst):
                encode(wav, dst, fmt)
                made += 1
        print(f"  {fmt}: mã hoá thêm {made} tệp -> {out_dir(fmt)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
