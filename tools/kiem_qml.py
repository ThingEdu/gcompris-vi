#!/usr/bin/env python3
"""Nạp thử QML của một mini app vào LÕI GCOMPRIS THẬT, bằng bộ máy Qt5.

    kiem_qml.py <tên_mini_app> [--core <đường/dẫn/core.rcc>]

    ví dụ:  kiem_qml.py lang_doidoi

VÌ SAO CẦN. Mã QML không có test tự động nào bắt lỗi. Trước đây phải đóng gói,
chép lên NEO One, cài bằng quyền root rồi mở ra nhìn mới biết mình gõ sai một
chữ — mỗi vòng như vậy mất vài phút và cần máy thật. Công cụ này làm việc đó
trong hai giây trên máy phát triển.

CÁCH LÀM — giống hệt cách GCompris nạp hoạt động, không phải mô phỏng:
  1. Đóng gói mini app thành `.rcc` bằng `tools/dong_goi_mini_app.py`.
  2. Nạp `core.rcc` LẤY TỪ MÁY THẬT và `.rcc` vừa đóng gói vào Qt bằng
     `QResource.registerResource` — đúng thứ `ActivityInfoTree.cpp` làm.
  3. Bảo `QQmlComponent` dựng từng tệp `.qml` theo đường dẫn `qrc:`.
Nhờ vậy `ActivityBase`, `Bar`, `Bonus`, `GCText`… là ĐỒ THẬT của GCompris trên
máy đích, không phải bản rút gọn. Chỉ mấy kiểu do C++ đăng ký (`ApplicationInfo`,
`ApplicationSettings`, `File`, `DownloadManager`) là hàng giả ở `tools/qml_gia/`,
vì chúng nằm trong chương trình chứ không nằm trong `.rcc`.

LẤY core.rcc Ở ĐÂU:
    scp neo@192.168.1.28:/usr/share/gcompris-qt/rcc/core.rcc build/
`build/` bị `.gitignore` bỏ qua nên tệp của GCompris không lọt vào kho này.

NÓ BẮT ĐƯỢC GÌ — đã thử bằng cách phá hỏng có chủ đích:
  - lỗi cú pháp (thiếu giá trị, thiếu dấu)              → bắt được
  - gán vào thuộc tính không tồn tại                    → bắt được
  - dùng thành phần lõi không có thật trong core.rcc    → bắt được
  - sai kiểu khi gán, tệp thiếu, import hỏng            → bắt được

NÓ KHÔNG BẮT ĐƯỢC GÌ — cũng đã thử, và nó báo SẠCH cả bốn:
  - `id` treo:            `anchors.centerIn: khong_co_id_nay`
  - gọi hàm không có:     `onClicked: nut.khongCoHamNay()`
  - tên cỡ chữ sai:       `fontSize: coChuKhongCo`
  - mọi định danh lạ khác nằm bên PHẢI dấu hai chấm
Lý do: Qt dựng KIỂU lúc phân tích, nhưng phân giải ĐỊNH DANH trong biểu thức
JavaScript lúc chạy. Muốn chắc tên cỡ chữ thì mở thẳng `GCText.qml` trong
core.rcc mà đối chiếu:
    python3 tools/rcc_extract.py build/core.rcc /tmp/core
    grep "property int .*Size" /tmp/core/*/gcompris/src/core/GCText.qml

Nó cũng mù với hành vi lúc chạy — thứ tự khởi tạo, ràng buộc vòng, thuộc tính
đọc trước khi gán, bố cục có tràn màn hình hay không.

**Kiểm sạch ở đây KHÔNG thay được việc chạy trên NEO One.** Nó chỉ dọn sẵn
nhóm lỗi rẻ tiền để buổi nghiệm thu trên máy thật dành cho những lỗi đáng giá.

Cần PyQt5 trên máy phát triển (`pip install PyQt5`), không cần trên máy đích.
"""
import os
import subprocess
import sys
import tempfile

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GIA = os.path.join(GOC, "tools", "qml_gia")
CORE_MAC_DINH = os.path.join(GOC, "build", "core.rcc")


def tim_core(duong_dan):
    if duong_dan:
        if not os.path.isfile(duong_dan):
            raise SystemExit(f"không thấy {duong_dan}")
        return duong_dan
    if os.path.isfile(CORE_MAC_DINH):
        return CORE_MAC_DINH
    raise SystemExit(
        "Thiếu core.rcc của GCompris. Lấy từ máy đích rồi chạy lại:\n"
        "    scp neo@192.168.1.28:/usr/share/gcompris-qt/rcc/core.rcc build/")


def kiem(ten_app, duong_dan_core=None):
    core = tim_core(duong_dan_core)
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from PyQt5.QtCore import QResource, QUrl
        from PyQt5.QtGui import QGuiApplication
        from PyQt5.QtQml import QQmlComponent, QQmlEngine
    except ImportError:
        raise SystemExit("cần PyQt5 trên máy phát triển: pip install PyQt5")

    nguon = os.path.join(GOC, "mini-app", ten_app,
                         "gcompris/src/activities", ten_app)
    if not os.path.isdir(nguon):
        raise SystemExit(f"không thấy mini app {ten_app} tại {nguon}")

    tam = tempfile.mkdtemp()
    try:
        subprocess.run([sys.executable,
                        os.path.join(GOC, "tools/dong_goi_mini_app.py"),
                        tam, ten_app],
                       check=True, stdout=subprocess.DEVNULL)
        goi = os.path.join(tam, ten_app + ".rcc")

        app = QGuiApplication(sys.argv[:1])          # noqa: F841 phải giữ sống
        for r in (core, goi):
            if not QResource.registerResource(r):
                raise SystemExit(f"Qt không nạp được {r}")

        eng = QQmlEngine()
        eng.addImportPath(GIA)                        # kiểu do C++ đăng ký

        tong = 0
        for t in sorted(f for f in os.listdir(nguon) if f.endswith(".qml")):
            url = QUrl(f"qrc:/gcompris/src/activities/{ten_app}/{t}")
            loi = QQmlComponent(eng, url).errors()
            print(f"  {t:24s} {'sạch' if not loi else str(len(loi)) + ' LỖI'}")
            for e in loi:
                print("      → " + e.toString())
            tong += len(loi)
        return tong
    finally:
        import shutil
        shutil.rmtree(tam)


def main():
    arg = sys.argv[1:]
    if not arg or arg[0].startswith("-"):
        raise SystemExit(__doc__)
    core = None
    if "--core" in arg:
        core = arg[arg.index("--core") + 1]
    tong = kiem(arg[0], core)
    print(f"\ntổng lỗi: {tong}")
    sys.exit(1 if tong else 0)


if __name__ == "__main__":
    main()
