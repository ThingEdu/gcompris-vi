# Nội dung không dịch được, phải thiết kế lại

Những chỗ này đã được dịch tạm để bản tiếng Việt chạy trọn vẹn, nhưng bản dịch
chỉ đúng một phần. Muốn dùng để dạy thật thì phải làm lại nội dung, không phải
sửa câu chữ.

## 1. Xưng hô gia đình — hoạt động `family`, `family_find_relative`

Hoạt động tự mô tả là dạy quan hệ họ hàng "theo hệ tuyến tính dùng ở phần lớn
xã hội phương Tây". Cây gia đình của nó có **một** ô Uncle và **một** ô Aunt.

Tiếng Việt tách ra theo bên nội/ngoại và theo thứ bậc tuổi:

| Nguồn | Tiếng Việt |
|---|---|
| Uncle | chú (em bố), bác (anh bố), cậu (anh em của mẹ) |
| Aunt | cô (chị em của bố), dì (chị em của mẹ), thím (vợ chú), mợ (vợ cậu) |
| Brother | anh trai, em trai |
| Sister | chị gái, em gái |
| Cousin | anh/chị/em họ — tuỳ tuổi và giới |
| Grandson / Nephew | đều là "cháu", phân biệt bằng cháu nội/cháu ngoại và con của ai |

**Đang tạm dịch theo bên nội**, vì cây ở cấp 10 là ông → bố và chú → mình, tức
họ hàng bên bố. Các cấp khác chưa soát. Thứ bậc tuổi thì cây gốc không hề thể
hiện, nên chú/bác là **đoán**.

**Cần làm:** hoặc dựng lại bộ dữ liệu cây gia đình cho đúng cách xưng hô Việt
(thêm nhánh nội/ngoại, thêm dấu hiệu tuổi), hoặc bỏ hai hoạt động này khỏi bản
Việt. Không nên phát hành cho lớp học ở dạng hiện tại.

## 2. Tiền — nhóm hoạt động `money`

Dùng ảnh SVG đồng euro (`c1e.svg`, `c20c.svg`…). Việt Nam không tiêu tiền xu,
mệnh giá là tờ từ 1.000 tới 500.000 đồng. Muốn dùng thật phải vẽ lại bộ ảnh và
sửa dữ liệu mệnh giá.

**Lưu ý pháp lý:** mô phỏng hình ảnh tiền đồng có quy định riêng của Ngân hàng
Nhà nước — kiểm tra trước khi phát hành công khai.

## 3. Địa lý — `geography`, `geo-country`

Chưa có bản đồ Việt Nam. Nên bổ sung bộ bản đồ 34 tỉnh thành; GCompris cho thêm
bộ bản đồ mới mà không phải đụng mã nguồn.

## 4. Bộ từ theo cấp độ — `gletters`, `wordsgame`, `hangman`, `click_on_letter`

Xây trên giả định "chữ cái rời ghép thành từ". Tiếng Việt có 29 chữ cái, thêm
ă â đ ê ô ơ ư, và 5 dấu thanh nằm trên nguyên âm; đơn vị đọc là âm tiết. Phải
soạn bộ từ theo cấp độ âm tiết, không phải dịch.

Đã làm tạm: bộ từ 3/4/5 ký tự cho `crane`, bảng chữ cái tiếng Việt cho
`alphabet-sequence`. Còn `gletters` và `wordsgame` cần `default-vi.json` riêng.
