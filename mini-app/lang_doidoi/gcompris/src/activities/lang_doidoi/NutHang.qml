/* GCompris - Đối Đôi Làng
 *
 * SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
 *   SPDX-License-Identifier: GPL-3.0-or-later
 *
 * Một hàng nút chọn một trong nhiều lựa chọn — dùng cho màn vào bàn.
 */
import QtQuick 2.12
import "../../core"

Row {
    id: hang
    property string nhan: ""
    property var lua: []
    property int dangChon: 0
    signal chonMuc(int muc)

    anchors.horizontalCenter: parent.horizontalCenter
    spacing: 14

    GCText {
        anchors.verticalCenter: parent.verticalCenter
        width: hang.parent.width * 0.22
        horizontalAlignment: Text.AlignRight
        fontSize: regularSize
        color: "#FBF8F1"
        text: hang.nhan
    }

    Repeater {
        model: hang.lua
        Rectangle {
            width: Math.max(96, chu.width + 28)
            height: 56
            radius: 8
            color: index === hang.dangChon ? "#E8A317" : "#1E3357"
            border { color: "#FBF8F1"; width: 2 }
            GCText {
                id: chu
                anchors.centerIn: parent
                fontSize: regularSize
                color: index === hang.dangChon ? "#141414" : "#FBF8F1"
                text: modelData
            }
            MouseArea {
                anchors.fill: parent
                onClicked: hang.chonMuc(index)
            }
        }
    }
}
