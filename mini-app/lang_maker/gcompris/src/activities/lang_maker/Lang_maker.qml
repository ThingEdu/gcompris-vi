/* GCompris - Làng Maker
 *
 * SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
 *   SPDX-License-Identifier: GPL-3.0-or-later
 */
import QtQuick 2.12
import GCompris 1.0

import "../../core"
import "lang_maker.js" as Activity

ActivityBase {
    id: activity

    onStart: focus = true
    onStop: {}

    pageComponent: Rectangle {
        id: background
        anchors.fill: parent
        color: "#7fc4e8"
        focus: true

        signal start
        signal stop

        Component.onCompleted: {
            activity.start.connect(start)
            activity.stop.connect(stop)
        }

        onStart: Activity.start(items)
        onStop: Activity.stop()

        QtObject {
            id: items
            property Item main: activity.main
            property alias background: background
            property alias bar: bar
            property alias bonus: bonus
            property GCSfx audioEffects: activity.audioEffects
            property bool khamPha: true
            property var diemDaTim: []
            property string loiNhac: ""
            property string tenDangHien: ""
            property string moDangHien: ""
            property int soCauHoi: 0
            property int daLam: 0
        }

        // ------------------------------------------------ lời của bạn Cáo
        Rectangle {
            id: bangNhac
            anchors { top: parent.top; horizontalCenter: parent.horizontalCenter }
            width: Math.min(parent.width * 0.94, chuNhac.width + 40)
            height: chuNhac.height + 20
            radius: 10
            color: "#ffffff"
            opacity: 0.92
            border { color: "#3f7cac"; width: 2 }

            GCText {
                id: chuNhac
                anchors.centerIn: parent
                width: background.width * 0.9
                horizontalAlignment: Text.AlignHCenter
                wrapMode: Text.WordWrap
                fontSizeMode: Text.Fit
                fontSize: regularSize
                color: "#1b3a4b"
                text: items.loiNhac
            }
        }

        // ------------------------------------------------ bức tranh của làng
        Item {
            id: vungTranh
            anchors {
                top: bangNhac.bottom; topMargin: 6
                left: parent.left; right: parent.right
                bottom: bar.top; bottomMargin: 6
            }
        }

        Image {
            id: tranh
            anchors.centerIn: vungTranh
            source: Activity.url + "lang-maker.png"
            // giữ đúng tỉ lệ ảnh; không đặt sourceSize để khỏi vòng lặp ràng buộc
            property real tiLe: sourceSize.height > 0 ? sourceSize.width / sourceSize.height : 1.79
            width: Math.min(vungTranh.width, vungTranh.height * tiLe)
            height: width / tiLe
            smooth: true

            Repeater {
                model: Activity.noiChon
                delegate: Item {
                    property real bk: modelData.r * tranh.width
                    x: modelData.x * tranh.width - bk
                    y: modelData.y * tranh.height - bk
                    width: bk * 2
                    height: bk * 2

                    Rectangle {
                        anchors.fill: parent
                        radius: width / 2
                        color: "#33ffd54f"
                        border.color: "#ffb300"
                        border.width: Math.max(2, parent.bk * 0.14)
                        opacity: items.diemDaTim.indexOf(modelData.ma) !== -1 ? 1 : 0
                        Behavior on opacity { NumberAnimation { duration: 250 } }
                    }

                    MouseArea {
                        anchors.fill: parent
                        onClicked: Activity.chamVao(modelData.ma)
                    }
                }
            }
        }

        // ------------------------------------------------ tên và mô tả nơi vừa chạm
        Rectangle {
            id: bangTen
            // đè lên mép dưới bức tranh, không chiếm chỗ, để tranh to hết cỡ
            anchors { bottom: tranh.bottom; horizontalCenter: tranh.horizontalCenter }
            width: tranh.width * 0.96
            height: Math.max(background.height * 0.13, 70)
            radius: 10
            color: "#ffffff"
            opacity: items.tenDangHien === "" ? 0 : 0.94
            border { color: "#3f7cac"; width: 2 }
            Behavior on opacity { NumberAnimation { duration: 200 } }

            Column {
                anchors.centerIn: parent
                width: parent.width - 30
                spacing: 4
                GCText {
                    width: parent.width
                    horizontalAlignment: Text.AlignHCenter
                    fontSize: mediumSize
                    color: "#1b3a4b"
                    font.bold: true
                    text: items.tenDangHien
                }
                GCText {
                    width: parent.width
                    horizontalAlignment: Text.AlignHCenter
                    wrapMode: Text.WordWrap
                    fontSizeMode: Text.Fit
                    fontSize: regularSize
                    color: "#1b3a4b"
                    text: items.moDangHien
                }
            }
        }

        Score {
            id: diem
            anchors {
                top: tranh.top
                right: tranh.right
                rightMargin: 8
                topMargin: 8
                bottom: undefined
                left: undefined
            }
            numberOfSubLevels: items.soCauHoi
            currentSubLevel: items.daLam
        }

        DialogHelp {
            id: dialogHelp
            onClose: home()
        }

        Bar {
            id: bar
            content: BarEnumContent { value: help | home | level | reload }
            onHelpClicked: displayDialog(dialogHelp)
            onPreviousLevelClicked: Activity.capTruoc()
            onNextLevelClicked: Activity.capTiep()
            onReloadClicked: Activity.lamLai()
            onHomeClicked: activity.home()
        }

        Bonus {
            id: bonus
            Component.onCompleted: win.connect(Activity.capTiep)
        }
    }
}
