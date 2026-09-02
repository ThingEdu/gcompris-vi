/* GCompris - Đối Đôi Làng · chế độ Học hình
 *
 * SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
 *   SPDX-License-Identifier: GPL-3.0-or-later
 *
 * Hiện TÊN bằng chữ, con chọn HÌNH đúng trong ba hình. Hoạt động này đòi hỏi
 * đọc được tiếng Việt — đã ghi ở prerequisite của ActivityInfo.qml. Em chưa
 * đọc được thì anh chị áo xanh đọc hộ. Không có giọng đọc — quyết định đã
 * chốt của chủ dự án, không phải thiếu sót.
 */
import QtQuick 2.12
import GCompris 1.0

import "../../core"
import "lang_doidoi.js" as Activity

Item {
    id: man
    property var items

    property int muc: 0
    property int daLam: 0
    property var cauHoi: null
    property int hienNghia: -1

    property var danhMucHinh: []

    // PHÁN QUYẾT F1 (task-8-brief.md): Lang_doidoi.qml dùng
    // Loader { onLoaded: item.items = items }, và onLoaded chạy SAU
    // Component.onCompleted của thành phần con. Lúc Component.onCompleted
    // chạy thì items còn undefined — đọc items.danhMucHinh ở đó làm app hỏng
    // ngay khi vào chế độ Học hình. Phải đợi onItemsChanged.
    onItemsChanged: {
        if (!items)
            return
        danhMucHinh = items.danhMucHinh
        cauMoi()
    }

    function cauMoi() {
        hienNghia = -1
        cauHoi = Activity.sinhCauHoi(man, muc)
    }

    // Chọn sai thì hình phải rung. Delegate không gọi ngược lên được, nên màn
    // phát tín hiệu và delegate nào trùng chỉ số thì tự rung.
    signal rungHinh(int chiSo)

    function chon(chiSo) {
        if (!cauHoi)
            return
        if (chiSo === cauHoi.dung) {
            hienNghia = chiSo
            items.audioEffects.play("qrc:/gcompris/src/core/resource/sounds/win.wav")
            daLam++
            if (daLam >= 10) {
                daLam = 0
                muc = (muc + 1) % 5
                items.bonus.good("flower")
            }
            hetGio.restart()
        } else {
            items.audioEffects.play("qrc:/gcompris/src/core/resource/sounds/brick.wav")
            man.rungHinh(chiSo)
        }
    }

    Timer { id: hetGio; interval: 1400; onTriggered: man.cauMoi() }

    Rectangle { anchors.fill: parent; color: "#16264A" }

    Column {
        anchors.centerIn: parent
        spacing: man.height * 0.05
        width: man.width * 0.9

        GCText {
            anchors.horizontalCenter: parent.horizontalCenter
            fontSize: regularSize; color: "#8A96AC"
            text: qsTr("Mức %1 · câu %2 trên 10").arg(man.muc + 1).arg(man.daLam + 1)
        }

        GCText {
            anchors.horizontalCenter: parent.horizontalCenter
            fontSize: hugeSize; font.bold: true; color: "#E8A317"
            text: man.cauHoi ? man.danhMucHinh[man.cauHoi.dung].ten : ""
        }

        Row {
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: 50
            Repeater {
                model: man.cauHoi ? man.cauHoi.lua : []
                delegate: Rectangle {
                    width: man.height * 0.30; height: width
                    radius: width / 2
                    color: "#FBF8F1"
                    border { color: "#141414"; width: 3 }
                    scale: man.hienNghia === modelData ? 1.12 : 1.0
                    Behavior on scale { NumberAnimation { duration: 180 } }

                    Image {
                        anchors.centerIn: parent
                        width: parent.width * 0.74; height: width
                        source: Activity.duongDanHinh(man, modelData)
                        sourceSize.width: 256; sourceSize.height: 256
                        smooth: true
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: man.chon(modelData)
                    }
                    // Rung bằng Translate, KHÔNG bằng x: hình nằm trong Row nên
                    // Row tự đặt x, animation trên x sẽ đánh nhau với bố cục.
                    transform: Translate { id: dich }
                    SequentialAnimation {
                        id: rung
                        NumberAnimation { target: dich; property: "x"; to: 12; duration: 60 }
                        NumberAnimation { target: dich; property: "x"; to: -12; duration: 60 }
                        NumberAnimation { target: dich; property: "x"; to: 0; duration: 60 }
                    }
                    Connections {
                        target: man
                        onRungHinh: if (chiSo === modelData) rung.restart()
                    }
                }
            }
        }

        GCText {
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width * 0.7
            horizontalAlignment: Text.AlignHCenter
            wrapMode: Text.WordWrap
            fontSize: mediumSize; color: "#FBF8F1"
            opacity: man.hienNghia >= 0 ? 1 : 0
            Behavior on opacity { NumberAnimation { duration: 200 } }
            text: man.hienNghia >= 0 && man.danhMucHinh.length > 0 ? man.danhMucHinh[man.hienNghia].nghia : ""
        }
    }
}
