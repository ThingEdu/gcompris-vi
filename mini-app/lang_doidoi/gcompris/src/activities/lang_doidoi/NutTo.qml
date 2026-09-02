/* GCompris - Đối Đôi Làng
 *
 * SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
 *   SPDX-License-Identifier: GPL-3.0-or-later
 *
 * Nút bấm to, dùng cho các lệnh chính của màn vào bàn (Vào bàn, Học hình...).
 */
import QtQuick 2.12
import "../../core"

Rectangle {
    id: nut
    property string chu: ""
    // Kiểu mờ hơn — dùng cho lựa chọn PHỤ đứng cạnh một lựa chọn chính (ví
    // dụ màn kết ván Luật ăn thua: "Sang Luật làng" nổi, "Chơi ván nữa" mờ).
    // Mặc định false nên mọi chỗ dùng NutTo trước đây không đổi giao diện.
    property bool nhat: false
    signal bam()

    width: Math.max(260, nhan.width + 60)
    height: 78
    radius: 12
    color: nut.nhat ? "#1E3357" : "#1F7A52"
    border { color: nut.nhat ? "#4A5A7C" : "#FBF8F1"; width: nut.nhat ? 2 : 3 }

    GCText {
        id: nhan
        anchors.centerIn: parent
        fontSize: mediumSize
        font.bold: !nut.nhat
        color: nut.nhat ? "#C9D3E6" : "#FBF8F1"
        text: nut.chu
    }
    MouseArea {
        anchors.fill: parent
        onClicked: nut.bam()
        onPressed: nut.color = nut.nhat ? "#28406A" : "#12958E"
        onReleased: nut.color = nut.nhat ? "#1E3357" : "#1F7A52"
    }
}
