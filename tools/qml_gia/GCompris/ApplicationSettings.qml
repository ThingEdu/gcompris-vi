/* tools/qml_gia/GCompris/ApplicationSettings.qml — BẢN GIẢ, không phải mã của GCompris.
 *
 * SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
 *   SPDX-License-Identifier: GPL-3.0-or-later
 *
 * Viết lại từ đầu để mô phỏng API của singleton `ApplicationSettings` do
 * C++ của GCompris đăng ký với QML — dùng cho `tools/kiem_qml.py` nạp thử
 * QML mini app trên máy phát triển. KHÔNG PHẢI mã chép về từ mã nguồn
 * GCompris.
 */
pragma Singleton
import QtQuick 2.12
QtObject {
    property bool isAudioVoicesEnabled: true
    property bool isAudioEffectsEnabled: true
    property bool isFullscreen: true
    property bool sectionVisible: true
    property bool isBarHidden: false
    property int baseFontSize: 0
    property real fontLetterSpacing: 0
    property string locale: "vi_VN.UTF-8"
    property string font: "Andika-R.ttf"
    property bool isEmbeddedFont: true
    property int fontCapitalization: 0
    property bool isVirtualKeyboard: false
    property bool isAutomaticDownloadsEnabled: false
    property int filterLevelMin: 1
    property int filterLevelMax: 6
    property bool useExternalWordset: false
    function notifyActivityLevels(a, b, c) {}
    function setFavorite(a, b) {}
}
