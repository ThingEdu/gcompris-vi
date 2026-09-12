#!/usr/bin/env python3
"""Thêm mục "Tiếng Việt" vào LanguageList.qml trong cây đã bung từ core.rcc.

Đặt locale trong tệp cấu hình là CHƯA ĐỦ. `ApplicationInfo::loadTranslation()`
đối chiếu locale với danh sách này và đẩy mọi ngôn ngữ lạ về mặc định
(qresource... thực ra là ApplicationInfo.cpp:359), in ra dòng
`locale "vi_VN.UTF-8" not supported, defaulting to system`. Tham số dòng lệnh
`--locale` cũng qua đúng cửa ải đó (main.cpp, `supportedLocales()`), nên không
né được bằng cách gọi khác — phải vá danh sách.

May là LanguageList.qml nằm trong core.rcc chứ không nằm trong tệp thực thi,
nên chỉ cần bung ra, chèn một dòng, đóng lại.

    them_tieng_viet.py <thư_mục_đã_bung_core.rcc>

SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
SPDX-License-Identifier: GPL-3.0-or-later
"""
import os
import re
import sys

LOCALE = "vi_VN.UTF-8"
MUC = '            { "text": "Tiếng Việt", "locale": "%s" },\n' % LOCALE
# chèn ngay sau mục "system" — mục đầu danh sách, có ở mọi đời GCompris
NEO = re.compile(r'^.*"locale":\s*"system"\s*\},\n', re.M)


def tim_danh_sach(goc):
    for thu_muc, _, tep in os.walk(goc):
        if "LanguageList.qml" in tep:
            return os.path.join(thu_muc, "LanguageList.qml")
    return None


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    qml = tim_danh_sach(sys.argv[1])
    if not qml:
        raise SystemExit("không thấy LanguageList.qml — đây có phải cây bung từ core.rcc?")
    s = open(qml, encoding="utf-8").read()
    if LOCALE in s:
        print("LanguageList.qml đã có tiếng Việt, giữ nguyên")
        return
    m = NEO.search(s)
    if not m:
        raise SystemExit("không tìm thấy mục 'system' trong LanguageList.qml")
    open(qml, "w", encoding="utf-8").write(s[:m.end()] + MUC + s[m.end():])
    print(f"thêm Tiếng Việt vào {qml}")


if __name__ == "__main__":
    main()
