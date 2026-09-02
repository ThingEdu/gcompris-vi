/* GCompris - Làng Maker
 *
 * SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
 *   SPDX-License-Identifier: GPL-3.0-or-later
 */
.pragma library
.import QtQuick 2.12 as Quick
.import "qrc:/gcompris/src/core/core.js" as Core

var url = "qrc:/gcompris/src/activities/lang_maker/resource/"

/* Mười hai nơi trong tranh làng Maker.
 * x, y là tâm tính theo phần của BỀ RỘNG và CHIỀU CAO ảnh nền.
 * r là bán kính vùng chạm, tính theo phần của BỀ RỘNG ảnh.
 */
var noiChon = [
    { ma: "san_robot",   ten: "Sân đấu rô bốt",
      mo: "Nơi các đội cho rô bốt của mình thi đấu với nhau.",
      x: 0.500, y: 0.275, r: 0.095 },
    { ma: "man_hinh_neo_sport", ten: "Màn hình Neo Sport",
      mo: "Màn hình Neo Sport báo đội nào đang dẫn trước trong trận đấu.",
      x: 0.640, y: 0.157, r: 0.045 },
    { ma: "nha_kinh",    ten: "Nhà kính thông minh",
      mo: "Cây trồng trong nhà kính, cảm biến tự đo nắng và độ ẩm.",
      x: 0.105, y: 0.545, r: 0.075 },
    { ma: "pin_mat_troi", ten: "Tấm pin mặt trời",
      mo: "Hứng nắng làm ra điện cho cả làng dùng.",
      x: 0.058, y: 0.280, r: 0.045 },
    { ma: "drone",       ten: "Máy bay không người lái",
      mo: "Bay lên cao chụp ảnh và chở đồ nhẹ.",
      x: 0.142, y: 0.222, r: 0.035 },
    { ma: "tram_song",   ten: "Trạm phát sóng",
      mo: "Gửi tín hiệu không dây để máy móc trong làng nói chuyện với nhau.",
      x: 0.205, y: 0.310, r: 0.042 },
    { ma: "may_in_3d",   ten: "Máy in ba chiều",
      mo: "In ra từng chi tiết bằng nhựa để lắp thành đồ vật.",
      x: 0.665, y: 0.480, r: 0.075 },
    { ma: "thingbot",    ten: "Rô bốt ThingBot và bộ đồ nghề",
      mo: "Xe rô bốt ThingBot nằm cạnh cờ lê, tua vít — đồ nghề để sửa chữa và lắp đặt.",
      x: 0.940, y: 0.690, r: 0.048 },
    { ma: "mach_dien",   ten: "Đường mạch điện",
      mo: "Những đường mạch nối máy móc khắp làng lại với nhau.",
      x: 0.205, y: 0.840, r: 0.080 },
    { ma: "cao",         ten: "Bạn Cáo dẫn đường",
      mo: "Bạn Cáo giới thiệu cho các bạn nhỏ mọi hoạt động của làng.",
      x: 0.420, y: 0.730, r: 0.070 },
    { ma: "neo_tre",     ten: "Rô bốt NEO Tre",
      mo: "Người bạn rô bốt của làng Maker, cầm bản vẽ đi cùng các bạn nhỏ.",
      x: 0.612, y: 0.735, r: 0.062 },
    { ma: "chao_ve_tinh", ten: "Chảo vệ tinh",
      mo: "Thu tín hiệu từ nơi rất xa gửi về cho làng.",
      x: 0.878, y: 0.320, r: 0.042 }
]

/* Ba cấp độ:
 *   1 — khám phá tự do, chạm vào đâu cũng được, tìm đủ 12 nơi là xong
 *   2 — Cáo gọi TÊN, trẻ tìm đúng nơi
 *   3 — Cáo tả VIỆC làm ở đó, trẻ tìm đúng nơi (khó hơn vì không có tên)
 */
var soCap = 3

var items
var capHienTai = 0
var daTim = []
var thuTuHoi = []
var viTriHoi = 0

function start(items_) {
    items = items_
    capHienTai = 0
    khoiDongCap()
}

function stop() {}

function khoiDongCap() {
    items.bar.level = capHienTai + 1
    daTim = []
    viTriHoi = 0
    items.diemDaTim = []
    items.khamPha = (capHienTai === 0)
    if (items.khamPha) {
        thuTuHoi = []
        items.soCauHoi = noiChon.length
        items.loiNhac = "Chạm vào từng nơi trong làng để xem đó là gì."
    } else {
        thuTuHoi = Core.shuffle(danhSachMa()).slice(0, 6)
        items.soCauHoi = thuTuHoi.length
        hoiTiep()
    }
    items.daLam = 0
    items.tenDangHien = ""
    items.moDangHien = ""
}

function danhSachMa() {
    var ds = []
    for (var i = 0; i < noiChon.length; i++)
        ds.push(noiChon[i].ma)
    return ds
}

function timTheoMa(ma) {
    for (var i = 0; i < noiChon.length; i++)
        if (noiChon[i].ma === ma)
            return noiChon[i]
    return null
}

function hoiTiep() {
    var noi = timTheoMa(thuTuHoi[viTriHoi])
    items.loiNhac = (capHienTai === 1)
        ? "Tìm giúp Cáo: " + noi.ten
        : "Cáo đố: " + noi.mo + " Đó là chỗ nào?"
}

function chamVao(ma) {
    var noi = timTheoMa(ma)
    if (noi === null)
        return

    if (items.khamPha) {
        items.tenDangHien = noi.ten
        items.moDangHien = noi.mo
        if (daTim.indexOf(ma) === -1) {
            daTim.push(ma)
            items.diemDaTim = daTim.slice()
            items.daLam = daTim.length
            items.audioEffects.play("qrc:/gcompris/src/core/resource/sounds/win.wav")
            if (daTim.length === noiChon.length)
                items.bonus.good("flower")
        }
        return
    }

    if (ma === thuTuHoi[viTriHoi]) {
        items.tenDangHien = noi.ten
        items.moDangHien = noi.mo
        daTim.push(ma)
        items.diemDaTim = daTim.slice()
        viTriHoi++
        items.daLam = viTriHoi
        if (viTriHoi >= thuTuHoi.length) {
            items.bonus.good("flower")
        } else {
            items.audioEffects.play("qrc:/gcompris/src/core/resource/sounds/win.wav")
            hoiTiep()
        }
    } else {
        items.tenDangHien = ""
        items.moDangHien = ""
        items.bonus.bad("flower")
    }
}

function capTiep() {
    capHienTai = (capHienTai + 1) % soCap
    khoiDongCap()
}

function capTruoc() {
    capHienTai = (capHienTai - 1 + soCap) % soCap
    khoiDongCap()
}

function lamLai() {
    khoiDongCap()
}
