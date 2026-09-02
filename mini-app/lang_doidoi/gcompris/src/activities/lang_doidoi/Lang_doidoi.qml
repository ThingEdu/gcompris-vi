/* GCompris - Đối Đôi Làng
 *
 * SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
 *   SPDX-License-Identifier: GPL-3.0-or-later
 */
import QtQuick 2.12
import GCompris 1.0

import "../../core"
import "lang_doidoi.js" as Activity

ActivityBase {
    id: activity

    onStart: focus = true
    onStop: {}

    pageComponent: Rectangle {
        id: background
        anchors.fill: parent
        color: "#16264A"                     // chàm đậm, nền nhận diện của làng
        focus: true

        signal start
        signal stop

        Component.onCompleted: {
            activity.start.connect(start)
            activity.stop.connect(stop)
        }

        onStart: Activity.start(items)
        onStop: Activity.stop()

        // items là "hộp thư chung" cho toàn bộ hoạt động: màn vào bàn ghi vào
        // đây, HocHinh.qml và LuatLang.qml (nhiệm vụ sau) đọc lại qua Loader.
        QtObject {
            id: items
            property Item main: activity.main
            property alias background: background
            property alias bar: bar
            property alias bonus: bonus
            property GCSfx audioEffects: activity.audioEffects
            property int soNguoi: 3
            property bool capKho: false      // false = 31 thẻ x 6 hình
            property int hoaTieu: -1         // -1 = không ai làm Hoa tiêu
            property string manHienTai: "vao_ban"
            property var danhMucHinh: []     // đọc từ hinh.json
            property var boCuc: ({})         // đọc từ bo_cuc.json
        }

        // ---------------------------------------------------- màn vào bàn
        Column {
            id: manVaoBan
            visible: items.manHienTai === "vao_ban"
            anchors.centerIn: parent
            width: parent.width * 0.8
            spacing: background.height * 0.035

            GCText {
                anchors.horizontalCenter: parent.horizontalCenter
                fontSize: hugeSize
                font.bold: true
                color: "#FBF8F1"
                text: qsTr("Đối Đôi Làng")
            }

            NutHang {
                nhan: qsTr("Mấy người chơi?")
                lua: ["2", "3", "4", "5", "6"]
                dangChon: items.soNguoi - 2
                onChonMuc: items.soNguoi = muc + 2
            }

            NutHang {
                nhan: qsTr("Bộ bài")
                lua: [qsTr("Dễ · 31 thẻ, 6 hình"), qsTr("Khó · 57 thẻ, 8 hình")]
                dangChon: items.capKho ? 1 : 0
                onChonMuc: items.capKho = (muc === 1)
            }

            NutHang {
                nhan: qsTr("Ai làm Hoa tiêu?")
                // "Không ai" đứng đầu, nên chỉ số muc 0 -> hoaTieu = -1
                lua: {
                    var d = [qsTr("Không ai")]
                    for (var i = 0; i < items.soNguoi; i++)
                        d.push(qsTr("Bạn %1").arg(i + 1))
                    return d
                }
                dangChon: items.hoaTieu + 1
                onChonMuc: items.hoaTieu = muc - 1
            }

            Row {
                anchors.horizontalCenter: parent.horizontalCenter
                spacing: 40
                NutTo {
                    chu: qsTr("Vào bàn")
                    onBam: items.manHienTai = "luat_lang"
                }
                NutTo {
                    chu: qsTr("Học hình một mình")
                    onBam: items.manHienTai = "hoc_hinh"
                }
            }
        }

        // Loader nạp LuatLang.qml (đấu cả bàn) hoặc HocHinh.qml (học một mình)
        // — hai tệp này do nhiệm vụ 7 và 8 viết. items được gán SAU khi thành
        // phần con đã Component.onCompleted xong (thứ tự thật của Qt Loader),
        // nên HocHinh.qml/LuatLang.qml phải đọc items qua onItemsChanged chứ
        // không phải Component.onCompleted — xem PHÁN QUYẾT F1 trong brief.
        Loader {
            anchors.fill: parent
            active: items.manHienTai !== "vao_ban"
            source: items.manHienTai === "luat_lang" ? "LuatLang.qml" : "HocHinh.qml"
            onLoaded: item.items = items
        }

        DialogHelp {
            id: dialogHelp
            onClose: home()
        }

        Bar {
            id: bar
            content: BarEnumContent { value: help | home }
            onHelpClicked: displayDialog(dialogHelp)
            onHomeClicked: {
                if (items.manHienTai === "vao_ban")
                    activity.home()
                else
                    items.manHienTai = "vao_ban"
            }
        }

        Bonus { id: bonus }
    }
}
