# Mini app · ĐỐI ĐÔI LÀNG (`lang_doidoi`)

**Bản thiết kế · 2026-09-02 · đầu vào cho bước lập kế hoạch code**

Bản số hoá bộ bài 57 hình Làng Maker Việt, dựng thành hoạt động GCompris chạy
trên NEO One. Mini app thứ hai của làng, sau `lang_maker`.

Tài liệu gốc của chủ dự án: `spec-app-doi-doi-lang-neo-one.md` và bộ hình
`bo-57-hinh-lang-maker.html`. Tài liệu này **thay thế** tài liệu gốc ở những chỗ
ghi rõ "khác tài liệu gốc" — lý do luôn là phần cứng thật hoặc quyết định của
chủ dự án ngày 2026-09-02.


## 1 · Máy chạy thật — đo được, không phải điền phỏng đoán

Tài liệu gốc để trống bảng phần cứng và bắt "điền trước khi code". Đã đo trên
NEO One `192.168.1.28` ngày 2026-09-02:

| Thông số | Giá trị thật |
|---|---|
| Hệ điều hành | Debian (bookworm), ARM64 |
| Màn hình | HDMI 1920×1080, 344×194 mm (~15,6"), 60 Hz |
| **Cảm ứng** | **KHÔNG CÓ.** Thiết bị nhập duy nhất: 1 chuột không dây + 1 bàn phím USB |
| CPU / RAM | 4 nhân / 1,9 GB |
| GCompris | 3.1 (Qt5, Debian bookworm) |
| Mạng | Không cần — app chạy trọn vẹn offline |
| Âm thanh | Loa ngoài |

Đây là phát hiện làm đổi thiết kế nhiều nhất. Tài liệu gốc đặt cả ba luật chơi
lên nền cảm ứng đa điểm ("vùng người chơi ở 2–4 cạnh màn", "bốn em chạm đồng
thời", "nút chạm tối thiểu 14 mm"). Không có cảm ứng thì không luật nào trong
số đó chạy được như viết.


## 2 · Quyết định đã chốt

Chủ dự án chốt ngày 2026-09-02. Những điều dưới đây **không đem ra bàn lại**.

| # | Quyết định | Khác tài liệu gốc? |
|---|---|---|
| Q1 | Số người chơi: **2–6** | Có — gốc ghi 2–4 |
| Q2 | **Máy là người chia bài, trọng tài và đồng hồ.** Trẻ vẫn reo lên bằng miệng như chơi bài giấy; ai gọi được cặp hình thì dùng chuột chọn để máy xác nhận | Có — gốc dựa trên chạm đồng thời |
| Q3 | Bỏ chế độ **Luật ăn thua** | Có — một con chuột thì không có gì để giành |
| Q4 | Làm hai chế độ: **Học hình** (1 người) và **Luật làng** (2–6 người) | Cắt bớt |
| Q5 | Hai cấp bộ bài, chọn ngay ở màn vào bàn: **Dễ = 31 thẻ × 6 hình**, **Khó = 57 thẻ × 8 hình** | Có — gốc giấu bộ 57 trong cài đặt facilitator |
| Q6 | Vai **Hoa tiêu** giữ lại: bị bỏ khỏi danh sách ghi lượt, gợi ý bằng phím `Space` | Đổi cách thao tác |
| Q7 | **Không có giọng đọc. Học trò cần đọc được tiếng Việt** — đây là điều kiện tiên quyết của hoạt động | Có — bỏ tiêu chí "trẻ 6 tuổi không cần biết chữ" |
| Q8 | v1 **không** có: log, CSV, PIN facilitator, attract mode, bảng xếp hạng | Cắt bớt |

Riêng Q8 kế thừa một ràng buộc **cửa một chiều** của tài liệu gốc (Điều 6 Giao
ước làng): app không thu, không hỏi, không lưu tên, tuổi, ảnh, giọng nói của
trẻ; không tài khoản; không gửi dữ liệu đi đâu. Các bản sau chỉ được siết thêm,
không được nới. v1 tuân điều này một cách dễ nhất có thể: **không ghi tệp gì
cả**.


## 3 · Phạm vi phiên bản 1

**Có:** hai chế độ Học hình và Luật làng · hai cấp bộ bài 31/57 · 2–6 người ·
vai Hoa tiêu · đồng hồ chung · kỷ lục của bàn trong phiên chạy · tiếng Việt ·
offline hoàn toàn.

**Không có (ghi rõ để không ai tiện tay làm):** giọng đọc · log và xuất CSV ·
khu facilitator có PIN · attract mode · bảng xếp hạng giữa các bàn hoặc các
buổi · hồ sơ người chơi · huy hiệu số · tiếng Anh · nhiều máy nối nhau.

Bảng xếp hạng cá nhân đi ngược luật làng nên nhiều khả năng **không bao giờ**
có, không chỉ riêng v1.


## 4 · Toán bộ bài

Bộ bài Dobble là một **mặt phẳng xạ ảnh hữu hạn** bậc `q`. Với `q` là luỹ thừa
của số nguyên tố:

- số thẻ = số hình = `q² + q + 1`
- mỗi thẻ có `q + 1` hình, mỗi hình xuất hiện trên `q + 1` thẻ
- **hai thẻ bất kỳ trùng đúng một hình** — đây là bất biến của cả trò chơi

| Cấp | `q` | Thẻ | Hình/thẻ | Dùng hình số |
|---|---|---|---|---|
| Dễ | 5 | 31 | 6 | 01–31 |
| Khó | 7 | 57 | 8 | 01–57 |

Bộ 57 hình của làng khớp chính xác bậc 7 — không thừa không thiếu một hình nào.

Bộ 31 hình cấp Dễ lấy **31 hình đầu theo số in trên bộ gốc**: trọn nhóm A Nhân
vật (01–10) + trọn nhóm B Công cụ tay (11–22) + chín hình đầu nhóm C Điện tử
(23–31). Đây là những hình dễ gọi tên nhất. Hệ quả phải biết: 26 hình của nhóm
D Vật liệu và E Làng & nghi lễ **không xuất hiện ở cấp Dễ**.

### Cách sinh (q nguyên tố, đúng cho cả 5 và 7)

Đánh số hình từ `0` đến `q² + q`:

```
Thẻ đầu:        { 0, 1, 2, …, q }
q thẻ tiếp:     với i = 0…q-1:
                { 0 } ∪ { q+1 + q·i + j  |  j = 0…q-1 }
q² thẻ cuối:    với i = 0…q-1, j = 0…q-1:
                { i+1 } ∪ { q+1 + q·k + ((i·k + j) mod q)  |  k = 0…q-1 }
```

### Tính sẵn, không tính lúc chạy

Bộ sinh viết bằng **Python trong `tools/`**, xuất ra `bo_bai_31.json` và
`bo_bai_57.json` nhúng vào rcc. QML chỉ đọc JSON, không tính toán gì.

Hai lý do. Một, máy 1,9 GB không nên tính bộ bài lúc khởi động. Hai, quan trọng
hơn: bất biến "mọi cặp thẻ trùng đúng một hình" được kiểm bằng `pytest` như cả
repo đang làm — hỏng thì test đỏ ngay trên máy phát triển, thay vì kiểm lúc
chạy rồi mới biết hỏng trên máy thật giữa buổi sinh hoạt.


## 5 · Tài sản 57 hình

Nguồn gốc là tệp HTML một trang, mỗi hình nằm trong một `div.card`:

```html
<div class="card c-luc"><span class="num">01</span>
  <svg viewBox="0 0 64 64" fill="none" stroke="#141414" stroke-width="2.6" …>
    <path d="…" fill="currentColor"/>
    <path d="…" stroke="var(--vang)" stroke-width="4"/>
  </svg>
  <div class="nm">Neo Tre</div><div class="vi">Măng tre — linh vật làng</div>
</div>
```

Chép tệp nguồn vào repo tại `mini-app/lang_doidoi/nguon/bo-57-hinh-lang-maker.html`
để về sau dựng lại được, rồi `tools/tach_57_hinh.py` bung ra:

- `…/resource/hinh/NN-<ma>.svg` — 57 tệp SVG rời
- `…/resource/hinh.json` — `[{so, ma, ten, nhom, mau}, …]`

### Bẫy phải xử lý: Qt5 không hiểu CSS của trình duyệt

Qt5 dựng SVG theo chuẩn **SVG Tiny 1.2**. Bộ hình dùng hai thứ Qt5 không hiểu:

- `fill="currentColor"` — màu thân hình, thừa hưởng từ class `c-luc`, `c-son`… của thẻ
- `stroke="var(--vang)"` — biến CSS

Script phải thay **hết** thành mã hex thật. Bảng tra tám màu sơn mài:

| Class | Tên | Hex |
|---|---|---|
| `c-son` | Son | `#C4231F` |
| `c-vang` | Vàng | `#E8A317` |
| `c-luc` | Lục | `#1F7A52` |
| `c-lam` | Chàm | `#2B57A6` |
| `c-tim` | Tím | `#6B3FA0` |
| `c-gian` | Cánh gián | `#8A4B24` |
| `c-ngoc` | Lam ngọc | `#12958E` |
| `c-then` | Đen then | `#3A3A3A` |

Ngoài ra `#FBF8F1` (nền kem) và `#141414` (mực) đã là hex sẵn, giữ nguyên.

### Đường lui nếu Qt5 vẫn không dựng nổi

Việc đầu tiên khi bắt tay code là **thử dựng một hình trên NEO One thật**. Nếu
Qt5 vẫn ra hình trắng hoặc méo, chuyển sang dựng sẵn PNG 256×256 lúc đóng gói
(`cairosvg` trên máy phát triển, không phải trên NEO One). Quyết định này chốt
sau phép thử, không đoán trước.

### Danh sách 57 hình

| # | Tên | Nhóm |
|---|---|---|
| 01–10 | Neo Tre · Tux · Trâu Mở · Rùa Logo · Con Bọ · Ong Thợ · Kiến Tha Mồi · Cụ Đồ Bình Dân · Anh Chị Áo Xanh · Bé Chế | A · Nhân vật & linh vật |
| 11–22 | Mỏ hàn · Kìm cắt · Tua vít · Kéo · Súng bắn keo · Thước cuộn · Dao rọc giấy · Bút chì gạch dấu · Băng dính điện · Kính bảo hộ · Khoan mini · Kẹp/ê tô | B · Công cụ tay |
| 23–34 | Bo mạch điều khiển · Đèn LED · Điện trở · Dây jumper · Cục pin · Động cơ servo · Nút nhấn · Còi buzzer · Cảm biến siêu âm · Breadboard · Công tắc gạt · Bánh răng | C · Điện tử & linh kiện |
| 35–45 | Ống tre · Bìa carton · Chai nhựa · Nắp chai · Que kem gỗ · Dây thun · Lon nước ngọt · Giấy gấp · Vải vụn · Đất nặn · Ống hút giấy | D · Vật liệu |
| 46–57 | Cổng làng · Cây đa · Trống làng · Giao ước · Thing Notebook · Huy hiệu rank · Hai bàn tay · Ngọn đèn · Bảng đen & phấn · Sân khấu Showcase · Cờ guild · Hòm dụng cụ chung | E · Làng & nghi lễ |


## 6 · Chế độ HỌC HÌNH (1 người)

Để em mới thuộc mặt hình trước khi vào bàn.

Mỗi lượt: hiện **một tên bằng chữ** giữa màn, dưới là **ba hình** để chọn. Chọn
đúng thì hình phóng to kèm dòng nghĩa (cột `vi` trong bộ gốc, ví dụ "Măng tre —
linh vật làng"); chọn sai thì hình rung và vẫn ở đó để chọn lại.

Hai hình sai lấy **cùng mức** với hình đúng — cùng nhóm thì trông giống nhau
hơn, đố mới có nghĩa. Riêng mức 5 trộn cả bộ nên lấy bất kỳ.

Năm mức theo đúng lệ GCompris:

| Mức | Rút hình từ |
|---|---|
| 1 | Nhóm A · Nhân vật (10 hình) |
| 2 | Nhóm B · Công cụ tay (12 hình) |
| 3 | Nhóm C · Điện tử (12 hình) |
| 4 | Nhóm D + E · Vật liệu, Làng & nghi lễ (23 hình) |
| 5 | Trộn cả 57 hình |

Mỗi mức 10 câu, hết là qua mức. **Học trò cần đọc được tiếng Việt** — ghi vào ô
`prerequisite` của `ActivityInfo.qml`, không giấu. Em chưa đọc được thì anh chị
áo xanh đọc hộ; đó là việc của người lớn trong buổi, không phải việc của máy.


## 7 · Chế độ LUẬT LÀNG (2–6 người)

Chế độ chính, lý do app tồn tại. Máy chia bài, lật thẻ, chạy giờ; trẻ chơi bằng
miệng như bài giấy.

### Vào bàn

Chọn **số người 2–6** · chọn **cấp Dễ/Khó** · chọn **Hoa tiêu** (một người, hoặc
không ai). Ba lựa chọn trên một màn, không có màn con.

### Chia bài

Cả bộ (31 hoặc 57 thẻ) xáo ngẫu nhiên. Thẻ đầu tiên đặt làm **thẻ chung**; phần
còn lại úp thành **chồng**. Máy lật thẻ trên cùng của chồng làm **thẻ lật**.

Không chia thẻ riêng cho từng người — cả bàn nhìn chung hai thẻ, ai gọi được thì
gọi. Đây là chỗ khác bài giấy, và là chỗ máy làm được việc mà bài giấy không
làm được: mọi người thấy đúng cùng một thứ, không ai bị che tay.

### Một lượt

1. Máy lật thẻ trên cùng của chồng lên vị trí *thẻ lật*. Đồng hồ chung chạy.
2. Có em reo lên tên hình trùng giữa hai thẻ.
3. Người cầm chuột **click ô tên em đó** — ô sáng lên — rồi **click hình** trên
   một trong hai thẻ.
4. **Đúng:** hình nhấp nháy trên cả hai thẻ; **thẻ lật trở thành thẻ chung mới**,
   máy rút thẻ kế từ chồng làm thẻ lật; ghi một lượt cho em.
   **Sai:** viền đỏ, ô của em đó khoá 3 giây, hai thẻ giữ nguyên.
5. Hết chồng thẻ → cả bàn thắng.

Một ván cấp Dễ đi hết 30 thẻ, cấp Khó 56 thẻ. Với nhịp khoảng 5 giây một thẻ thì
ván Dễ khoảng 2 phút rưỡi, ván Khó khoảng 5 phút — vừa khung phiên chơi 3–10
phút của buổi sinh hoạt.

Click người trước rồi mới click hình: lúc reo lên thì biết ngay ai, và như thế
không ai nhận vơ được lượt của bạn. Đây cũng là chỗ duy nhất máy biết ai làm
gì — không có nó thì không ghi được lượt nào.

### Ba luật của làng, máy cưỡng chế bằng cơ chế

1. **Đồng hồ chung.** Cả bàn phá hết chồng thẻ → cả bàn thắng. **Trong ván tuyệt
   đối không hiện số lượt của ai** — màn hình chỉ có đồng hồ và số thẻ còn lại.
   Máy vẫn đếm ngầm, nhưng chỉ để dùng ở luật 2.
2. **Không ai bị bỏ lại.** Số lượt chỉ lộ ra ở **màn kết ván**, và chỉ khi chênh
   lệch giữa người nhiều nhất và ít nhất vượt quá một phần ba tổng số thẻ. Lúc
   đó máy hiện dòng mời bàn chơi lại và nhường nhau. Máy nhắc, không phạt, không
   xếp hạng.
3. **Hoa tiêu im lặng.** Em nhận vai Hoa tiêu hiện trong dải người chơi như một
   **thẻ ghi chú không bấm được** (khác hẳn ô tên: xám, không viền, không nhận
   click), nên không có đường nào ghi lượt. Bù lại em bấm `Space` để bật một vòng
   nhấp nháy quanh **một phần tư của thẻ lật** — phần tư có chứa hình trùng. Mỗi
   thẻ lật chỉ gợi ý được một lần. Gợi ý mà không nói, đúng nghĩa đen.

### Kết ván

Hiện thời gian của ván và **kỷ lục của chính bàn này trong phiên chạy** — không
so với bàn khác, không so với buổi khác, không ghi ra tệp. Tắt app là mất; đó là
chủ ý, không phải thiếu sót.

Phá kỷ lục thì đánh **ba tiếng trống**. v1 chưa có tiếng trống thu riêng nên
dùng âm mừng sẵn có của GCompris (`core/resource/sounds/`); thu trống thật là
việc của bản sau.


## 8 · Màn hình

Màn 1920×1080 nằm ngang, mọi người ngồi cùng phía (không phải giao diện mặt bàn
— không có cảm ứng thì không ai với tới màn hình cả).

```
┌────────────────────────────────────────────────────────────┐
│  ⏱ 01:24          Chồng còn 18 thẻ          Kỷ lục 02:07   │
│                                                            │
│        ╭─────────────╮        ╭─────────────╮              │
│        │  THẺ CHUNG  │        │   THẺ LẬT   │              │
│        │   ◕ ✿ ⚙ ▲   │        │   ⚙ ☂ ✚ ◆   │              │
│        │   ✎ ⌾ ◈ ✦   │        │   ✺ ◑ ✧ ✜   │              │
│        ╰─────────────╯        ╰─────────────╯              │
│                                                            │
│   [ P1 ]  [ P2 ]  [ P3 ]  [ P4 ]  [ P5 ]      ⚑ P6         │
│                                              Hoa tiêu      │
└────────────────────────────────────────────────────────────┘
```

Năm ô tên bấm được (viền, nền kem); ô Hoa tiêu xám và không nhận click. **Dưới
ô tên không có con số nào** — luật 1 cấm hiện điểm cá nhân trong ván.

Kích thước tính từ 1080 px chiều cao: thanh trên 120 · vùng thẻ 800 · dải người
chơi 160. Thẻ hình tròn đường kính **700 px**, hai thẻ cạnh nhau vừa trong 1920.
Ở cấp Khó, tám hình trên một thẻ 700 px → mỗi hình khoảng **180 px**, đủ to trên
màn 15,6".

Hình trên thẻ **xoay ngẫu nhiên**, cỡ lệch nhau ±15%, xếp không đè nhau — giống
thẻ giấy. Vị trí sinh bằng vòng tròn đồng tâm rồi nhiễu nhẹ, kiểm không chồng
lấn trước khi vẽ.

**Không có chữ trên thẻ chơi** — quy tắc không đổi từ bản giấy. Chữ chỉ xuất
hiện ở chế độ Học hình và các nhãn giao diện.


## 9 · Cấu trúc tệp

```
mini-app/lang_doidoi/
  nguon/bo-57-hinh-lang-maker.html            nguồn gốc, giữ để dựng lại
  gcompris/src/activities/lang_doidoi/
    ActivityInfo.qml                          tên, mô tả, mục, icon Neo Tre
    Lang_doidoi.qml                           khung màn, điều phối hai chế độ
    HocHinh.qml                               chế độ 1 người
    LuatLang.qml                              chế độ 2–6 người
    The.qml                                   một thẻ tròn, xếp hình không đè
    lang_doidoi.js                            trạng thái ván, chấm đúng sai
    resource/hinh/NN-<ma>.svg                 57 hình
    resource/hinh.json                        tên, nhóm, màu
    resource/bo_bai_31.json                   bộ bài cấp Dễ
    resource/bo_bai_57.json                   bộ bài cấp Khó

tools/tach_57_hinh.py                         bung SVG + sinh hinh.json
tools/sinh_bo_bai.py                          sinh mặt phẳng xạ ảnh
tests/test_bo_bai.py
tests/test_tach_57_hinh.py
```

Đóng gói và gắn dùng lại đồ có sẵn, không viết mới:
`tools/dong_goi_mini_app.py` → `lang_doidoi.rcc`, rồi `deploy/gan_mini_app.sh`
thêm tên vào `activities_out.txt`. Mục **Làng Maker** đã dựng sẵn bằng
`tools/va_muc_lang.py`, chỉ cần đặt `section: "langmaker discovery"`.

Icon hoạt động: **hình 01 Neo Tre** trong bộ 57, không dùng lại
`mini-app/chung/neo_tre.svg` của `lang_maker` — để hai app dùng chung một nét vẽ
với bộ bài.


## 10 · Kiểm thử

Theo lệ repo: test bằng `pytest`, và **mỗi quy tắc phải chứng minh biết fail
bằng cách phá hỏng có chủ đích** trước khi tính là xong.

`tests/test_bo_bai.py`
- đúng 31 thẻ × 6 hình và 57 thẻ × 8 hình
- **mọi cặp thẻ trùng đúng một hình** — bất biến chính
- mỗi hình xuất hiện đúng `q+1` lần
- không thẻ nào có hình lặp
- bộ 31 chỉ dùng hình số 01–31
- phá thử: đổi một hình trên một thẻ · xoá một thẻ · nhân đôi một hình trong thẻ

`tests/test_tach_57_hinh.py`
- đúng 57 tệp SVG, mỗi tệp parse được bằng bộ đọc XML
- **không tệp nào còn `var(--` hay `currentColor`**
- mọi mã màu trong tệp nằm trong bảng mười màu đã biết
- `hinh.json` đủ 57 mục, không trùng mã, không trùng tên, nhóm thuộc A–E
- phá thử: bỏ bước thay `currentColor` · sửa một mã màu thành mã lạ · làm trùng
  tên hai hình · xoá một thẻ khỏi tệp HTML nguồn


## 11 · Tiêu chí nghiệm thu

Chạy trên NEO One thật, không phải trên Mac.

1. Khởi động nguội → vào được ván đầu **dưới 60 giây**, không cần người hướng dẫn.
2. Kiểm toán bộ bài chạy trong `pytest`, hỏng thì test đỏ — không đợi tới lúc chạy.
3. Sáu người chơi, ô tên hiện đủ sáu, click ghi đúng lượt cho đúng người.
4. **Hoa tiêu không thể ghi lượt trong mọi trường hợp** — thẻ Hoa tiêu không
   nhận click, kể cả bấm nhanh liên tiếp hay bấm đúng lúc đang chấm thẻ.
   Trong ván không có con số nào dưới ô tên người chơi.
5. Gợi ý của Hoa tiêu chỉ dùng được một lần cho mỗi thẻ, bấm `Space` lần hai
   không có tác dụng.
6. Chọn sai thì ô người đó khoá đủ 3 giây, click trong lúc khoá không ghi gì.
7. Cả 57 hình dựng ra hình đúng trên NEO One, không hình nào trắng hoặc méo.
8. Toàn bộ app **không có ô nhập tên hay thông tin cá nhân nào**, và không ghi
   ra tệp nào ngoài thư mục cấu hình sẵn có của GCompris.

Tiêu chí "trẻ 6 tuổi chơi được mà không cần biết chữ" của tài liệu gốc **bị bỏ**
theo quyết định Q7 — học trò cần đọc được tiếng Việt.


## 12 · Rủi ro

| Rủi ro | Mức | Đường lui |
|---|---|---|
| Qt5 SVG Tiny không dựng nổi bộ hình | Cao | Dựng sẵn PNG 256 px lúc đóng gói. **Thử ngay việc đầu tiên**, trước khi viết QML |
| 57 SVG nạp cùng lúc làm chậm máy 1,9 GB | Vừa | Chỉ nạp hình của hai thẻ đang hiện, không nạp cả bộ |
| Xếp 8 hình không đè nhau trên thẻ tròn có thể lặp vô hạn | Vừa | Giới hạn số lần thử, quá thì lùi về bố cục cố định theo vòng tròn |
| Sáu ô tên trên màn 1920 bị hẹp | Thấp | Ô rộng 280 px, sáu ô + khoảng cách vừa trong 1920 |

## 13 · Giấy phép

Bộ 57 hình phát hành **CC BY-SA**, làng giữ quyền. Mã hoạt động theo
**GPL-3.0-or-later** như `lang_maker` và như GCompris. CC BY-SA 4.0 có điều
khoản tương thích một chiều sang GPLv3 nên trộn được, miễn tác phẩm hợp thành
phát hành theo GPLv3 — **cần bước rà pháp lý xác nhận trước khi phát hành công
khai**, đánh dấu chờ, không chặn việc code.

Hình **Tux** trong bộ là bản vẽ lại; ghi công linh vật Linux của Larry Ewing ở
`ActivityInfo.qml`.

Kho `gcompris-vi` là kho công khai AGPL nên mọi hình đưa vào phải sạch thương
hiệu bên thứ ba — bài học từ `lang_maker` (xem `MINI_APP_LANG_MAKER.md`, mục
Bản quyền ảnh nền). Bộ 57 hình là nét vẽ riêng của làng nên không vướng.
