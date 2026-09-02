#!/usr/bin/env python3
"""Đóng gói các mini app do ThingEdu thêm vào GCompris.

GCompris nạp hoạt động từ tệp .rcc BÊN NGOÀI, không nhúng vào chương trình
(`ActivityInfoTree.cpp`): nó đọc danh sách tên trong `activities_out.txt` của
`activities.rcc`, rồi với mỗi tên thì `registerResource(<tên>.rcc)` và nạp
`qrc:/gcompris/src/activities/<tên>/ActivityInfo.qml`. Vì vậy thêm hoạt động
mới KHÔNG cần biên dịch lại C++.

Chỗ duy nhất phải đụng vào phần của GCompris là một dòng tên trong
`activities_out.txt`. Mọi thứ khác chỉ là thêm tệp mới. Nhờ vậy nâng đời
GCompris xong chỉ cần chạy lại script này một lần là các mini app trở lại.

Quy ước đặt tên: mọi mini app của Làng Maker bắt đầu bằng `lang_`. GCompris
gốc không dùng tiền tố này nên danh sách hoạt động không bao giờ đụng nhau.

    dong_goi_mini_app.py <thư_mục_ra> [tên_app ...]     # mặc định: tất cả

Sinh ra <tên>.rcc cho từng app. Tài sản dùng chung ở mini-app/chung/ được chép
vào resource/chung/ của từng app, để đổi nhân vật một chỗ là đổi hết.
"""
import os
import shutil
import subprocess
import sys
import tempfile

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NGUON = os.path.join(GOC, "mini-app")
CHUNG = os.path.join(NGUON, "chung")
TIEN_TO = "lang_"


def danh_sach_app():
    return sorted(t for t in os.listdir(NGUON)
                  if t.startswith(TIEN_TO) and os.path.isdir(os.path.join(NGUON, t)))


def dong_goi(ten, ra):
    goc_app = os.path.join(NGUON, ten)
    thu_muc = os.path.join(goc_app, "gcompris/src/activities", ten)
    if not os.path.isdir(thu_muc):
        raise SystemExit(f"{ten}: thiếu {thu_muc}")
    for bat_buoc in ("ActivityInfo.qml", ten[0].upper() + ten[1:] + ".qml"):
        if not os.path.exists(os.path.join(thu_muc, bat_buoc)):
            raise SystemExit(f"{ten}: thiếu {bat_buoc}")

    tam = tempfile.mkdtemp()
    try:
        cay = os.path.join(tam, "cay")
        shutil.copytree(goc_app, cay)
        # tài sản dùng chung -> resource/chung/ của app
        dich = os.path.join(cay, "gcompris/src/activities", ten, "resource", "chung")
        os.makedirs(dich, exist_ok=True)
        n = 0
        for tep in sorted(os.listdir(CHUNG)):
            if not tep.startswith("."):
                shutil.copy2(os.path.join(CHUNG, tep), os.path.join(dich, tep))
                n += 1
        out = os.path.join(ra, ten + ".rcc")
        subprocess.run([sys.executable, os.path.join(GOC, "tools/rcc_repack.py"),
                        cay, out, "--version", "3"], check=True)
        print(f"  ({n} tệp dùng chung)")
        return out
    finally:
        shutil.rmtree(tam)


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    ra = sys.argv[1]
    os.makedirs(ra, exist_ok=True)
    tens = sys.argv[2:] or danh_sach_app()
    if not tens:
        raise SystemExit(f"không thấy mini app nào có tiền tố {TIEN_TO} trong {NGUON}")
    for ten in tens:
        dong_goi(ten, ra)
    print("tên cần thêm vào activities_out.txt: " + " ".join(tens))


if __name__ == "__main__":
    main()
