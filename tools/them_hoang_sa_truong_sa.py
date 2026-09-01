#!/usr/bin/env python3
"""Vẽ lại bản đồ Việt Nam trong GCompris cho có quần đảo Hoàng Sa và Trường Sa.

Bản gốc của GCompris chỉ vẽ phần đất liền, thiếu hai quần đảo — không dùng được
trong trường học Việt Nam (Nghị định 18/2020/NĐ-CP, Điều 11 khoản 2).

Công cụ này sửa ba thứ trong tài nguyên hoạt động "Tìm quốc gia trên bản đồ":

  1. asiasoutheast/vietnam.svgz      — thêm hai quần đảo vào chính mảnh Việt Nam,
                                        để kéo Việt Nam là hai quần đảo đi theo
  2. asiasoutheast/southeast_asia.svgz — vẽ hai quần đảo lên nền, kèm khung và nhãn
  3. board/board12_0.qml            — tính lại tâm mảnh vì khung mảnh đã rộng ra

PHÉP CHIẾU
Bản đồ nền của GCompris là equirectangular. Hệ số suy ra từ chính dữ liệu: lấy
khung bao của 10 nước Đông Nam Á trên nền (tính từ posX/posY và kích thước từng
mảnh SVG) hồi quy với khung bao địa lý thật:

    x = 9.86092 * kinh_độ - 899.2087      (sai lệch RMS 0,23 đơn vị nền)
    y = -9.83827 * vĩ_độ  + 287.7737      (sai lệch RMS 1,11 đơn vị nền)

Kiểm chứng: mảnh Việt Nam gốc mang transform translate(-107.702 -57.826), tức
toạ độ trong tệp chính là toạ độ nền. Công thức trên cho cạnh tây của Việt Nam
(A Pa Chải 102,144°Đ) ra 108,0 so với 107,7 thực tế, cạnh bắc (Lũng Cú 23,393°B)
ra 57,6 so với 57,8 thực tế.

Usage: them_hoang_sa_truong_sa.py <thư_mục_đã_bung_geography.rcc>
"""
import gzip
import os
import re
import sys

# ------------------------------------------------------------------ phép chiếu
AX, BX = 9.86092, -899.2087
AY, BY = -9.83827, 287.7737


def toa_do(lat, lon):
    return AX * lon + BX, AY * lat + BY


# --------------------------------------------------------------- hai quần đảo
# Toạ độ các đảo, đá, bãi chính. Nguồn: danh mục địa danh hành chính Việt Nam —
# huyện đảo Hoàng Sa (Đà Nẵng) và huyện đảo Trường Sa (Khánh Hòa).
HOANG_SA = [
    ("Đá Bắc", 17.083, 111.500),
    ("Đảo Hoàng Sa", 16.833, 111.600),
    ("Đảo Hữu Nhật", 16.517, 111.583),
    ("Đảo Quang Ảnh", 16.450, 111.505),
    ("Đảo Duy Mộng", 16.467, 111.700),
    ("Đảo Quang Hòa", 16.443, 111.703),
    ("Đảo Tri Tôn", 15.783, 111.200),
    ("Đảo Phú Lâm", 16.833, 112.333),
    ("Đảo Linh Côn", 16.667, 112.733),
    ("Bãi Bông Bay", 16.050, 112.500),
]
TRUONG_SA = [
    ("Đảo Song Tử Tây", 11.427, 114.330),
    ("Đảo Song Tử Đông", 11.452, 114.362),
    ("Đảo Thị Tứ", 11.053, 114.283),
    ("Đá Xu Bi", 10.917, 114.083),
    ("Đảo Loại Ta", 10.673, 114.417),
    ("Đảo Sơn Ca", 10.383, 114.483),
    ("Đảo Ba Bình", 10.378, 114.365),
    ("Đảo Nam Yết", 10.183, 114.367),
    ("Đảo Sinh Tồn", 9.883, 114.333),
    ("Đá Vành Khăn", 9.900, 115.533),
    ("Bãi Cỏ Rong", 11.400, 116.700),
    ("Đá Chữ Thập", 9.550, 112.890),
    ("Đá Tây", 8.850, 112.200),
    ("Đá Lát", 8.667, 111.667),
    ("Đảo Trường Sa Lớn", 8.643, 111.920),
    ("Bãi Thuyền Chài", 8.167, 113.300),
    ("Đảo An Bang", 7.883, 112.917),
]
BAN_KINH = 1.15  # đơn vị nền; đảo thật quá nhỏ nên phải vẽ to lên mới thấy


def diem(nhom):
    return [(ten,) + toa_do(la, lo) for ten, la, lo in nhom]


def khung(diems, lem=2.6):
    xs = [d[1] for d in diems]
    ys = [d[2] for d in diems]
    return min(xs) - lem, min(ys) - lem, max(xs) + lem, max(ys) + lem


def doc(p):
    return gzip.open(p, "rt", encoding="utf-8").read()


def ghi(p, s):
    with gzip.open(p, "wt", encoding="utf-8") as f:
        f.write(s)


# ------------------------------------------------------- 1. mảnh Việt Nam
def sua_manh_viet_nam(path):
    s = doc(path)
    w = float(re.search(r'width="([\d.]+)"', s).group(1))
    h = float(re.search(r'height="([\d.]+)"', s).group(1))
    m = re.search(r'transform="translate\((-?[\d.]+)[ ,]+(-?[\d.]+)\)"', s)
    ox, oy = -float(m.group(1)), -float(m.group(2))   # gốc mảnh trên nền
    print(f"   mảnh gốc: {w:.3f}×{h:.3f} tại ({ox:.3f}, {oy:.3f})")

    hs, ts = diem(HOANG_SA), diem(TRUONG_SA)
    xs = [ox, ox + w] + [d[1] for d in hs + ts]
    ys = [oy, oy + h] + [d[2] for d in hs + ts]
    r = BAN_KINH
    left, top = min(xs) - r, min(ys) - r
    right, bottom = max(xs) + r, max(ys) + r
    nw, nh = right - left, bottom - top
    print(f"   mảnh mới: {nw:.3f}×{nh:.3f} tại ({left:.3f}, {top:.3f})")

    style = ("display:inline;fill:#36e79c;fill-opacity:1;stroke:#505050;"
             "stroke-width:.5;stroke-linejoin:round;stroke-opacity:1")
    cham = "\n".join(
        f'    <circle cx="{x:.3f}" cy="{y:.3f}" r="{r}" style="{style}" '
        f'transform="translate({-left:.3f} {-top:.3f})" id="hs_ts_{i}" />'
        for i, (_, x, y) in enumerate(hs + ts))

    s = re.sub(r'width="[\d.]+"', f'width="{nw:.3f}"', s, count=1)
    s = re.sub(r'height="[\d.]+"', f'height="{nh:.3f}"', s, count=1)
    s = re.sub(r'transform="translate\(-?[\d.]+[ ,]+-?[\d.]+\)"',
               f'transform="translate({-left:.3f} {-top:.3f})"', s, count=1)
    s = s.replace("</g>", cham + "\n  </g>", 1)
    ghi(path, s)
    return left, top, nw, nh


# ------------------------------------------------------------ 2. bản đồ nền
def sua_nen(path):
    s = doc(path)
    hs, ts = diem(HOANG_SA), diem(TRUONG_SA)
    dat = ("display:inline;fill:#ffffff;fill-opacity:1;stroke:#333333;"
           "stroke-width:.4;stroke-linejoin:round;stroke-opacity:1")
    khung_style = ("fill:none;stroke:#333333;stroke-width:.45;"
                   "stroke-dasharray:2.2,1.6;stroke-opacity:.85")
    chu = ("font-family:sans-serif;font-size:5.2px;font-weight:bold;"
           "fill:#333333;stroke:none")
    out = ['  <g id=\"hoang_sa_truong_sa\">']
    for ten, nhom, nhan in (("hoangsa", hs, "QĐ. HOÀNG SA"),
                            ("truongsa", ts, "QĐ. TRƯỜNG SA")):
        x0, y0, x1, y1 = khung(nhom)
        out.append(f'    <rect x="{x0:.2f}" y="{y0:.2f}" width="{x1-x0:.2f}" '
                   f'height="{y1-y0:.2f}" rx="1.5" style="{khung_style}" id="k_{ten}" />')
        for i, (_, x, y) in enumerate(nhom):
            out.append(f'    <circle cx="{x:.3f}" cy="{y:.3f}" r="{BAN_KINH}" '
                       f'style="{dat}" id="{ten}_{i}" />')
        out.append(f'    <text x="{(x0+x1)/2:.2f}" y="{y0-1.6:.2f}" '
                   f'text-anchor="middle" style="{chu}" id="t_{ten}">{nhan}</text>')
        out.append(f'    <text x="{(x0+x1)/2:.2f}" y="{y1+5.4:.2f}" '
                   f'text-anchor="middle" style="{chu};font-size:4.2px;font-weight:normal">'
                   f'(VIỆT NAM)</text>')
    out.append("  </g>")
    s = s.replace("</svg>", "\n".join(out) + "\n</svg>", 1)
    ghi(path, s)
    print(f"   nền: thêm {len(hs)+len(ts)} đảo, 2 khung, 4 nhãn")


# ------------------------------------------------------ 3. vị trí trong board
def sua_board(path, left, top, w, h, bg=(500.0, 405.0)):
    s = open(path, encoding="utf-8").read()
    px = (left + w / 2) / bg[0]
    py = (top + h / 2) / bg[1]
    i = s.find('"pixmapfile": "asiasoutheast/vietnam.svgz"')
    assert i > 0, "không thấy mục Việt Nam trong board"
    j = s.find("}", i)
    khoi = s[i:j]
    cu = re.search(r'"x":\s*"([\d.]+)".*?"y":\s*"([\d.]+)"', khoi, re.S)
    khoi_moi = re.sub(r'"x":\s*"[\d.]+"', f'"x": "{px:.4f}"', khoi)
    khoi_moi = re.sub(r'"y":\s*"[\d.]+"', f'"y": "{py:.4f}"', khoi_moi)
    open(path, "w", encoding="utf-8").write(s[:i] + khoi_moi + s[j:])
    print(f"   board: tâm ({cu.group(1)}, {cu.group(2)}) -> ({px:.4f}, {py:.4f})")


if __name__ == "__main__":
    root = sys.argv[1]
    res = None
    for dp, _, fn in os.walk(root):
        if "vietnam.svgz" in fn and dp.endswith("asiasoutheast"):
            res = dp
    assert res, "không tìm thấy thư mục asiasoutheast"
    board = os.path.join(os.path.dirname(res), "board", "board12_0.qml")
    print("1. Mảnh Việt Nam")
    left, top, w, h = sua_manh_viet_nam(os.path.join(res, "vietnam.svgz"))
    print("2. Bản đồ nền Đông Nam Á")
    sua_nen(os.path.join(res, "southeast_asia.svgz"))
    print("3. Vị trí mảnh trên nền")
    sua_board(board, left, top, w, h)
    print("Xong.")
