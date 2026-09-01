# Kho giọng đọc tiếng Việt

Sinh bằng [VieNeu-TTS](https://huggingface.co/pnnbao-ump) (zero-shot, chạy trên máy),
giọng mẫu lấy từ `~/Ai-Code/NeoTeach/voices/giong_tuan/ref.wav`.

## Cách làm

```bash
# 1. Sinh giọng (chạy trong venv có gói vieneu — hiện dùng của NeoTeach)
cd ~/Ai-Code/NeoTeach/voice-studio
.venv/bin/python ~/Ai-Code/gcompris-vi/tools/make_voices.py

# 2. Soát lại
cd ~/Ai-Code/gcompris-vi && .venv/bin/python tools/check_voices.py --fmt ogg

# 3. Đóng gói (ogg cho NEO One Linux, aac cho macOS)
./tools/pack_voices.sh ogg
```

## Vì sao phải soát

VieNeu-TTS không tất định. Với câu ngắn (một, hai âm tiết) nó thỉnh thoảng
cho ra tệp cụt 0,1 giây hoặc chạy loạn hơn 10 giây — đủ để hỏng cả bộ chữ cái.
`make_voices.py` cắt lặng hai đầu rồi kiểm tra thời lượng theo số âm tiết, sai
thì sinh lại tới 6 lần. Dải thời lượng hiệu chuẩn từ 116 câu dài đã sinh:
0,19–0,32 giây mỗi âm tiết.

## Đã có

| Nhóm | Số tệp | Nội dung |
|---|---|---|
| `intro` | 114 | Lời dẫn mở đầu từng hoạt động |
| `alphabet` | 54 | 33 chữ cái (đọc theo **âm**: bờ, cờ, dờ…, có đủ ă â đ ê ô ơ ư), 10 chữ số, số 10–20 |
| `misc` | 23 | Lời khen, lời nhắc |
| `colors` | 11 | Tên màu |

## Còn thiếu

| Nhóm | Số tệp | Ghi chú |
|---|---|---|
| `words` | 564 | Từ vựng cho hoạt động Mở rộng vốn từ — cần dịch `content-vi.json` trước |
| `geography` | 129 | Tên nước và châu lục |

## Hai điểm cần chốt

1. **Giọng mẫu.** Đang dùng giọng của anh Tuấn (lấy từ NeoTeach). Với trẻ mẫu
   giáo, giọng cô giáo thường hợp hơn. Đổi giọng chỉ cần thay `--ref` rồi chạy
   lại — mất khoảng 10 phút cho cả 202 tệp.
2. **Cách đọc bảng chữ cái.** Đang đọc theo **âm** (bờ, cờ, dờ) như sách Tiếng
   Việt 1, chứ không theo **tên chữ** (bê, xê, dê). Nếu muốn đổi thì sửa
   `voices/manifest/alphabet.tsv` rồi sinh lại.
