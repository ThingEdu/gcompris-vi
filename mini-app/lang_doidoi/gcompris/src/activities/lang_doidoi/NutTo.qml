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
    signal bam()

    width: Math.max(260, nhan.width + 60)
    height: 78
    radius: 12
    color: "#1F7A52"
    border { color: "#FBF8F1"; width: 3 }

    GCText {
        id: nhan
        anchors.centerIn: parent
        fontSize: mediumSize
        font.bold: true
        color: "#FBF8F1"
        text: nut.chu
    }
    MouseArea {
        anchors.fill: parent
        onClicked: nut.bam()
        onPressed: nut.color = "#12958E"
        onReleased: nut.color = "#1F7A52"
    }
}
