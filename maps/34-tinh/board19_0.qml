/* GCompris - bản Việt hoá của ThingEdu
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
      {
         "pixmapfile" : "vietnam/ha_noi.svgz",
         //: Tỉnh thành Việt Nam: Hà Nội
         "toolTipText" : qsTr("Hà Nội"),
         "x" : "0.2379",
         "y" : "0.1680"
      },
      {
         "pixmapfile" : "vietnam/cao_bang.svgz",
         //: Tỉnh thành Việt Nam: Cao Bằng
         "toolTipText" : qsTr("Cao Bằng"),
         "x" : "0.2633",
         "y" : "0.0592"
      },
      {
         "pixmapfile" : "vietnam/tuyen_quang.svgz",
         //: Tỉnh thành Việt Nam: Tuyên Quang
         "toolTipText" : qsTr("Tuyên Quang"),
         "x" : "0.1959",
         "y" : "0.0781"
      },
      {
         "pixmapfile" : "vietnam/lao_cai.svgz",
         //: Tỉnh thành Việt Nam: Lào Cai
         "toolTipText" : qsTr("Lào Cai"),
         "x" : "0.1543",
         "y" : "0.0999"
      },
      {
         "pixmapfile" : "vietnam/thai_nguyen.svgz",
         //: Tỉnh thành Việt Nam: Thái Nguyên
         "toolTipText" : qsTr("Thái Nguyên"),
         "x" : "0.2523",
         "y" : "0.1030"
      },
      {
         "pixmapfile" : "vietnam/dien_bien.svgz",
         //: Tỉnh thành Việt Nam: Điện Biên
         "toolTipText" : qsTr("Điện Biên"),
         "x" : "0.0599",
         "y" : "0.1231"
      },
      {
         "pixmapfile" : "vietnam/lai_chau.svgz",
         //: Tỉnh thành Việt Nam: Lai Châu
         "toolTipText" : qsTr("Lai Châu"),
         "x" : "0.0739",
         "y" : "0.0838"
      },
      {
         "pixmapfile" : "vietnam/son_la.svgz",
         //: Tỉnh thành Việt Nam: Sơn La
         "toolTipText" : qsTr("Sơn La"),
         "x" : "0.1435",
         "y" : "0.1472"
      },
      {
         "pixmapfile" : "vietnam/lang_son.svgz",
         //: Tỉnh thành Việt Nam: Lạng Sơn
         "toolTipText" : qsTr("Lạng Sơn"),
         "x" : "0.3064",
         "y" : "0.1106"
      },
      {
         "pixmapfile" : "vietnam/quang_ninh.svgz",
         //: Tỉnh thành Việt Nam: Quảng Ninh
         "toolTipText" : qsTr("Quảng Ninh"),
         "x" : "0.3377",
         "y" : "0.1550"
      },
      {
         "pixmapfile" : "vietnam/phu_tho.svgz",
         //: Tỉnh thành Việt Nam: Phú Thọ
         "toolTipText" : qsTr("Phú Thọ"),
         "x" : "0.2181",
         "y" : "0.1654"
      },
      {
         "pixmapfile" : "vietnam/bac_ninh.svgz",
         //: Tỉnh thành Việt Nam: Bắc Ninh
         "toolTipText" : qsTr("Bắc Ninh"),
         "x" : "0.2915",
         "y" : "0.1471"
      },
      {
         "pixmapfile" : "vietnam/hung_yen.svgz",
         //: Tỉnh thành Việt Nam: Hưng Yên
         "toolTipText" : qsTr("Hưng Yên"),
         "x" : "0.2769",
         "y" : "0.1889"
      },
      {
         "pixmapfile" : "vietnam/hai_phong.svgz",
         //: Tỉnh thành Việt Nam: Hải Phòng
         "toolTipText" : qsTr("Hải Phòng"),
         "x" : "0.2899",
         "y" : "0.1713"
      },
      {
         "pixmapfile" : "vietnam/ninh_binh.svgz",
         //: Tỉnh thành Việt Nam: Ninh Bình
         "toolTipText" : qsTr("Ninh Bình"),
         "x" : "0.2639",
         "y" : "0.2068"
      },
      {
         "pixmapfile" : "vietnam/thanh_hoa.svgz",
         //: Tỉnh thành Việt Nam: Thanh Hóa
         "toolTipText" : qsTr("Thanh Hóa"),
         "x" : "0.2105",
         "y" : "0.2302"
      },
      {
         "pixmapfile" : "vietnam/nghe_an.svgz",
         //: Tỉnh thành Việt Nam: Nghệ An
         "toolTipText" : qsTr("Nghệ An"),
         "x" : "0.1859",
         "y" : "0.2719"
      },
      {
         "pixmapfile" : "vietnam/ha_tinh.svgz",
         //: Tỉnh thành Việt Nam: Hà Tĩnh
         "toolTipText" : qsTr("Hà Tĩnh"),
         "x" : "0.2476",
         "y" : "0.3302"
      },
      {
         "pixmapfile" : "vietnam/quang_tri.svgz",
         //: Tỉnh thành Việt Nam: Quảng Trị
         "toolTipText" : qsTr("Quảng Trị"),
         "x" : "0.2922",
         "y" : "0.4012"
      },
      {
         "pixmapfile" : "vietnam/hue.svgz",
         //: Tỉnh thành Việt Nam: Huế
         "toolTipText" : qsTr("Huế"),
         "x" : "0.3640",
         "y" : "0.4503"
      },
      {
         "pixmapfile" : "vietnam/da_nang.svgz",
         //: Tỉnh thành Việt Nam: Đà Nẵng
         "toolTipText" : qsTr("Đà Nẵng (quản lý quần đảo Hoàng Sa)"),
         "x" : "0.3845",
         "y" : "0.4991"
      },
      {
         "pixmapfile" : "vietnam/quang_ngai.svgz",
         //: Tỉnh thành Việt Nam: Quảng Ngãi
         "toolTipText" : qsTr("Quảng Ngãi"),
         "x" : "0.4005",
         "y" : "0.5554"
      },
      {
         "pixmapfile" : "vietnam/gia_lai.svgz",
         //: Tỉnh thành Việt Nam: Gia Lai
         "toolTipText" : qsTr("Gia Lai"),
         "x" : "0.4109",
         "y" : "0.6068"
      },
      {
         "pixmapfile" : "vietnam/dak_lak.svgz",
         //: Tỉnh thành Việt Nam: Đắk Lắk
         "toolTipText" : qsTr("Đắk Lắk"),
         "x" : "0.4167",
         "y" : "0.6631"
      },
      {
         "pixmapfile" : "vietnam/khanh_hoa.svgz",
         //: Tỉnh thành Việt Nam: Khánh Hòa
         "toolTipText" : qsTr("Khánh Hòa (quản lý quần đảo Trường Sa)"),
         "x" : "0.4533",
         "y" : "0.7150"
      },
      {
         "pixmapfile" : "vietnam/lam_dong.svgz",
         //: Tỉnh thành Việt Nam: Lâm Đồng
         "toolTipText" : qsTr("Lâm Đồng"),
         "x" : "0.3915",
         "y" : "0.7417"
      },
      {
         "pixmapfile" : "vietnam/dong_nai.svgz",
         //: Tỉnh thành Việt Nam: Đồng Nai
         "toolTipText" : qsTr("Đồng Nai"),
         "x" : "0.3239",
         "y" : "0.7545"
      },
      {
         "pixmapfile" : "vietnam/tay_ninh.svgz",
         //: Tỉnh thành Việt Nam: Tây Ninh
         "toolTipText" : qsTr("Tây Ninh"),
         "x" : "0.2688",
         "y" : "0.7759"
      },
      {
         "pixmapfile" : "vietnam/ho_chi_minh.svgz",
         //: Tỉnh thành Việt Nam: Thành phố Hồ Chí Minh
         "toolTipText" : qsTr("Thành phố Hồ Chí Minh"),
         "x" : "0.3216",
         "y" : "0.7853"
      },
      {
         "pixmapfile" : "vietnam/dong_thap.svgz",
         //: Tỉnh thành Việt Nam: Đồng Tháp
         "toolTipText" : qsTr("Đồng Tháp"),
         "x" : "0.2603",
         "y" : "0.8065"
      },
      {
         "pixmapfile" : "vietnam/vinh_long.svgz",
         //: Tỉnh thành Việt Nam: Vĩnh Long
         "toolTipText" : qsTr("Vĩnh Long"),
         "x" : "0.2759",
         "y" : "0.8468"
      },
      {
         "pixmapfile" : "vietnam/an_giang.svgz",
         //: Tỉnh thành Việt Nam: An Giang
         "toolTipText" : qsTr("An Giang"),
         "x" : "0.1787",
         "y" : "0.8322"
      },
      {
         "pixmapfile" : "vietnam/can_tho.svgz",
         //: Tỉnh thành Việt Nam: Cần Thơ
         "toolTipText" : qsTr("Cần Thơ"),
         "x" : "0.2575",
         "y" : "0.8708"
      },
      {
         "pixmapfile" : "vietnam/ca_mau.svgz",
         //: Tỉnh thành Việt Nam: Cà Mau
         "toolTipText" : qsTr("Cà Mau"),
         "x" : "0.2155",
         "y" : "0.8992"
      }
   ]
}
