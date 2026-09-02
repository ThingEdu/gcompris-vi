/* tools/qml_gia/GCompris/ApplicationInfo.qml — BẢN GIẢ, không phải mã của GCompris.
 *
 * SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
 *   SPDX-License-Identifier: GPL-3.0-or-later
 *
 * Viết lại từ đầu để mô phỏng API của singleton `ApplicationInfo` do C++ của
 * GCompris đăng ký với QML — dùng cho `tools/kiem_qml.py` nạp thử QML mini
 * app trên máy phát triển. KHÔNG PHẢI mã chép về từ mã nguồn GCompris.
 */
pragma Singleton
import QtQuick 2.12
QtObject {
    property int applicationWidth: 1920
    property real ratio: 1.0
    property real fontRatio: 1.0
    property bool isMobile: false
    property bool useOpenGL: false
    property string localeShort: "vi"
    function getResourceDataPath(p) { return p }
    function getAudioFilePath(p) { return p }
    function getAudioFilePathForLocale(p, l) { return p }
    function getLocaleFilePath(p) { return p }
    function screenshot(p) {}
}
