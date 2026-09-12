# Lưu ý về bản đồ và chủ quyền Việt Nam

**Ngày rà soát:** 02/09/2026 · **Người rà:** kiểm tra trực tiếp mã nguồn GCompris 26.1
và chạy thật trên NEO One (gcompris-qt 3.1-2).

> **KẾT LUẬN NGẮN: bản đồ gốc của GCompris thiếu quần đảo Hoàng Sa và Trường Sa.
> ĐÃ VẼ LẠI VÀ SỬA XONG cho bản đồ Đông Nam Á — xem phần "Đã sửa" ở cuối.**

## Hai hoạt động có bản đồ

| Hoạt động | Tên tiếng Việt | Nội dung |
|---|---|---|
| `geography` | Tìm quốc gia trên bản đồ | 14 cấp: châu lục, rồi từng vùng của thế giới. Cấp 12 là Đông Nam Á, có mảnh Việt Nam. |
| `geo-country` | Tìm vùng trên bản đồ | 18 bộ bản đồ hành chính: Ý, Ấn Độ, Trung Quốc, Úc, Mỹ, Pháp, Đức… **Không có Việt Nam.** |

## Bốn phát hiện

### 1. Bản đồ Việt Nam thiếu Hoàng Sa và Trường Sa — VẤN ĐỀ NẶNG NHẤT

Tệp `src/activities/geography/resource/asiasoutheast/vietnam.svgz` chỉ vẽ phần đất liền
cùng vài đảo ven bờ (Phú Quốc, Côn Đảo). **Không có quần đảo Hoàng Sa, không có quần đảo
Trường Sa.**

![Bản đồ Việt Nam trong GCompris](anh/ban-do-viet-nam-trong-gcompris.png)

### 2. Biển Đông trên bản đồ nền hoàn toàn trống

Nền `asiasoutheast/southeast_asia.svgz` không vẽ bất kỳ đảo nào của hai quần đảo — không
gán cho ai cả, mà là **không tồn tại trên bản đồ**.

![Biển Đông trong GCompris](anh/bien-dong-trong-gcompris.png)

![Bản đồ Đông Nam Á chạy trên NEO One](anh/ban-do-dong-nam-a-neo-one.png)

### 3. Điểm tích cực: KHÔNG có đường lưỡi bò

Bản đồ Trung Quốc (`asiaeast/china.svgz`) chỉ có phần đất liền và đảo Hải Nam. **Không có
đường chín đoạn, không lấn xuống Biển Đông, không gộp Hoàng Sa hay Trường Sa.** Đây là
điều đáng ghi nhận — nhiều phần mềm nước ngoài mắc lỗi này.

![Bản đồ Trung Quốc trong GCompris](anh/ban-do-trung-quoc-trong-gcompris.png)

### 4. Đài Loan được liệt kê ngang hàng quốc gia

Cấp 13 "Đông Á" xếp Đài Loan thành một mảnh riêng, ngang với Trung Quốc, Nhật Bản, Hàn
Quốc, Triều Tiên, Mông Cổ. Việt Nam theo chính sách Một Trung Quốc và sách giáo khoa
Việt Nam không liệt Đài Loan là quốc gia. Nhà trường cần cân nhắc.

## Căn cứ pháp lý

**Nghị định 18/2020/NĐ-CP** ngày 11/02/2020 về xử phạt vi phạm hành chính trong lĩnh vực
đo đạc và bản đồ, hiệu lực từ 01/4/2020. Theo **Điều 11 khoản 2**, hành vi lưu hành sản
phẩm đo đạc và bản đồ, xuất bản phẩm bản đồ liên quan đến chủ quyền lãnh thổ quốc gia mà
không thể hiện hoặc thể hiện không đúng chủ quyền, biên giới quốc gia bị phạt tiền
**30–40 triệu đồng**, kèm tịch thu tang vật và buộc cải chính, sửa chữa sản phẩm.

Đã có nhiều vụ bị xử lý vì in bản đồ Việt Nam thiếu Hoàng Sa, Trường Sa trên áo, decal
xe, xuất bản phẩm và quảng cáo.

## Phải làm gì

### Ngay lập tức, trước khi đưa vào lớp

Khoá hai hoạt động **Tìm quốc gia trên bản đồ** và **Tìm vùng trên bản đồ** khỏi bản dùng
trong trường, hoặc chỉ mở những cấp không liên quan tới Việt Nam. Việc khoá làm được bằng
cách bỏ tệp `.rcc` tương ứng khỏi thư mục `rcc/` của máy.

### Sửa nội dung

1. **Vẽ lại `vietnam.svgz`**: thêm quần đảo Hoàng Sa và quần đảo Trường Sa vào cùng một
   mảnh với phần đất liền, để khi trẻ kéo mảnh Việt Nam thì hai quần đảo đi theo.
2. **Vẽ lại nền `southeast_asia.svgz`**: thêm hai quần đảo, có nhãn.
3. Làm tương tự với mảnh `continents/asia.svgz` nếu tỉ lệ cho phép.
4. **Bổ sung bộ bản đồ 34 tỉnh thành Việt Nam** cho `geo-country` — GCompris cho thêm bộ
   bản đồ mới mà không phải sửa mã nguồn.
5. Cân nhắc cách xử lý cấp Đông Á đối với Đài Loan.

### Khi gửi ngược lên KDE

Bản vá bổ sung Hoàng Sa và Trường Sa nên gửi lên kho GCompris của KDE kèm nguồn tham
chiếu. Đây là việc có ích cho cộng đồng, không chỉ cho bản Việt.

## Ghi chú

Bản dịch đã sửa xong phần tên gọi: 185 tên quốc gia và châu lục trước đây bị để nguyên
tiếng Anh nay đã dịch — **Việt Nam**, Trung Quốc, Lào, Campuchia, Thái Lan, Đài Loan,
Đông Nam Á, Các châu lục… Nhưng dịch tên không giải quyết được vấn đề hình vẽ.


---

# ĐÃ SỬA — 02/09/2026

## Làm gì

`tools/them_hoang_sa_truong_sa.py` sửa ba thứ trong tài nguyên hoạt động
**Tìm quốc gia trên bản đồ**:

1. **Mảnh Việt Nam** (`asiasoutheast/vietnam.svgz`): thêm 10 đảo, đá của quần đảo
   Hoàng Sa và 17 đảo, đá, bãi của quần đảo Trường Sa vào chính mảnh Việt Nam.
   Trẻ kéo Việt Nam thì hai quần đảo đi theo, cùng màu.
2. **Bản đồ nền Đông Nam Á** (`asiasoutheast/southeast_asia.svgz`): vẽ hai quần đảo
   kèm khung nét đứt và nhãn **QĐ. HOÀNG SA (VIỆT NAM)**, **QĐ. TRƯỜNG SA (VIỆT NAM)**.
3. **`board/board12_0.qml`**: tính lại tâm mảnh, vì khung bao của mảnh rộng ra
   (72,655×145,853 → 146,159×154,693). Tâm đổi từ (0,2881; 0,3228) sang (0,3593; 0,3309).

## Phép chiếu — cách xác định

GCompris đặt mảnh **theo tâm** tại `(posX, posY)` là tỉ lệ trên nền, và tỉ lệ mảnh
theo kích thước SVG riêng của nó (`Babymatch.qml` dòng 268–282). Vậy muốn thêm đảo
đúng chỗ thì phải biết phép chiếu.

Suy ra từ chính dữ liệu: lấy khung bao của 10 nước Đông Nam Á trên nền (tính từ
`posX/posY` và kích thước từng tệp SVG) rồi hồi quy với khung bao địa lý thật:

```
x =  9.86092 × kinh_độ − 899.2087     sai lệch RMS 0,23 đơn vị nền
y = −9.83827 × vĩ_độ   + 287.7737     sai lệch RMS 1,11 đơn vị nền
```

Hai hệ số gần bằng nhau về trị tuyệt đối → bản đồ là **equirectangular**.

Kiểm chứng độc lập: mảnh Việt Nam gốc mang `transform="translate(-107.702 -57.826)"`,
tức toạ độ trong tệp chính là toạ độ nền. Công thức cho cạnh tây Việt Nam
(A Pa Chải 102,144°Đ) ra 108,0 so với 107,7 thật; cạnh bắc (Lũng Cú 23,393°B) ra
57,6 so với 57,8 thật. Sai số dưới 0,3 đơn vị, tức khoảng 0,03 độ.

## Bằng chứng

Ghép mảnh mới lên nền đúng công thức của GCompris — phần đất liền trùng khít viền nền,
hai quần đảo đúng vị trí:

![Ghép kiểm chứng](anh/ban-do-moi-ghep-kiem-chung.png)

Chạy thật trên NEO One:

![Bản đồ mới trên NEO One](anh/ban-do-moi-tren-neo-one.png)

Mảnh Việt Nam trong cột chọn — thân chữ S kèm hai chùm đảo:

![Mảnh Việt Nam](anh/manh-viet-nam-co-hai-quan-dao.png)

## Cách áp lên một máy khác

```bash
scp neo@<ip>:/usr/share/gcompris-qt/rcc/geography.rcc /tmp/
./deploy/va_ban_do_chu_quyen.sh /tmp/geography.rcc
scp /tmp/geography-vi.rcc neo@<ip>:/tmp/
ssh neo@<ip> 'sudo cp -n /usr/share/gcompris-qt/rcc/geography.rcc{,.orig}; \
              sudo cp /tmp/geography-vi.rcc /usr/share/gcompris-qt/rcc/geography.rcc'
```

Script tự kiểm khứ hồi tệp `.rcc` trước khi sửa; khứ hồi không khớp từng byte thì dừng.

## CÒN LẠI

- **Bản đồ thế giới ở cấp 1 (Các châu lục) chưa vẽ.** Phép chiếu của bản đồ này không
  khớp mô hình tuyến tính (hồi quy cho sai lệch tới ±34 đơn vị), nên đặt đảo vào đó dễ
  sai vị trí — sai còn tệ hơn thiếu. Cần dựng lại phép chiếu bằng cách khác trước khi làm.
- ~~**Bản đồ hành chính Việt Nam** cho hoạt động *Tìm vùng trên bản đồ* vẫn chưa có~~
  **ĐÃ LÀM 02/09/2026** — bộ 34 tỉnh thành theo Nghị quyết 202/2025/QH15, có Hoàng Sa
  và Trường Sa vẽ đúng toạ độ trên lớp nền. Xem [BAN_DO_34_TINH_THANH.md](BAN_DO_34_TINH_THANH.md).
- **Gửi ngược lên KDE**: bản vá này nên đề nghị đưa vào GCompris gốc.
- Toạ độ các đảo lấy theo danh mục địa danh hành chính huyện đảo Hoàng Sa (Đà Nẵng) và
  huyện đảo Trường Sa (Khánh Hòa) — nên để một người có chuyên môn bản đồ soát lại
  trước khi phát hành rộng.
