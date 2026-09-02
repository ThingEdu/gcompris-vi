/* tools/qml_gia/GCompris/ActivityInfo.qml — BẢN GIẢ, không phải mã của GCompris.
 *
 * SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
 *   SPDX-License-Identifier: GPL-3.0-or-later
 *
 * Viết lại từ đầu để mô phỏng API của kiểu `ActivityInfo` do C++ của
 * GCompris đăng ký với QML (`ActivityInfoTree.cpp`) — dùng cho
 * `tools/kiem_qml.py` nạp thử QML mini app trên máy phát triển, vì kiểu do
 * C++ đăng ký không nằm trong `core.rcc` nên không nạp được từ đó.
 * KHÔNG PHẢI mã chép về từ mã nguồn GCompris.
 */
import QtQuick 2.12
QtObject {
    property string name; property int difficulty; property string icon
    property string author; property string title; property string description
    property string goal; property string prerequisite; property string manual
    property string credit; property string section; property int createdInVersion
}
