/* GCompris - Đối Đôi Làng · chế độ Luật làng
 *
 * SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
 *   SPDX-License-Identifier: GPL-3.0-or-later
 *
 * Bố cục ván: MỘT thẻ chung cố định giữa màn cộng thẻ riêng của từng người
 * bày thành hàng dưới, tất cả hiện cùng lúc (xem DOCS/MINI_APP_DOI_DOI_LANG.md
 * mục "Chia bài"/"Một lượt"/mục 8).
 *
 * Ba luật cưỡng chế bằng cơ chế, không bằng lời nhắc:
 *   1. Trong ván KHÔNG hiện số lượt của ai — chỉ đồng hồ và số thẻ còn lại.
 *   2. Số lượt chỉ lộ ở màn kết ván, chỉ khi chênh lệch vượt quá một phần ba
 *      TỔNG SỐ THẺ CỦA CHỒNG (phụ thuộc cả số người: (capKho?56:30) - soNguoi).
 *   3. Người làm Hoa tiêu không có ô bấm được, nên không đường nào ghi lượt.
 *      Gợi ý của em chỉ bật được sau khi đã tick một người, và mỗi thẻ riêng
 *      chỉ dùng được một lần (thẻ mới rút lên lại được gợi ý một lần nữa).
 */
import QtQuick 2.12
import GCompris 1.0

import "../../core"
import "lang_doidoi.js" as Activity

Item {
    id: man
    property var items

    property int soConLai: 0

    // Thẻ chung: cố định suốt ván, bố cục/goc tính một lần lúc chia bài.
    property var theChung: []
    property var boCucChung: []
    property var gocChung: []

    // Thẻ riêng: soNguoi phần tử — cùng chỉ số với dải người chơi dưới màn.
    // Mặc định [] để mọi ràng buộc khai báo đọc trước khi batDauVan() chạy
    // (Repeater dựng theo man.soNguoi có thể xảy ra trước) đều ra mảng rỗng,
    // không bao giờ ra undefined — xem bẫy 2 trong brief.
    property var theRieng: []
    property var boCucRieng: []
    property var gocRieng: []

    property int nguoiDangChon: -1
    property bool vanXong: false
    property var luot: []
    property var daGoiY: []          // theo TỪNG người

    property int hinhNhay: -1        // chỉ số hình đang nháy, -1 = không
    property int hinhNhayNguoi: -1   // người sở hữu thẻ riêng đang nháy cùng
    property int giay: 0

    property real gocGoiY: 0
    property int goiYNguoi: -1       // người đang được Hoa tiêu gợi ý
    property bool hienGoiY: false

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
        // Chia bài + tính hết bố cục (thẻ chung MỘT LẦN, mỗi thẻ riêng một
        // lần) đều nằm trong lang_doidoi.js — capNhat() ở cuối đổ thẳng vào
        // các property trên, không còn bước "moiBoCuc()" phản ứng riêng ở
        // phía QML như bản trước (thẻ lật không còn tồn tại).
        Activity.batDauVan(man)
    }

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

    // Đường kính thẻ riêng co theo số người, luôn vừa bề ngang 1840px hữu
    // dụng (1920 trừ lề hai bên) — công thức đúng nguyên văn spec mục 8.
    property real duongKinhRieng: Math.min(380, (1840 - 20 * (man.soNguoi - 1)) / Math.max(1, man.soNguoi))

    // ------------------------------------------------------- vùng chơi
    // VÒNG SỬA 1: trên NEO One thật, GCompris tự vẽ thanh nút (Bar) ở góc
    // dưới màn — bản dựng trên Mac không có Bar (chỉ LuatLang.qml, không đi
    // qua Lang_doidoi.qml) nên không lộ ra Bar che mất "Bạn 1"/"Bạn 2" khi
    // hàng thẻ riêng neo thẳng vào parent.bottom.
    //
    // lang_maker (mini-app/lang_maker/.../Lang_maker.qml:78-81) né Bar bằng
    // `anchors.bottom: bar.top` — làm được vì ở đó vùng tranh và Bar là HAI
    // ANH EM ruột cùng một tệp. Ở đây thì KHÔNG: LuatLang.qml được Lang_doidoi.qml
    // nạp qua Loader, nên "man" (và mọi thứ bên trong nó, kể cả vungChoi) nằm
    // sâu hơn Bar một cấp — không phải cha/con/anh em của Bar theo đúng nghĩa
    // QML. Thử `anchors.bottom: items.bar.top` bắn lỗi runtime thật
    // "Cannot anchor to an item that isn't a parent or sibling" (đã thấy khi
    // dựng thử) — QML cấm neo (anchor) xuyên qua ranh giới Loader kiểu này,
    // dù đọc property THƯỜNG (không phải anchor) thì lại được.
    //
    // Nên né Bar bằng SỐ, không bằng AnchorLine: cộng thêm chiều cao thật
    // của Bar (items.bar.height — đọc property thường, không giới hạn cha/con)
    // vào bottomMargin của vungChoi, đáy vungChoi vẫn neo vào parent.bottom
    // của chính "man" (== đáy màn, vì Loader tự giãn "man" khớp đúng
    // background). man.height và bar.height cùng một hệ toạ độ (man được
    // Loader giãn khớp "background", bar cũng là con của "background"), nên
    // phép cộng số học này ra đúng vị trí, bất kể Bar thật cao bao nhiêu.
    // items.bar chỉ có sau khi Loader gán items (PHÁN QUYẾT F1) — items có
    // thể còn null/chưa có "bar" lúc ràng buộc này chạy lần đầu, gác bằng
    // toán tử bậc ba, coi như Bar cao 0 cho tới khi items.bar có thật.
    Item {
        id: vungChoi
        anchors {
            top: thanhTren.bottom; topMargin: 8
            left: parent.left; right: parent.right
            bottom: parent.bottom
            bottomMargin: 16 + ((man.items && man.items.bar) ? man.items.bar.height : 0)
        }

        // Thẻ chung + hàng thẻ riêng gộp thành MỘT khối, canh giữa trong
        // vùng chơi còn lại (giữa thanh trên và Bar). Trước đây thẻ chung
        // neo topMargin cố định 34px còn hàng riêng neo đáy màn cố định —
        // trên máy thật khoảng trống giữa hai khối hoá ra rất rộng vì phần
        // dành cho Bar bị tính nhầm là "chỗ chơi". Gộp vào Column canh giữa
        // thì khoảng trống thật (nếu có) chia đều hai đầu vùng chơi thay vì
        // dồn hết vào giữa hai khối — không cần đoán chiều cao Bar thật.
        Column {
            id: khoiVanChoi
            anchors.centerIn: parent
            spacing: 40

            The {
                id: theChungHien
                items: man
                anchors.horizontalCenter: parent.horizontalCenter
                // 420px đúng số spec mục 8 — KHÔNG tăng lên dù còn dư chỗ:
                // chưa biết chính xác Bar thật trên NEO One cao bao nhiêu
                // (chỉ có ô giả 560×130 để kiểm bằng mắt trên Mac), tăng theo
                // số đo giả có thể sai trên máy thật. Xem task-10-report.md.
                width: 420; height: 420
                hinh: man.theChung
                boCuc: man.boCucChung
                goc: man.gocChung
                nhayHinh: man.hinhNhay
                chonDuoc: man.nguoiDangChon >= 0 && !man.vanXong
                onBamHinh: Activity.chonHinh(man, chiSoHinh)
            }

            // ------------------------------------------- dải thẻ riêng + tên
            Row {
                id: hangRieng
                anchors.horizontalCenter: parent.horizontalCenter
                spacing: 20
                Repeater {
                    model: man.soNguoi
                    // VÒNG SỬA 2: chủ dự án gợi ý đặt Ô TÊN LÊN TRÊN thẻ riêng
                    // (trước ở dưới) — thanh Bar nằm ở góc dưới TRÁI màn hình,
                    // đặt tên lên trên đẩy cả khối lên cao, chừa hẳn phần đáy
                    // trống cho Bar, không phải thu nhỏ thẻ để né.
                    delegate: Column {
                        id: oNguoi
                        spacing: 8
                        property bool laHoaTieu: index === man.hoaTieu
                        property bool dangChonToi: index === man.nguoiDangChon
                        // man.nhip đứng đây để QML tính lại khi đồng hồ nhịp chạy —
                        // bỏ nó ra là ô khoá không bao giờ tự sáng lại.
                        property bool dangKhoa: man.nhip >= 0 && Activity.biKhoa(index)

                        // Ô tên: chỗ bấm để tick. Hoa tiêu = thẻ ghi chú xám, không
                        // nhận click — không có đường nào ghi lượt cho em (luật 3).
                        // Trên/dưới tên KHÔNG có con số nào (luật 1).
                        Rectangle {
                            id: oTen
                            anchors.horizontalCenter: parent.horizontalCenter
                            width: man.duongKinhRieng; height: 64; radius: 10
                            color: laHoaTieu ? "#2A3A5C"
                                 : dangChonToi ? "#E8A317"
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
                                    fontSize: smallSize; font.bold: !laHoaTieu
                                    color: laHoaTieu ? "#8A96AC" : "#141414"
                                    text: qsTr("Bạn %1").arg(index + 1)
                                }
                                GCText {
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    visible: laHoaTieu
                                    fontSize: tinySize; color: "#8A96AC"
                                    // "đã gợi ý" theo TỪNG thẻ (man.daGoiY[index]) — thẻ
                                    // mới rút lên lại đặt lại false, lại hiện "phím cách".
                                    text: (index < man.daGoiY.length && man.daGoiY[index])
                                          ? qsTr("Hoa tiêu · đã gợi ý")
                                          : qsTr("Hoa tiêu · phím cách")
                                }
                            }
                            MouseArea {
                                anchors.fill: parent
                                // Hoa tiêu KHÔNG có đường nào ghi lượt: chuột không bật ở đây.
                                enabled: !laHoaTieu && !man.vanXong
                                onClicked: Activity.chonNguoi(man, index)
                            }
                        }

                        The {
                            id: theRiengHien
                            items: man
                            anchors.horizontalCenter: parent.horizontalCenter
                            width: man.duongKinhRieng; height: width
                            // index luôn nằm trong [0, soNguoi), nhưng mảng theRieng
                            // có thể còn rỗng nếu ràng buộc này chạy trước khi
                            // Activity.batDauVan() kịp đổ dữ liệu vào — ra [] thay vì
                            // undefined để The.qml không vỡ ở the.hinh.length.
                            hinh: index < man.theRieng.length ? man.theRieng[index] : []
                            boCuc: index < man.boCucRieng.length ? man.boCucRieng[index] : []
                            goc: index < man.gocRieng.length ? man.gocRieng[index] : []
                            // Chỉ thẻ riêng của người vừa được ghi lượt mới nháy cùng
                            // thẻ chung — hình trùng số có thể tình cờ xuất hiện trên
                            // thẻ của người khác, không được nháy lây.
                            nhayHinh: index === man.hinhNhayNguoi ? man.hinhNhay : -1
                            chonDuoc: oNguoi.dangChonToi && !man.vanXong
                            onBamHinh: Activity.chonHinh(man, chiSoHinh)

                            // vòng gợi ý của Hoa tiêu: một phần tư thẻ riêng của
                            // người đang được tick — phần tư chứa hình trùng thẻ chung.
                            Rectangle {
                                visible: man.hienGoiY && index === man.goiYNguoi
                                width: parent.width * 0.5
                                height: width
                                radius: width / 2
                                color: "#33E8A317"
                                border { color: "#E8A317"; width: 4 }
                                x: parent.width / 2 + Math.cos(man.gocGoiY) * parent.width * 0.28 - width / 2
                                y: parent.height / 2 + Math.sin(man.gocGoiY) * parent.height * 0.28 - height / 2
                                SequentialAnimation on opacity {
                                    running: man.hienGoiY && index === man.goiYNguoi
                                    loops: 6
                                    NumberAnimation { to: 0.2; duration: 320 }
                                    NumberAnimation { to: 1.0; duration: 320 }
                                    onFinished: man.hienGoiY = false
                                }
                            }
                        }
                    }
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
                // Luật 2: số lượt chỉ lộ ra ở đây, và chỉ khi lệch quá 1/3
                // TỔNG SỐ THẺ CỦA CHỒNG — tổng này trừ cả soNguoi, không phải
                // hằng số 30/56 như bản trước.
                visible: {
                    if (man.luot.length === 0) return false
                    var lon = Math.max.apply(null, man.luot)
                    var nho = Math.min.apply(null, man.luot)
                    var tong = (man.capKho ? 56 : 30) - man.soNguoi
                    return (lon - nho) > tong / 3
                }
                text: qsTr("Có bạn gọi được nhiều hơn hẳn các bạn khác. Ván sau nhường nhau một chút nhé — cả bàn cùng thắng mới là thắng.")
            }
            NutTo {
                anchors.horizontalCenter: parent.horizontalCenter
                chu: qsTr("Chơi ván nữa")
                onBam: { dongHo.giay = 0; man.batDau() }
            }
        }
    }
}
