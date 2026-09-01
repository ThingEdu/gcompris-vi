#!/usr/bin/env python3
"""Sinh bộ bản đồ hành chính 34 tỉnh thành Việt Nam cho hoạt động "Tìm vùng
trên bản đồ" (geo-country) của GCompris.

GCompris có bản đồ hành chính của Ý, Ấn Độ, Trung Quốc, Úc, Mỹ, Pháp, Đức…
nhưng KHÔNG có Việt Nam. Công cụ này tạo bộ mới theo 34 đơn vị hành chính cấp
tỉnh sau sáp nhập (Nghị quyết 202/2025/QH15, hiệu lực 01/7/2025).

DỮ LIỆU
Ranh giới lấy từ Natural Earth 10m admin-1 (miền công cộng). Bộ này còn theo 63
tỉnh cũ nên phải hợp nhất theo bảng SAP_NHAP. Ba bản ghi trong Natural Earth bị
đặt nhầm tên vùng — đã đối chiếu bằng toạ độ tâm và diện tích để xác định:
Đông Nam Bộ = Đồng Nai, Vùng Đông Bắc = Bắc Kạn, Đồng Bằng Sông Hồng = Hưng Yên.

CHỦ QUYỀN
Quần đảo Hoàng Sa và quần đảo Trường Sa vẽ đúng toạ độ thật trên lớp nền. Chúng
KHÔNG nhập vào mảnh kéo thả: nếu nhập, mảnh Đà Nẵng rộng 180 đơn vị và mảnh
Khánh Hòa rộng 260 đơn vị trên khung 504 — trẻ không cầm nổi. Quy thuộc hành
chính (huyện đảo Hoàng Sa thuộc Đà Nẵng, huyện đảo Trường Sa thuộc Khánh Hòa)
nói bằng tên gợi ý của hai mảnh đó.

QUY CÁCH (đọc ngược từ bộ bản đồ Ý của GCompris)
- Nền: tệp .svgz, width/height = khung bản đồ, hình chữ nhật fill:gray phủ kín,
  bên trên là hình đất nước fill:#fff;stroke:#505050;stroke-width:.5
- Mảnh: toạ độ đường vẽ giữ nguyên hệ toạ độ của nền, cắt bằng
  transform="translate(-minx -miny)", width/height = kích thước khung bao
- Vị trí trong board: x = tâm_x / bề_rộng_nền, y = tâm_y / chiều_cao_nền
  (Babymatch.qml: x = posX * backgroundImage.width - width / 2)

Công cụ này chỉ SINH tài nguyên (cần shapely + pyshp + dữ liệu Natural Earth).
Việc gắn vào gói .rcc do tools/gan_ban_do_34_tinh.py làm, chỉ dùng thư viện chuẩn.

Cách chạy:
    tao_ban_do_34_tinh.py <thư_mục_natural_earth> <thư_mục_ra>   # mặc định maps/34-tinh
"""
import gzip
import os
import sys
import unicodedata

import shapefile
from shapely.geometry import Point, shape
from shapely.ops import unary_union

# --------------------------------------------------- 63 tỉnh cũ -> 34 đơn vị mới
SAP_NHAP = {
    "Hà Nội": ["Hà Nội"],
    "Cao Bằng": ["Cao Bằng"],
    "Tuyên Quang": ["Hà Giang", "Tuyên Quang"],
    "Lào Cai": ["Yên Bái", "Lào Cai"],
    "Thái Nguyên": ["Bắc Kạn", "Thái Nguyên"],
    "Điện Biên": ["Điện Biên"],
    "Lai Châu": ["Lai Châu"],
    "Sơn La": ["Sơn La"],
    "Lạng Sơn": ["Lạng Sơn"],
    "Quảng Ninh": ["Quảng Ninh"],
    "Phú Thọ": ["Vĩnh Phúc", "Hòa Bình", "Phú Thọ"],
    "Bắc Ninh": ["Bắc Giang", "Bắc Ninh"],
    "Hưng Yên": ["Thái Bình", "Hưng Yên"],
    "Hải Phòng": ["Hải Dương", "Hải Phòng"],
    "Ninh Bình": ["Hà Nam", "Nam Định", "Ninh Bình"],
    "Thanh Hóa": ["Thanh Hóa"],
    "Nghệ An": ["Nghệ An"],
    "Hà Tĩnh": ["Hà Tĩnh"],
    "Quảng Trị": ["Quảng Bình", "Quảng Trị"],
    "Huế": ["Thừa Thiên Huế"],
    "Đà Nẵng": ["Quảng Nam", "Đà Nẵng"],
    "Quảng Ngãi": ["Kon Tum", "Quảng Ngãi"],
    "Gia Lai": ["Bình Định", "Gia Lai"],
    "Đắk Lắk": ["Phú Yên", "Đắk Lắk"],
    "Khánh Hòa": ["Ninh Thuận", "Khánh Hòa"],
    "Lâm Đồng": ["Đắk Nông", "Bình Thuận", "Lâm Đồng"],
    "Đồng Nai": ["Đồng Nai", "Bình Phước"],
    "Tây Ninh": ["Tây Ninh", "Long An"],
    "Thành phố Hồ Chí Minh": ["Thành phố Hồ Chí Minh", "Bình Dương", "Bà Rịa - Vũng Tàu"],
    "Đồng Tháp": ["Tiền Giang", "Đồng Tháp"],
    "Vĩnh Long": ["Bến Tre", "Vĩnh Long", "Trà Vinh"],
    "An Giang": ["Kiên Giang", "An Giang"],
    "Cần Thơ": ["Cần Thơ", "Sóc Trăng", "Hậu Giang"],
    "Cà Mau": ["Bạc Liêu", "Cà Mau"],
}
# Natural Earth đặt nhầm tên vùng cho ba tỉnh; xác định lại bằng tâm + diện tích
SUA_TEN = {
    "Đông Nam Bộ": "Đồng Nai",
    "Vùng Đông Bắc": "Bắc Kạn",
    "Đồng Bằng Sông Hồng": "Hưng Yên",
}
# tên tệp không dấu, giữ thứ tự bắc -> nam để đọc board cho dễ
TEN_TEP = {
    "Hà Nội": "ha_noi", "Cao Bằng": "cao_bang", "Tuyên Quang": "tuyen_quang",
    "Lào Cai": "lao_cai", "Thái Nguyên": "thai_nguyen", "Điện Biên": "dien_bien",
    "Lai Châu": "lai_chau", "Sơn La": "son_la", "Lạng Sơn": "lang_son",
    "Quảng Ninh": "quang_ninh", "Phú Thọ": "phu_tho", "Bắc Ninh": "bac_ninh",
    "Hưng Yên": "hung_yen", "Hải Phòng": "hai_phong", "Ninh Bình": "ninh_binh",
    "Thanh Hóa": "thanh_hoa", "Nghệ An": "nghe_an", "Hà Tĩnh": "ha_tinh",
    "Quảng Trị": "quang_tri", "Huế": "hue", "Đà Nẵng": "da_nang",
    "Quảng Ngãi": "quang_ngai", "Gia Lai": "gia_lai", "Đắk Lắk": "dak_lak",
    "Khánh Hòa": "khanh_hoa", "Lâm Đồng": "lam_dong", "Đồng Nai": "dong_nai",
    "Tây Ninh": "tay_ninh", "Thành phố Hồ Chí Minh": "ho_chi_minh",
    "Đồng Tháp": "dong_thap", "Vĩnh Long": "vinh_long", "An Giang": "an_giang",
    "Cần Thơ": "can_tho", "Cà Mau": "ca_mau",
}
THU_TU = list(TEN_TEP.keys())          # bắc -> nam, dùng làm thứ tự trong board
# chú thích quần đảo cho hai tỉnh quản lý
CHU_THICH = {
    "Đà Nẵng": "Đà Nẵng (quản lý quần đảo Hoàng Sa)",
    "Khánh Hòa": "Khánh Hòa (quản lý quần đảo Trường Sa)",
}
HOANG_SA = [(17.083, 111.500), (16.833, 111.600), (16.517, 111.583), (16.450, 111.505),
            (16.467, 111.700), (16.443, 111.703), (15.783, 111.200), (16.833, 112.333),
            (16.667, 112.733), (16.050, 112.500)]
TRUONG_SA = [(11.427, 114.330), (11.452, 114.362), (11.053, 114.283), (10.917, 114.083),
             (10.673, 114.417), (10.383, 114.483), (10.378, 114.365), (10.183, 114.367),
             (9.883, 114.333), (9.900, 115.533), (11.400, 116.700), (9.550, 112.890),
             (8.850, 112.200), (8.667, 111.667), (8.643, 111.920), (8.167, 113.300),
             (7.883, 112.917)]

# khung bản đồ 504x520: đất liền + Phú Quốc + Côn Đảo + Hoàng Sa + Trường Sa
TL = 32.0                       # đơn vị nền trên mỗi độ
LON0, LAT1 = 101.9, 23.7
W, H = 504.0, 520.0
DON_GIAN = 0.006                # dung sai làm trơn (độ), ~0,66 km
DT_TOI_THIEU = 0.0018           # bỏ mảnh vụn nhỏ hơn ~22 km²
BAN_KINH_DAO = 1.9              # bán kính chấm đảo trên nền, phóng to cho thấy rõ
MAU = ["#e7b736", "#7ee736", "#56a9eb", "#ec885a",
       "#b98fe8", "#4fd2c2", "#e9d94a", "#ee8fc4"]


def chuan(s):
    return unicodedata.normalize("NFC", (s or "").strip())


def xy(lon, lat):
    return (lon - LON0) * TL, (LAT1 - lat) * TL


def doc_63_tinh(thu_muc):
    """Đọc 63 tỉnh cũ của Việt Nam, sửa ba tên bị Natural Earth đặt nhầm."""
    r = shapefile.Reader(os.path.join(thu_muc, "ne_10m_admin_1_states_provinces"))
    truong = [f[0] for f in r.fields[1:]]
    i_a3, i_vi = truong.index("adm0_a3"), truong.index("name_vi")
    ra = {}
    for sr in r.shapeRecords():
        if sr.record[i_a3] != "VNM":
            continue
        ten = chuan(sr.record[i_vi])
        ten = SUA_TEN.get(ten, ten)
        hinh = shape(sr.shape.__geo_interface__).buffer(0)
        ra[ten] = unary_union([ra[ten], hinh]) if ten in ra else hinh
    return ra


def bo_manh_vun(hinh):
    """Bỏ đảo nhỏ hơn ~22 km² nhưng luôn giữ mảnh lớn nhất."""
    if hinh.geom_type == "Polygon":
        return hinh
    manh = sorted(hinh.geoms, key=lambda g: g.area, reverse=True)
    giu = [manh[0]] + [g for g in manh[1:] if g.area >= DT_TOI_THIEU]
    return unary_union(giu)


def hop_nhat_34(tinh_cu):
    ra = {}
    for moi, cu in SAP_NHAP.items():
        thieu = [c for c in cu if c not in tinh_cu]
        if thieu:
            raise SystemExit(f"thiếu ranh giới tỉnh cũ: {thieu}")
        hinh = unary_union([tinh_cu[c] for c in cu]).buffer(0)
        ra[moi] = bo_manh_vun(hinh.simplify(DON_GIAN, preserve_topology=True))
    return ra


def quan_dao():
    """Hai quần đảo, vẽ thành chấm tròn đúng toạ độ thật (chỉ dùng cho nền)."""
    bk = BAN_KINH_DAO / TL      # bán kính tính theo độ, cộng trước khi chiếu
    return unary_union([Point(lon, lat).buffer(bk, quad_segs=8)
                        for lat, lon in HOANG_SA + TRUONG_SA])


def to_mau(tinh):
    """Tô màu tham lam để hai tỉnh giáp nhau không trùng màu."""
    ten = THU_TU
    ke = {t: set() for t in ten}
    for i, a in enumerate(ten):
        for b in ten[i + 1:]:
            if tinh[a].distance(tinh[b]) < 0.01:
                ke[a].add(b)
                ke[b].add(a)
    mau = {}
    for i, t in enumerate(ten):
        dung = {mau[k] for k in ke[t] if k in mau}
        # xoay điểm bắt đầu để dùng hết bảng màu, không dồn vào vài màu đầu
        vong = MAU[i % len(MAU):] + MAU[:i % len(MAU)]
        mau[t] = next(m for m in vong if m not in dung)
    return mau


def duong_ve(hinh):
    """Đổi hình shapely thành chuỗi đường vẽ SVG trong hệ toạ độ của nền."""
    dsach = []

    def vong(toa_do):
        d = []
        for i, (lon, lat) in enumerate(toa_do):
            x, y = xy(lon, lat)
            d.append(f"{'M' if i == 0 else 'L'}{x:.2f} {y:.2f}")
        return "".join(d) + "Z"

    manh = hinh.geoms if hinh.geom_type == "MultiPolygon" else [hinh]
    for p in manh:
        dsach.append(vong(p.exterior.coords))
        for lo in p.interiors:
            dsach.append(vong(lo.coords))
    return " ".join(dsach)


DAU_SVG = ('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
           '<svg width="{w}" height="{h}" version="1.1" '
           'xmlns="http://www.w3.org/2000/svg">\n')


def ghi_svgz(duong_dan, noi_dung):
    with gzip.GzipFile(duong_dan, "wb", mtime=0) as f:
        f.write(noi_dung.encode("utf-8"))


def ve_nen(tinh, dao, duong_dan):
    """Nền: nếu vẽ gộp thành một khối trắng thì học sinh không thấy ranh giới
    tỉnh nào, chỉ còn mấy chấm đích để đoán. Nên vẽ RIÊNG từng tỉnh, giữ nguyên
    nét viền — giống nền Argentina, Hoa Kỳ, Úc của GCompris."""
    svg = DAU_SVG.format(w=f"{W:g}", h=f"{H:g}")
    svg += '  <g>\n'
    svg += f'    <path style="fill:gray;fill-opacity:1" d="M0 0h{W:g}v{H:g}H0Z" />\n'
    net = ("fill:#fff;fill-opacity:1;stroke:#505050;stroke-width:.5;"
           "stroke-linejoin:bevel;stroke-opacity:1")
    for ten in THU_TU:
        svg += f'    <path style="{net}" d="{duong_ve(tinh[ten])}" />\n'
    svg += f'    <path style="{net}" d="{duong_ve(dao)}" />\n'
    svg += '  </g>\n</svg>\n'
    ghi_svgz(duong_dan, svg)


def ve_manh(hinh, mau, duong_dan):
    """Trả về (bề_rộng, chiều_cao, tâm_x, tâm_y) trong hệ toạ độ của nền."""
    lon0, lat0, lon1, lat1 = hinh.bounds
    x0, y0 = xy(lon0, lat1)          # góc trên trái
    x1, y1 = xy(lon1, lat0)          # góc dưới phải
    w, h = x1 - x0, y1 - y0
    d = duong_ve(hinh)
    svg = DAU_SVG.format(w=f"{w:.3f}", h=f"{h:.3f}")
    svg += '  <g>\n'
    svg += (f'    <path style="fill:{mau};fill-opacity:1;stroke:#505050;stroke-width:.5;'
            f'stroke-linejoin:bevel;stroke-opacity:1" d="{d}" '
            f'transform="translate({-x0:.3f} {-y0:.3f})" />\n')
    svg += '  </g>\n</svg>\n'
    ghi_svgz(duong_dan, svg)
    return w, h, x0 + w / 2, y0 + h / 2


BOARD_DAU = '''/* GCompris - bản Việt hoá của ThingEdu
 *
 * SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
 *
 * Ranh giới lấy từ Natural Earth 10m admin-1 (miền công cộng), hợp nhất theo
 * Nghị quyết 202/2025/QH15 về sắp xếp đơn vị hành chính cấp tỉnh (34 tỉnh
 * thành, hiệu lực 01/7/2025). Quần đảo Hoàng Sa thuộc Đà Nẵng, quần đảo
 * Trường Sa thuộc Khánh Hòa.
 *
 *   SPDX-License-Identifier: GPL-3.0-or-later
 */
import QtQuick 2.12

QtObject {
   property string instruction: qsTr("Các tỉnh thành Việt Nam")
   property var levels: [
      {
         "pixmapfile" : "vietnam/vietnam.svgz",
         "type" : "SHAPE_BACKGROUND_IMAGE"
      },
'''


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    thu_muc_ne, ra_goc = sys.argv[1], sys.argv[2]
    ra = os.path.join(ra_goc, "vietnam")
    os.makedirs(ra, exist_ok=True)

    cu = doc_63_tinh(thu_muc_ne)
    print(f"đọc {len(cu)} tỉnh cũ từ Natural Earth")
    if len(cu) != 63:
        raise SystemExit("phải đủ 63 tỉnh cũ")
    tinh = hop_nhat_34(cu)
    dao = quan_dao()
    print(f"hợp nhất thành {len(tinh)} đơn vị hành chính")

    lon0, lat0, lon1, lat1 = unary_union(list(tinh.values()) + [dao]).bounds
    print(f"khung địa lý: kinh {lon0:.2f}–{lon1:.2f}, vĩ {lat0:.2f}–{lat1:.2f}")
    for goc_x, goc_y in [xy(lon0, lat1), xy(lon1, lat0)]:
        if not (0 <= goc_x <= W and 0 <= goc_y <= H):
            raise SystemExit(f"bản đồ tràn khung tại ({goc_x:.1f},{goc_y:.1f})")

    ve_nen(tinh, dao, os.path.join(ra, "vietnam.svgz"))
    mau = to_mau(tinh)
    dong = []
    for ten in THU_TU:
        tep = TEN_TEP[ten] + ".svgz"
        w, h, cx, cy = ve_manh(tinh[ten], mau[ten], os.path.join(ra, tep))
        nhan = CHU_THICH.get(ten, ten)
        dong.append('      {\n'
                    f'         "pixmapfile" : "vietnam/{tep}",\n'
                    f'         //: Tỉnh thành Việt Nam: {ten}\n'
                    f'         "toolTipText" : qsTr("{nhan}"),\n'
                    f'         "x" : "{cx / W:.4f}",\n'
                    f'         "y" : "{cy / H:.4f}"\n'
                    '      }')
        print(f"  {ten:24s} {tep:16s} {w:7.2f}x{h:7.2f}  ({cx / W:.4f},{cy / H:.4f})")

    board = os.path.join(ra_goc, "board19_0.qml")
    with open(board, "w", encoding="utf-8") as f:
        f.write(BOARD_DAU + ",\n".join(dong) + "\n   ]\n}\n")
    print(f"ghi {board}")


if __name__ == "__main__":
    main()
