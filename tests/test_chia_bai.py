"""Kiểm bất biến sống còn của luồng CHIA BÀI lúc chạy, bằng cách chạy CHÍNH
`lang_doidoi.js` thật qua `node` — không chép logic sang Python.

BẤT BIẾN: thẻ riêng của MỌI người chơi luôn trùng với thẻ chung ĐÚNG MỘT
hình. Vỡ bất biến này thì có lượt gọi hình nào cũng đúng (thẻ riêng trùng
CẢ thẻ chung), hoặc có lượt không ai gọi được (hai thẻ riêng trùng nhau
nhưng không trùng thẻ chung ở đúng hình cần tìm).

`tests/test_bo_bai.py` chỉ kiểm BỘ BÀI TĨNH do `tools/sinh_bo_bai.py` sinh ra
lúc dựng — bộ bài đúng không có nghĩa là LUỒNG CHIA BÀI LÚC CHẠY (ai nhận
thẻ nào, xáo lại ra sao khi chồng cạn) cũng đúng. `tools/kiem_qml.py` chỉ nạp
QML, không chạy logic chia bài. Luồng chia bài thật nằm trong
`lang_doidoi.js` (`batDauVan`, `motLaTuChong`, `doiTheRiengCaBan`,
`doiTheChungCaBan`) và có cơ chế XÁO LẠI THẺ ĐÃ DÙNG khi chồng cạn — cơ chế
này mở đường cho một lớp lỗi riêng: nếu một em nhận đúng thẻ giống hệt thẻ
chung thì hai thẻ đó trùng NHAU TẤT CẢ các hình, vỡ bất biến ngay. Trước khi
có tệp này, không có gì báo đỏ nếu người sau sửa `motLaTuChong` mà không biết
bẫy đó — xem docstring của các hàm trên trong `lang_doidoi.js` để đọc đủ bối
cảnh (bẫy "khi xáo lại phải loại thẻ chung hiện tại ra").

VÌ SAO CHẠY JS THẬT, KHÔNG CHÉP LOGIC SANG PYTHON. Chép logic chia bài sang
Python thì kho có HAI bản: bản JS phát hành trên NEO One và bản Python trong
test. Hai bản đó trôi khỏi nhau dần theo thời gian (ai đó sửa JS mà quên sửa
Python, hoặc ngược lại) mà không ai biết, tới lúc đó test chỉ còn bảo vệ một
thứ KHÔNG được phát hành — vô dụng đúng vào lúc cần nhất. Nên ở đây: đọc
`lang_doidoi.js`, bỏ `.pragma`/`.import` (cú pháp riêng của QML, `node` không
hiểu, còn Qt thì CẦN — không được sửa vào bản đã phát hành), giả một
`XMLHttpRequest` đồng bộ đọc thẳng từ đĩa (bản thật chạy trong Qt đọc từ
`.rcc` qua `XMLHttpRequest`, không có trong `node`), dựng một `items` giả đủ
thuộc tính mà luồng chia bài đọc/ghi, rồi CHẠY THẬT bằng `node` — cùng một
tệp `.js`, không phải bản diễn giải lại.

QUY MÔ. Cơ chế xáo-lại chỉ lộ ra khi CHỒNG CẠN — chồng chưa cạn thì bẫy không
có đường nào bị đụng tới. Nên bộ mô phỏng dưới đây chơi đủ nhiều ván, đủ
2-6 người × Dễ/Khó × Luật làng/Luật ăn thua (20 tổ hợp), để chồng cạn NHIỀU
LẦN trong tổng số ván — và tự khẳng định số lần cạn > 0, nếu không thì đợt
kiểm này coi như vô nghĩa (phải đỏ, xem `test_bo_ban_khong_vo_bat_bien`).

BỐN PHÉP PHÁ HỎNG CÓ CHỦ ĐÍCH (đã làm tay, xác nhận rồi hoàn nguyên bằng
`git checkout`, xem task-13-report.md để biết đầy đủ):
  1. Bỏ đoạn loại thẻ chung ra khỏi chồng khi xáo lại (vô hiệu hoá điều kiện
     `la === cam` trong `motLaTuChong`) → KHÔNG bắt được. Đã chứng minh bằng
     cách đo thêm: ngay cả ở mã GỐC (chưa phá), điều kiện `la === cam` không
     bao giờ đúng trong 60 ván/51 lần cạn chồng — vì `the_chung` hiện tại
     luôn bị `shift()` ra khỏi chồng và giữ riêng, KHÔNG BAO GIỜ có mặt đồng
     thời trong chồng/da_dung trong lúc nó còn là thẻ chung "hiện tại" (chỉ
     vào da_dung đúng lúc bị THAY, trong `doiTheChungCaBan`, thay xong thì
     `cam` đã trỏ sang thẻ chung MỚI). Với đúng thứ tự gọi hàm hiện tại, nhánh
     này là code chết — đây là lớp bảo vệ CHO TƯƠNG LAI (lỡ ai đổi thứ tự
     gọi hoặc thêm chỗ đẩy vào da_dung), KHÔNG phải lỗi đang sống hôm nay.
     KHÔNG có test nào (chạy JS thật) bắt được phép phá này mà không đổi
     cách chơi/thứ tự gọi hàm — ghi nhận đúng như thấy, không tự nới lỏng.
  2. Cho phép hai người nhận cùng một thẻ (đổi `van.chong.shift()` thành
     `van.chong[0]` — không xoá khỏi chồng) → BẮT ĐƯỢC: `node` crash với
     `RangeError` (vòng lặp loại-thẻ-cấm không bao giờ tiến được vì chồng
     không vơi).
  3. Cho `motLaTuChong` trả thẻ từ vị trí cố định thay vì rút tuần tự (đổi
     `shift()` thành `pop()`) → KHÔNG bắt được (xanh) — đúng như dự đoán:
     rút từ đầu hay cuối chồng đều cho thẻ PHÂN BIỆT, bất biến không phụ
     thuộc thứ tự rút, chỉ phụ thuộc rút có trùng hay không.
  4. Bỏ hẳn cơ chế xáo lại khi chồng cạn (nhánh cạn trả `null` thay vì xáo
     `da_dung`) → BẮT ĐƯỢC: `node` crash với `TypeError` (gọi `.indexOf` lên
     `null`) khi có người nhận thẻ riêng là `null`.

SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
SPDX-License-Identifier: GPL-3.0-or-later
"""
import json
import os
import shutil
import subprocess
import tempfile
import time

import pytest

GOC = os.path.join(os.path.dirname(__file__), "..")
APP_DIR = os.path.join(
    GOC, "mini-app", "lang_doidoi", "gcompris", "src", "activities", "lang_doidoi"
)
JS_PATH = os.path.join(APP_DIR, "lang_doidoi.js")
RESOURCE_DIR = os.path.join(APP_DIR, "resource")

NODE = shutil.which("node")

pytestmark = pytest.mark.skipif(
    NODE is None,
    reason=(
        "Cần `node` để chạy CHÍNH lang_doidoi.js thật — test này là bài kiểm "
        "DUY NHẤT bảo vệ bất biến sống còn của Đối Đôi Làng lúc chạy (thẻ "
        "riêng của mọi người luôn trùng thẻ chung đúng một hình), qua cơ chế "
        "chia bài + xáo lại khi cạn chồng viết bằng JavaScript. Không có "
        "node thì lỗ hổng này không ai bắt được. Cài: `brew install node` "
        "(macOS) hoặc xem https://nodejs.org."
    ),
)

# Đủ 2-6 người × Dễ/Khó × Luật làng/Luật ăn thua = 20 tổ hợp.
SO_NGUOI_DAI = range(2, 7)
SO_VAN_MOI_TO_HOP = 3  # 20 tổ hợp x 3 = 60 ván, đo được ~0,06 giây riêng node.


def _doc_ma_nguon_da_loc():
    """Đọc lang_doidoi.js, bỏ các dòng `.pragma`/`.import` — cú pháp QML mà
    `node` không hiểu, còn Qt thì CẦN nên không được sửa vào tệp gốc."""
    dong = []
    with open(JS_PATH, encoding="utf-8") as tep:
        for d in tep:
            t = d.strip()
            if t.startswith(".pragma") or t.startswith(".import"):
                continue
            dong.append(d)
    return "".join(dong)


def _sinh_ma_javascript():
    """Lắp một tệp .js hoàn chỉnh: giả XMLHttpRequest đọc từ đĩa (thay cho
    bản thật đọc từ .rcc trong Qt) + mã nguồn thật đã lọc + một bộ MÔ PHỎNG
    CHƠI (gọi thẳng batDauVan/chonNguoi/chonHinh/sauKhiNhayAnThua/
    tickDemNguoc — không chép lại logic chia bài) + phần kiểm bất biến sau
    mỗi lần chia/đổi thẻ."""
    ma_nguon = _doc_ma_nguon_da_loc()
    resource_dir_json = json.dumps(RESOURCE_DIR)

    phan_dau = r"""
'use strict';
const fs = require('fs');
const path = require('path');

// docJson() trong lang_doidoi.js dùng XMLHttpRequest ĐỒNG BỘ để đọc tệp từ
// .rcc — node không có kiểu này. Giả một bản đọc thẳng từ đĩa, ĐỊNH NGHĨA
// TRƯỚC khi mã nguồn thật chạy, để không phải sửa lang_doidoi.js.
const THU_MUC_TAI_NGUYEN = __RESOURCE_DIR_JSON__;
const TIEN_TO_QRC = 'qrc:/gcompris/src/activities/lang_doidoi/resource/';

function XMLHttpRequest() {
    this._url = null;
    this.responseText = null;
}
XMLHttpRequest.prototype.open = function (method, url) { this._url = url; };
XMLHttpRequest.prototype.send = function () {
    var duongDan = this._url;
    if (duongDan.indexOf(TIEN_TO_QRC) === 0)
        duongDan = duongDan.slice(TIEN_TO_QRC.length);
    this.responseText = fs.readFileSync(path.join(THU_MUC_TAI_NGUYEN, duongDan), 'utf8');
};

// ============ mã nguồn THẬT của lang_doidoi.js (đã lọc .pragma/.import) ============
__MA_NGUON__
// ============ hết mã nguồn thật ============

// Đếm số lần chồng THẬT SỰ cạn (phải xáo lại từ đống thẻ đã dùng), KHÔNG
// chép lại điều kiện cạn — chỉ đếm mỗi lần tron() được gọi. tron() được gọi
// ĐÚNG một lần lúc chia bài ban đầu của MỖI ván (tron(bộ bài đầy đủ)) và
// ĐÚNG một lần mỗi khi motLaTuChong() xáo lại từ da_dung khi cạn — nên
// (tổng số lần gọi tron) - (số ván) = số lần chồng thật sự cạn.
var soLanGoiTron = 0;
var tronGoc = tron;
tron = function (ds) { soLanGoiTron++; return tronGoc(ds); };

function moiItems(soNguoi, capKho, anThua) {
    // Đủ các thuộc tính mà luồng chia bài đọc (soNguoi, capKho, hoaTieu,
    // anThua, boCuc, danhMucHinh) hoặc ghi (capNhat() đổ vào items.theChung,
    // items.theRieng, ... — object thường của JS nên không cần khai trước).
    return {
        soNguoi: soNguoi,
        capKho: capKho,
        anThua: anThua,
        hoaTieu: -1,               // -1 = không ai làm Hoa tiêu (mặc định thật)
        danhMucHinh: DANH_MUC_HINH,
        boCuc: BO_CUC,
        kyLuc: -1,                 // mặc định thật (LuatLang.qml: man.kyLuc = -1)
        audioEffects: { play: function () {} },
        bonus: { good: function () {} },
    };
}

/* Ba khẳng định của bất biến sống còn: (1) mỗi thẻ riêng trùng thẻ chung
 * ĐÚNG một hình, (2) các thẻ riêng khác nhau đôi một, (3) không thẻ riêng
 * nào trùng HẾT thẻ chung. */
function kiemBatBien(loi, ghiChu) {
    var chung = van.the_chung;
    var rieng = van.the_rieng;
    for (var i = 0; i < rieng.length; i++) {
        var giao = chung.filter(function (h) { return rieng[i].indexOf(h) !== -1; });
        if (giao.length !== 1)
            loi.push(ghiChu + ": nguoi " + i + " giao thechung=" + giao.length + " (can dung 1)");
    }
    for (var i = 0; i < rieng.length; i++) {
        for (var j = i + 1; j < rieng.length; j++) {
            if (rieng[i].slice().sort().join(',') === rieng[j].slice().sort().join(','))
                loi.push(ghiChu + ": nguoi " + i + " va nguoi " + j + " nhan trung the rieng");
        }
    }
    var chungKy = chung.slice().sort().join(',');
    for (var i = 0; i < rieng.length; i++) {
        if (rieng[i].slice().sort().join(',') === chungKy)
            loi.push(ghiChu + ": nguoi " + i + " nhan the rieng trung HET the chung");
    }
}

/* Chơi trọn MỘT ván (đúng SO_LUOT_VAN lượt, người 0 luôn gọi ĐÚNG để lượt
 * nào cũng có đổi thẻ — driver này chỉ LÁI luồng có thật (chonNguoi/
 * chonHinh/sauKhiNhayAnThua/tickDemNguoc), không tính lại ai đúng ai sai;
 * hinhTrung() cũng là hàm thật trong lang_doidoi.js). Kiểm bất biến ngay
 * sau khi chia bài lần đầu và sau MỌI lần đổi thẻ (cả hai chế độ). */
function choiMotVan(soNguoi, capKho, anThua, loi) {
    var ghiChuToHop = "soNguoi=" + soNguoi + " capKho=" + capKho + " anThua=" + anThua;
    var items = moiItems(soNguoi, capKho, anThua);
    batDauVan(items);
    kiemBatBien(loi, "chia bai (" + ghiChuToHop + ")");

    var buoc = 0;
    while (!van.xong) {
        if (van.khoa_tam) {
            // Luật ăn thua: đúng lúc QML gọi sau khi Timer 900ms hết —
            // đây là lúc thẻ chung + thẻ riêng cả bàn thật sự đổi.
            sauKhiNhayAnThua(items);
            kiemBatBien(loi, "doi the (an thua, " + ghiChuToHop + ")");
        } else if (van.dang_dem_nguoc) {
            // Đếm 3-2-1 che thẻ trước lượt (Luật ăn thua) — không đổi thẻ,
            // chỉ mở khoá để chonNguoi() chạy được.
            var canGio = 0;
            while (van.dang_dem_nguoc && canGio++ < 10)
                tickDemNguoc(items);
        } else {
            chonNguoi(items, 0);
            var dung = hinhTrung(van.the_chung, van.the_rieng[0]);
            var ketQua = chonHinh(items, dung);
            if (!ketQua && !van.xong)
                // Luật làng: chonHinh() đã tự đổi thẻ riêng cả bàn bên trong.
                kiemBatBien(loi, "doi the (lang, " + ghiChuToHop + ")");
        }
        buoc++;
        if (buoc > 500)
            throw new Error("choiMotVan(" + ghiChuToHop + "): qua 500 buoc, nghi vong lap vo han");
    }
}

var DANH_MUC_HINH = docJson("hinh.json");
var BO_CUC = docJson("bo_cuc.json");

var loi = [];
var soVan = 0;
var soNguoiDai = __SO_NGUOI_DAI__;
var soVanMoiToHop = __SO_VAN_MOI_TO_HOP__;

for (var iN = 0; iN < soNguoiDai.length; iN++) {
    for (var iCapKho = 0; iCapKho < 2; iCapKho++) {
        for (var iAnThua = 0; iAnThua < 2; iAnThua++) {
            for (var lan = 0; lan < soVanMoiToHop; lan++) {
                choiMotVan(soNguoiDai[iN], iCapKho === 1, iAnThua === 1, loi);
                soVan++;
            }
        }
    }
}

var soLanCanChong = soLanGoiTron - soVan;

process.stdout.write(JSON.stringify({
    so_van: soVan,
    so_lan_can_chong: soLanCanChong,
    loi: loi,
}));
"""
    phan_dau = phan_dau.replace("__RESOURCE_DIR_JSON__", resource_dir_json)
    phan_dau = phan_dau.replace("__MA_NGUON__", ma_nguon)
    phan_dau = phan_dau.replace("__SO_NGUOI_DAI__", json.dumps(list(SO_NGUOI_DAI)))
    phan_dau = phan_dau.replace("__SO_VAN_MOI_TO_HOP__", str(SO_VAN_MOI_TO_HOP))
    return phan_dau


@pytest.fixture(scope="module")
def ket_qua_mo_phong():
    """Chạy một lần cho cả tệp: sinh .js, gọi node, đo thời gian, trả JSON."""
    ma_javascript = _sinh_ma_javascript()
    with tempfile.TemporaryDirectory() as thu_muc_tam:
        duong_dan_js = os.path.join(thu_muc_tam, "chay_chia_bai.js")
        with open(duong_dan_js, "w", encoding="utf-8") as tep:
            tep.write(ma_javascript)

        bat_dau = time.perf_counter()
        tien_trinh = subprocess.run(
            [NODE, duong_dan_js],
            capture_output=True,
            text=True,
            timeout=30,
        )
        thoi_gian_chay = time.perf_counter() - bat_dau

    assert tien_trinh.returncode == 0, (
        "node chạy lang_doidoi.js thật bị lỗi/crash — đây CHÍNH LÀ một cách "
        "test này báo đỏ (ví dụ khi motLaTuChong() trả về null lúc chồng "
        "cạn mà không xáo lại). Lỗi:\n"
        f"--- stdout ---\n{tien_trinh.stdout}\n"
        f"--- stderr ---\n{tien_trinh.stderr}"
    )
    try:
        du_lieu = json.loads(tien_trinh.stdout)
    except json.JSONDecodeError:
        pytest.fail(
            "node chạy xong (mã thoát 0) nhưng stdout không phải JSON hợp lệ:\n"
            f"--- stdout ---\n{tien_trinh.stdout}\n"
            f"--- stderr ---\n{tien_trinh.stderr}"
        )
    du_lieu["thoi_gian_chay"] = thoi_gian_chay
    return du_lieu


def test_qua_trinh_mo_phong_thuc_su_lam_chong_can(ket_qua_mo_phong):
    """Nếu chồng chưa từng cạn thì bẫy 'xáo lại khi cạn chồng' không có
    đường nào bị đụng tới — cả bộ test này coi như KHÔNG kiểm được gì, phải
    tự báo đỏ chứ không được lặng lẽ báo xanh vô nghĩa."""
    assert ket_qua_mo_phong["so_lan_can_chong"] > 0, (
        "Chồng KHÔNG cạn lần nào trong toàn bộ "
        f"{ket_qua_mo_phong['so_van']} ván mô phỏng — cơ chế xáo lại (nơi "
        "chứa bẫy 'phải loại thẻ chung hiện tại ra') chưa từng chạy, nên "
        "test này chưa kiểm được gì. Tăng SO_VAN_MOI_TO_HOP hoặc SO_LUOT_VAN "
        "giả lập."
    )


def test_the_rieng_luon_trung_the_chung_dung_mot_hinh(ket_qua_mo_phong):
    """Bất biến sống còn: sau chia bài lần đầu VÀ sau MỌI lần đổi thẻ (cả
    Luật làng lẫn Luật ăn thua), thẻ riêng của mọi người trùng thẻ chung
    đúng một hình, các thẻ riêng khác nhau đôi một, không ai trùng hết thẻ
    chung — trên đủ 2-6 người × Dễ/Khó × Luật làng/Luật ăn thua."""
    loi = ket_qua_mo_phong["loi"]
    assert loi == [], (
        f"Vỡ bất biến chia bài ở {len(loi)} chỗ (trong "
        f"{ket_qua_mo_phong['so_van']} ván, {ket_qua_mo_phong['so_lan_can_chong']} "
        "lần chồng cạn):\n" + "\n".join(loi)
    )


def test_bo_mo_phong_chay_du_nhanh(ket_qua_mo_phong):
    """Bộ test này gọi ra process node thật — phải ở dưới 10 giây, không thì
    thành gánh nặng cho cả bộ test hiện chỉ mất 0,2 giây."""
    assert ket_qua_mo_phong["thoi_gian_chay"] < 10.0, (
        f"node chạy hết {ket_qua_mo_phong['thoi_gian_chay']:.2f}s — vượt "
        "quá 10 giây cho phép. Giảm SO_VAN_MOI_TO_HOP nếu chậm đi bất "
        "thường."
    )
