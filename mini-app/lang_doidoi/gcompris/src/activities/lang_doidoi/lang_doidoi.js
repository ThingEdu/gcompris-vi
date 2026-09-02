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
 * và Luật ăn thua (mục 7b: dùng lại y nguyên bố cục, khác ba điều — xem
 * DOCS/MINI_APP_DOI_DOI_LANG.md).
 *
 * Chia bài: xáo cả bộ, thẻ đầu làm THẺ CHUNG — đặt giữa màn. Tiếp theo mỗi
 * người một THẺ RIÊNG, bày thành hàng, ai cũng thấy thẻ của mọi người. Số
 * còn lại úp thành CHỒNG.
 *
 * MỘT ván dài đúng SO_LUOT_VAN lượt (chốt 2026-09-02, chơi thử thấy ván tới
 * lúc hết chồng quá dài) — không còn chơi tới lúc hết chồng. Mỗi lần có
 * người gọi đúng, TOÀN BỘ thẻ riêng của cả bàn đổi mới (không riêng người
 * gọi đúng — chốt cùng ngày, tránh em chậm ngồi nhìn mãi một thẻ cũ), áp
 * dụng cho CẢ HAI chế độ. 12 lượt × 6 người = 72 thẻ, nhiều hơn cả bộ Khó
 * (57), nên chồng cạn thì xáo lại từ đống thẻ đã dùng (van.da_dung) — xem
 * motLaTuChong().
 *
 * Luật làng (an_thua=false): thẻ chung giữ nguyên suốt ván, chỉ thẻ riêng
 * đổi (doiTheRiengCaBan()).
 * Luật ăn thua (an_thua=true): thẻ chung CŨNG đổi sau mỗi lần đúng
 * (doiTheChungCaBan(), gọi TRƯỚC doiTheRiengCaBan() — xem sauKhiNhayAnThua()).
 * Đổi thẻ xong còn phải che lại đếm 3-2-1 rồi mới mở (dang_dem_nguoc/dem —
 * xem batDauDemNguoc()/tickDemNguoc()), và điểm (dùng lại field luot có sẵn)
 * hiện công khai suốt ván thay vì giấu tới cuối ván.
 */

/* Độ dài MỘT ván, tính bằng số lượt (= số lần có người gọi đúng, KHÔNG phải
 * số thẻ). Hằng số DUY NHẤT — dùng cho cả điều kiện kết ván (chonHinh()),
 * hiện "Lượt n / SO_LUOT_VAN" (LuatLang.qml đọc qua Activity.SO_LUOT_VAN) và
 * ngưỡng luật 2 "không ai bị bỏ lại" (SO_LUOT_VAN / 3 = 4). Đừng viết số 12
 * rải rác ở nơi khác. */
var SO_LUOT_VAN = 12

var van = null

function batDauVan(items) {
    var boBai = docJson(items.capKho ? "bo_bai_57.json" : "bo_bai_31.json")
    var the = tron(boBai.the.slice())
    var soHinh = items.capKho ? 8 : 6
    var anThua = !!items.anThua

    van = {
        chong: the,
        da_dung: [],              // thẻ đã dùng — xáo lại thành chồng mới khi
                                   // cạn (xem motLaTuChong()). KHÔNG BAO GIỜ
                                   // chứa thẻ chung đang sống (bẫy "khi chia
                                   // phải loại thẻ chung hiện tại ra").
        the_chung: [],
        the_rieng: [],          // soNguoi phần tử, mỗi phần tử là một thẻ
        bo_cuc_chung: [], goc_chung: [],
        bo_cuc_rieng: [], goc_rieng: [],
        luot: [],                // số lượt/điểm từng người — Luật làng giấu
                                  // trong ván, Luật ăn thua hiện công khai
        so_luot: 0,               // TỔNG số lượt của cả ván (0..SO_LUOT_VAN) —
                                   // khác luot[] (theo TỪNG người). Quyết định
                                   // lúc nào ván kết thúc, hiện "Lượt n / N".
        khoa_den: [],             // mốc thời gian hết khoá của từng người
        nguoi_dang_chon: -1,
        da_goi_y: [],             // theo TỪNG người, không phải một cờ chung
        bat_dau: Date.now(),
        xong: false,
        an_thua: anThua,
        dang_dem_nguoc: false,    // Luật ăn thua: đang che thẻ đếm 3-2-1
        dem: -1,                  // 3,2,1,0 = "Tìm đi!", -1 = không đếm
        khoa_tam: false           // Luật ăn thua: giữa lúc vòng nháy đang chạy
                                   // và lúc che+đếm bắt đầu — chưa tick/chọn
                                   // hình được, nhưng CHƯA che thẻ (khác
                                   // dang_dem_nguoc). Xem sauKhiNhayAnThua().
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

    // Luật ăn thua: "cả bàn cùng bắt đầu nhìn một lúc" áp dụng cả lượt đầu
    // tiên, không chỉ những lượt sau một lần gọi đúng.
    if (anThua) {
        van.dang_dem_nguoc = true
        van.dem = 3
    }
    capNhat(items)
    return van
}

/* Rút MỘT thẻ hợp lệ từ chồng, xáo lại từ đống thẻ đã dùng (van.da_dung) khi
 * cạn. `cam` là một thẻ không được trùng — dùng để LOẠI THẺ CHUNG hiện tại ra
 * khỏi lượt chia (bẫy phải chặn khi xáo lại, xem DOCS mục "Hết chồng thì xáo
 * lại"/"Chia bài"): quên loại thì một em có thể nhận đúng thẻ giống hệt thẻ
 * chung — hai thẻ đó trùng NHAU TẤT CẢ các hình thay vì đúng một hình, vỡ bất
 * biến của cả trò chơi, và lượt đó gọi hình nào cũng đúng. Truyền `null` nếu
 * không cần loại gì (rút thẻ chung MỚI cho Luật ăn thua: chính thẻ chung cũ
 * đã bị đưa vào da_dung trước khi gọi hàm này, không còn gì phải loại).
 *
 * Chồng không bao giờ chứa hai thẻ giống nhau (bộ bài không có thẻ trùng),
 * và mỗi thẻ chỉ bị `shift()` ra khỏi chồng đúng một lần trước khi được gán
 * cho một người/thẻ chung — nên các thẻ rút liên tiếp trong CÙNG một lượt
 * (gọi lặp lại hàm này) tự động khác nhau đôi một, không cần kiểm thêm. */
function motLaTuChong(items, cam) {
    while (true) {
        if (van.chong.length === 0) {
            // Lý thuyết không xảy ra: tổng số thẻ trong bộ luôn đủ cho một
            // lượt (xem test mô phỏng). Gác lại để không lặp vô hạn.
            if (van.da_dung.length === 0)
                return null
            van.chong = tron(van.da_dung.splice(0))
        }
        var la = van.chong.shift()
        if (cam !== null && la === cam) {
            // Gặp đúng thẻ cấm (thẻ chung hiện tại) trong chồng — không bao
            // giờ chia thẻ này ra, đưa sang đống đã dùng để xáo lại rồi rút
            // tiếp lá khác.
            van.da_dung.push(la)
            continue
        }
        return la
    }
}

/* Thay thẻ riêng của TẤT CẢ mọi người bằng thẻ mới rút từ chồng, kèm bố cục
 * mới riêng cho từng ô — mỗi lần có người gọi đúng thì toàn bộ thẻ riêng của
 * cả bàn đổi mới, không riêng người gọi đúng (chốt 2026-09-02, tránh em chậm
 * ngồi nhìn mãi một thẻ cũ). Áp dụng cho CẢ HAI chế độ. Thẻ chung giữ nguyên
 * object bố cục cũ — không tính lại — nên không nháy/xoay lại vô cớ.
 *
 * Thẻ CŨ của từng người được đưa vào đống đã dùng (da_dung) TRƯỚC khi rút
 * thẻ mới, để những thẻ vừa thay có thể quay lại chồng ngay trong lượt xáo
 * lại kế tiếp — không mất đi. */
function doiTheRiengCaBan(items) {
    var soHinh = items.capKho ? 8 : 6
    for (var i = 0; i < van.the_rieng.length; i++)
        van.da_dung.push(van.the_rieng[i])
    for (var i = 0; i < van.the_rieng.length; i++) {
        van.the_rieng[i] = motLaTuChong(items, van.the_chung)
        var b = bocucNgauNhien(items, soHinh)
        van.bo_cuc_rieng[i] = b.boCuc
        van.goc_rieng[i] = b.goc
        van.da_goi_y[i] = false      // thẻ mới — Hoa tiêu lại được gợi ý một lần
    }
}

/* Thay THẺ CHUNG bằng thẻ mới rút từ chồng — điều khác thứ hai của Luật ăn
 * thua (mục 7b). PHẢI gọi hàm này TRƯỚC doiTheRiengCaBan() trong cùng một
 * lượt (xem sauKhiNhayAnThua()): thẻ chung mới phải có mặt lúc rút thẻ riêng
 * để hàm kia loại nó ra (bẫy xáo lại) — gọi ngược thứ tự thì thẻ riêng mới sẽ
 * loại nhầm thẻ chung CŨ, và thẻ chung MỚI có thể trùng một thẻ riêng nào đó. */
function doiTheChungCaBan(items) {
    var soHinh = items.capKho ? 8 : 6
    van.da_dung.push(van.the_chung)
    van.the_chung = motLaTuChong(items, null)
    var b = bocucNgauNhien(items, soHinh)
    van.bo_cuc_chung = b.boCuc
    van.goc_chung = b.goc
}

/* Bắt đầu đếm 3-2-1 trước một lượt của Luật ăn thua: che thẻ, khoá mọi thao
 * tác (chonNguoi/chonHinh/goiY đều gác van.dang_dem_nguoc hoặc đọc
 * nguoi_dang_chon === -1) cho tới khi tickDemNguoc() đếm hết. */
function batDauDemNguoc(items) {
    van.khoa_tam = false     // hết giai đoạn "chờ nháy", chuyển sang che hẳn
    van.dang_dem_nguoc = true
    van.dem = 3
    capNhat(items)
}

/* Gọi từ LuatLang.qml SAU KHI vòng nháy đúng đã chạy đủ lâu để cả bàn thấy
 * (Timer doiNhayAnThua, ~900ms — xem chonHinh()). Đây là lúc thật sự đổi
 * THẺ CHUNG rồi che lại đếm 3-2-1 — tách khỏi chonHinh() để hình nhấp nháy
 * (điều KHÔNG khác so với Luật làng: "hình nhấp nháy trên cả hai thẻ") có
 * thời gian thật hiện ra trên thẻ chung CŨ trước khi nó bị thay/che, thay vì
 * bị đổi thẻ ngay lập tức làm vòng nháy mất chỗ bám. */
function sauKhiNhayAnThua(items) {
    // Ván có thể đã kết thúc hoặc bị dựng lại (batDau() gọi lại) trong lúc
    // Timer 900ms còn đang chạy — không còn gì để đổi/che nữa.
    if (van === null || van.xong || !van.an_thua)
        return
    // Thứ tự bắt buộc: thẻ chung TRƯỚC (để doiTheRiengCaBan() loại đúng thẻ
    // chung MỚI ra khỏi lượt chia thẻ riêng) — xem docstring hai hàm này.
    doiTheChungCaBan(items)
    doiTheRiengCaBan(items)
    batDauDemNguoc(items)
}

/* Một nhịp của bộ đếm: 3 → 2 → 1 → 0 ("Tìm đi!") → mở thẻ (dang_dem_nguoc
 * = false). Gọi từ Timer bên LuatLang.qml, mỗi lần đúng một bước. */
function tickDemNguoc(items) {
    if (van === null || !van.dang_dem_nguoc)
        return
    van.dem--
    if (van.dem < 0)
        van.dang_dem_nguoc = false
    capNhat(items)
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
    // Luật ăn thua: đang che thẻ đếm 3-2-1 thì chưa ai được tick — "cả bàn
    // cùng bắt đầu nhìn một lúc", không ai bấm trước lúc thẻ còn úp. khoa_tam
    // chặn thêm khoảng chờ vòng nháy (thẻ vẫn mở, nhưng chưa tới lượt mới).
    if (van.xong || van.dang_dem_nguoc || van.khoa_tam || nguoi === items.hoaTieu || biKhoa(nguoi))
        return
    // Xoá vòng nháy của lượt trước ngay khi bắt đầu tick người mới, để hình
    // nháy ở lượt vừa rồi có thời gian thật để thấy (không bị chính lượt đó
    // xoá đi trong cùng một lần gọi hàm — xem chonHinh()).
    items.hinhNhay = -1
    items.hinhNhayNguoi = -1
    van.nguoi_dang_chon = nguoi
    capNhat(items)
}

/* Trả về true CHỈ khi vừa ghi một lượt đúng ở Luật ăn thua và ván còn tiếp
 * tục — đó là dấu hiệu để LuatLang.qml khởi động Timer doiNhayAnThua (~900ms)
 * rồi mới gọi sauKhiNhayAnThua() để đổi thẻ chung + che đếm. Mọi trường hợp
 * khác trả về false (không cần chờ gì thêm). */
function chonHinh(items, chiSoHinh) {
    if (van.xong || van.dang_dem_nguoc || van.khoa_tam || van.nguoi_dang_chon < 0)
        return false
    var nguoi = van.nguoi_dang_chon
    var dung = hinhTrung(van.the_chung, van.the_rieng[nguoi])
    if (chiSoHinh === dung) {
        // luot[nguoi] = số lượt CỦA RIÊNG người đó (Luật làng, giấu trong
        // ván, chỉ dùng cho ngưỡng luật 2) VÀ điểm (Luật ăn thua, hiện công
        // khai dưới tên) — cùng một field, hai cách đọc.
        // so_luot = TỔNG số lượt của CẢ VÁN (bất kể ai gọi đúng) — quyết
        // định lúc nào ván kết thúc và hiện "Lượt n / SO_LUOT_VAN".
        van.luot[nguoi]++
        van.so_luot++
        items.hinhNhay = dung
        items.hinhNhayNguoi = nguoi     // chỉ thẻ chung + thẻ riêng của em này nháy
        items.audioEffects.play("qrc:/gcompris/src/core/resource/sounds/win.wav")
        van.nguoi_dang_chon = -1
        if (van.so_luot >= SO_LUOT_VAN) {
            // Ván dừng đúng SO_LUOT_VAN lượt, KHÔNG phải lúc hết chồng (chốt
            // 2026-09-02) — không đổi thẻ nữa, ván đã xong.
            van.xong = true
            items.giay = Math.round((Date.now() - van.bat_dau) / 1000)
            // Kỷ lục "thời gian xong ván" là khái niệm riêng của Luật làng
            // (mục 7 Kết ván) — Luật ăn thua không có kỷ lục, chỉ có điểm,
            // và điểm không lưu ra đâu cả (Q9).
            if (!van.an_thua && (items.kyLuc < 0 || items.giay < items.kyLuc))
                items.kyLuc = items.giay
            items.bonus.good("flower")
            capNhat(items)
            return false
        } else if (van.an_thua) {
            // Điều khác thứ hai: thẻ CHUNG đổi VÀ thẻ riêng của cả bàn cũng
            // đổi — nhưng CHƯA đổi ngay ở đây. khoa_tam khoá thao tác trong
            // lúc thẻ vẫn còn mở để vòng nháy chạy trọn vẹn; QML mới là nơi
            // thật sự chờ đủ ~900ms rồi gọi sauKhiNhayAnThua() để đổi thẻ +
            // che đếm.
            van.khoa_tam = true
            capNhat(items)
            return true
        } else {
            doiTheRiengCaBan(items)
            capNhat(items)
            return false
        }
    } else {
        van.khoa_den[nguoi] = Date.now() + 3000
        van.nguoi_dang_chon = -1
        items.audioEffects.play("qrc:/gcompris/src/core/resource/sounds/brick.wav")
        capNhat(items)
        return false
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
    items.luotHienTai = van.so_luot     // 0..SO_LUOT_VAN, cho "Lượt n / N"
    // boCuc*/goc* PHẢI gán trước the*: "hinh:" và "boCuc:" trong LuatLang.qml
    // đều ràng buộc QML vào items.theChung/items.boCucChung (tương tự với
    // Rieng); gán theChung trước sẽ làm Repeater trong The.qml dựng delegate
    // ngay với hinh mới nhưng boCuc còn giá trị cũ ([] lúc khởi tạo) — mỗi
    // delegate đọc boCuc[index] undefined ném TypeError. Đảo thứ tự để boCuc
    // (và goc) đã sẵn sàng trước khi hinh đổi.
    items.boCucChung = van.bo_cuc_chung
    items.gocChung = van.goc_chung
    items.theChung = van.the_chung
    items.boCucRieng = van.bo_cuc_rieng.slice()
    items.gocRieng = van.goc_rieng.slice()
    items.theRieng = van.the_rieng.slice()
    items.nguoiDangChon = van.nguoi_dang_chon
    items.vanXong = van.xong
    items.luot = van.luot.slice()
    items.daGoiY = van.da_goi_y.slice()
    items.dangDemNguoc = van.dang_dem_nguoc
    items.dem = van.dem
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
