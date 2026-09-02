#!/usr/bin/env python3
"""Phân tích cú pháp QML của một mini app bằng chính bộ máy Qt5.

    kiem_qml.py <tên_mini_app>        # ví dụ: kiem_qml.py lang_doidoi

VÌ SAO CẦN. Mã QML của GCompris chỉ chạy được trên máy có GCompris, mà lỗi
QML thì không có test tự động nào bắt. Trước đây phải cài lên NEO One rồi mở
ra nhìn mới biết gõ sai một chữ. Công cụ này bắt phần lớn lỗi đó ngay trên máy
phát triển, trong vài giây.

CÁCH LÀM. Dựng một cây thư mục tạm đúng dạng `gcompris/src/{core,activities/<app>}`
để đường dẫn tương đối `../../core` trong mã phân giải được, đặt vào đó bộ
KHUNG GIẢ ở `tools/qml_gia/` (ActivityBase, Bar, Bonus, GCText… rút gọn), rồi
bảo `QQmlComponent` phân tích từng tệp.

NÓ BẮT ĐƯỢC GÌ — đã thử bằng cách phá hỏng có chủ đích:
  - lỗi cú pháp (thiếu giá trị, thiếu dấu)      → bắt được
  - gán vào thuộc tính không tồn tại            → bắt được
  - tệp thiếu, import hỏng, sai kiểu khi gán    → bắt được

NÓ KHÔNG BẮT ĐƯỢC GÌ — cũng đã thử, và nó báo SẠCH:
  - `id` treo: `anchors.centerIn: khong_co_id_nay`
  - gọi hàm không tồn tại: `onClicked: nut.khongCoHamNay()`
Lý do: QML phân giải biểu thức JavaScript lúc CHẠY, không phải lúc phân tích.
Ngoài ra nó mù hoàn toàn với hành vi lúc chạy — thứ tự khởi tạo, ràng buộc
vòng, thuộc tính đọc trước khi gán — và với mọi khác biệt giữa khung giả ở
`tools/qml_gia/` với GCompris thật.

**Kiểm sạch ở đây KHÔNG thay được việc chạy trên NEO One.** Nó chỉ làm cho
việc chạy thật đỡ tốn công vì đã loại sẵn nhóm lỗi rẻ tiền.

Cần PyQt5 (`pip install PyQt5`), không cần trên máy đích.
"""
import os
import shutil
import sys
import tempfile

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GIA = os.path.join(GOC, "tools", "qml_gia")


def kiem(ten_app):
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from PyQt5.QtCore import QUrl
        from PyQt5.QtGui import QGuiApplication
        from PyQt5.QtQml import QQmlComponent, QQmlEngine
    except ImportError:
        raise SystemExit("cần PyQt5: pip install PyQt5")

    nguon = os.path.join(GOC, "mini-app", ten_app,
                         "gcompris/src/activities", ten_app)
    if not os.path.isdir(nguon):
        raise SystemExit(f"không thấy {nguon}")

    tam = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(tam, "gcompris/src/activities"))
        shutil.copytree(os.path.join(GIA, "core"),
                        os.path.join(tam, "gcompris/src/core"))
        shutil.copytree(nguon,
                        os.path.join(tam, "gcompris/src/activities", ten_app))

        app = QGuiApplication(sys.argv[:1])          # noqa: F841 giữ sống
        eng = QQmlEngine()
        eng.addImportPath(GIA)                       # để "import GCompris 1.0" chạy

        dich = os.path.join(tam, "gcompris/src/activities", ten_app)
        tong = 0
        for t in sorted(f for f in os.listdir(dich) if f.endswith(".qml")):
            c = QQmlComponent(eng, QUrl.fromLocalFile(os.path.join(dich, t)))
            loi = c.errors()
            print(f"  {t:24s} {'sạch' if not loi else str(len(loi)) + ' LỖI'}")
            for e in loi:
                print("      → " + e.toString().replace(tam, ""))
            tong += len(loi)
        return tong
    finally:
        shutil.rmtree(tam)


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    tong = kiem(sys.argv[1])
    print(f"\ntổng lỗi: {tong}")
    sys.exit(1 if tong else 0)


if __name__ == "__main__":
    main()
