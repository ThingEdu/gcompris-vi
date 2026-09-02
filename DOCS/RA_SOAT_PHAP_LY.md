# Rà soát pháp lý trước khi phát hành công khai

**2026-09-02 · cho mini app `lang_doidoi` (Đối Đôi Làng) và bộ 57 hình Làng Maker**

Bản thiết kế `MINI_APP_DOI_DOI_LANG.md` §13 đặt một cửa: *"cần bước rà pháp lý xác
nhận trước khi phát hành công khai"*. Tài liệu này đóng cửa đó về mặt kỹ thuật —
phần còn lại cần chủ dự án ký.

**Đây không phải tư vấn pháp lý.** Đây là rà soát dữ kiện: giấy phép nào đang áp
cho cái gì, có xung đột không, và tiền lệ của chính dự án gốc ra sao. Chỗ nào cần
người có chuyên môn thì ghi rõ.

---

## 1 · Câu hỏi phải trả lời

1. Trộn tài sản **CC BY-SA** vào một kho mã **AGPL** có được không?
2. Bộ 57 hình có dính bản quyền hay nhãn hiệu của ai không?
3. Tệp mã mới ghi `GPL-3.0-or-later` trong khi kho là AGPL — có sai không?
4. Có tài sản nào của GCompris bị phát hành lại mà không được phép không?

---

## 2 · Dữ kiện đã kiểm, kèm bằng chứng

| Việc kiểm | Kết quả | Bằng chứng |
|---|---|---|
| Giấy phép kho này | **AGPL-3.0** | `LICENSE`, 661 dòng, tiêu đề *GNU Affero General Public License Version 3* |
| Giấy phép GCompris | **AGPL-3.0** ở tầng dự án | `COPYING` bung từ `core.rcc` của máy đích |
| Giấy phép tệp mã GCompris | **GPL-3.0-or-later** | `ActivityBase.qml` của họ: `SPDX-License-Identifier: GPL-3.0-or-later` |
| GCompris có tài sản CC BY-SA không | **CÓ — 110 tệp CC BY-SA 4.0** | Quét `core.rcc`: 110 lần xuất hiện `creativecommons.org/licenses/by-sa/4.0`, cộng 2 tệp phạm vi công cộng |
| Nguồn gốc 57 hình | **Hình vẽ gốc của làng** | `mini-app/nguon/bo-57-hinh-lang-maker.html:798` — *"hình vẽ gốc cho Làng Maker Việt, không sao chép nhãn hiệu của bên nào"* |
| Tux | **Bản vẽ lại**, không dùng hình của Larry Ewing | cùng dòng 798 |
| Trâu Mở | **Hình thay thế bản địa** cho linh vật GNU, không dùng hình gốc | cùng dòng 798 |
| Tình trạng CC BY-SA của bộ hình | **Mới là ĐỀ XUẤT, chưa chốt** | dòng 799: *"**Đề xuất phát hành.** Giấy phép CC BY-SA cho cộng đồng"* — và **không ghi phiên bản** |
| Dữ liệu GCompris có bị phát hành lại không | **Không** | `build/core.rcc` nằm trong `build/`, đã bị `.gitignore` bỏ qua |

---

## 3 · Trả lời từng câu hỏi

### 3.1 Trộn CC BY-SA vào kho AGPL — ĐƯỢC

Đây không phải chuyện phải suy luận, vì **chính GCompris đang làm đúng như vậy**:
110 tệp tài sản CC BY-SA 4.0 nằm ngay trong `core.rcc`, cạnh mã AGPL/GPL, trong
cùng một bản phát hành.

Lý do nó không xung đột: bộ hình là **tệp tài sản nạp lúc chạy**, không biên dịch
vào mã, không liên kết với mã. Về mặt giấy phép đây là *gộp chung* chứ không phải
*tác phẩm phái sinh*. Hình giữ CC BY-SA, mã giữ AGPL/GPL, hai giấy phép chạy song
song trong cùng một kho. **Không phải đổi giấy phép cho bên nào.**

### 3.2 Bộ 57 hình — SẠCH, nhưng phải chốt phiên bản

Tài liệu nguồn của chính làng khẳng định đây là hình vẽ gốc, không sao chép nhãn
hiệu bên nào. Hai chỗ có thể bị hỏi thì đã xử lý sẵn: Tux vẽ lại chứ không dùng
hình của Larry Ewing, và Trâu Mở thay cho linh vật GNU chứ không dùng hình gốc.

**Hai việc còn thiếu, cần chủ dự án làm:**

**(a) Chốt phiên bản CC BY-SA — nên chọn 4.0.** Tài liệu nguồn chỉ ghi "CC BY-SA"
không có số. Ba lý do chọn 4.0:
- GCompris dùng đúng **CC BY-SA 4.0** cho 110 tài sản của họ — cùng phiên bản thì
  người dùng lại không phải đối chiếu hai bộ điều khoản.
- Creative Commons tuyên bố CC BY-SA 4.0 **tương thích một chiều sang GPLv3**.
  Bản 3.0 trở về trước **không có** điều khoản này. Nếu sau này có ai muốn nhập
  hình vào một tác phẩm GPL hợp nhất, 4.0 cho đường đi, bản cũ thì tắc.
- 4.0 áp dụng quốc tế, không phải bản dịch theo từng nước như 3.0.

**(b) Biến "đề xuất" thành quyết định.** Dòng 799 tệp nguồn ghi *"Đề xuất phát
hành"*. Đề xuất không phải giấy phép. Chủ dự án cần tuyên bố dứt khoát trong
`README.md` và trong chính tệp nguồn: bộ hình phát hành theo CC BY-SA 4.0, chủ
sở hữu là *(tên chính thức — xem mục 5)*.

### 3.3 Ghi `GPL-3.0-or-later` trên tệp mã — ĐÚNG, không phải sai

Đây là điều đáng ngạc nhiên nhất khi rà: **GCompris cũng làm y hệt.** Tệp
`ActivityBase.qml` của họ ghi `SPDX-License-Identifier: GPL-3.0-or-later`, trong
khi `COPYING` của dự án là AGPL-3.0.

Cách này hợp lệ vì AGPLv3 §13 cho phép kết hợp với mã GPLv3. Mã GPLv3 nằm trong
một tác phẩm AGPLv3 thì tác phẩm hợp thành chịu ràng buộc AGPL, còn từng tệp giữ
giấy phép của nó.

Nên các tệp mới ghi `GPL-3.0-or-later` là **theo đúng lệ của dự án gốc**, tiện cho
việc sau này đóng góp ngược lên l10n KDE.

Có **một câu sai trong tài liệu** đã phát hiện: `MINI_APP_DOI_DOI_LANG.md` §13 viết
*"GPL-3.0-or-later… như GCompris"* — hàm ý GCompris là GPL. Thực tế GCompris là
**AGPL** ở tầng dự án và GPL ở tầng tệp. Câu đó đang được sửa.

### 3.4 Tài sản GCompris — KHÔNG phát hành lại

`build/core.rcc` là dữ liệu của GCompris, chép về để `tools/kiem_qml.py` nạp thử
QML. Nó nằm trong `build/`, mà `build/` đã bị `.gitignore` bỏ qua từ trước. Đã
kiểm: không có tệp nào của GCompris trong danh sách tệp mà nhánh này thêm vào.

Bộ khung giả ở `tools/qml_gia/` **không phải mã chép về**. Đó là các tệp QML tự
viết, mô phỏng vài kiểu do C++ của GCompris đăng ký (`ApplicationInfo`,
`ApplicationSettings`, `File`, `DownloadManager`), chỉ có tên thuộc tính và chữ ký
hàm, không có phần thân thực thi nào của GCompris. Tên gọi và chữ ký giao diện nói
chung không được bảo hộ như mã nguồn. Dù vậy đã ghi rõ trong tệp rằng đây là bản
viết lại, để không ai hiểu nhầm.

---

## 4 · Rủi ro còn lại — nhỏ, nhưng nên biết

**Ảnh chụp màn hình trong `DOCS/anh/`** có chứa giao diện của GCompris: hàng biểu
tượng mục (mèo, chim cánh cụt, khủng long…), thanh nút, nền cỏ. Những thứ đó là
tài sản của GCompris theo CC BY-SA 4.0 hoặc GPL. Chụp màn hình một phần mềm tự do
để minh hoạ tài liệu là việc bình thường và chính GCompris cũng làm, nhưng nếu
muốn chặt chẽ thì thêm một dòng trong `README.md`: *ảnh chụp có chứa giao diện
GCompris, thuộc bản quyền dự án GCompris, dùng theo giấy phép của họ.*

**Điều khoản ShareAlike đi theo hình mãi mãi.** Ai vẽ thêm hình mới dựa trên bộ
này, hoặc sửa hình trong bộ, thì bản sửa cũng phải là CC BY-SA 4.0. Đây là điều
làng muốn — nhưng cần nói rõ với các trường dùng lại, kẻo họ tưởng lấy về sửa rồi
đóng lại được.

**Bài học đã trả giá ở mini app trước.** `MINI_APP_LANG_MAKER.md` ghi lại chuyện
ảnh nền có logo FPT Telecom lọt vào commit `bcbea87` rồi mới gỡ ở `2d71cdb` — bản
còn logo **vẫn nằm trong lịch sử công khai** tới hôm nay. Bộ 57 hình lần này là
hình vẽ gốc nên không vướng, nhưng quy tắc rút ra vẫn đúng: **soi nhãn hiệu bên
thứ ba trước khi commit, vì lịch sử git không xoá được bằng một commit sau.**

---

## 5 · Ba việc chủ dự án ĐÃ CHỐT (2026-09-03)

| Việc | Quyết định |
|---|---|
| Phiên bản giấy phép hình | **CC BY-SA 4.0** |
| Chủ sở hữu ghi trên giấy phép | **ThingEdu** |
| Trạng thái | **Quyết định**, không còn là đề xuất |

Đã điền vào bốn chỗ: `ActivityInfo.qml` trường `credit:` (ô GCompris hiện cho
người dùng), `README.md` mục Giấy phép, `mini-app/nguon/bo-57-hinh-lang-maker.html`
(thay dòng "Đề xuất phát hành"), và `MINI_APP_DOI_DOI_LANG.md` §13.

**Cửa pháp lý ở §13 đã đóng.** Phần dưới giữ lại làm hồ sơ của việc rà soát.

### (hồ sơ) Ba việc khi rà soát còn để ngỏ

Rà soát kỹ thuật đã xong, ba chỗ dưới đây cần người có thẩm quyền quyết:

1. **Phiên bản giấy phép hình.** Đề nghị **CC BY-SA 4.0**, cùng phiên bản GCompris
   dùng và là bản duy nhất có đường tương thích sang GPLv3.
2. **Tên chủ sở hữu ghi trên giấy phép.** Hiện tài liệu nói *"Làng Maker Việt"*,
   `ActivityInfo.qml` ghi tác giả là *ThingEdu*, kho nằm dưới tổ chức *ThingEdu*
   trên GitHub. Ba tên cho cùng một chủ thể. Cần chọn một tên đứng trên giấy phép
   (có thể ghi kèm: *"Làng Maker Việt · ThingEdu"*).
3. **Xác nhận đây là quyết định, không phải đề xuất.** Tệp nguồn đang ghi *"Đề
   xuất phát hành"*. Sửa thành câu khẳng định thì cửa pháp lý đóng.

Ba việc này đều là **một dòng chữ**, nhưng phải là chữ của chủ dự án, không phải
của người rà soát.

---

## 6 · Kết luận

Không tìm thấy xung đột giấy phép nào cản việc phát hành công khai. Cách trộn
CC BY-SA vào kho AGPL đúng như chính GCompris đang làm; cách ghi
`GPL-3.0-or-later` trên tệp mã cũng đúng lệ của họ; bộ hình là tác phẩm gốc của
làng và hai chỗ dễ vướng đã được xử lý từ khâu vẽ.

Cái thiếu không phải là quyền, mà là **lời tuyên bố**: bộ hình chưa được chính
thức đặt dưới một phiên bản giấy phép cụ thể, và ghi công chưa xuất hiện ở chỗ
người dùng nhìn thấy. Cả hai đang được bổ sung.
