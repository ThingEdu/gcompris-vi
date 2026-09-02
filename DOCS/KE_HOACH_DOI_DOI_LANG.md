# Kế hoạch triển khai · ĐỐI ĐÔI LÀNG (`lang_doidoi`)

> **Cho người thi công tự động:** BẮT BUỘC dùng skill `superpowers:subagent-driven-development`
> (khuyến nghị) hoặc `superpowers:executing-plans` để thi công từng nhiệm vụ một.
> Các bước dùng ô đánh dấu `- [ ]` để theo dõi.

**Mục tiêu:** Dựng mini app thứ hai của Làng Maker — bản số hoá bộ bài 57 hình
kiểu Dobble — chạy trong GCompris trên NEO One, gồm chế độ Học hình một người và
chế độ Luật làng 2–6 người.

**Kiến trúc:** Mọi thứ tính được trước đều tính bằng Python lúc dựng và xuất ra
JSON nhúng trong `.rcc` — bộ bài, danh mục hình, bố cục xếp hình trên thẻ. QML
chỉ đọc JSON và vẽ. Nhờ vậy phần khó nhất (bất biến bộ bài, chuyện hai hình đè
nhau) được kiểm bằng `pytest` trên máy phát triển, còn máy NEO One 1,9 GB không
phải tính gì lúc chạy.

**Công nghệ:** Python 3.14 (`.venv` sẵn trong repo) · `pytest` · QML/Qt5 của
GCompris 3.1 · công cụ đóng gói `.rcc` đã có sẵn trong `tools/`.

**Spec:** `DOCS/MINI_APP_DOI_DOI_LANG.md` — đọc trước khi làm bất cứ nhiệm vụ nào.

## Ràng buộc chung cho mọi nhiệm vụ

- Tên hoạt động là `lang_doidoi`. Tiền tố `lang_` là bắt buộc — `tools/dong_goi_mini_app.py`
  chỉ nhận thư mục có tiền tố này, và GCompris gốc không dùng tiền tố này nên
  không bao giờ đụng tên.
- `tools/dong_goi_mini_app.py` bắt buộc có đúng hai tệp: `ActivityInfo.qml` và
  `Lang_doidoi.qml` (chữ cái đầu viết hoa). Thiếu là nó dừng.
- `section: "langmaker discovery"` trong `ActivityInfo.qml` — GCompris lọc mục
  bằng tìm chuỗi con, nên hoạt động hiện ở cả mục Làng Maker lẫn Khám phá. Mục
  Làng Maker đã dựng sẵn bằng `tools/va_muc_lang.py`, **không cần sửa gì thêm**.
- Giấy phép mỗi tệp mã: `SPDX-License-Identifier: GPL-3.0-or-later`,
  `SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>`.
- Chạy Python bằng `.venv/bin/python`, chạy test bằng `.venv/bin/pytest`.
- **Không ghi tệp nào lúc chạy.** Không log, không CSV, không kỷ lục ra đĩa.
- **Không có chữ trên thẻ chơi.** Chữ chỉ ở chế độ Học hình và nhãn giao diện.
- Mọi test phải **chứng minh biết fail** bằng cách phá hỏng có chủ đích trước
  khi tính là xong — lệ của repo này, xem `DOCS/MINI_APP_LANG_MAKER.md`.
- Tám màu sơn mài: Son `#C4231F` · Vàng `#E8A317` · Lục `#1F7A52` · Chàm
  `#2B57A6` · Tím `#6B3FA0` · Cánh gián `#8A4B24` · Lam ngọc `#12958E` · Đen then
  `#3A3A3A`. Thêm nền kem `#FBF8F1` và mực `#141414`.
- Máy thật: `ssh neo@192.168.1.28`, màn 1920×1080, GCompris 3.1.
  Tắt app bằng `pkill -f '[g]compris-qt'` — có ngoặc vuông, không thì lệnh ssh
  tự giết chính nó.

---

## Cấu trúc tệp

| Tệp | Trách nhiệm |
|---|---|
| `mini-app/nguon/bo-57-hinh-lang-maker.html` | Nguồn gốc 57 hình. **Nằm ngoài thư mục app** vì `dong_goi_mini_app.py` chép cả thư mục app vào `.rcc` |
| `tools/sinh_bo_bai.py` | Sinh mặt phẳng xạ ảnh → `bo_bai_31.json`, `bo_bai_57.json` |
| `tools/tach_57_hinh.py` | Bung 57 SVG khỏi HTML, thay màu CSS → SVG rời + `hinh.json` |
| `tools/sinh_bo_cuc.py` | Sinh bố cục xếp hình không đè nhau → `bo_cuc.json` |
| `…/lang_doidoi/ActivityInfo.qml` | Tên, mô tả, mục, icon, điều kiện tiên quyết |
| `…/lang_doidoi/Lang_doidoi.qml` | Khung màn, màn vào bàn, điều phối hai chế độ |
| `…/lang_doidoi/The.qml` | Vẽ một thẻ tròn từ bố cục + danh sách hình |
| `…/lang_doidoi/LuatLang.qml` | Ván chơi 2–6 người |
| `…/lang_doidoi/HocHinh.qml` | Chế độ một người, 5 mức |
| `…/lang_doidoi/lang_doidoi.js` | Trạng thái ván: chia bài, chấm đúng sai, khoá ô |
| `tests/test_bo_bai.py`, `tests/test_tach_57_hinh.py`, `tests/test_bo_cuc.py` | Kiểm ba bộ dữ liệu sinh ra |

**Khác spec một chỗ, có chủ ý:** spec §8 nói xếp hình lúc chạy rồi kiểm không đè
nhau; kế hoạch chuyển việc đó sang **lúc dựng** (nhiệm vụ 3). Lý do: bất biến
"không hai hình nào đè nhau" trở nên kiểm được bằng `pytest`, và rủi ro "vòng
lặp thử vô hạn" ghi ở spec §12 biến mất khỏi máy thật. QML chỉ chọn ngẫu nhiên
một bố cục đã kiểm sẵn rồi xoay từng hình quanh tâm của nó — xoay không đổi
đường tròn bao nên không phá vỡ bất biến.

---

## Nhiệm vụ 1 · Bộ sinh bộ bài

**Tệp:**
- Tạo: `tools/sinh_bo_bai.py`
- Tạo: `tests/test_bo_bai.py`

**Giao diện:**
- Dùng của nhiệm vụ trước: không có, đây là nhiệm vụ đầu.
- Cung cấp cho nhiệm vụ sau: `sinh_bo_bai(q) -> list[list[int]]` trả về danh
  sách thẻ, mỗi thẻ là danh sách chỉ số hình 0-based. `ghi_json(q, duong_dan)`
  ghi ra tệp `{"q": q, "so_the": n, "so_hinh_moi_the": q+1, "the": [[...], ...]}`.

- [ ] **Bước 1: Viết test đỏ**

Tạo `tests/test_bo_bai.py`:

```python
"""Kiểm bộ bài Dobble sinh từ mặt phẳng xạ ảnh hữu hạn.

Bất biến của cả trò chơi: HAI THẺ BẤT KỲ TRÙNG ĐÚNG MỘT HÌNH. Hỏng bất biến
này thì trò chơi vô nghĩa — có lượt không ai gọi được, hoặc có lượt gọi kiểu
gì cũng đúng. Vì vậy kiểm ở đây, lúc dựng, chứ không kiểm lúc chạy trên máy.
"""
from collections import Counter
from itertools import combinations

import pytest

from tools.sinh_bo_bai import sinh_bo_bai

CAP = [(5, 31, 6), (7, 57, 8)]


@pytest.mark.parametrize("q,so_the,moi_the", CAP)
def test_dung_so_the_va_so_hinh(q, so_the, moi_the):
    bai = sinh_bo_bai(q)
    assert len(bai) == so_the
    assert all(len(t) == moi_the for t in bai)


@pytest.mark.parametrize("q,so_the,moi_the", CAP)
def test_moi_cap_the_trung_dung_mot_hinh(q, so_the, moi_the):
    bai = sinh_bo_bai(q)
    sai = [(a, b) for a, b in combinations(range(len(bai)), 2)
           if len(set(bai[a]) & set(bai[b])) != 1]
    assert sai == []


@pytest.mark.parametrize("q,so_the,moi_the", CAP)
def test_moi_hinh_xuat_hien_dung_so_lan(q, so_the, moi_the):
    bai = sinh_bo_bai(q)
    dem = Counter(h for t in bai for h in t)
    assert set(dem.values()) == {moi_the}


@pytest.mark.parametrize("q,so_the,moi_the", CAP)
def test_khong_the_nao_co_hinh_lap(q, so_the, moi_the):
    bai = sinh_bo_bai(q)
    assert all(len(set(t)) == len(t) for t in bai)


@pytest.mark.parametrize("q,so_the,moi_the", CAP)
def test_dung_dung_cac_hinh_tu_0_den_n_tru_1(q, so_the, moi_the):
    bai = sinh_bo_bai(q)
    assert set(h for t in bai for h in t) == set(range(so_the))


def test_bo_de_chi_dung_hinh_01_den_31():
    """Cấp Dễ dùng hình số 01-31 của bộ gốc: trọn nhóm A + trọn nhóm B +
    chín hình đầu nhóm C. Chỉ số 0-based nên là 0..30."""
    bai = sinh_bo_bai(5)
    assert max(h for t in bai for h in t) == 30


def test_tu_choi_bac_khong_phai_so_nguyen_to():
    with pytest.raises(ValueError):
        sinh_bo_bai(6)
```

- [ ] **Bước 2: Chạy test cho thấy nó đỏ**

Chạy: `.venv/bin/pytest tests/test_bo_bai.py -q`
Chờ đợi: FAIL — `ModuleNotFoundError: No module named 'tools.sinh_bo_bai'`

- [ ] **Bước 3: Viết bộ sinh**

Tạo `tools/sinh_bo_bai.py`:

```python
#!/usr/bin/env python3
"""Sinh bộ bài Dobble từ mặt phẳng xạ ảnh hữu hạn bậc q.

Với q là số nguyên tố: số thẻ = số hình = q² + q + 1, mỗi thẻ q + 1 hình, và
hai thẻ bất kỳ trùng ĐÚNG MỘT hình. Bộ 57 hình của làng khớp chính xác bậc 7.

    sinh_bo_bai.py <thư_mục_ra>      # ghi bo_bai_31.json và bo_bai_57.json

Bộ bài tính sẵn rồi nhúng vào .rcc, QML chỉ đọc. Hai lý do: máy NEO One 1,9 GB
không nên tính lúc khởi động, và bất biến trên kiểm được bằng pytest.
"""
import json
import os
import sys

NGUYEN_TO = (2, 3, 5, 7, 11, 13)


def sinh_bo_bai(q):
    """Trả về danh sách thẻ, mỗi thẻ là danh sách chỉ số hình 0-based."""
    if q not in NGUYEN_TO:
        raise ValueError(f"bậc {q} phải là số nguyên tố, đã biết: {NGUYEN_TO}")
    # Thẻ đầu là "đường vô tận": q+1 hình đầu tiên.
    the = [list(range(q + 1))]
    # q thẻ đi qua hình 0.
    for i in range(q):
        the.append([0] + [q + 1 + q * i + j for j in range(q)])
    # q² thẻ còn lại, mỗi thẻ đi qua đúng một hình vô tận 1+i.
    for i in range(q):
        for j in range(q):
            the.append([1 + i] + [q + 1 + q * k + ((i * k + j) % q)
                                  for k in range(q)])
    return the


def ghi_json(q, duong_dan):
    bai = sinh_bo_bai(q)
    du_lieu = {"q": q, "so_the": len(bai), "so_hinh_moi_the": q + 1, "the": bai}
    with open(duong_dan, "w", encoding="utf-8") as f:
        json.dump(du_lieu, f, ensure_ascii=False, indent=1)
    return du_lieu


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    ra = sys.argv[1]
    os.makedirs(ra, exist_ok=True)
    for q in (5, 7):
        d = ghi_json(q, os.path.join(ra, f"bo_bai_{q * q + q + 1}.json"))
        print(f"bậc {q}: {d['so_the']} thẻ × {d['so_hinh_moi_the']} hình")


if __name__ == "__main__":
    main()
```

- [ ] **Bước 4: Chạy test cho thấy nó xanh**

Chạy: `.venv/bin/pytest tests/test_bo_bai.py -q`
Chờ đợi: PASS, 11 test.

- [ ] **Bước 5: Chứng minh test biết fail**

Phá hỏng có chủ đích, mỗi lần một chỗ, xác nhận test đỏ rồi hoàn nguyên:

1. Đổi `((i * k + j) % q)` thành `((i * k * k + j) % q)` →
   `test_moi_cap_the_trung_dung_mot_hinh` phải đỏ.

   *Đừng phá bằng `+ 1`*: cộng thêm hằng số chỉ hoán vị nhãn hình trong cùng
   một lớp, cấu trúc xạ ảnh không đổi nên test vẫn xanh. Phải phá vào chỗ
   `i · k` — chính tích này mới là thứ bảo đảm hai đường thẳng cắt nhau đúng
   một điểm.
2. Đổi thẻ đầu thành `list(range(q))` →
   `test_dung_so_the_va_so_hinh` phải đỏ.
3. Đổi `[1 + i]` thành `[0]` ở vòng cuối →
   `test_moi_hinh_xuat_hien_dung_so_lan` phải đỏ.
4. Bỏ dòng `raise ValueError` → `test_tu_choi_bac_khong_phai_so_nguyen_to` phải đỏ.

Ghi lại bốn kết quả vào phần mô tả commit. **Chỗ nào phá mà test vẫn xanh thì
test đó vô dụng, phải viết lại.**

- [ ] **Bước 6: Sinh dữ liệu thật**

```bash
mkdir -p mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/resource
.venv/bin/python tools/sinh_bo_bai.py \
  mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/resource
```

Chờ đợi in ra: `bậc 5: 31 thẻ × 6 hình` và `bậc 7: 57 thẻ × 8 hình`.

- [ ] **Bước 7: Commit**

```bash
git add tools/sinh_bo_bai.py tests/test_bo_bai.py \
        mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/resource/bo_bai_*.json
git commit -m "Đối Đôi Làng: bộ sinh bài từ mặt phẳng xạ ảnh"
```

---

## Nhiệm vụ 2 · Tách 57 hình khỏi tệp HTML

**Tệp:**
- Dời: `mini-app/lang_doidoi/nguon/bo-57-hinh-lang-maker.html` → `mini-app/nguon/bo-57-hinh-lang-maker.html`
- Tạo: `tools/tach_57_hinh.py`
- Tạo: `tests/test_tach_57_hinh.py`

**Giao diện:**
- Dùng của nhiệm vụ trước: thư mục `resource/` đã tạo ở nhiệm vụ 1.
- Cung cấp cho nhiệm vụ sau: 57 tệp `resource/hinh/NN-<ma>.svg` (NN là số hai
  chữ số 01–57, `<ma>` là tên không dấu nối gạch dưới, ví dụ `01-neo_tre.svg`)
  và `resource/hinh.json` là danh sách
  `[{"so": 1, "ma": "neo_tre", "ten": "Neo Tre", "nhom": "A", "mau": "#1F7A52", "nghia": "Măng tre — linh vật làng"}, …]`.

**Vì sao dời tệp nguồn:** `tools/dong_goi_mini_app.py` chép **cả thư mục app**
vào `.rcc` (`shutil.copytree(goc_app, cay)`). Để nguyên `nguon/` bên trong thì
tệp HTML 41 KB chui vào gói tài nguyên của máy thật một cách vô ích. Thư mục
`mini-app/nguon/` không có tiền tố `lang_` nên `danh_sach_app()` bỏ qua.

- [ ] **Bước 1: Dời tệp nguồn**

```bash
mkdir -p mini-app/nguon
git mv mini-app/lang_doidoi/nguon/bo-57-hinh-lang-maker.html mini-app/nguon/
rmdir mini-app/lang_doidoi/nguon
```

- [ ] **Bước 2: Viết test đỏ**

Tạo `tests/test_tach_57_hinh.py`:

```python
"""Kiểm 57 hình bung ra từ tệp HTML nguồn.

Bẫy lớn nhất: Qt5 trong GCompris 3.1 dựng SVG theo chuẩn SVG Tiny 1.2, KHÔNG
hiểu `fill="currentColor"` lẫn `stroke="var(--vang)"` — mà bộ hình gốc dùng cả
hai. Không thay hết thành mã hex thì hình ra trắng trơn trên máy thật, mà trên
trình duyệt lại nhìn vẫn đẹp. Vì vậy phải kiểm ở đây.
"""
import json
import os
import re
import xml.etree.ElementTree as ET

import pytest

GOC = os.path.join(os.path.dirname(__file__), "..")
RA = os.path.join(GOC, "mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/resource")
THU_MUC_HINH = os.path.join(RA, "hinh")

MAU_HOP_LE = {
    "#C4231F", "#E8A317", "#1F7A52", "#2B57A6",
    "#6B3FA0", "#8A4B24", "#12958E", "#3A3A3A",
    "#FBF8F1", "#141414",
}
NHOM_HOP_LE = set("ABCDE")


@pytest.fixture(scope="module")
def danh_muc():
    with open(os.path.join(RA, "hinh.json"), encoding="utf-8") as f:
        return json.load(f)


def tep_svg():
    return sorted(t for t in os.listdir(THU_MUC_HINH) if t.endswith(".svg"))


def test_du_57_tep_svg():
    assert len(tep_svg()) == 57


def test_moi_tep_svg_doc_duoc_bang_bo_doc_xml():
    for t in tep_svg():
        ET.parse(os.path.join(THU_MUC_HINH, t))


def test_khong_con_bien_css_hay_currentcolor():
    hong = []
    for t in tep_svg():
        noi_dung = open(os.path.join(THU_MUC_HINH, t), encoding="utf-8").read()
        if "var(--" in noi_dung or "currentColor" in noi_dung:
            hong.append(t)
    assert hong == []


def test_moi_ma_mau_nam_trong_bang_da_biet():
    la = {}
    for t in tep_svg():
        noi_dung = open(os.path.join(THU_MUC_HINH, t), encoding="utf-8").read()
        for m in re.findall(r"#[0-9A-Fa-f]{6}", noi_dung):
            if m.upper() not in MAU_HOP_LE:
                la.setdefault(t, set()).add(m)
    assert la == {}


def test_danh_muc_du_57_muc(danh_muc):
    assert len(danh_muc) == 57


def test_danh_muc_khong_trung_ma_khong_trung_ten(danh_muc):
    ma = [h["ma"] for h in danh_muc]
    ten = [h["ten"] for h in danh_muc]
    assert len(set(ma)) == 57
    assert len(set(ten)) == 57


def test_danh_muc_du_truong_va_nhom_hop_le(danh_muc):
    for h in danh_muc:
        assert set(h) == {"so", "ma", "ten", "nhom", "mau", "nghia"}
        assert h["nhom"] in NHOM_HOP_LE
        assert h["mau"].upper() in MAU_HOP_LE
        assert h["ten"].strip()


def test_so_chay_lien_tuc_tu_1_den_57(danh_muc):
    assert [h["so"] for h in danh_muc] == list(range(1, 58))


def test_moi_muc_danh_muc_co_dung_mot_tep_svg(danh_muc):
    co = set(tep_svg())
    thieu = [h for h in danh_muc
             if f"{h['so']:02d}-{h['ma']}.svg" not in co]
    assert thieu == []


def test_dung_so_luong_tung_nhom(danh_muc):
    from collections import Counter
    assert Counter(h["nhom"] for h in danh_muc) == {
        "A": 10, "B": 12, "C": 12, "D": 11, "E": 12}


def test_ma_khong_dau_va_khong_khoang_trang(danh_muc):
    for h in danh_muc:
        assert re.fullmatch(r"[a-z0-9_]+", h["ma"]), h["ma"]
```

- [ ] **Bước 3: Chạy test cho thấy nó đỏ**

Chạy: `.venv/bin/pytest tests/test_tach_57_hinh.py -q`
Chờ đợi: FAIL — `FileNotFoundError` vì chưa có thư mục `resource/hinh`.

- [ ] **Bước 4: Viết bộ tách**

Tạo `tools/tach_57_hinh.py`:

```python
#!/usr/bin/env python3
"""Bung 57 hình của Làng Maker khỏi tệp HTML một trang thành SVG rời.

Bẫy phải xử lý: Qt5 dựng SVG theo chuẩn SVG Tiny 1.2, không hiểu hai thứ mà
bộ hình gốc dùng:

  fill="currentColor"     màu thân hình, thừa hưởng từ class c-luc, c-son… của thẻ
  stroke="var(--vang)"    biến CSS của trình duyệt

Cả hai phải thay thành mã hex thật, nếu không hình ra trắng trơn trên máy thật
mà xem trên trình duyệt vẫn thấy đẹp.

    tach_57_hinh.py <tệp_html> <thư_mục_ra>
"""
import json
import os
import re
import sys
import unicodedata

MAU = {
    "son": "#C4231F", "vang": "#E8A317", "luc": "#1F7A52", "lam": "#2B57A6",
    "tim": "#6B3FA0", "gian": "#8A4B24", "ngoc": "#12958E", "then": "#3A3A3A",
}
NHOM_THEO_SO = [("A", 1, 10), ("B", 11, 22), ("C", 23, 34),
                ("D", 35, 45), ("E", 46, 57)]

THE = re.compile(
    r'<div class="card c-(?P<mau>[\w-]+)"><span class="num">(?P<so>\d+)</span>\s*'
    r'(?P<svg><svg.*?</svg>)\s*'
    r'<div class="nm">(?P<ten>.*?)</div><div class="vi">(?P<nghia>.*?)</div>',
    re.S)


def khong_dau(s):
    """"Bảng đen & phấn" -> "bang_den_phan". Chỉ dùng cho tên tệp và mã."""
    s = s.replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_").lower()
    return s


def nhom_cua(so):
    for ten, dau, cuoi in NHOM_THEO_SO:
        if dau <= so <= cuoi:
            return ten
    raise ValueError(f"hình số {so} không thuộc nhóm nào")


def go_html(s):
    return (s.replace("&amp;", "&").replace("&lt;", "<")
             .replace("&gt;", ">").replace("&quot;", '"').strip())


def sua_mau(svg, mau_than):
    """Thay currentColor và var(--x) bằng mã hex thật."""
    svg = svg.replace("currentColor", mau_than)
    def thay(m):
        ten = m.group(1)
        if ten not in MAU:
            raise ValueError(f"biến màu lạ: var(--{ten})")
        return MAU[ten]
    return re.sub(r"var\(--([\w-]+)\)", thay, svg)


def tach(html, ra):
    thu_muc_hinh = os.path.join(ra, "hinh")
    os.makedirs(thu_muc_hinh, exist_ok=True)
    noi_dung = open(html, encoding="utf-8").read()

    danh_muc = []
    for m in THE.finditer(noi_dung):
        so = int(m.group("so"))
        ten = go_html(m.group("ten"))
        ma = khong_dau(ten)
        mau_than = MAU[m.group("mau")]
        svg = sua_mau(m.group("svg"), mau_than)
        if "var(--" in svg or "currentColor" in svg:
            raise ValueError(f"hình {so:02d} còn sót màu chưa thay")
        ten_tep = f"{so:02d}-{ma}.svg"
        with open(os.path.join(thu_muc_hinh, ten_tep), "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n' + svg + "\n")
        danh_muc.append({"so": so, "ma": ma, "ten": ten, "nhom": nhom_cua(so),
                         "mau": mau_than, "nghia": go_html(m.group("nghia"))})

    if len(danh_muc) != 57:
        raise SystemExit(f"chỉ tách được {len(danh_muc)} hình, phải đủ 57")
    danh_muc.sort(key=lambda h: h["so"])
    with open(os.path.join(ra, "hinh.json"), "w", encoding="utf-8") as f:
        json.dump(danh_muc, f, ensure_ascii=False, indent=1)
    return danh_muc


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    d = tach(sys.argv[1], sys.argv[2])
    print(f"tách được {len(d)} hình")


if __name__ == "__main__":
    main()
```

- [ ] **Bước 5: Sinh dữ liệu rồi chạy test**

```bash
.venv/bin/python tools/tach_57_hinh.py \
  mini-app/nguon/bo-57-hinh-lang-maker.html \
  mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/resource
.venv/bin/pytest tests/test_tach_57_hinh.py -q
```

Chờ đợi: in `tách được 57 hình`, rồi 11 test PASS.

Nếu `test_moi_ma_mau_nam_trong_bang_da_biet` đỏ vì có mã màu lạ, **đừng nới
bảng màu** — mở tệp HTML nguồn xem hình nào dùng màu ngoài bảng và hỏi chủ dự
án, vì tám màu sơn mài là quy ước nhận diện của làng.

- [ ] **Bước 6: Chứng minh test biết fail**

1. Bỏ dòng `svg = svg.replace("currentColor", mau_than)` →
   `test_khong_con_bien_css_hay_currentcolor` phải đỏ.
2. Bỏ hàm `thay` (trả nguyên `svg` trong `sua_mau`) → cũng test đó phải đỏ.
3. Đổi một mã trong `MAU` thành `#123456` →
   `test_moi_ma_mau_nam_trong_bang_da_biet` phải đỏ.
4. Sửa `NHOM_THEO_SO` cho nhóm C thành `(23, 33)` →
   `test_dung_so_luong_tung_nhom` phải đỏ (và `nhom_cua(34)` ném lỗi).
5. Bỏ `khong_dau` (dùng thẳng `ten.lower()`) →
   `test_ma_khong_dau_va_khong_khoang_trang` phải đỏ.
6. Xoá một `<div class="card …>` khỏi bản sao tệp HTML →
   `tach()` phải dừng với "chỉ tách được 56 hình".

- [ ] **Bước 7: Commit**

```bash
git add tools/tach_57_hinh.py tests/test_tach_57_hinh.py mini-app/nguon \
        mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/resource/hinh \
        mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/resource/hinh.json
git commit -m "Đối Đôi Làng: tách 57 hình, thay màu CSS thành hex cho Qt5"
```

---

## Nhiệm vụ 3 · Bố cục xếp hình trên thẻ

**Tệp:**
- Tạo: `tools/sinh_bo_cuc.py`
- Tạo: `tests/test_bo_cuc.py`

**Giao diện:**
- Dùng của nhiệm vụ trước: không.
- Cung cấp cho nhiệm vụ sau: `resource/bo_cuc.json` dạng
  `{"6": [[[x, y, r], …6 hình], …24 bố cục], "8": [[…8 hình], …24 bố cục]}`.
  `x`, `y`, `r` là số thực trong **đĩa đơn vị**: tâm thẻ ở `(0, 0)`, mép thẻ ở
  bán kính `1`. QML nhân với bán kính thẻ thật để ra pixel.

**Tham số đã dò được bằng thực nghiệm** (dựng 40/40 lần thành công cho cả hai
cấp — đừng đổi nếu không dò lại):

| Số hình | Vòng trong | Bán kính gốc |
|---|---|---|
| 6 | 1 hình ở tâm | 0,255 |
| 8 | 2 hình quanh tâm | 0,215 |

- [ ] **Bước 1: Viết test đỏ**

Tạo `tests/test_bo_cuc.py`:

```python
"""Kiểm bố cục xếp hình trên thẻ tròn.

Xếp hình lúc DỰNG chứ không lúc chạy: nhờ vậy bất biến "không hai hình nào đè
nhau" kiểm được bằng pytest, và máy thật không phải chạy vòng lặp thử-và-sai
giữa buổi chơi. QML chỉ chọn ngẫu nhiên một bố cục rồi xoay từng hình quanh
tâm của chính nó — xoay không đổi đường tròn bao nên bất biến vẫn còn.
"""
import json
import math
import os
from itertools import combinations

import pytest

GOC = os.path.join(os.path.dirname(__file__), "..")
RA = os.path.join(GOC, "mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/resource")

KHE = 0.012        # khe hở tối thiểu giữa hai hình, theo bán kính thẻ


@pytest.fixture(scope="module")
def bo_cuc():
    with open(os.path.join(RA, "bo_cuc.json"), encoding="utf-8") as f:
        return json.load(f)


def test_co_du_hai_cap(bo_cuc):
    assert set(bo_cuc) == {"6", "8"}


def test_moi_cap_co_it_nhat_20_bo_cuc(bo_cuc):
    for so, ds in bo_cuc.items():
        assert len(ds) >= 20, f"cấp {so} chỉ có {len(ds)} bố cục"


def test_moi_bo_cuc_dung_so_hinh(bo_cuc):
    for so, ds in bo_cuc.items():
        assert all(len(b) == int(so) for b in ds)


def test_khong_hai_hinh_nao_de_nhau(bo_cuc):
    for so, ds in bo_cuc.items():
        for i, b in enumerate(ds):
            for (x1, y1, r1), (x2, y2, r2) in combinations(b, 2):
                d = math.hypot(x1 - x2, y1 - y2)
                assert d >= r1 + r2 + KHE, f"cấp {so} bố cục {i}: đè nhau"


def test_moi_hinh_nam_tron_trong_the(bo_cuc):
    for so, ds in bo_cuc.items():
        for i, b in enumerate(ds):
            for x, y, r in b:
                assert math.hypot(x, y) + r <= 1.0, f"cấp {so} bố cục {i}: tràn mép"


def test_co_lech_co_giua_cac_hinh(bo_cuc):
    """Giống thẻ giấy: hình to nhỏ lệch nhau, không đều tăm tắp."""
    for so, ds in bo_cuc.items():
        for b in ds:
            bk = [r for _, _, r in b]
            assert max(bk) / min(bk) > 1.05


def test_lech_co_khong_qua_15_phan_tram(bo_cuc):
    for so, ds in bo_cuc.items():
        for b in ds:
            bk = [r for _, _, r in b]
            assert max(bk) / min(bk) <= 1.15 / 0.85 + 1e-9


def test_cac_bo_cuc_khac_nhau(bo_cuc):
    for so, ds in bo_cuc.items():
        khoa = {json.dumps(b) for b in ds}
        assert len(khoa) == len(ds)
```

- [ ] **Bước 2: Chạy test cho thấy nó đỏ**

Chạy: `.venv/bin/pytest tests/test_bo_cuc.py -q`
Chờ đợi: FAIL — `FileNotFoundError: … bo_cuc.json`

- [ ] **Bước 3: Viết bộ sinh bố cục**

Tạo `tools/sinh_bo_cuc.py`:

```python
#!/usr/bin/env python3
"""Sinh sẵn các bố cục xếp hình trên thẻ tròn, không hình nào đè hình nào.

Toạ độ tính trong ĐĨA ĐƠN VỊ: tâm thẻ (0, 0), mép thẻ bán kính 1. QML nhân với
bán kính thẻ thật để ra pixel, nên bố cục dùng được cho mọi cỡ màn.

Sinh lúc dựng thay vì lúc chạy: bất biến "không đè nhau" kiểm được bằng pytest,
và máy thật khỏi chạy vòng thử-và-sai giữa buổi chơi.

    sinh_bo_cuc.py <thư_mục_ra>
"""
import json
import math
import os
import random
import sys
from itertools import combinations

GIEO = 20260902        # gieo cố định để lần dựng nào cũng ra bộ bố cục y hệt
SO_BO_CUC = 24
KHE = 0.012

# (số hình ở vòng trong, bán kính gốc) — dò bằng thực nghiệm, 40/40 lần đạt
CAU_HINH = {6: (1, 0.255), 8: (2, 0.215)}


def mot_bo_cuc(so_hinh, rng, so_lan=600):
    trong, r_goc = CAU_HINH[so_hinh]
    ngoai = so_hinh - trong
    for _ in range(so_lan):
        diem = []
        for i in range(so_hinh):
            r = r_goc * rng.uniform(0.85, 1.15)          # lệch cỡ ±15%
            if i < trong:
                if trong == 1:
                    x = y = 0.0
                else:
                    goc = 2 * math.pi * i / trong + rng.uniform(-0.3, 0.3)
                    x, y = 0.30 * math.cos(goc), 0.30 * math.sin(goc)
                x += rng.uniform(-0.05, 0.05)
                y += rng.uniform(-0.05, 0.05)
            else:
                k = i - trong
                goc = 2 * math.pi * k / ngoai + rng.uniform(-0.15, 0.15)
                bk = (1 - r) * rng.uniform(0.80, 0.95)
                x, y = bk * math.cos(goc), bk * math.sin(goc)
            diem.append((x, y, r))
        roi = any(math.hypot(x1 - x2, y1 - y2) < r1 + r2 + KHE
                  for (x1, y1, r1), (x2, y2, r2) in combinations(diem, 2))
        tran = any(math.hypot(x, y) + r > 1.0 for x, y, r in diem)
        if not roi and not tran:
            return [[round(x, 5), round(y, 5), round(r, 5)] for x, y, r in diem]
    return None


def sinh(ra):
    rng = random.Random(GIEO)
    ket = {}
    for so_hinh in sorted(CAU_HINH):
        ds = []
        while len(ds) < SO_BO_CUC:
            b = mot_bo_cuc(so_hinh, rng)
            if b is None:
                raise SystemExit(f"không dựng nổi bố cục {so_hinh} hình — "
                                 f"giảm bán kính gốc trong CAU_HINH")
            if b not in ds:
                ds.append(b)
        ket[str(so_hinh)] = ds
    with open(os.path.join(ra, "bo_cuc.json"), "w", encoding="utf-8") as f:
        json.dump(ket, f, ensure_ascii=False, indent=1)
    return ket


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    k = sinh(sys.argv[1])
    for so, ds in k.items():
        print(f"{so} hình: {len(ds)} bố cục")


if __name__ == "__main__":
    main()
```

- [ ] **Bước 4: Sinh dữ liệu rồi chạy test**

```bash
.venv/bin/python tools/sinh_bo_cuc.py \
  mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/resource
.venv/bin/pytest tests/test_bo_cuc.py -q
```

Chờ đợi: in `6 hình: 24 bố cục` và `8 hình: 24 bố cục`, rồi 8 test PASS.

- [ ] **Bước 5: Chứng minh test biết fail**

1. Đổi `KHE` trong `sinh_bo_cuc.py` thành `-0.20` (cho phép đè) →
   `test_khong_hai_hinh_nao_de_nhau` phải đỏ.
2. Đổi `bk = (1 - r) * …` thành `bk = 1.0 * …` →
   `test_moi_hinh_nam_tron_trong_the` phải đỏ.
3. Bỏ nhiễu cỡ (`r = r_goc`) → `test_co_lech_co_giua_cac_hinh` phải đỏ.
4. Đổi `rng.uniform(0.85, 1.15)` thành `rng.uniform(0.5, 1.5)` →
   `test_lech_co_khong_qua_15_phan_tram` phải đỏ.
5. Đổi `SO_BO_CUC` thành `5` → `test_moi_cap_co_it_nhat_20_bo_cuc` phải đỏ.

- [ ] **Bước 6: Commit**

```bash
git add tools/sinh_bo_cuc.py tests/test_bo_cuc.py \
        mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/resource/bo_cuc.json
git commit -m "Đối Đôi Làng: bố cục xếp hình không đè nhau, sinh lúc dựng"
```

---

## Nhiệm vụ 4 · Thử SVG trên NEO One thật (cửa gác)

Đây là **rủi ro số một** của cả dự án (spec §12). Làm trước khi viết bất kỳ QML
nào khác. Nếu Qt5 không dựng nổi bộ hình thì toàn bộ nhiệm vụ 5–8 phải đổi
cách, nên phải biết ngay bây giờ.

**Tệp:**
- Tạo tạm: `/tmp/thu_svg.qml` trên NEO One (không commit)

- [ ] **Bước 1: Chép sáu hình đại diện sang máy thật**

Chọn sáu hình khó nhất — nhiều lớp, nhiều màu, có nét trắng đè lên nền màu:

```bash
cd mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/resource/hinh
scp 01-neo_tre.svg 02-tux.svg 03-trau_mo.svg \
    24-den_led.svg 31-cam_bien_sieu_am.svg 48-trong_lang.svg \
    neo@192.168.1.28:/tmp/
```

- [ ] **Bước 2: Viết màn thử trên máy thật**

```bash
ssh neo@192.168.1.28 'cat > /tmp/thu_svg.qml' <<"EOF"
import QtQuick 2.12
import QtQuick.Window 2.12
Window {
    visible: true; width: 1200; height: 300; color: "#FBF8F1"
    Row {
        anchors.centerIn: parent; spacing: 24
        Repeater {
            model: ["01-neo_tre", "02-tux", "03-trau_mo",
                    "24-den_led", "31-cam_bien_sieu_am", "48-trong_lang"]
            Image {
                source: "file:///tmp/" + modelData + ".svg"
                sourceSize.width: 180; sourceSize.height: 180
                onStatusChanged: if (status === Image.Error)
                                     console.log("HỎNG: " + modelData)
            }
        }
    }
}
EOFEOF
```

- [ ] **Bước 3: Chạy thử và chụp lại**

```bash
ssh neo@192.168.1.28 "pkill -f '[g]compris-qt'; sleep 1; \
  export DISPLAY=:0 XDG_RUNTIME_DIR=/run/user/1000; \
  setsid nohup qmlscene /tmp/thu_svg.qml > /tmp/thu_svg.log 2>&1 < /dev/null & \
  sleep 5; gnome-screenshot -f /tmp/thu_svg.png; cat /tmp/thu_svg.log"
scp neo@192.168.1.28:/tmp/thu_svg.png /tmp/
```

Nếu máy không có `qmlscene`, cài bằng `sudo apt install qml-module-qtquick2 qmlscene`,
hoặc bỏ qua bước này và thử thẳng bằng nhiệm vụ 5 (chậm hơn nhưng vẫn được).

- [ ] **Bước 4: Xem ảnh và quyết**

Mở `/tmp/thu_svg.png` và nhìn tận mắt. **Không được tin vào việc "không có lỗi
trong log"** — Qt dựng SVG hỏng thường ra hình trắng hoặc mất lớp mà không báo
lỗi gì.

- **Sáu hình đều đúng** → ghi kết quả vào `DOCS/MINI_APP_DOI_DOI_LANG.md` mục
  Rủi ro, đóng rủi ro này lại, đi tiếp nhiệm vụ 5.
- **Có hình sai** → dừng, báo chủ dự án, chuyển sang đường lui: thêm bước dựng
  PNG 256×256 vào `tools/tach_57_hinh.py` (dùng `cairosvg` trên máy phát triển,
  KHÔNG cài gì lên NEO One), và mọi `source:` trong nhiệm vụ 5–8 đổi từ `.svg`
  sang `.png`.

- [ ] **Bước 5: Ghi kết quả**

```bash
git commit -am "Đối Đôi Làng: kết quả thử SVG trên NEO One thật"
```

---

## Nhiệm vụ 5 · Khung hoạt động và màn vào bàn

**Tệp:**
- Tạo: `mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/ActivityInfo.qml`
- Tạo: `mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/Lang_doidoi.qml`

**Giao diện:**
- Dùng của nhiệm vụ trước: `resource/hinh.json`, `resource/bo_bai_31.json`,
  `resource/bo_bai_57.json`, `resource/bo_cuc.json`, `resource/hinh/*.svg`.
- Cung cấp cho nhiệm vụ sau: `Lang_doidoi.qml` giữ `QtObject { id: items }` với
  các thuộc tính `soNguoi` (int 2–6), `capKho` (bool, false = 31 thẻ),
  `hoaTieu` (int, chỉ số người 0-based hoặc −1 nếu không ai), `manHienTai`
  (string: `"vao_ban"` / `"luat_lang"` / `"hoc_hinh"`). `HocHinh.qml` và
  `LuatLang.qml` nạp bằng `Loader` theo `manHienTai`.

- [ ] **Bước 1: Viết ActivityInfo.qml**

```qml
/* GCompris - Đối Đôi Làng
 *
 * SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
 *   SPDX-License-Identifier: GPL-3.0-or-later
 *
 * Linh vật Tux trong bộ hình là bản vẽ lại; linh vật Linux gốc của Larry Ewing.
 */
import GCompris 1.0

ActivityInfo {
  name: "lang_doidoi/Lang_doidoi.qml"
  difficulty: 2
  icon: "lang_doidoi/resource/hinh/01-neo_tre.svg"
  author: "ThingEdu &lt;tuan@rogo.com.vn&gt;"
  title: qsTr("Đối Đôi Làng")
  description: qsTr("Bộ bài 57 hình của Làng Maker: hai thẻ bất kỳ luôn có đúng một hình giống nhau.")
  goal: qsTr("Nhìn nhanh, gọi to, tìm ra hình giống nhau giữa hai thẻ. Cả bàn cùng phá hết chồng thẻ trước khi hết giờ.")
  prerequisite: qsTr("Đọc được tiếng Việt.")
  manual: qsTr("Học hình: một mình, nhớ mặt và tên 57 hình của làng qua năm mức.") + "<br><br>" +
          qsTr("Luật làng: 2 đến 6 người quanh một máy. Máy chia bài, lật thẻ và bấm giờ; các con nhìn chung hai thẻ rồi REO TO tên hình giống nhau. Ai gọi được thì bấm vào ô tên mình, rồi bấm vào hình đó.") + "<br><br>" +
          qsTr("Cả bàn thắng cùng nhau, không ai thắng một mình. Bạn làm Hoa tiêu không được ghi lượt, nhưng bấm phím cách để nháy gợi ý cho cả bàn.")
  credit: ""
  section: "langmaker discovery"
  createdInVersion: 0
}
```

- [ ] **Bước 2: Viết Lang_doidoi.qml — màn vào bàn**

```qml
/* GCompris - Đối Đôi Làng
 *
 * SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
 *   SPDX-License-Identifier: GPL-3.0-or-later
 */
import QtQuick 2.12
import GCompris 1.0

import "../../core"
import "lang_doidoi.js" as Activity

ActivityBase {
    id: activity

    onStart: focus = true
    onStop: {}

    pageComponent: Rectangle {
        id: background
        anchors.fill: parent
        color: "#16264A"                     // chàm đậm, nền nhận diện của làng
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
            property int soNguoi: 3
            property bool capKho: false      // false = 31 thẻ x 6 hình
            property int hoaTieu: -1         // -1 = không ai làm Hoa tiêu
            property string manHienTai: "vao_ban"
            property var danhMucHinh: []     // đọc từ hinh.json
            property var boCuc: ({})         // đọc từ bo_cuc.json
        }

        // ---------------------------------------------------- màn vào bàn
        Column {
            id: manVaoBan
            visible: items.manHienTai === "vao_ban"
            anchors.centerIn: parent
            width: parent.width * 0.8
            spacing: background.height * 0.035

            GCText {
                anchors.horizontalCenter: parent.horizontalCenter
                fontSize: hugeSize
                font.bold: true
                color: "#FBF8F1"
                text: qsTr("Đối Đôi Làng")
            }

            NutHang {
                nhan: qsTr("Mấy người chơi?")
                lua: ["2", "3", "4", "5", "6"]
                dangChon: items.soNguoi - 2
                onChonMuc: items.soNguoi = muc + 2
            }

            NutHang {
                nhan: qsTr("Bộ bài")
                lua: [qsTr("Dễ · 31 thẻ, 6 hình"), qsTr("Khó · 57 thẻ, 8 hình")]
                dangChon: items.capKho ? 1 : 0
                onChonMuc: items.capKho = (muc === 1)
            }

            NutHang {
                nhan: qsTr("Ai làm Hoa tiêu?")
                // "Không ai" đứng đầu, nên chỉ số muc 0 -> hoaTieu = -1
                lua: {
                    var d = [qsTr("Không ai")]
                    for (var i = 0; i < items.soNguoi; i++)
                        d.push(qsTr("Bạn %1").arg(i + 1))
                    return d
                }
                dangChon: items.hoaTieu + 1
                onChonMuc: items.hoaTieu = muc - 1
            }

            Row {
                anchors.horizontalCenter: parent.horizontalCenter
                spacing: 40
                NutTo {
                    chu: qsTr("Vào bàn")
                    onBam: items.manHienTai = "luat_lang"
                }
                NutTo {
                    chu: qsTr("Học hình một mình")
                    onBam: items.manHienTai = "hoc_hinh"
                }
            }
        }

        Loader {
            anchors.fill: parent
            active: items.manHienTai !== "vao_ban"
            source: items.manHienTai === "luat_lang" ? "LuatLang.qml" : "HocHinh.qml"
            onLoaded: item.items = items
        }

        DialogHelp {
            id: dialogHelp
            onClose: home()
        }

        Bar {
            id: bar
            content: BarEnumContent { value: help | home }
            onHelpClicked: displayDialog(dialogHelp)
            onHomeClicked: {
                if (items.manHienTai === "vao_ban")
                    activity.home()
                else
                    items.manHienTai = "vao_ban"
            }
        }

        Bonus { id: bonus }
    }
}
```

- [ ] **Bước 3: Viết hai thành phần nút dùng lại**

Tạo `NutHang.qml` cùng thư mục — một hàng nút chọn một trong nhiều:

```qml
/* SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
 * SPDX-License-Identifier: GPL-3.0-or-later */
import QtQuick 2.12
import "../../core"

Row {
    id: hang
    property string nhan: ""
    property var lua: []
    property int dangChon: 0
    signal chonMuc(int muc)

    anchors.horizontalCenter: parent.horizontalCenter
    spacing: 14

    GCText {
        anchors.verticalCenter: parent.verticalCenter
        width: hang.parent.width * 0.22
        horizontalAlignment: Text.AlignRight
        fontSize: regularSize
        color: "#FBF8F1"
        text: hang.nhan
    }

    Repeater {
        model: hang.lua
        Rectangle {
            width: Math.max(96, chu.width + 28)
            height: 56
            radius: 8
            color: index === hang.dangChon ? "#E8A317" : "#1E3357"
            border { color: "#FBF8F1"; width: 2 }
            GCText {
                id: chu
                anchors.centerIn: parent
                fontSize: regularSize
                color: index === hang.dangChon ? "#141414" : "#FBF8F1"
                text: modelData
            }
            MouseArea {
                anchors.fill: parent
                onClicked: hang.chonMuc(index)
            }
        }
    }
}
```

Tạo `NutTo.qml` cùng thư mục:

```qml
/* SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
 * SPDX-License-Identifier: GPL-3.0-or-later */
import QtQuick 2.12
import "../../core"

Rectangle {
    id: nut
    property string chu: ""
    signal bam()

    width: Math.max(260, nhan.width + 60)
    height: 78
    radius: 12
    color: "#1F7A52"
    border { color: "#FBF8F1"; width: 3 }

    GCText {
        id: nhan
        anchors.centerIn: parent
        fontSize: mediumSize
        font.bold: true
        color: "#FBF8F1"
        text: nut.chu
    }
    MouseArea {
        anchors.fill: parent
        onClicked: nut.bam()
        onPressed: nut.color = "#12958E"
        onReleased: nut.color = "#1F7A52"
    }
}
```

- [ ] **Bước 4: Viết lang_doidoi.js đọc dữ liệu**

```javascript
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
```

- [ ] **Bước 5: Đóng gói và cài lên NEO One**

```bash
.venv/bin/python tools/dong_goi_mini_app.py /tmp lang_doidoi
scp neo@192.168.1.28:/usr/share/gcompris-qt/rcc/activities.rcc /tmp/
./deploy/gan_mini_app.sh /tmp/activities.rcc lang_maker lang_doidoi
scp /tmp/activities-vi.rcc /tmp/lang_doidoi.rcc neo@192.168.1.28:/tmp/
ssh neo@192.168.1.28 'sudo cp /tmp/lang_doidoi.rcc /usr/share/gcompris-qt/rcc/; \
  sudo cp /tmp/activities-vi.rcc /usr/share/gcompris-qt/rcc/activities.rcc'
```

Chú ý truyền **cả hai** tên `lang_maker lang_doidoi` cho `gan_mini_app.sh`, nếu
không nó chỉ đóng gói app được nêu và `activities_out.txt` mất dòng của app kia.

- [ ] **Bước 6: Chạy trên máy thật và nhìn tận mắt**

```bash
ssh neo@192.168.1.28 "pkill -f '[g]compris-qt'; sleep 2; \
  export DISPLAY=:0 XDG_RUNTIME_DIR=/run/user/1000; \
  setsid nohup /usr/games/gcompris-qt --fullscreen --software-renderer \
    > /tmp/gc.log 2>&1 < /dev/null & sleep 8; \
  grep -iE 'lang_doidoi|error|warning.*qml' /tmp/gc.log | head -20"
```

Vào mục **Làng Maker**, phải thấy hai hoạt động: Làng Maker và Đối Đôi Làng.
Mở Đối Đôi Làng, phải thấy màn vào bàn với ba hàng nút chọn.

Chụp ảnh làm bằng chứng:

```bash
ssh neo@192.168.1.28 "export DISPLAY=:0; gnome-screenshot -f /tmp/vao_ban.png"
scp neo@192.168.1.28:/tmp/vao_ban.png DOCS/anh/neo-one-doidoi-vao-ban.png
```

- [ ] **Bước 7: Commit**

```bash
git add mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/*.qml \
        mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/lang_doidoi.js \
        DOCS/anh/neo-one-doidoi-vao-ban.png
git commit -m "Đối Đôi Làng: khung hoạt động và màn vào bàn, chạy trên NEO One"
```

---

## Nhiệm vụ 6 · The.qml — vẽ một thẻ

**Tệp:**
- Tạo: `mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/The.qml`

**Giao diện:**
- Dùng của nhiệm vụ trước: `items.danhMucHinh`, `items.boCuc`, `Activity.url`.
- Cung cấp cho nhiệm vụ sau: thành phần `The` với thuộc tính `hinh` (mảng chỉ
  số hình 0-based), `boCuc` (một bố cục lấy từ `bo_cuc.json`), `goc` (mảng góc
  xoay tính bằng độ, cùng độ dài với `hinh`), `chonDuoc` (bool). Phát tín hiệu
  `bamHinh(int chiSoHinh)` khi bấm vào một hình — **truyền chỉ số hình trong bộ
  57, không phải vị trí trong thẻ**.

- [ ] **Bước 1: Viết The.qml**

```qml
/* GCompris - Đối Đôi Làng · một thẻ tròn
 *
 * SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
 *   SPDX-License-Identifier: GPL-3.0-or-later
 *
 * Bố cục (x, y, r) tính trong ĐĨA ĐƠN VỊ: tâm thẻ (0,0), mép thẻ bán kính 1.
 * Nhân với bán kính thẻ thật để ra pixel. Xoay từng hình quanh tâm của chính
 * nó nên không đổi đường tròn bao — bất biến "không đè nhau" đã kiểm lúc dựng
 * vẫn còn nguyên.
 */
import QtQuick 2.12
import "lang_doidoi.js" as Activity

Item {
    id: the

    property var items
    property var hinh: []           // chỉ số hình 0-based trong bộ 57
    property var boCuc: []          // [[x, y, r], …] cùng độ dài với hinh
    property var goc: []            // góc xoay từng hình, tính bằng độ
    property bool chonDuoc: true
    property int nhayHinh: -1       // chỉ số hình đang nhấp nháy, -1 là không

    signal bamHinh(int chiSoHinh)

    property real banKinh: Math.min(width, height) / 2

    Rectangle {
        anchors.centerIn: parent
        width: the.banKinh * 2
        height: width
        radius: width / 2
        color: "#FBF8F1"
        border { color: "#141414"; width: 3 }
    }

    Repeater {
        model: the.hinh.length
        delegate: Item {
            // boCuc[index] = [x, y, r] trong đĩa đơn vị
            property real bk: the.boCuc[index][2] * the.banKinh
            x: the.width / 2 + the.boCuc[index][0] * the.banKinh - bk
            y: the.height / 2 + the.boCuc[index][1] * the.banKinh - bk
            width: bk * 2
            height: bk * 2

            Image {
                id: anh
                anchors.fill: parent
                source: Activity.duongDanHinh(the.items, the.hinh[index])
                sourceSize.width: 256
                sourceSize.height: 256
                rotation: the.goc.length > index ? the.goc[index] : 0
                smooth: true
            }

            Rectangle {
                anchors.fill: parent
                radius: width / 2
                color: "transparent"
                border { color: "#E8A317"; width: Math.max(3, parent.bk * 0.12) }
                opacity: the.nhayHinh === the.hinh[index] ? 1 : 0
                SequentialAnimation on scale {
                    running: the.nhayHinh === the.hinh[index]
                    loops: Animation.Infinite
                    NumberAnimation { to: 1.15; duration: 300 }
                    NumberAnimation { to: 1.0; duration: 300 }
                }
                Behavior on opacity { NumberAnimation { duration: 150 } }
            }

            MouseArea {
                anchors.fill: parent
                enabled: the.chonDuoc
                onClicked: the.bamHinh(the.hinh[index])
            }
        }
    }
}
```

- [ ] **Bước 2: Thêm hàm đường dẫn hình vào lang_doidoi.js**

Thêm vào cuối `lang_doidoi.js`:

```javascript
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
```

- [ ] **Bước 3: Xem thử trên máy thật**

Tạm cho `Lang_doidoi.qml` hiện thẳng một thẻ khi bấm "Vào bàn" (sửa `Loader`
thành `The`), đóng gói và cài như bước 5 nhiệm vụ 5, rồi chụp ảnh. Nhìn kiểm
ba việc:

1. Sáu (hoặc tám) hình hiện đủ, không hình nào trắng.
2. Không hai hình nào đè lên nhau.
3. Không hình nào tràn ra ngoài mép thẻ.

Xem xong thì hoàn nguyên `Lang_doidoi.qml` về dùng `Loader`.

- [ ] **Bước 4: Commit**

```bash
git add mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/The.qml \
        mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/lang_doidoi.js
git commit -m "Đối Đôi Làng: thành phần thẻ tròn"
```

---

## Nhiệm vụ 7 · Chế độ Luật làng

**Tệp:**
- Tạo: `mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/LuatLang.qml`
- Sửa: `mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/lang_doidoi.js`

**Giao diện:**
- Dùng của nhiệm vụ trước: `The`, `Activity.tron`, `Activity.bocucNgauNhien`,
  `items.soNguoi`, `items.capKho`, `items.hoaTieu`.
- Cung cấp cho nhiệm vụ sau: không, đây là nhánh cuối.

**Luật phải cưỡng chế bằng cơ chế, không bằng lời nhắc** (spec §7):
- Trong ván **không hiện con số lượt của ai**.
- Người làm Hoa tiêu **không có ô bấm được** — không có đường nào ghi lượt.
- Gợi ý của Hoa tiêu chỉ một lần cho mỗi thẻ lật.
- Bấm sai thì ô người đó khoá đúng 3 giây.

- [ ] **Bước 1: Thêm phần trạng thái ván vào lang_doidoi.js**

Thêm vào cuối tệp:

```javascript
/* ---------------------------------------------------- trạng thái ván Luật làng
 * Chia bài: xáo cả bộ, thẻ đầu làm THẺ CHUNG, phần còn lại úp thành CHỒNG.
 * Gọi đúng: thẻ lật thành thẻ chung mới, rút thẻ kế từ chồng làm thẻ lật.
 */
var van = null

function batDauVan(items) {
    var boBai = docJson(items.capKho ? "bo_bai_57.json" : "bo_bai_31.json")
    var the = tron(boBai.the.slice())
    van = {
        chong: the,
        the_chung: null,
        the_lat: null,
        luot: [],              // số lượt từng người, KHÔNG hiện trong ván
        khoa_den: [],          // mốc thời gian hết khoá của từng người
        nguoi_dang_chon: -1,
        da_goi_y: false,
        bat_dau: Date.now(),
        xong: false
    }
    for (var i = 0; i < items.soNguoi; i++) {
        van.luot.push(0)
        van.khoa_den.push(0)
    }
    van.the_chung = van.chong.shift()
    latTheKe(items)
    return van
}

function latTheKe(items) {
    van.the_lat = van.chong.shift()
    van.da_goi_y = false
    van.nguoi_dang_chon = -1
    capNhat(items)
}

function hinhTrung(a, b) {
    for (var i = 0; i < a.length; i++)
        if (b.indexOf(a[i]) !== -1)
            return a[i]
    return -1
}

function biKhoa(nguoi) {
    return Date.now() < van.khoa_den[nguoi]
}

function chonNguoi(items, nguoi) {
    if (van.xong || nguoi === items.hoaTieu || biKhoa(nguoi))
        return
    van.nguoi_dang_chon = nguoi
    capNhat(items)
}

function chonHinh(items, chiSoHinh) {
    if (van.xong || van.nguoi_dang_chon < 0)
        return
    var dung = hinhTrung(van.the_chung, van.the_lat)
    if (chiSoHinh === dung) {
        van.luot[van.nguoi_dang_chon]++
        items.hinhNhay = dung
        items.audioEffects.play("qrc:/gcompris/src/core/resource/sounds/win.wav")
        if (van.chong.length === 0) {
            van.xong = true
            items.giay = Math.round((Date.now() - van.bat_dau) / 1000)
            if (items.kyLuc < 0 || items.giay < items.kyLuc)
                items.kyLuc = items.giay
            capNhat(items)
            items.bonus.good("flower")
        } else {
            van.the_chung = van.the_lat
            latTheKe(items)
        }
    } else {
        van.khoa_den[van.nguoi_dang_chon] = Date.now() + 3000
        van.nguoi_dang_chon = -1
        items.audioEffects.play("qrc:/gcompris/src/core/resource/sounds/brick.wav")
        capNhat(items)
    }
}

function goiY(items) {
    if (van.xong || items.hoaTieu < 0 || van.da_goi_y)
        return
    van.da_goi_y = true
    var dung = hinhTrung(van.the_chung, van.the_lat)
    // Phần tư của THẺ LẬT có chứa hình trùng
    var vt = van.the_lat.indexOf(dung)
    var b = items.boCucLat[vt]
    items.gocGoiY = Math.atan2(b[1], b[0])
    items.hienGoiY = true
    capNhat(items)
}

function capNhat(items) {
    items.soConLai = van.chong.length
    items.theChung = van.the_chung
    items.theLat = van.the_lat
    items.nguoiDangChon = van.nguoi_dang_chon
    items.vanXong = van.xong
    items.luot = van.luot.slice()
    items.daGoiY = van.da_goi_y
}
```

- [ ] **Bước 2: Viết LuatLang.qml**

```qml
/* GCompris - Đối Đôi Làng · chế độ Luật làng
 *
 * SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
 *   SPDX-License-Identifier: GPL-3.0-or-later
 *
 * Ba luật cưỡng chế bằng cơ chế, không bằng lời nhắc:
 *   1. Trong ván KHÔNG hiện số lượt của ai — chỉ đồng hồ và số thẻ còn lại.
 *   2. Số lượt chỉ lộ ở màn kết ván, và chỉ khi chênh lệch quá một phần ba.
 *   3. Người làm Hoa tiêu không có ô bấm được, nên không đường nào ghi lượt.
 */
import QtQuick 2.12
import GCompris 1.0

import "../../core"
import "lang_doidoi.js" as Activity

Item {
    id: man
    property var items

    property int soConLai: 0
    property var theChung: []
    property var theLat: []
    property int nguoiDangChon: -1
    property bool vanXong: false
    property var luot: []
    property bool daGoiY: false
    property int hinhNhay: -1
    property int giay: 0
    property real gocGoiY: 0
    property bool hienGoiY: false
    property var boCucChung: []
    property var boCucLat: []
    property var gocChung: []
    property var gocLat: []

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

    Component.onCompleted: {
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
        Activity.batDauVan(man)
        moiBoCuc()
    }

    function moiBoCuc() {
        var soHinh = capKho ? 8 : 6
        var a = Activity.bocucNgauNhien(man, soHinh)
        var b = Activity.bocucNgauNhien(man, soHinh)
        boCucChung = a.boCuc; gocChung = a.goc
        boCucLat = b.boCuc;   gocLat = b.goc
    }

    onTheLatChanged: moiBoCuc()

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

    // ------------------------------------------------------- hai thẻ
    Row {
        anchors.centerIn: parent
        spacing: 60
        The {
            id: theChungHien
            items: man
            width: Math.min(man.width * 0.42, man.height * 0.72)
            height: width
            hinh: man.theChung
            boCuc: man.boCucChung
            goc: man.gocChung
            nhayHinh: man.hinhNhay
            chonDuoc: man.nguoiDangChon >= 0 && !man.vanXong
            onBamHinh: Activity.chonHinh(man, chiSoHinh)
        }
        The {
            id: theLatHien
            items: man
            width: theChungHien.width
            height: width
            hinh: man.theLat
            boCuc: man.boCucLat
            goc: man.gocLat
            nhayHinh: man.hinhNhay
            chonDuoc: man.nguoiDangChon >= 0 && !man.vanXong
            onBamHinh: Activity.chonHinh(man, chiSoHinh)

            // vòng gợi ý của Hoa tiêu: một phần tư thẻ chứa hình trùng
            Rectangle {
                visible: man.hienGoiY
                width: parent.width * 0.5
                height: width
                radius: width / 2
                color: "#33E8A317"
                border { color: "#E8A317"; width: 4 }
                x: parent.width / 2 + Math.cos(man.gocGoiY) * parent.width * 0.28 - width / 2
                y: parent.height / 2 + Math.sin(man.gocGoiY) * parent.height * 0.28 - height / 2
                SequentialAnimation on opacity {
                    running: man.hienGoiY
                    loops: 6
                    NumberAnimation { to: 0.2; duration: 320 }
                    NumberAnimation { to: 1.0; duration: 320 }
                    onFinished: man.hienGoiY = false
                }
            }
        }
    }

    // ------------------------------------------------------- dải người chơi
    Row {
        anchors { bottom: parent.bottom; bottomMargin: 24; horizontalCenter: parent.horizontalCenter }
        spacing: 20
        Repeater {
            model: man.soNguoi
            delegate: Rectangle {
                property bool laHoaTieu: index === man.hoaTieu
                // man.nhip đứng đây để QML tính lại khi đồng hồ nhịp chạy —
                // bỏ nó ra là ô khoá không bao giờ tự sáng lại.
                property bool dangKhoa: man.nhip >= 0 && Activity.biKhoa(index)
                width: 260; height: 92; radius: 10
                color: laHoaTieu ? "#2A3A5C"
                     : index === man.nguoiDangChon ? "#E8A317"
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
                        fontSize: mediumSize; font.bold: !parent.parent.laHoaTieu
                        color: parent.parent.laHoaTieu ? "#8A96AC" : "#141414"
                        text: qsTr("Bạn %1").arg(index + 1)
                    }
                    GCText {
                        anchors.horizontalCenter: parent.horizontalCenter
                        visible: parent.parent.laHoaTieu
                        fontSize: smallSize; color: "#8A96AC"
                        text: man.daGoiY ? qsTr("Hoa tiêu · đã gợi ý")
                                         : qsTr("Hoa tiêu · phím cách")
                    }
                }
                MouseArea {
                    anchors.fill: parent
                    // Hoa tiêu KHÔNG có đường nào ghi lượt: chuột không bật ở đây.
                    enabled: !parent.laHoaTieu && !man.vanXong
                    onClicked: Activity.chonNguoi(man, index)
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
                // Luật 2: số lượt chỉ lộ ra ở đây, và chỉ khi lệch quá 1/3.
                visible: {
                    if (man.luot.length === 0) return false
                    var lon = Math.max.apply(null, man.luot)
                    var nho = Math.min.apply(null, man.luot)
                    var tong = man.capKho ? 56 : 30
                    return (lon - nho) > tong / 3
                }
                text: qsTr("Có bạn gọi được nhiều hơn hẳn các bạn khác. Ván sau nhường nhau một chút nhé — cả bàn cùng thắng mới là thắng.")
            }
            NutTo {
                anchors.horizontalCenter: parent.horizontalCenter
                chu: qsTr("Chơi ván nữa")
                onBam: { dongHo.giay = 0; man.hinhNhay = -1; man.batDau() }
            }
        }
    }
}
```

- [ ] **Bước 3: Đóng gói, cài, chạy thử trên NEO One**

Lặp lại bước 5 và 6 của nhiệm vụ 5.

- [ ] **Bước 4: Nghiệm thu từng luật trên máy thật**

Làm đủ sáu phép thử, ghi kết quả:

1. Chọn 6 người, đủ sáu ô tên hiện ra.
2. Chọn Hoa tiêu là Bạn 3 → ô Bạn 3 xám, bấm chuột vào không có phản ứng gì.
   Bấm liên tiếp mười lần cũng không ghi lượt nào.
3. Bấm phím cách → vòng nháy hiện đúng phần tư có hình trùng. Bấm lần hai
   trong cùng thẻ → không có gì xảy ra.
4. Bấm Bạn 1 rồi bấm hình SAI → ô Bạn 1 chuyển màu cánh gián, bấm vào trong
   3 giây không có tác dụng, sau 3 giây bấm lại được.
5. Trong suốt ván, **không có con số nào** dưới ô tên.
6. Chơi hết chồng thẻ → hiện "Cả bàn thắng" và số giây.

- [ ] **Bước 5: Commit**

```bash
git add mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/LuatLang.qml \
        mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/lang_doidoi.js
git commit -m "Đối Đôi Làng: chế độ Luật làng 2-6 người"
```

---

## Nhiệm vụ 8 · Chế độ Học hình

**Tệp:**
- Tạo: `mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/HocHinh.qml`
- Sửa: `lang_doidoi.js` — thêm phần chọn câu hỏi theo mức

**Giao diện:**
- Dùng của nhiệm vụ trước: `items.danhMucHinh`, `Activity.duongDanHinh`,
  `Activity.tron`.
- Cung cấp cho nhiệm vụ sau: không.

Năm mức, mỗi mức 10 câu, hai hình sai lấy **cùng mức** với hình đúng (mức 5
trộn cả bộ nên lấy bất kỳ):

| Mức | Nhóm | Số hình |
|---|---|---|
| 1 | A | 10 |
| 2 | B | 12 |
| 3 | C | 12 |
| 4 | D + E | 23 |
| 5 | tất cả | 57 |

- [ ] **Bước 1: Thêm phần Học hình vào lang_doidoi.js**

```javascript
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
```

- [ ] **Bước 2: Viết HocHinh.qml**

```qml
/* GCompris - Đối Đôi Làng · chế độ Học hình
 *
 * SPDX-FileCopyrightText: 2026 ThingEdu <tuan@rogo.com.vn>
 *   SPDX-License-Identifier: GPL-3.0-or-later
 *
 * Hiện TÊN bằng chữ, con chọn HÌNH đúng trong ba hình. Hoạt động này đòi hỏi
 * đọc được tiếng Việt — ghi rõ ở prerequisite của ActivityInfo.qml. Em chưa
 * đọc được thì anh chị áo xanh đọc hộ.
 */
import QtQuick 2.12
import GCompris 1.0

import "../../core"
import "lang_doidoi.js" as Activity

Item {
    id: man
    property var items

    property int muc: 0
    property int daLam: 0
    property var cauHoi: null
    property int hienNghia: -1

    property var danhMucHinh: []

    Component.onCompleted: {
        danhMucHinh = items.danhMucHinh
        cauMoi()
    }

    function cauMoi() {
        hienNghia = -1
        cauHoi = Activity.sinhCauHoi(man, muc)
    }

    // Chọn sai thì hình phải rung. Delegate không gọi ngược lên được, nên màn
    // phát tín hiệu và delegate nào trùng chỉ số thì tự rung.
    signal rungHinh(int chiSo)

    function chon(chiSo) {
        if (chiSo === cauHoi.dung) {
            hienNghia = chiSo
            items.audioEffects.play("qrc:/gcompris/src/core/resource/sounds/win.wav")
            daLam++
            if (daLam >= 10) {
                daLam = 0
                muc = (muc + 1) % 5
                items.bonus.good("flower")
            }
            hetGio.restart()
        } else {
            items.audioEffects.play("qrc:/gcompris/src/core/resource/sounds/brick.wav")
            man.rungHinh(chiSo)
        }
    }

    Timer { id: hetGio; interval: 1400; onTriggered: man.cauMoi() }

    Rectangle { anchors.fill: parent; color: "#16264A" }

    Column {
        anchors.centerIn: parent
        spacing: man.height * 0.05
        width: man.width * 0.9

        GCText {
            anchors.horizontalCenter: parent.horizontalCenter
            fontSize: regularSize; color: "#8A96AC"
            text: qsTr("Mức %1 · câu %2 trên 10").arg(man.muc + 1).arg(man.daLam + 1)
        }

        GCText {
            anchors.horizontalCenter: parent.horizontalCenter
            fontSize: hugeSize; font.bold: true; color: "#E8A317"
            text: man.cauHoi ? man.danhMucHinh[man.cauHoi.dung].ten : ""
        }

        Row {
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: 50
            Repeater {
                model: man.cauHoi ? man.cauHoi.lua : []
                delegate: Rectangle {
                    width: man.height * 0.30; height: width
                    radius: width / 2
                    color: "#FBF8F1"
                    border { color: "#141414"; width: 3 }
                    scale: man.hienNghia === modelData ? 1.12 : 1.0
                    Behavior on scale { NumberAnimation { duration: 180 } }

                    Image {
                        anchors.centerIn: parent
                        width: parent.width * 0.74; height: width
                        source: Activity.duongDanHinh(man, modelData)
                        sourceSize.width: 256; sourceSize.height: 256
                        smooth: true
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: man.chon(modelData)
                    }
                    // Rung bằng Translate, KHÔNG bằng x: hình nằm trong Row nên
                    // Row tự đặt x, animation trên x sẽ đánh nhau với bố cục.
                    transform: Translate { id: dich }
                    SequentialAnimation {
                        id: rung
                        NumberAnimation { target: dich; property: "x"; to: 12; duration: 60 }
                        NumberAnimation { target: dich; property: "x"; to: -12; duration: 60 }
                        NumberAnimation { target: dich; property: "x"; to: 0; duration: 60 }
                    }
                    Connections {
                        target: man
                        onRungHinh: if (chiSo === modelData) rung.restart()
                    }
                }
            }
        }

        GCText {
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width * 0.7
            horizontalAlignment: Text.AlignHCenter
            wrapMode: Text.WordWrap
            fontSize: mediumSize; color: "#FBF8F1"
            opacity: man.hienNghia >= 0 ? 1 : 0
            Behavior on opacity { NumberAnimation { duration: 200 } }
            text: man.hienNghia >= 0 ? man.danhMucHinh[man.hienNghia].nghia : ""
        }
    }
}
```

- [ ] **Bước 3: Đóng gói, cài, thử trên máy thật**

Lặp lại bước 5 và 6 của nhiệm vụ 5. Kiểm bốn việc:

1. Tên hình hiện bằng chữ tiếng Việt có dấu đầy đủ, không ô vuông.
2. Ba hình hiện đủ, không hình nào trắng.
3. Chọn đúng → hình phóng to, hiện dòng nghĩa, sau 1,4 giây sang câu mới.
4. Đủ 10 câu → sang mức kế; ở mức 4 kiểm có hình của cả nhóm D lẫn E.

- [ ] **Bước 4: Commit**

```bash
git add mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/HocHinh.qml \
        mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/lang_doidoi.js
git commit -m "Đối Đôi Làng: chế độ Học hình năm mức"
```

---

## Nhiệm vụ 9 · Nghiệm thu trọn vẹn và tài liệu

**Tệp:**
- Sửa: `DOCS/MINI_APP_DOI_DOI_LANG.md` — ghi kết quả nghiệm thu
- Sửa: `README.md` — thêm dòng cho mini app thứ hai
- Tạo: `DOCS/anh/neo-one-doidoi-*.png`

- [ ] **Bước 1: Chạy toàn bộ test**

```bash
.venv/bin/pytest -q
```

Chờ đợi: tất cả xanh — 93 test cũ cộng thêm test của ba nhiệm vụ đầu.

- [ ] **Bước 2: Đóng gói sạch từ đầu và cài lên NEO One**

```bash
.venv/bin/python tools/sinh_bo_bai.py mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/resource
.venv/bin/python tools/tach_57_hinh.py mini-app/nguon/bo-57-hinh-lang-maker.html \
  mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/resource
.venv/bin/python tools/sinh_bo_cuc.py mini-app/lang_doidoi/gcompris/src/activities/lang_doidoi/resource
git diff --stat        # phải KHÔNG có thay đổi: ba bộ sinh đều tất định
.venv/bin/python tools/dong_goi_mini_app.py /tmp
```

Nếu `git diff --stat` có thay đổi thì một trong ba bộ sinh không tất định —
tìm chỗ dùng `random` không gieo cố định và sửa, vì bộ bài đổi giữa hai lần
dựng là chuyện không chấp nhận được.

- [ ] **Bước 3: Chạy đủ tám tiêu chí nghiệm thu của spec §11**

Chạy từng cái trên NEO One thật, ghi ĐẠT/HỎNG kèm bằng chứng vào
`DOCS/MINI_APP_DOI_DOI_LANG.md`. Tiêu chí 7 (cả 57 hình dựng đúng) kiểm bằng
cách chơi cấp Khó vài ván và nhìn, hoặc viết màn thử hiện cả 57 hình một lượt.

- [ ] **Bước 4: Chụp ảnh làm bằng chứng**

```bash
for m in vao-ban luat-lang hoc-hinh ket-van; do
  echo "Chuyển màn hình sang $m rồi Enter"; read
  ssh neo@192.168.1.28 "export DISPLAY=:0; gnome-screenshot -f /tmp/$m.png"
  scp neo@192.168.1.28:/tmp/$m.png DOCS/anh/neo-one-doidoi-$m.png
done
```

- [ ] **Bước 5: Cập nhật tài liệu**

Trong `DOCS/MINI_APP_DOI_DOI_LANG.md`: thêm mục "Nghiệm thu" với kết quả tám
tiêu chí, đóng rủi ro SVG ở §12, chèn ảnh chụp.

Trong `README.md`: bảng trạng thái thêm dòng cho `lang_doidoi`, và mục cấu trúc
thư mục ghi thêm `mini-app/nguon/`.

- [ ] **Bước 6: Commit cuối**

```bash
git add DOCS README.md
git commit -m "Đối Đôi Làng: nghiệm thu trên NEO One thật, kèm ảnh chụp"
```

---

## Việc còn lại sau kế hoạch này

- Thu tiếng trống thật (ba kiểu: mở buổi, gọi đúng, phá kỷ lục) thay cho âm mừng
  mượn của GCompris.
- Ảnh nền và hình có độ phân giải cao hơn nếu chuyển sang màn lớn.
- Rà pháp lý: bộ hình CC BY-SA trộn với mã GPLv3 (spec §13).
- Đóng góp ngược hoạt động này cho GCompris upstream — một hoạt động mang bản
  sắc Việt trong bộ giáo dục mở toàn cầu.
