# Nhật ký thay đổi

Theo [Keep a Changelog](https://keepachangelog.com/vi/1.1.0/) và
[Semantic Versioning](https://semver.org/lang/vi/).

## [0.2.0] — 2026-09-12

Gói `.deb` đầu tiên. v0.1.0 phát hành bản dịch và kho giọng dạng tệp rời; từ bản
này cài qua `apt` và phụ thuộc `gcompris-qt-data`.

### Thêm

- **Gói Debian `gcompris-vi`** (`Architecture: all`) — dựng ở đâu cũng được, cài
  được lên NEO One (ARM64). Không kèm mã biên dịch.
- **Bản đồ Việt Nam có quần đảo Hoàng Sa và Trường Sa**, vá vào hoạt động *Tìm
  quốc gia trên bản đồ* (Nghị định 18/2020/NĐ-CP, Điều 11 khoản 2).
- **Bản đồ hành chính 34 tỉnh thành** cho hoạt động *Tìm vùng trên bản đồ* —
  GCompris gốc không có.
- **Hai mini app của Làng Maker**: *Làng Maker* (`lang_maker`) và *Đối Đôi Làng*
  (`lang_doidoi`, bộ bài 57 hình kiểu Dobble, ba chế độ chơi).
- **`scripts/install_on_neo.sh`** — cài một dòng theo chuẩn NEO Installation
  Script Convention v2, kèm dọn dẹp bản cài tay cũ của `deploy/install_vi.sh`.
- **`tools/them_tieng_viet.py`** — tách bộ vá `LanguageList.qml` ra thành công
  cụ riêng, dùng chung cho `install_vi.sh` và postinst của gói.

### Thay đổi

- **`tools/rcc_repack.py` viết định dạng `.rcc` bằng Python thuần**, không còn
  gọi lệnh `rcc` của Qt. Nhờ vậy postinst vá `.rcc` ngay trên NEO One mà chỉ cần
  `python3`.
- **Nâng đời GCompris không làm mất bản việt hóa.** Năm tệp `.rcc` của
  `gcompris-qt-data` được vá qua `dpkg-divert`; một trigger dpkg vá lại tự động
  mỗi khi gói gốc nâng đời. Gỡ gói thì mọi thứ trở lại nguyên bản.

### Kiểm thử

- 148 test chạy trong lúc dựng gói; `lintian` không báo lỗi nào.
- Nghiệm thu trên `gcompris-qt-data 3.1-2` thật: cài, 5 chuyển hướng, nội dung 5
  tệp `.rcc` đã vá đúng, trigger vá lại sau khi nâng đời, gỡ gói trả `core.rcc`
  về đúng md5 gốc.
- Đã chạy thử trên máy NEO One thật.

### Chưa có

- **Kho giọng đọc** — mới xong 202/888 tệp, chưa đóng vào gói. Tạm dùng
  `deploy/install_vi.sh`.
- **Xưng hô gia đình** vẫn chưa dùng được cho lớp học — xem
  [docs/NOI_DUNG_CAN_THIET_KE_LAI.md](docs/NOI_DUNG_CAN_THIET_KE_LAI.md).

## [0.1.0] — 2026-09-01

### Thêm

- Bản dịch 4.277/4.277 chuỗi — 3.662 dịch, 615 cố ý giữ nguyên. Nghiệm thu trên
  GCompris thật: 382/382 hoạt động hiện tiếng Việt.
- Kho giọng 202 tệp (8,2 phút) sinh bằng VieNeu-TTS, giọng Bình (nam miền Bắc).
- `deploy/install_vi.sh` — cài tay bản dịch, vá `core.rcc`, cài kho giọng.

[0.2.0]: https://github.com/ThingEdu/gcompris-vi/releases/tag/v0.2.0
[0.1.0]: https://github.com/ThingEdu/gcompris-vi/releases/tag/v0.1.0
