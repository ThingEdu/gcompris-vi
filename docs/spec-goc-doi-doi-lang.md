# MÔ TẢ APP · ĐỐI ĐÔI LÀNG
**Hoạt động học kiểu GCompris · Phiên bản 1 chạy trên NEO One · Tài liệu đầu vào cho việc tạo app**

---

## 0 · Tóm tắt một đoạn

Đối Đôi Làng là bản số hoá của bộ bài 57 hình Làng Maker Việt, xây theo chuẩn hoạt động GCompris (Qt/QML, mã mở), chạy trước tiên trên thiết bị NEO One đặt tại điểm sinh hoạt. App có ba chế độ xếp theo đúng kịch bản sư phạm của làng: **Học hình → Luật ăn thua → Luật làng**, trong đó chế độ Luật làng (chơi hợp tác, cả bàn chung một đồng hồ, không ai bị bỏ lại) là chế độ chính và là lý do app tồn tại. App **không thay bộ bài giấy** — nó là trạm luyện, trạm thu hút người mới, và máy đo được thứ bộ bài giấy không đo được.

---

## 1 · Vì sao làm app này (đọc để hiểu ý đồ, không phải để code)

1. **Trạm thu hút tại điểm đối tác:** NEO One đặt ở cửa hàng/điểm sinh hoạt chạy chế độ tự giới thiệu (attract mode) — trẻ đi ngang, chơi thử 2 phút, nhận lời mời tham gia làng. Đây là phễu tuyển sinh chạy không cần người.
2. **Đo được:** thời gian phản xạ, ai gọi bao nhiêu lượt, chênh lệch giữa người nhanh nhất và chậm nhất trong bàn — dữ liệu nuôi phiếu quan sát facilitator mà mắt người dễ bỏ sót.
3. **Chứng minh năng lực Rogo:** app đầu tiên chạy trên phần cứng nhà, nội dung nhà, làm mẫu cho dòng Neo Play.

## 2 · Nền tảng & giả định phần cứng (ĐIỀN TRƯỚC KHI CODE)

| Thông số NEO One | Giá trị | Ghi chú |
|---|---|---|
| Hệ điều hành | `[Linux / Android — điền]` | GCompris chạy được cả hai |
| Màn hình | `[kích thước, độ phân giải — điền]` | Spec dưới viết cho màn ngang ≥ 10", cảm ứng đa điểm |
| Tư thế đặt máy | `[đứng / nằm mặt bàn — điền]` | Chế độ Luật làng cần 2–4 em quanh máy → ưu tiên nằm ngang hoặc nghiêng thấp |
| Cảm ứng | `[số điểm chạm — điền]` | Luật làng cần tối thiểu 2 điểm chạm đồng thời |
| Nút cứng | `[có/không — điền]` | Nếu có nút kiểu arcade: dùng làm nút "gọi" cho từng người chơi |
| Mạng | Mặc định **offline hoàn toàn** | Đồng bộ log qua USB hoặc khi có mạng, không bắt buộc |
| Âm thanh | Loa ngoài | Tiếng trống là âm chủ đạo |

> Quy tắc chung: mọi tính năng phải chạy trọn vẹn **không mạng, không tài khoản, không đăng nhập**.

## 3 · Người dùng & bối cảnh

- **Người chơi:** trẻ 6–14, chơi theo bàn 2–4 em quanh một máy; nhiều em lần đầu chạm thiết bị này.
- **Facilitator:** 16–19 tuổi, cần vào khu cài đặt bằng mã PIN, thao tác dưới 30 giây.
- **Bối cảnh:** ồn, đông, phiên chơi ngắn 3–10 phút; máy công cộng → không lưu bất kỳ thông tin cá nhân nào của trẻ.

## 4 · Ba chế độ chơi

### Chế độ 1 · HỌC HÌNH (1 người, chuẩn bị)
- Mục đích: em mới thuộc mặt 31 hình Bậc 1 trước khi vào bàn.
- Chơi: mỗi lượt hiện 1 hình to giữa màn + đọc tên tiếng Việt (giọng thu sẵn); em chọn đúng tên trong 3 phương án hình ảnh (không chữ với nhóm nhỏ; kèm chữ với nhóm lớn — bật/tắt trong cài đặt).
- 5 mức GCompris chuẩn: mức 1 nhóm Nhân vật → mức 5 trộn cả bộ, thời gian rút ngắn dần.

### Chế độ 2 · LUẬT ĂN THUA (2–4 người, dùng có chủ đích)
- Đúng luật gốc: thẻ chung giữa màn, mỗi em một thẻ riêng ở cạnh màn phía mình; ai chạm đúng hình trùng trước thì ăn thẻ.
- **Tồn tại để bị vượt qua:** kết thúc ván, màn kết quả hỏi đúng câu của kịch bản buổi chơi: *"Trò này vui với một người hay vui với cả bàn?"* và mời chuyển sang Luật làng. Không có bảng xếp hạng lưu lâu dài, không leaderboard giữa các buổi.

### Chế độ 3 · LUẬT LÀNG (2–4 người, chế độ chính)
Ba luật của kịch bản buổi chơi được máy **cưỡng chế bằng cơ chế**, không bằng lời nhắc:
1. **Đồng hồ chung:** cả bàn phá hết chồng thẻ trong thời gian mục tiêu → cả bàn thắng. Không có điểm cá nhân hiển thị trong ván.
2. **Không ai bị bỏ lại:** mỗi lượt máy chỉ nhận chạm từ **vùng của người đến lượt** (viền vùng sáng lên); lượt xoay vòng bắt buộc. Người khác chạm không có tác dụng.
3. **Hoa tiêu im lặng:** em thắng nhiều nhất ở ván trước (hoặc do facilitator chỉ định) nhận vai Hoa tiêu: vùng của em không "gọi" được, nhưng em chạm vào thẻ chung sẽ tạo **vòng nhấp nháy gợi ý** quanh vùng em chạm — giúp mà không nói, đúng nghĩa đen.
- Kết ván: chỉ hiện **kỷ lục của chính bàn này hôm nay** và mời phá kỷ lục — không so với bàn khác, không so với hôm khác.
- Ba tiếng trống khi phá kỷ lục — trùng nghi thức trống của làng ngoài đời.

### Chế độ phụ · TỰ GIỚI THIỆU (attract mode)
- Máy để yên 90 giây → tự chạy demo: các thẻ trôi, thỉnh thoảng hai thẻ chập lại và hình trùng phát sáng, kèm một dòng mời chạm để chơi. Sau ván chơi thử của khách vãng lai, hiện màn hình duy nhất có thông tin thật: *"Muốn tự tay làm bộ bài này? Hỏi anh chị áo xanh."* + mã QR nhóm Zalo (bật/tắt được).

## 5 · Toán bộ bài (đã có sẵn, không chế lại)

- Bộ Bậc 1: 31 thẻ × 6 hình (mặt phẳng xạ ảnh bậc 5). Bộ đầy đủ: 57 thẻ × 8 hình (bậc 7). Sinh bằng thuật toán, kiểm bất biến khi khởi động: *mọi cặp thẻ trùng đúng một hình*.
- Trên thẻ số: hình xoay góc ngẫu nhiên, kích thước lệch nhau nhẹ (±15%), sắp không đè nhau — giống thẻ giấy.
- Phiên bản 1 mặc định **Bậc 1 (31 thẻ)**; bộ đầy đủ mở trong cài đặt facilitator.

## 6 · Tài sản có sẵn (bàn giao kèm tài liệu này)

| Tài sản | Nguồn | Định dạng |
|---|---|---|
| 57 hình vector | Bộ hình gốc của làng (file `bo-57-hinh-lang-maker.html`) | SVG, viền đen 2.6, nền kem `#FBF8F1` |
| Bảng 8 màu sơn mài | Son `#C4231F` · Vàng `#E8A317` · Lục `#1F7A52` · Chàm `#2B57A6` · Tím `#6B3FA0` · Gián `#8A4B24` · Ngọc `#12958E` · Then `#3A3A3A` | mã hex |
| Nền giao diện | Chàm đậm `#16264A`, thẻ nền kem | — |
| Chữ | Be Vietnam Pro (đủ dấu tiếng Việt) | font mở |
| Âm | Cần thu: tiếng trống ×3 kiểu (mở buổi, đúng, phá kỷ lục), 31 tên hình giọng đọc trẻ em Việt | wav/ogg |

Quy tắc không đổi từ bản giấy: **không chữ trên thẻ chơi**, hình nhận ra được khi xoay mọi góc.

## 7 · Màn hình & luồng

```
[Tự giới thiệu] ←(máy rảnh 90s)── [TRANG LÀNG]
                                   ├─ Học hình (chạm là vào, chọn mức 1–5)
                                   ├─ Vào bàn → chọn số người (2/3/4)
                                   │            → chọn luật: Ăn thua / Luật làng
                                   │            → ván chơi → kết ván → chơi lại / đổi luật
                                   └─ (giữ 5s góc màn) Cài đặt facilitator [PIN]
```

**Trang làng:** cổng làng + Neo Tre vẫy, ba cửa lớn bằng hình không chữ (rùa = học; bốn bàn tay = vào bàn). Mọi nút chạm tối thiểu 14 mm.

**Ván chơi (2–4 người):** thẻ chung ở tâm, vùng người chơi ở 2–4 cạnh màn, mỗi vùng xoay hướng về phía người ngồi (giao diện mặt bàn — hai em đối diện nhìn ngược nhau đều đúng chiều của mình).

**Cài đặt facilitator (PIN 4 số, đổi được):** chọn bộ 31/57 · bật tắt chữ kèm hình · thời lượng đồng hồ chung · bật tắt QR Zalo · xuất log ra USB · xoá log.

## 8 · Dữ liệu & quyền riêng tư (điều kiện cứng)

- **Không thu, không hỏi, không lưu:** tên, tuổi, ảnh, giọng nói người chơi. Không tài khoản. Không gửi dữ liệu đi đâu khi chưa cắm USB/lệnh xuất.
- Log mỗi ván, nặc danh hoàn toàn: `thời điểm, chế độ, số người, số lượt mỗi vùng (P1..P4), thời gian ván, kỷ lục, số lần gợi ý của Hoa tiêu`.
- Xuất CSV một chạm trong khu facilitator — file này đối chiếu với phiếu quan sát giấy A5 sau buổi, phục vụ chỉ số quay lại buổi 4.
- Điều khoản này viết theo Điều 6 Giao ước làng và **chỉ được siết thêm ở các bản sau, không được nới** (cửa một chiều).

## 9 · Giấy phép & ghi công

- Nếu xây trong mã nguồn GCompris: tuân GPLv3 của dự án, cân nhắc đóng góp ngược (upstream) hoạt động này cho cộng đồng — một hoạt động mang bản sắc Việt trong bộ giáo dục mở toàn cầu là điểm truyền thông mạnh.
- Nếu chỉ xây "kiểu GCompris" (app riêng bằng Qt/QML hoặc công nghệ khác): không dùng mã, tên, linh vật của GCompris; Tux trong bộ hình là bản vẽ lại, ghi công linh vật Linux của Larry Ewing ở màn giới thiệu.
- Bộ 57 hình phát hành CC BY-SA, làng giữ quyền. **Kiểm tra tương thích giấy phép hình ↔ mã trước khi trộn** (việc của bước pháp lý, đánh dấu chờ).

## 10 · Phạm vi phiên bản 1 (cắt gọn để chạy được ở Thọ Xuân)

**Có:** Học hình (5 mức) · Vào bàn 2–4 người · hai luật chơi · bộ 31 thẻ · attract mode · cài đặt facilitator + xuất CSV · tiếng Việt · offline.
**Chưa có (để bản sau, ghi rõ để không ai tiện tay làm):** bộ 57 thẻ mặc định · nhiều máy nối nhau · hồ sơ người chơi · huy hiệu số · tiếng Anh · bảng xếp hạng (có thể sẽ không bao giờ có — xếp hạng cá nhân đi ngược luật làng).

## 11 · Tiêu chí nghiệm thu (chạy thử tại bàn thật)

1. Khởi động nguội → chơi được ván đầu dưới 60 giây, không cần người hướng dẫn.
2. Kiểm toán tự động khi build: 31 thẻ, mọi cặp trùng đúng 1 hình — build fail nếu sai.
3. Bốn em chạm đồng thời: máy chỉ nhận vùng đến lượt, ba vùng kia không gây hiệu ứng gì ngoài rung nhẹ viền.
4. Vai Hoa tiêu không thể ghi lượt trong mọi trường hợp, kể cả chạm nhanh liên tiếp.
5. Rút điện giữa ván → bật lại không mất log các ván đã xong.
6. Một facilitator mới, chưa đọc tài liệu, tự đổi bộ thẻ và xuất CSV trong dưới 2 phút chỉ nhờ giao diện.
7. Trẻ 6 tuổi chơi Học hình mức 1 không cần biết chữ.
8. Toàn bộ app không hiển thị bất kỳ ô nhập tên/thông tin cá nhân nào.

---

*Tài liệu này là đầu vào cho bước tạo app. Chỗ nào ghi `[điền]` phải chốt trước khi viết dòng mã đầu tiên; chỗ nào ghi "cửa một chiều" thì mọi phiên bản sau bị ràng buộc.*
