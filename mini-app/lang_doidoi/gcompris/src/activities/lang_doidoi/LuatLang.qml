/* GCompris - Đối Đôi Làng · chế độ Luật làng + Luật ăn thua
 *
 * SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
 *   SPDX-License-Identifier: GPL-3.0-or-later
 *
 * Bố cục ván: MỘT thẻ chung cố định giữa màn cộng thẻ riêng của từng người
 * bày thành hàng dưới, tất cả hiện cùng lúc (xem DOCS/MINI_APP_DOI_DOI_LANG.md
 * mục "Chia bài"/"Một lượt"/mục 8). Cùng một tệp phục vụ HAI chế độ — cờ
 * man.anThua rẽ nhánh ở vài chỗ thay vì chép nguyên tệp thành bản thứ hai (lý
 * do chọn hướng này: xem task-11-report.md).
 *
 * Ba luật của LUẬT LÀNG (an_thua=false), cưỡng chế bằng cơ chế, không bằng
 * lời nhắc:
 *   1. Trong ván KHÔNG hiện số lượt CỦA AI — chỉ đồng hồ và "Lượt n / N"
 *      (tổng của cả bàn, không phải của riêng ai, nên không lộ ai đang hơn).
 *   2. Số lượt (riêng từng người) chỉ lộ ở màn kết ván, chỉ khi chênh lệch
 *      vượt quá một phần ba TỔNG SỐ LƯỢT CỦA VÁN (Activity.SO_LUOT_VAN / 3 —
 *      chốt 2026-09-02, đổi từ tính theo số thẻ sang tính theo số lượt).
 *   3. Người làm Hoa tiêu không có ô bấm được, nên không đường nào ghi lượt.
 *      Gợi ý của em chỉ bật được sau khi đã tick một người, và mỗi thẻ riêng
 *      chỉ dùng được một lần (thẻ mới rút lên lại được gợi ý một lần nữa).
 *
 * MỘT ván dài đúng Activity.SO_LUOT_VAN lượt (chốt 2026-09-02, không còn
 * chơi tới lúc hết chồng), và MỖI LẦN CÓ NGƯỜI GỌI ĐÚNG, thẻ riêng của CẢ BÀN
 * đổi mới — không riêng người gọi đúng (chốt cùng ngày, tránh em chậm ngồi
 * nhìn mãi một thẻ cũ). Áp dụng cho CẢ HAI chế độ; xem lang_doidoi.js
 * doiTheRiengCaBan()/motLaTuChong() cho phần chia bài + xáo lại khi cạn.
 *
 * Ba điều khác của LUẬT ĂN THUA (an_thua=true, mục 7b của spec) — CHỈ áp
 * dụng khi man.anThua === true, không đụng tới hành vi Luật làng ở trên:
 *   1. Đếm 3-2-1 che thẻ trước mỗi lượt (man.dangDemNguoc/man.dem).
 *   2. Thẻ CHUNG cũng đổi sau mỗi lần đúng (ngược Luật làng, nơi thẻ chung cố
 *      định) — thẻ riêng của cả bàn vẫn đổi như trên, không phải điều khác.
 *   3. Điểm (dùng lại field luot) hiện công khai dưới tên, cộng ngay.
 */
import QtQuick 2.12
import GCompris 1.0

import "../../core"
import "lang_doidoi.js" as Activity

Item {
    id: man
    property var items

    property int luotHienTai: 0      // 0..Activity.SO_LUOT_VAN, cho "Lượt n / N"

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

    // ---- Luật ăn thua (mục 7b) ----
    property bool anThua: false       // sao chép từ items.anThua lúc vào ván
    property bool dangDemNguoc: false // đang che thẻ đếm 3-2-1
    property int dem: -1              // 3,2,1,0 = "Tìm đi!", -1 = không đếm

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

    // Luật ăn thua: nhịp đếm 3-2-1-"Tìm đi!" — mỗi 700ms một bước, chỉ chạy
    // khi đang che thẻ. Ba điều KHÔNG khác giữ nguyên: Timer này không tồn
    // tại tác dụng gì ở Luật làng vì man.dangDemNguoc không bao giờ bật lên
    // (tickDemNguoc() trong JS chỉ được gọi từ batDauDemNguoc(), mà hàm đó
    // chỉ được gọi khi van.an_thua === true).
    Timer {
        interval: 700; running: man.anThua && man.dangDemNguoc; repeat: true
        onTriggered: Activity.tickDemNguoc(man)
    }

    // Luật ăn thua: SAU một lần gọi đúng, để vòng nháy (điều KHÔNG khác —
    // "hình nhấp nháy trên cả hai thẻ" vẫn còn) chạy trọn ~900ms (đủ vài
    // nhịp animate 300ms/pha trong The.qml) rồi mới thật sự đổi thẻ chung +
    // bắt đầu che/đếm — nếu đổi/che ngay thì cả bàn không kịp thấy hình nào
    // vừa trùng, mất hẳn phần dạy học của trò chơi. Bấm chạy (restart) từ
    // hai onBamHinh bên dưới, chỉ khi Activity.chonHinh() trả về true (đúng
    // NGHĨA LÀ: vừa ghi một lượt đúng ở Luật ăn thua, ván còn tiếp tục).
    Timer {
        id: doiNhayAnThua
        interval: 900; repeat: false; running: false
        onTriggered: Activity.sauKhiNhayAnThua(man)
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
        man.anThua = items.anThua
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
            // Tổng lượt của CẢ BÀN, không phải của riêng ai — không vi phạm
            // luật 1 ("trong ván không hiện số lượt của ai"). man.luotHienTai
            // là số lượt ĐÃ XONG (0 lúc mới vào ván) nên hiện lượt SẮP/ĐANG
            // chơi là +1, chặn trần ở SO_LUOT_VAN cho chắc.
            text: qsTr("Lượt %1 / %2")
                  .arg(Math.min(man.luotHienTai + 1, Activity.SO_LUOT_VAN))
                  .arg(Activity.SO_LUOT_VAN)
        }
        GCText {
            // Kỷ lục "thời gian phá hết chồng" chỉ có nghĩa ở Luật làng
            // (Luật ăn thua không có kỷ lục, chỉ có điểm — mục 7b, Q9).
            fontSize: mediumSize; color: "#E8A317"
            visible: !man.anThua && man.kyLuc >= 0
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

        // Thẻ chung + hàng thẻ riêng gộp thành MỘT khối. Trước đây (task-10)
        // neo anchors.centerIn: parent để khoảng trống thật (nếu dư) chia
        // đều hai đầu vùng chơi. VÒNG SỬA (máy thật, nhìn ảnh): với 6 người +
        // cấp Khó, khối này CAO HƠN vùng chơi thật trên NEO One (Bar thật cao
        // hơn ô giả 130px dùng lúc dựng) — centerIn để phần dư TRÀN ĐỀU cả
        // hai phía, nên nửa trên đè lên "Lượt n / N" ở thanh trên. Đổi sang
        // neo ĐỈNH vào đỉnh vùng chơi (ngay dưới thanh trên, có topMargin
        // riêng) — mép trên thẻ chung không bao giờ vượt lên trên vùng chơi
        // được nữa, dù khối có cao hơn chỗ trống thật đến đâu; phần tràn (nếu
        // có) chỉ còn tràn xuống phía Bar, ít hại hơn tràn lên chữ.
        Column {
            id: khoiVanChoi
            anchors {
                top: parent.top; topMargin: 10
                horizontalCenter: parent.horizontalCenter
            }
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
                onBamHinh: { if (Activity.chonHinh(man, chiSoHinh)) doiNhayAnThua.restart() }
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
                        // Luật ăn thua (điều khác thứ ba, mục 7b): "Điểm hiện rõ ngay
                        // dưới tên mỗi người" — dùng lại field luot (số lượt gọi đúng),
                        // vốn đã có sẵn cho Luật làng nhưng bị giấu trong ván ở đó.
                        property bool coDiem: man.anThua && !laHoaTieu
                        property int diemCuaToi: index < man.luot.length ? man.luot[index] : 0
                        property bool dangDanDau: man.anThua && man.luot.length > 0 &&
                                                   diemCuaToi > 0 &&
                                                   diemCuaToi === Math.max.apply(null, man.luot)

                        Rectangle {
                            id: oTen
                            anchors.horizontalCenter: parent.horizontalCenter
                            width: man.duongKinhRieng
                            // VÒNG SỬA 3: trên NEO One thật GCompris nhân cỡ chữ
                            // theo màn hình (ApplicationInfo.ratio) — khung dựng
                            // giả trên Mac cho ratio=1.0 cố định nên chữ nhỏ hơn,
                            // và một chiều cao SỐ CỨNG (64/80) từng vừa trên Mac
                            // lại cắt mất nửa dưới dòng "0 điểm" trên máy thật vì
                            // chữ to hơn. Đổi sang co giãn theo NỘI DUNG thật
                            // (cot.height, xem Column bên dưới) + lề cố định 16 —
                            // đúng cho cả ba trường hợp: Luật làng một dòng, Luật
                            // ăn thua hai dòng (tên+điểm), Hoa tiêu hai dòng
                            // (tên+"phím cách"), bất kể cỡ chữ máy nào.
                            height: cot.height + 16
                            radius: 10
                            color: laHoaTieu ? "#2A3A5C"
                                 : dangChonToi ? "#E8A317"
                                 : dangKhoa ? "#8A4B24" : "#FBF8F1"
                            border {
                                color: laHoaTieu ? "#4A5A7C" : oNguoi.dangDanDau ? "#E8A317" : "#141414"
                                width: laHoaTieu ? 1 : (oNguoi.dangDanDau ? 4 : 3)
                            }
                            Column {
                                id: cot
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
                                GCText {
                                    // Luật làng: Hoa tiêu KHÔNG ghi điểm được (điều
                                    // KHÔNG khác) nên oNguoi.coDiem đã loại laHoaTieu ra.
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    visible: oNguoi.coDiem
                                    fontSize: tinySize; font.bold: oNguoi.dangDanDau
                                    color: oNguoi.dangDanDau ? "#8A4B24" : "#3A3A3A"
                                    text: qsTr("%1 điểm").arg(oNguoi.diemCuaToi)
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
                            onBamHinh: { if (Activity.chonHinh(man, chiSoHinh)) doiNhayAnThua.restart() }

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

        // Luật ăn thua điều khác thứ nhất (mục 7b): che thẻ + đếm 3-2-1
        // trước mỗi lượt. Phủ đúng vùng thẻ chung+thẻ riêng (vungChoi), KHÔNG
        // phủ thanh trên hay ô tên — vungChoi là anh em ruột thật của Item
        // này trong cùng tệp (không qua Loader) nên anchors.fill: vungChoi
        // hợp lệ, khác bẫy 4 trong brief (Bar mới là thứ ở ngoài Loader).
        // MouseArea rỗng bên trong nuốt hết mọi click lọt qua lúc còn che,
        // phòng khi ô tên/hình nào đó lỡ vẫn "enabled" (JS đã gác rồi, đây
        // là lớp phòng thủ thứ hai, không phải nguồn sự thật duy nhất).
        Rectangle {
            id: mHDemNguoc
            anchors.fill: vungChoi
            color: "#16264A"
            visible: man.anThua && man.dangDemNguoc
            z: 10
            MouseArea { anchors.fill: parent; onClicked: {} }
            GCText {
                anchors.centerIn: parent
                fontSize: hugeSize; font.bold: true; color: "#E8A317"
                text: man.dem > 0 ? String(man.dem) : qsTr("Tìm đi!")
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
                text: man.anThua ? qsTr("Hết ván!") : qsTr("Cả bàn thắng!")
            }
            GCText {
                anchors.horizontalCenter: parent.horizontalCenter
                fontSize: mediumSize; color: "#FBF8F1"
                // Ván nay dừng đúng SO_LUOT_VAN lượt, KHÔNG còn phải "phá hết
                // chồng thẻ" (chốt 2026-09-02) — đổi câu chữ cho khớp.
                text: qsTr("Xong %1 lượt trong %2 giây").arg(Activity.SO_LUOT_VAN).arg(man.giay)
            }

            // ---- Luật ăn thua: bảng điểm (mục 7b, "hiện bảng điểm") ----
            Column {
                anchors.horizontalCenter: parent.horizontalCenter
                visible: man.anThua
                spacing: 10
                GCText {
                    anchors.horizontalCenter: parent.horizontalCenter
                    fontSize: regularSize; font.bold: true; color: "#FBF8F1"
                    text: qsTr("Bảng điểm")
                }
                Repeater {
                    model: man.anThua ? man.soNguoi : 0
                    delegate: GCText {
                        anchors.horizontalCenter: parent.horizontalCenter
                        property int diem: index < man.luot.length ? man.luot[index] : 0
                        // Ai nhiều nhất được đánh dấu — điểm 0 không tính là
                        // "dẫn đầu" (không đánh dấu cả bàn lúc chưa ai ghi).
                        property bool danDau: man.luot.length > 0 && diem > 0 &&
                                               diem === Math.max.apply(null, man.luot)
                        fontSize: regularSize
                        font.bold: danDau
                        color: danDau ? "#E8A317" : "#FBF8F1"
                        // Hoa tiêu không ghi điểm được (điều KHÔNG khác) — ghi rõ
                        // vai trò thay vì hiện "0 điểm" gây hiểu lầm em chơi kém.
                        text: (index === man.hoaTieu)
                              ? qsTr("Bạn %1 · Hoa tiêu").arg(index + 1)
                              : qsTr("Bạn %1 — %2 điểm").arg(index + 1).arg(diem)
                    }
                }
            }

            GCText {
                anchors.horizontalCenter: parent.horizontalCenter
                width: man.width * 0.7
                horizontalAlignment: Text.AlignHCenter
                wrapMode: Text.WordWrap
                fontSize: regularSize; color: "#FBF8F1"
                // Luật 2 của LUẬT LÀNG: số lượt chỉ lộ ra ở đây, và chỉ khi
                // lệch quá 1/3 TỔNG SỐ LƯỢT CỦA VÁN (chốt 2026-09-02 — đổi
                // từ tính theo số thẻ của chồng sang tính theo số lượt, vì
                // ván nay dừng theo số lượt chứ không theo chồng cạn). Luật
                // ăn thua không có luật này — điểm đã hiện công khai suốt
                // ván rồi (điều khác thứ ba), nên câu nhắc "nhường nhau"
                // không áp dụng ở đây.
                visible: {
                    if (man.anThua) return false
                    if (man.luot.length === 0) return false
                    var lon = Math.max.apply(null, man.luot)
                    var nho = Math.min.apply(null, man.luot)
                    return (lon - nho) > Activity.SO_LUOT_VAN / 3
                }
                text: qsTr("Có bạn gọi được nhiều hơn hẳn các bạn khác. Ván sau nhường nhau một chút nhé — cả bàn cùng thắng mới là thắng.")
            }

            // ---- Luật ăn thua: câu hỏi kịch bản + nút mời sang Luật làng ----
            GCText {
                anchors.horizontalCenter: parent.horizontalCenter
                width: man.width * 0.7
                horizontalAlignment: Text.AlignHCenter
                wrapMode: Text.WordWrap
                visible: man.anThua
                fontSize: regularSize; color: "#FBF8F1"
                text: qsTr("Trò này vui với một người hay vui với cả bàn?")
            }
            // Spec ghi rõ đây là một LỜI MỜI, không phải bắt buộc — để một
            // lối ra duy nhất là ép, ngược tinh thần Luật làng đang muốn dạy.
            // "Sang Luật làng" đứng trước, nổi hơn (NutTo mặc định); "Chơi
            // ván nữa" đứng sau, mờ hơn (nhat: true) — bàn nào muốn đua tiếp
            // cứ để họ đua tiếp.
            Row {
                anchors.horizontalCenter: parent.horizontalCenter
                visible: man.anThua
                spacing: 30
                NutTo {
                    chu: qsTr("Sang Luật làng")
                    onBam: {
                        // Điểm không lưu ra đâu cả (Q9) — chỉ đổi cờ luật rồi
                        // chia ván mới, không mang gì từ ván ăn thua sang.
                        man.items.anThua = false
                        man.anThua = false
                        dongHo.giay = 0
                        man.batDau()
                    }
                }
                NutTo {
                    nhat: true
                    chu: qsTr("Chơi ván nữa")
                    onBam: { dongHo.giay = 0; man.batDau() }
                }
            }
            NutTo {
                anchors.horizontalCenter: parent.horizontalCenter
                visible: !man.anThua
                chu: qsTr("Chơi ván nữa")
                onBam: { dongHo.giay = 0; man.batDau() }
            }
        }
    }
}
