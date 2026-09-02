/* GCompris - Đối Đôi Làng · một thẻ tròn
 *
 * SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
 *   SPDX-License-Identifier: GPL-3.0-or-later
 *
 * Bố cục (x, y, r) tính trong ĐĨA ĐƠN VỊ: tâm thẻ (0,0), mép thẻ bán kính 1.
 * Nhân với bán kính thẻ thật để ra pixel. Xoay từng hình quanh tâm của chính
 * nó nên không đổi đường tròn bao — bất biến "không đè nhau" đã kiểm lúc dựng
 * vẫn còn nguyên.
 */
import QtQuick 2.12
import "lang_doidoi.js" as Activity

Item {
    id: the

    property var items
    property var hinh: []           // chỉ số hình 0-based trong bộ 57
    property var boCuc: []          // [[x, y, r], …] cùng độ dài với hinh
    property var goc: []            // góc xoay từng hình, tính bằng độ
    property bool chonDuoc: true
    property int nhayHinh: -1       // chỉ số hình đang nhấp nháy, -1 là không

    signal bamHinh(int chiSoHinh)

    property real banKinh: Math.min(width, height) / 2

    Rectangle {
        anchors.centerIn: parent
        width: the.banKinh * 2
        height: width
        radius: width / 2
        color: "#FBF8F1"
        border { color: "#141414"; width: 3 }
    }

    Repeater {
        model: the.hinh.length
        delegate: Item {
            // boCuc[index] = [x, y, r] trong đĩa đơn vị
            property real bk: the.boCuc[index][2] * the.banKinh
            x: the.width / 2 + the.boCuc[index][0] * the.banKinh - bk
            y: the.height / 2 + the.boCuc[index][1] * the.banKinh - bk
            width: bk * 2
            height: bk * 2

            Image {
                id: anh
                anchors.fill: parent
                source: Activity.duongDanHinh(the.items, the.hinh[index])
                sourceSize.width: 256
                sourceSize.height: 256
                rotation: the.goc.length > index ? the.goc[index] : 0
                smooth: true
            }

            Rectangle {
                anchors.fill: parent
                radius: width / 2
                color: "transparent"
                border { color: "#E8A317"; width: Math.max(3, parent.bk * 0.12) }
                opacity: the.nhayHinh === the.hinh[index] ? 1 : 0
                SequentialAnimation on scale {
                    running: the.nhayHinh === the.hinh[index]
                    loops: Animation.Infinite
                    NumberAnimation { to: 1.15; duration: 300 }
                    NumberAnimation { to: 1.0; duration: 300 }
                }
                Behavior on opacity { NumberAnimation { duration: 150 } }
            }

            MouseArea {
                anchors.fill: parent
                enabled: the.chonDuoc
                onClicked: the.bamHinh(the.hinh[index])
            }
        }
    }
}
