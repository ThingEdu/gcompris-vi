#!/bin/bash
# Mở quyền cài tệp .rcc vào GCompris trên NEO One mà không phải gõ mật khẩu mỗi lần.
#
# CHẠY MỘT LẦN DUY NHẤT, TRÊN CHÍNH MÁY NEO ONE (hoặc qua ssh có bàn phím để
# nhập mật khẩu). Sau đó mọi lần triển khai đều tự động được.
#
#   ssh neo@192.168.1.28 'bash -s' < deploy/mo_quyen_cai_rcc.sh
#
# Vì sao cần: GCompris nạp hoạt động từ .rcc trong /usr/share/gcompris-qt/rcc/,
# mà thư mục đó của root. Đã thử đường không cần quyền root — đặt .rcc vào
# ~/.local/share/GCompris/rcc/ — và chứng minh được GCompris KHÔNG đọc chỗ đó.
#
# Mở quyền tới đâu: KHÔNG mở sudo toàn phần. Chỉ cho phép chạy đúng một script
# do chính tệp này tạo ra, và script đó chỉ biết làm một việc — chép tệp .rcc
# từ /tmp vào thư mục tài nguyên GCompris, có sao lưu bản gốc lần đầu. Script
# từ chối mọi đường dẫn khác, từ chối cả liên kết mềm (tránh trò trỏ /tmp/x.rcc
# sang /etc/shadow rồi chép ra chỗ ai cũng đọc được).
set -e

echo "== 1/3 tạo script cài đặt =="
sudo tee /usr/local/sbin/cai-rcc-gcompris >/dev/null <<'HET'
#!/bin/bash
# Chép tệp .rcc vào thư mục tài nguyên GCompris. Chỉ nhận /tmp/<tên>.rcc.
set -e
DICH=/usr/share/gcompris-qt/rcc
[ $# -gt 0 ] || { echo "dùng: cai-rcc-gcompris /tmp/<tên>.rcc ..." >&2; exit 1; }
for t in "$@"; do
    case "$t" in
        /tmp/*.rcc) ;;
        *) echo "từ chối: chỉ nhận /tmp/*.rcc, không nhận $t" >&2; exit 1 ;;
    esac
    [ -f "$t" ] || { echo "không thấy tệp $t" >&2; exit 1; }
    [ -L "$t" ] && { echo "từ chối: $t là liên kết mềm" >&2; exit 1; }
    ten=$(basename "$t")
    if [ -f "$DICH/$ten" ] && [ ! -f "$DICH/$ten.orig" ]; then
        cp "$DICH/$ten" "$DICH/$ten.orig"
        echo "   (đã giữ bản gốc $DICH/$ten.orig)"
    fi
    cp "$t" "$DICH/$ten"
    chmod 644 "$DICH/$ten"
    echo "-> $DICH/$ten"
done
HET
sudo chmod 755 /usr/local/sbin/cai-rcc-gcompris

echo "== 2/3 cho phép chạy script đó không cần mật khẩu =="
echo 'neo ALL=(root) NOPASSWD: /usr/local/sbin/cai-rcc-gcompris' \
    | sudo tee /etc/sudoers.d/gcompris-rcc >/dev/null
sudo chmod 440 /etc/sudoers.d/gcompris-rcc

echo "== 3/3 kiểm lại =="
sudo visudo -c
sudo -n /usr/local/sbin/cai-rcc-gcompris 2>&1 | head -1
echo
echo "XONG. Từ nay chép .rcc bằng:"
echo "    scp <tệp>.rcc neo@<ip>:/tmp/"
echo "    ssh neo@<ip> 'sudo cai-rcc-gcompris /tmp/<tệp>.rcc'"
echo
echo "Gỡ quyền này về sau:"
echo "    sudo rm /etc/sudoers.d/gcompris-rcc /usr/local/sbin/cai-rcc-gcompris"
