/* tools/qml_gia/GCompris/DownloadManager.qml — BẢN GIẢ, không phải mã của GCompris.
 *
 * SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
 *   SPDX-License-Identifier: GPL-3.0-or-later
 *
 * Viết lại từ đầu để mô phỏng API của singleton `DownloadManager` do C++
 * của GCompris đăng ký với QML — dùng cho `tools/kiem_qml.py` nạp thử QML
 * mini app trên máy phát triển. KHÔNG PHẢI mã chép về từ mã nguồn GCompris.
 */
pragma Singleton
import QtQuick 2.12
QtObject {
    function haveLocalResource(p) { return true }
    function downloadResource(p) { return false }
    function areVoicesRegistered() { return true }
    function getVoicesResourceForLocale(l) { return "" }
}
