/* GCompris - Đối Đôi Làng · chế độ Luật làng
 *
 * SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
 *   SPDX-License-Identifier: GPL-3.0-or-later
 *
 * Ba luật cưỡng chế bằng cơ chế, không bằng lời nhắc:
 *   1. Trong ván KHÔNG hiện số lượt của ai — chỉ đồng hồ và số thẻ còn lại.
 *   2. Số lượt chỉ lộ ở màn kết ván, và chỉ khi chênh lệch quá một phần ba.
 *   3. Người làm Hoa tiêu không có ô bấm được, nên không đường nào ghi lượt.
 */
import QtQuick 2.12
import GCompris 1.0

import "../../core"
import "lang_doidoi.js" as Activity

Item {
    id: man
    property var items

    property int soConLai: 0
    property var theChung: []
    property var theLat: []
    property int nguoiDangChon: -1
    property bool vanXong: false
    property var luot: []
    property bool daGoiY: false
    property int hinhNhay: -1
    property int giay: 0
    property real gocGoiY: 0
    property bool hienGoiY: false
    property var boCucChung: []
    property var boCucLat: []
    property var gocChung: []
    property var gocLat: []

    focus: true
    Keys.onSpacePressed: Activity.goiY(man)

    /* Đồng hồ nhịp: khoá 3 giây sau khi bấm sai là chuyện của Date.now(), mà
     * QML không tự tính lại khi thời gian trôi. Không có nhịp này thì ô bấm
     * sai giữ nguyên màu cánh gián mãi cho tới lần vẽ lại tiếp theo. */
    property int nhip: 0
    Timer {
        interval: 250; running: !man.vanXong; repeat: true
        onTriggered: man.nhip++
    }

    // PHÁN QUYẾT F1: Lang_doidoi.qml dùng Loader { onLoaded: item.items = items },
    // và onLoaded chạy SAU Component.onCompleted của thành phần con. Lúc
    // Component.onCompleted chạy thì items còn undefined — phải đợi onItemsChanged.
    onItemsChanged: {
        if (!items)
            return
        man.audioEffects = items.audioEffects
        man.bonus = items.bonus
        man.soNguoi = items.soNguoi
        man.capKho = items.capKho
        man.hoaTieu = items.hoaTieu
        man.danhMucHinh = items.danhMucHinh
        man.boCuc = items.boCuc
        man.kyLuc = -1
        batDau()
    }

    property var audioEffects
    property var bonus
    property int soNguoi: 2
    property bool capKho: false
    property int hoaTieu: -1
    property var danhMucHinh: []
    property var boCuc: ({})
    property int kyLuc: -1

    function batDau() {
        Activity.batDauVan(man)
        moiBoCuc()
    }

    function moiBoCuc() {
        var soHinh = capKho ? 8 : 6
        var a = Activity.bocucNgauNhien(man, soHinh)
        var b = Activity.bocucNgauNhien(man, soHinh)
        boCucChung = a.boCuc; gocChung = a.goc
        boCucLat = b.boCuc;   gocLat = b.goc
    }

    onTheLatChanged: moiBoCuc()

    Rectangle { anchors.fill: parent; color: "#16264A" }

    // ------------------------------------------------------- thanh trên
    Row {
        id: thanhTren
        anchors { top: parent.top; topMargin: 18; horizontalCenter: parent.horizontalCenter }
        spacing: 70
        GCText {
            fontSize: mediumSize; font.bold: true; color: "#FBF8F1"
            text: "⏱ " + Math.floor(dongHo.giay / 60) + ":" +
                  (dongHo.giay % 60 < 10 ? "0" : "") + (dongHo.giay % 60)
        }
        GCText {
            fontSize: mediumSize; color: "#FBF8F1"
            text: qsTr("Chồng còn %1 thẻ").arg(man.soConLai)
        }
        GCText {
            fontSize: mediumSize; color: "#E8A317"
            visible: man.kyLuc >= 0
            text: qsTr("Kỷ lục %1 giây").arg(man.kyLuc)
        }
    }

    Timer {
        id: dongHo
        property int giay: 0
        interval: 1000; running: !man.vanXong; repeat: true
        onTriggered: giay++
    }

    // ------------------------------------------------------- hai thẻ
    Row {
        anchors.centerIn: parent
        spacing: 60
        The {
            id: theChungHien
            items: man
            width: Math.min(man.width * 0.42, man.height * 0.72)
            height: width
            hinh: man.theChung
            boCuc: man.boCucChung
            goc: man.gocChung
            nhayHinh: man.hinhNhay
            chonDuoc: man.nguoiDangChon >= 0 && !man.vanXong
            onBamHinh: Activity.chonHinh(man, chiSoHinh)
        }
        The {
            id: theLatHien
            items: man
            width: theChungHien.width
            height: width
            hinh: man.theLat
            boCuc: man.boCucLat
            goc: man.gocLat
            nhayHinh: man.hinhNhay
            chonDuoc: man.nguoiDangChon >= 0 && !man.vanXong
            onBamHinh: Activity.chonHinh(man, chiSoHinh)

            // vòng gợi ý của Hoa tiêu: một phần tư thẻ chứa hình trùng
            Rectangle {
                visible: man.hienGoiY
                width: parent.width * 0.5
                height: width
                radius: width / 2
                color: "#33E8A317"
                border { color: "#E8A317"; width: 4 }
                x: parent.width / 2 + Math.cos(man.gocGoiY) * parent.width * 0.28 - width / 2
                y: parent.height / 2 + Math.sin(man.gocGoiY) * parent.height * 0.28 - height / 2
                SequentialAnimation on opacity {
                    running: man.hienGoiY
                    loops: 6
                    NumberAnimation { to: 0.2; duration: 320 }
                    NumberAnimation { to: 1.0; duration: 320 }
                    onFinished: man.hienGoiY = false
                }
            }
        }
    }

    // ------------------------------------------------------- dải người chơi
    Row {
        anchors { bottom: parent.bottom; bottomMargin: 24; horizontalCenter: parent.horizontalCenter }
        spacing: 20
        Repeater {
            model: man.soNguoi
            delegate: Rectangle {
                property bool laHoaTieu: index === man.hoaTieu
                // man.nhip đứng đây để QML tính lại khi đồng hồ nhịp chạy —
                // bỏ nó ra là ô khoá không bao giờ tự sáng lại.
                property bool dangKhoa: man.nhip >= 0 && Activity.biKhoa(index)
                width: 260; height: 92; radius: 10
                color: laHoaTieu ? "#2A3A5C"
                     : index === man.nguoiDangChon ? "#E8A317"
                     : dangKhoa ? "#8A4B24" : "#FBF8F1"
                border {
                    color: laHoaTieu ? "#4A5A7C" : "#141414"
                    width: laHoaTieu ? 1 : 3
                }
                Column {
                    anchors.centerIn: parent
                    spacing: 2
                    GCText {
                        anchors.horizontalCenter: parent.horizontalCenter
                        fontSize: mediumSize; font.bold: !parent.parent.laHoaTieu
                        color: parent.parent.laHoaTieu ? "#8A96AC" : "#141414"
                        text: qsTr("Bạn %1").arg(index + 1)
                    }
                    GCText {
                        anchors.horizontalCenter: parent.horizontalCenter
                        visible: parent.parent.laHoaTieu
                        fontSize: smallSize; color: "#8A96AC"
                        text: man.daGoiY ? qsTr("Hoa tiêu · đã gợi ý")
                                         : qsTr("Hoa tiêu · phím cách")
                    }
                }
                MouseArea {
                    anchors.fill: parent
                    // Hoa tiêu KHÔNG có đường nào ghi lượt: chuột không bật ở đây.
                    enabled: !parent.laHoaTieu && !man.vanXong
                    onClicked: Activity.chonNguoi(man, index)
                }
            }
        }
    }

    // ------------------------------------------------------- màn kết ván
    Rectangle {
        anchors.fill: parent
        color: "#E616264A"
        visible: man.vanXong
        Column {
            anchors.centerIn: parent
            spacing: 26
            GCText {
                anchors.horizontalCenter: parent.horizontalCenter
                fontSize: hugeSize; font.bold: true; color: "#E8A317"
                text: qsTr("Cả bàn thắng!")
            }
            GCText {
                anchors.horizontalCenter: parent.horizontalCenter
                fontSize: mediumSize; color: "#FBF8F1"
                text: qsTr("Phá hết chồng thẻ trong %1 giây").arg(man.giay)
            }
            GCText {
                anchors.horizontalCenter: parent.horizontalCenter
                width: man.width * 0.7
                horizontalAlignment: Text.AlignHCenter
                wrapMode: Text.WordWrap
                fontSize: regularSize; color: "#FBF8F1"
                // Luật 2: số lượt chỉ lộ ra ở đây, và chỉ khi lệch quá 1/3.
                visible: {
                    if (man.luot.length === 0) return false
                    var lon = Math.max.apply(null, man.luot)
                    var nho = Math.min.apply(null, man.luot)
                    var tong = man.capKho ? 56 : 30
                    return (lon - nho) > tong / 3
                }
                text: qsTr("Có bạn gọi được nhiều hơn hẳn các bạn khác. Ván sau nhường nhau một chút nhé — cả bàn cùng thắng mới là thắng.")
            }
            NutTo {
                anchors.horizontalCenter: parent.horizontalCenter
                chu: qsTr("Chơi ván nữa")
                onBam: { dongHo.giay = 0; man.hinhNhay = -1; man.batDau() }
            }
        }
    }
}
