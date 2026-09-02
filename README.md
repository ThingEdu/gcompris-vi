# GCompris tiếng Việt

Bản việt hóa [GCompris](https://gcompris.net) — bộ phần mềm giáo dục 203 hoạt động
cho trẻ 2–10 tuổi của cộng đồng KDE. Đích chạy thật là **NEO One (Linux ARM64)**
của [ThingEdu](https://github.com/ThingEdu) · Làng Maker.

Trước dự án này, GCompris có 52 ngôn ngữ nhưng **chưa từng có tiếng Việt**:
thống kê KDE ghi nhận 6.190 chuỗi, 0% đã dịch.

## Đang có gì

| Phần | Trạng thái |
|---|---|
| Giao diện, tên và mô tả 203 hoạt động, hướng dẫn | **4.277/4.277 chuỗi đã xử lý** — 3.662 dịch, 615 cố ý giữ nguyên (tên riêng nước ngoài, ký hiệu) |
| Kho giọng đọc tiếng Việt | 202/888 tệp — lời dẫn 114 hoạt động, bảng chữ cái, chữ số, lời khen, màu sắc |
| Bản đồ Việt Nam | Hoàng Sa + Trường Sa vá vào bản đồ châu Á; **bản đồ hành chính 34 tỉnh thành** mới, GCompris gốc không có |
| Mini app của Làng Maker | Thêm hoạt động mới **không cần biên dịch lại** — xem [DOCS/MINI_APP_LANG_MAKER.md](DOCS/MINI_APP_LANG_MAKER.md) |
| Đường ống dựng lại từ đầu | `.qm`, `core.rcc` đã vá, `voices-vi.rcc`, `geography.rcc`, `geo-country.rcc` |

Đã nghiệm thu trên GCompris thật: **382/382 hoạt động** hiện tên, mô tả và
hướng dẫn bằng tiếng Việt.

## Cài lên máy đã có GCompris

```bash
git clone https://github.com/ThingEdu/gcompris-vi.git
cd gcompris-vi
python3 -m venv .venv && ./.venv/bin/pip install polib
./tools/build_qm.sh                       # dựng gcompris_qt_vi.qm
sudo ./deploy/install_vi.sh --root /usr/share/GCompris
```

Rồi thêm vào `~/.config/gcompris/gcompris-qt.conf` (xem `deploy/gcompris-qt.conf.vi`):

```ini
[%General]
locale=vi_VN.UTF-8
enableAutomaticDownloads=false
```

## Vì sao phải vá `core.rcc`

Đặt `locale` trong tệp cấu hình là **chưa đủ**. `ApplicationInfo::loadTranslation()`
đối chiếu locale với danh sách trong `LanguageList.qml` và đẩy mọi ngôn ngữ lạ về
mặc định — chạy thử sẽ thấy dòng `locale "vi_VN.UTF-8" not supported, defaulting to system`.

May là `LanguageList.qml` không nằm trong tệp thực thi mà ở trong `core.rcc`, một
tệp tài nguyên Qt riêng nạp lúc chạy. `tools/rcc_extract.py` bung nó ra,
`tools/rcc_repack.py` đóng lại — **không cần trình biên dịch C++**. Kiểm tra khứ
hồi: đóng gói lại y nguyên rồi bung ra cho 142/142 tệp khớp từng byte.

## Kho giọng đọc

Sinh bằng [VieNeu-TTS](https://huggingface.co/pnnbao-ump) chạy trên máy, giọng
**Bình (nam miền Bắc)**. Xem `voices/README.md`.

Một lưu ý đắt giá: bộ sinh gieo số ngẫu nhiên cố định, nên gọi lại y hệt sẽ ra y
hệt — "thử lại" mà không đổi tham số thì vô nghĩa. Mỗi lần thử lại nay dùng một
nhiệt độ lấy mẫu khác, kèm cắt lặng và kiểm thời lượng theo số âm tiết.

## Còn phải làm

- 564 từ vựng và 129 tên nước cho kho giọng
- Bộ từ theo cấp độ âm tiết cho `gletters` và `wordsgame`
- Bốn chỗ nội dung phải thiết kế lại chứ không dịch được — xem
  [`DOCS/NOI_DUNG_CAN_THIET_KE_LAI.md`](DOCS/NOI_DUNG_CAN_THIET_KE_LAI.md).
  Đáng chú ý nhất là **xưng hô gia đình**: cây gia đình gốc có đúng một ô "Uncle"
  và một ô "Aunt", trong khi tiếng Việt tách thành chú, bác, cậu, cô, dì, thím, mợ
  theo bên nội/ngoại và thứ bậc tuổi. Bản dịch hiện tại theo bên nội và **không
  nên phát hành cho lớp học ở dạng này**.
- Nghiệm thu trên NEO One thật
- Gửi bản dịch lên kho l10n của KDE

## Cấu trúc

```
po/gcompris_qt.po        bản dịch
po/giu-nguyen.txt        chuỗi cố ý để nguyên tiếng Anh
voices/manifest/*.tsv    lời đọc cho từng tệp giọng
maps/34-tinh/            bản đồ hành chính 34 tỉnh thành (1 nền + 34 mảnh + board)
mini-app/chung/          nhân vật NEO Tre dùng chung cho mọi mini app
mini-app/lang_*/         mini app do ThingEdu thêm vào (tiền tố lang_ để không đụng bản gốc)
tools/                   dựng khung po, xuất/nhập đợt dịch, kiểm tra,
                         bung/đóng .rcc, sinh giọng, dựng .qm
deploy/install_vi.sh     cài vào một bản GCompris đã có
tests/                   test cho bộ kiểm tra bản dịch
```

```bash
./.venv/bin/python -m pytest tests/          # 87 test
./.venv/bin/python tools/check_po.py po/gcompris_qt.po
./.venv/bin/python tools/po_batch.py stats po/gcompris_qt.po
```

## Giấy phép

GCompris phát hành theo **AGPL v3**, nên bản việt hóa này cũng vậy — xem
[LICENSE](LICENSE). Mã nguồn gốc: https://invent.kde.org/education/gcompris
(khảo sát trên commit `8b49e97f`, bản 26.1.0).
