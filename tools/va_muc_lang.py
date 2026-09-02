#!/usr/bin/env python3
"""Thêm mục "Làng Maker" vào hàng biểu tượng đầu màn hình chính của GCompris.

Hàng mục đó là một mảng JS thuần trong `Menu.qml`, mà `Menu.qml` nằm trong
`menu.rcc` — cũng là tệp ngoài như mọi gói tài nguyên khác. Nên thêm mục mới
chỉ là chèn một phần tử vào mảng, không phải biên dịch lại.

GCompris lọc hoạt động theo mục bằng `activity->section().indexOf(tag)`
(`ActivityInfoTree::filterByTag`) — tức là tìm chuỗi con. Vì vậy một hoạt động
ghi `section: "langmaker discovery"` sẽ hiện ở CẢ mục Làng Maker lẫn mục Khám
phá. Không mục nào của bản gốc chứa chuỗi "langmaker" nên không đụng nhau.

Lưu ý: KHÔNG dùng được mục mặt trời (Yêu thích) làm chỗ mặc định. `ActivityInfo`
đọc lại cờ yêu thích từ thiết lập của người dùng ngay sau khi dựng
(`ActivityInfo.cpp:48`), nên giá trị khai trong `ActivityInfo.qml` bị ghi đè.

    va_muc_lang.py <thư_mục_đã_bung_menu.rcc>
"""
import os
import sys

TAG = "langmaker"
MOI = '''        {
            icon: "qrc:/gcompris/src/activities/lang_maker/resource/chung/neo_tre.svg",
            tag: "%s"
        },
''' % TAG
NEO = '''        {
            icon: activity.url + "all.svg",
            tag: "favorite"
        },
'''
# Bề rộng ô mục: bản gốc chia cho (số mục + 1) rồi nhân 1,1 thành bề rộng ô,
# vừa khít đúng 10 mục. Thêm mục thứ 11 là tràn, mục cuối (Tìm kiếm) bị đẩy ra
# khỏi màn hình. Chia cho (số mục × 1,15) thì tổng bề rộng luôn bằng 96% màn
# hình, đúng với mọi số mục. Phải sửa cả bốn chỗ: khai mặc định và ba state
# ghi đè lại (nằm ngang, dựng đứng, có bàn phím ảo) — sửa mỗi chỗ đầu thì state
# ghi đè lên, mục thứ 11 vẫn bị cắt.
RONG_CU = "/ (sections.length + 1))"
RONG_MOI = "/ (sections.length * 1.15))"
SO_CHO = 4      # một chỗ khai mặc định, ba chỗ trong các state ghi đè lại


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    qml = os.path.join(sys.argv[1], "gcompris/src/activities/menu/Menu.qml")
    if not os.path.exists(qml):
        raise SystemExit(f"không thấy {qml} — đây có phải cây bung từ menu.rcc?")
    s = open(qml, encoding="utf-8").read()
    if TAG in s:
        print("Menu.qml đã có mục Làng Maker, bỏ qua")
        return
    if NEO not in s:
        raise SystemExit("không nhận ra mảng mục trong Menu.qml")
    # đặt ngay sau mục Yêu thích để dễ thấy; muốn dời chỗ thì đổi mỏ neo này
    s = s.replace(NEO, NEO + MOI, 1)
    n = s.count(RONG_CU)
    if n != SO_CHO:
        raise SystemExit(f"chờ {SO_CHO} chỗ công thức bề rộng ô mục, thấy {n}")
    s = s.replace(RONG_CU, RONG_MOI)
    open(qml, "w", encoding="utf-8").write(s)
    print(f"thêm mục {TAG} và nới bề rộng ô mục trong {qml}")


if __name__ == "__main__":
    main()
