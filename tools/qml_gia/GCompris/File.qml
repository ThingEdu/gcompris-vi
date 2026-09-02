/* tools/qml_gia/GCompris/File.qml — BẢN GIẢ, không phải mã của GCompris.
 *
 * SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
 *   SPDX-License-Identifier: GPL-3.0-or-later
 *
 * Viết lại từ đầu để mô phỏng API của kiểu `File` do C++ của GCompris đăng
 * ký với QML — dùng cho `tools/kiem_qml.py` nạp thử QML mini app trên máy
 * phát triển. KHÔNG PHẢI mã chép về từ mã nguồn GCompris.
 */
import QtQuick 2.12
QtObject {
    property string name
    function exists(p) { return false }
    function read(p) { return "" }
    function write(d, p) { return false }
    function append(d, p) { return false }
    function rmpath(p) { return false }
    function mkpath(p) { return false }
}
