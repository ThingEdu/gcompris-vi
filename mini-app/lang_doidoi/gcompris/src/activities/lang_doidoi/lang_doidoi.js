/* GCompris - Đối Đôi Làng
 *
 * SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
 *   SPDX-License-Identifier: GPL-3.0-or-later
 */
.pragma library
.import QtQuick 2.12 as Quick

var url = "qrc:/gcompris/src/activities/lang_doidoi/resource/"

var items

function docJson(ten) {
    var xhr = new XMLHttpRequest()
    xhr.open("GET", url + ten, false)      // đồng bộ: tệp nằm trong .rcc, không qua mạng
    xhr.send()
    return JSON.parse(xhr.responseText)
}

function start(items_) {
    items = items_
    items.danhMucHinh = docJson("hinh.json")
    items.boCuc = docJson("bo_cuc.json")
    items.manHienTai = "vao_ban"
}

function stop() {}

/* Chỉ số hình 0-based -> đường dẫn tệp SVG.
 * danhMucHinh xếp theo số 1..57 nên chỉ số i ứng với mục i. */
function duongDanHinh(items, chiSo) {
    var h = items.danhMucHinh[chiSo]
    return url + "hinh/" + (h.so < 10 ? "0" : "") + h.so + "-" + h.ma + ".svg"
}

/* Trộn mảng tại chỗ, thuật toán Fisher-Yates. */
function tron(ds) {
    for (var i = ds.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1))
        var t = ds[i]; ds[i] = ds[j]; ds[j] = t
    }
    return ds
}

/* Một bố cục ngẫu nhiên đã kiểm sẵn, kèm góc xoay ngẫu nhiên cho từng hình. */
function bocucNgauNhien(items, soHinh) {
    var ds = items.boCuc[String(soHinh)]
    var b = ds[Math.floor(Math.random() * ds.length)]
    var g = []
    for (var i = 0; i < soHinh; i++)
        g.push(Math.random() * 360)
    return { boCuc: b, goc: g }
}

/* ---------------------------------------------------- trạng thái ván Luật làng
 * Chia bài: xáo cả bộ, thẻ đầu làm THẺ CHUNG — đặt giữa màn, KHÔNG đổi suốt
 * ván. Tiếp theo mỗi người một THẺ RIÊNG, bày thành hàng, ai cũng thấy thẻ
 * của mọi người. Số còn lại úp thành CHỒNG.
 * Gọi đúng: thẻ riêng của người đó được thay bằng thẻ mới rút từ chồng; thẻ
 * chung giữ nguyên suốt ván — chỉ bố cục/bo_cuc của thẻ chung được tính MỘT
 * LẦN lúc chia bài, không tính lại.
 */
var van = null

function batDauVan(items) {
    var boBai = docJson(items.capKho ? "bo_bai_57.json" : "bo_bai_31.json")
    var the = tron(boBai.the.slice())
    var soHinh = items.capKho ? 8 : 6

    van = {
        chong: the,
        the_chung: [],
        the_rieng: [],          // soNguoi phần tử, mỗi phần tử là một thẻ
        bo_cuc_chung: [], goc_chung: [],
        bo_cuc_rieng: [], goc_rieng: [],
        luot: [],                // số lượt từng người, KHÔNG hiện trong ván
        khoa_den: [],             // mốc thời gian hết khoá của từng người
        nguoi_dang_chon: -1,
        da_goi_y: [],             // theo TỪNG người, không phải một cờ chung
        bat_dau: Date.now(),
        xong: false
    }

    van.the_chung = van.chong.shift()
    var bcc = bocucNgauNhien(items, soHinh)
    van.bo_cuc_chung = bcc.boCuc
    van.goc_chung = bcc.goc

    for (var i = 0; i < items.soNguoi; i++) {
        van.the_rieng.push(van.chong.shift())
        var b = bocucNgauNhien(items, soHinh)
        van.bo_cuc_rieng.push(b.boCuc)
        van.goc_rieng.push(b.goc)
        van.luot.push(0)
        van.khoa_den.push(0)
        van.da_goi_y.push(false)
    }

    items.hinhNhay = -1
    items.hinhNhayNguoi = -1
    items.goiYNguoi = -1
    items.hienGoiY = false
    capNhat(items)
    return van
}

/* Thay thẻ riêng của một người bằng thẻ mới rút từ chồng, kèm bố cục mới
 * riêng cho ô đó. Các thẻ riêng khác và thẻ chung giữ nguyên object bố cục
 * cũ — không tính lại — nên không có thẻ nào khác nháy/xoay lại vô cớ. */
function rutTheMoi(items, nguoi) {
    var soHinh = items.capKho ? 8 : 6
    van.the_rieng[nguoi] = van.chong.shift()
    var b = bocucNgauNhien(items, soHinh)
    van.bo_cuc_rieng[nguoi] = b.boCuc
    van.goc_rieng[nguoi] = b.goc
    van.da_goi_y[nguoi] = false      // thẻ mới — Hoa tiêu lại được gợi ý một lần
}

function hinhTrung(a, b) {
    for (var i = 0; i < a.length; i++)
        if (b.indexOf(a[i]) !== -1)
            return a[i]
    return -1
}

function biKhoa(nguoi) {
    // Delegate của Repeater dựng TRƯỚC khi batDauVan() gán van, nên ràng buộc
    // dangKhoa gọi vào đây lúc van còn null. Không chặn thì log đầy lỗi mỗi
    // nhịp 250ms và dangKhoa trả undefined thay vì false.
    if (van === null)
        return false
    return Date.now() < van.khoa_den[nguoi]
}

function chonNguoi(items, nguoi) {
    if (van.xong || nguoi === items.hoaTieu || biKhoa(nguoi))
        return
    // Xoá vòng nháy của lượt trước ngay khi bắt đầu tick người mới, để hình
    // nháy ở lượt vừa rồi có thời gian thật để thấy (không bị chính lượt đó
    // xoá đi trong cùng một lần gọi hàm — xem chonHinh()).
    items.hinhNhay = -1
    items.hinhNhayNguoi = -1
    van.nguoi_dang_chon = nguoi
    capNhat(items)
}

function chonHinh(items, chiSoHinh) {
    if (van.xong || van.nguoi_dang_chon < 0)
        return
    var nguoi = van.nguoi_dang_chon
    var dung = hinhTrung(van.the_chung, van.the_rieng[nguoi])
    if (chiSoHinh === dung) {
        van.luot[nguoi]++
        items.hinhNhay = dung
        items.hinhNhayNguoi = nguoi     // chỉ thẻ chung + thẻ riêng của em này nháy
        items.audioEffects.play("qrc:/gcompris/src/core/resource/sounds/win.wav")
        if (van.chong.length === 0) {
            van.xong = true
            items.giay = Math.round((Date.now() - van.bat_dau) / 1000)
            if (items.kyLuc < 0 || items.giay < items.kyLuc)
                items.kyLuc = items.giay
            items.bonus.good("flower")
        } else {
            rutTheMoi(items, nguoi)
        }
        van.nguoi_dang_chon = -1
        capNhat(items)
    } else {
        van.khoa_den[nguoi] = Date.now() + 3000
        van.nguoi_dang_chon = -1
        items.audioEffects.play("qrc:/gcompris/src/core/resource/sounds/brick.wav")
        capNhat(items)
    }
}

function goiY(items) {
    // Chỉ gợi ý được SAU KHI đã tick một người — trước đó chưa biết chỉ vào
    // thẻ của ai (luật 3).
    if (van.xong || items.hoaTieu < 0 || van.nguoi_dang_chon < 0)
        return
    var nguoi = van.nguoi_dang_chon
    if (van.da_goi_y[nguoi])
        return
    van.da_goi_y[nguoi] = true
    var dung = hinhTrung(van.the_chung, van.the_rieng[nguoi])
    // Phần tư của THẺ RIÊNG người đang được tick, chứa hình trùng
    var vt = van.the_rieng[nguoi].indexOf(dung)
    var b = van.bo_cuc_rieng[nguoi][vt]
    items.gocGoiY = Math.atan2(b[1], b[0])
    items.goiYNguoi = nguoi
    items.hienGoiY = true
    capNhat(items)
}

function capNhat(items) {
    items.soConLai = van.chong.length
    items.theChung = van.the_chung
    items.boCucChung = van.bo_cuc_chung
    items.gocChung = van.goc_chung
    items.theRieng = van.the_rieng.slice()
    items.boCucRieng = van.bo_cuc_rieng.slice()
    items.gocRieng = van.goc_rieng.slice()
    items.nguoiDangChon = van.nguoi_dang_chon
    items.vanXong = van.xong
    items.luot = van.luot.slice()
    items.daGoiY = van.da_goi_y.slice()
}

/* ---------------------------------------------------- chế độ Học hình */
var NHOM_THEO_MUC = [["A"], ["B"], ["C"], ["D", "E"], ["A", "B", "C", "D", "E"]]
var SO_CAU_MOI_MUC = 10

function hinhTheoMuc(items, muc) {
    var nhom = NHOM_THEO_MUC[muc]
    var ds = []
    for (var i = 0; i < items.danhMucHinh.length; i++)
        if (nhom.indexOf(items.danhMucHinh[i].nhom) !== -1)
            ds.push(i)
    return ds
}

function sinhCauHoi(items, muc) {
    var kho = hinhTheoMuc(items, muc)
    var dung = kho[Math.floor(Math.random() * kho.length)]
    var sai = []
    var con = kho.slice()
    con.splice(con.indexOf(dung), 1)
    tron(con)
    sai.push(con[0]); sai.push(con[1])
    var lua = tron([dung, sai[0], sai[1]])
    return { dung: dung, lua: lua }
}
