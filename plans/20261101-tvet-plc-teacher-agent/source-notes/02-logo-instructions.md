> **Ghi chú nguồn — Chương 2.1 — Danh mục lệnh LOGO (Co/BF/SF)**
> Trích xuất tự động bởi agent tầng **Haiku** ngày 2026-11-01 từ tài liệu giảng dạy nội bộ "Chuyên đề Điều khiển lập trình cỡ nhỏ" (Trường CĐ Kiên Giang, 2025). Tài liệu gốc **không** lưu trong repo (lưu hành nội bộ). Số dòng (L…) tính theo chunk `B_ch2_logo_instructions.md (dòng 950–2154)` của bản chuyển .docx→Markdown bằng pandoc; ảnh `imageNNN` là ảnh nhúng trong .docx.
> Trạng thái: `unreviewed`. Mọi mục đánh dấu [SUY LUẬN]/[SUY RA] chưa được chạy thử trên thiết bị thật. Không dùng làm đáp án cho sinh viên trước khi giáo viên kiểm chứng trên kit.

# Chương 2 — Chỉ dẫn LOGO! (trích xuất có cấu trúc)

Nguồn: chunk `B_ch2_logo_instructions.md.` Số trong ngoặc là dòng của file nguồn. Đã mở 5 ảnh: image31, 32, 33, 34, 38 (bảng tổng hợp SF). Tên EN lấy theo thuật ngữ LOGO! Manual; đánh dấu * là không có trong chunk, cần đối chiếu.

## Bảng Co (connectors)

| Ký hiệu | Ý nghĩa | Ghi chú |
|---|---|---|
| I1, I2, … | Ngõ vào số | Số lượng theo model, không nêu (27) |
| AI1, AI2 | Ngõ vào analog, lập trình trên I7, I8 | Chỉ LOGO! 24, 24o, 12/24RC, 12/24RCo (29) |
| Q1…Q16 | Ngõ ra số | (31) |
| AQ1, AQ2 | Ngõ ra analog | Tối đa 2; không nêu model hỗ trợ (33) |
| M, M1… | Bit nhớ trung gian | Số lượng không nêu (17) |
| M8 | Cờ start-up: = 1 trong chu kỳ quét đầu, sau đó = 0; dùng được như bit nhớ | (35) |
| S1…S8 | Thanh ghi dịch bit | Chỉ đọc; chỉ đổi bằng SF Shift register (37) |
| hi / lo | Hằng 1 / 0 | (39–41) |
| x | Kết nối hở | AND: x = 1; OR, NOR, XOR: x = 0 (43, 62, 80, 86, 92) |

## Bảng BF

| Tên | Ký hiệu khối | Logic / bảng chân trị | Ví dụ |
|---|---|---|---|
| AND | AND | Q = 1 khi tất cả ngõ vào = 1; tối đa 4 ngõ vào (53, 62) | Điều kiện đồng thời: nút Start AND cảm biến an toàn |
| OR | OR | Q = 1 khi ít nhất 1 ngõ vào = 1 (80) | Hai nút nhấn song song |
| NOT | NOT | Q = đảo I; phần mô tả và bảng bị thiếu (100–102) | Đảo tiếp điểm thường đóng |
| NAND | NAND | Q = 0 chỉ khi tất cả = 1 (68) | Báo khi chưa đủ điều kiện |
| NOR | NOR | Q = 1 chỉ khi tất cả = 0 (86) | Cho phép chạy khi không có tín hiệu dừng |
| XOR | XOR | Q = 1 khi 2 ngõ vào khác nhau (92) | Công tắc 2 vị trí, đảo chiều |
| AND cạnh | AND (edge) | Q = 1 đúng 1 chu kỳ quét khi tổ hợp chuyển 0→1 (62) | Đếm đúng 1 lần mỗi lần nhấn |
| NAND cạnh | NAND (edge) | Q = 1 đúng 1 chu kỳ khi NAND chuyển 0→1, tức một ngõ vào vừa về 0 (72) | Phát hiện vật vừa rời cảm biến |

## Bảng SF (có mô tả trong chunk)

| Tên VI | Tên EN | Ngõ vào | Tham số | Hành vi | Ứng dụng | Dòng nguồn |
|---|---|---|---|---|---|---|
| On-delay | On-delay | Trg | T, Rem | Trg↑ bắt đầu đếm Ta; Q = 1 khi Ta = T nếu Trg còn 1; Trg↓ trước T → Q = 0 và reset Ta. Rem = Off: mất nguồn reset Q, Ta. | Trì hoãn khởi động; Y→Δ | 142–173 |
| Off-delay | Off-delay | Trg, R | T, Rem | Trg↑ → Q = 1 ngay; Trg↓ bắt đầu đếm; Q = 0 khi Ta = T; R↑ reset Q, Ta. Xem mục Vấn đề về Trg↑ khi đang đếm. | Giữ cửa mở; băng tải chạy thêm T | 221–237 |
| On/Off-delay | On/Off-delay | Trg | TH (trễ bật), TL (trễ tắt), Rem | Trg↑ đếm TH → Q = 1 nếu Trg vẫn 1; Trg↓ đếm TL → Q = 0 nếu Trg vẫn 0; chuyển ngược thì reset đếm. | Cảm biến có trễ hai chiều | 269–298 |
| Retentive on-delay (On-delay có nhớ) | Retentive on-delay | Trg, R | T, Rem | Trg↑ đếm Ta; khi Ta = T thì Q = 1 và giữ dù Trg xuống; chỉ R↑ reset Q, Ta. | Báo động cần reset tay | 300–368 |
| Wiping relay (Relay xung có trì hoãn) | Wiping relay* | Trg | T, Rem | Trg↑ → Q = 1 ngay; Q = 0 khi hết T (Trg còn 1) hoặc khi Trg↓ trước T. Q là xung dài tối đa T. | Đèn/còi báo đúng T giây | 370–428 |
| Relay thời gian lấy cạnh xung lên | Edge triggered wiping relay* | Trg, R | TH, TL, N, Rem | Trg↑ → Q = 0 trong TL, rồi Q = 1 trong TH; lặp N xung. Trg↑ giữa chu trình → chạy lại. R reset. | Tạo N xung sau một lệnh | 430–501 |
| Bộ phát xung không đồng bộ | Asynchronous pulse generator | En, INV | TH, TL | En = 1: Q lặp chu kỳ TH/TL; INV = 1 đảo pha. Trạng thái Q khi En = 0 không nêu. | Nhấp nháy đèn vàng | 503–568 |
| Bộ phát xung ngẫu nhiên | Random generator | En | TH, TL | En↑: trễ ngẫu nhiên trong [0, TH] rồi Q = 1; En↓: trễ ngẫu nhiên trong [0, TL] rồi Q = 0; En↑ trước khi hết trễ tắt thì reset. | Mô phỏng người ở nhà | 570–619 |
| Công tắc đèn cầu thang | Staircase lighting switch | Trg | T, T!, T!L | Trg↑ → Q = 1 ngay; Trg↓ đếm T rồi Q = 0; trong khoảng (T−T!; T−T!+T!L) Q tắt nhấp như cảnh báo; kích lại khởi động lại T. | Đèn hành lang tự tắt | 621–687 |
| Công tắc đa chức năng | Multiple function switch | Trg, R | T, TL, T!, T!L, Rem | Trg↑ → Q = 1; giữ Trg > TL (khi Q = 0) → Q bật liên tục; nhấn ngắn < TL → Q = 1 rồi tắt sau T. Cách thoát chế độ liên tục không nêu. | Một nút: nhấn ngắn / nhấn giữ | 689–764 |
| Ngày giờ trong tuần | Weekly timer | Kênh No1–No3 | ON/OFF theo ngày, 3 kênh | Q = 1 trong khoảng ON của kênh. Khi các kênh chồng nhau, kênh số cao hơn quyết định: No3 > No2 > No1. | Lịch bật/tắt theo giờ và ngày | 766–827 |
| Ngày trong năm | Yearly timer | No | ON, OFF theo MM/DD | Q = 1 khi ngày hiện tại nằm trong khoảng ON–OFF. Trường hợp khoảng vượt cuối năm không nêu. | Vận hành theo mùa | 829–881 |
| Bộ đếm lên xuống | Up/down counter | R, Cnt, Dir | On, Off (0–999999) | Mỗi cạnh Cnt ±1 (Dir 0 = lên, 1 = xuống); R↑ → đếm = 0. On ≥ Off: Q = 1 khi Cnt ≥ On, Q = 0 khi Cnt < Off. On < Off: Q = 1 khi On < Cnt < Off. Cnt: I5/I6 tới 2 kHz, các ngõ khác "trong vòng 4 Hz". | Đếm sản phẩm, báo đầy | 883–967; 923–924 |
| Bộ đếm giờ | Hour counter | R, En, Ral | MI (0–9999 h), OT (tối đa 99999 h), MN | En = 1: MN đếm xuống; MN = 0 → Q = 1. R↑: Q = 0, MN = MI, OT giữ. Ral↑: Q = 0, MN = MI, OT = 0. | Nhắc bảo trì theo giờ chạy | 969–1068 |
| Bộ chốt relay | Latching relay | S, R | Không | S↑ → Q = 1 và giữ; R↑ → Q = 0; S = R = 1 → Q = 0 (R ưu tiên). | Start/stop; dừng ưu tiên | 1070–1126 |
| Bộ relay xung | Pulse relay | Trg, S, R | RS (R ưu tiên) hoặc SR (S ưu tiên) | Mỗi cạnh Trg↑ đảo Q; S = 1 → Q = 1; R = 1 → Q = 0; khi S hoặc R = 1 thì Trg bị bỏ qua. | Nút bật/tắt luân phiên | 1128–1204 |

Chỉ có trong hình 31–38, không có mô tả trong chunk: Bộ phát xung theo tần số*, theo analog (ngưỡng và sai lệch)*, Bộ so sánh analog*, Bộ chọn giá trị analog*, Hàm dốc*, PI*, Analog amplifier*, Bộ tạo thông báo*, Bộ khoá mềm*, Thanh ghi dịch bit* (dòng 37 có nhắc).

## Thứ tự dạy đề xuất

1. **Co và BF cơ bản** (AND, OR, NOT, NAND, NOR, XOR, hi/lo, x). Nền của mọi sơ đồ; không đọc được block khác nếu chưa hiểu tổ hợp logic.
2. **Cạnh và bộ nhớ** (AND/NAND cạnh, Latching relay, Pulse relay, RS/SR). Tự giữ và khóa liên động dựa trên khái niệm mức, cạnh và ưu tiên S/R.
3. **Timer cơ bản** (On-delay, Off-delay, On/Off-delay, Rem). Cần để hiểu Trg, T, Ta, Q và tác động của mất nguồn trước khi học các biến thể.
4. **Timer mở rộng và tạo xung** (Retentive on-delay, Wiping, Edge wiping, Async pulse, Random, Staircase, Multi-function). Đều là biến thể của chu kỳ Ta ở bước 3.
5. **Đếm và lịch** (Up/down, Hour counter, Weekly, Yearly). Cần quen khái niệm ngưỡng và reset; lịch là phần trừu tượng nhất.
6. **Analog, thông báo, softkey, shift register** (chỉ có tên trong hình). Không thuộc chunk này và không cần cho 4 lab; dạy sau hoặc bỏ qua.

Bắt buộc cho 4 lab (BB = bắt buộc, KN = khuyến nghị, — = không cần):

| Hàm | Động cơ (start/stop, Y-Δ, đảo chiều) | Đèn giao thông | Cửa tự động | Băng tải |
|---|---|---|---|---|
| AND / OR / NOT | BB (tự giữ, khóa liên động) | BB | BB | BB |
| AND / NAND cạnh | KN | — | KN (cảm biến) | — |
| Latching relay | KN (start/stop) | — | — | KN |
| On-delay | BB (chuyển Y→Δ) | BB (chuyển pha; hoặc chuỗi on-delay) | KN | KN |
| Off-delay | — | — | BB (giữ cửa mở T) | BB (chạy trễ) |
| Wiping relay | — | — | KN (đèn báo) | — |
| Async pulse | — | KN (nhấp nháy) | — | — |
| Staircase | — | — | KN | — |
| Up/down counter | — | — | — | KN (đếm sản phẩm) |
| Hour counter | KN (bảo trì) | — | — | KN |

Các hàm còn lại không bắt buộc cho 4 lab. Cửa có thể dùng On-delay kết hợp BF thay Off-delay; đèn giao thông cần một trong hai: chuỗi on-delay hoặc Async pulse.

## Hiểu lầm thường gặp

1. **Rem chỉ giữ ngõ ra.** Probe: On-delay T = 10 s, Rem = On. Trg = 1 đếm được 6 s, mất điện 3 s, có điện lại và Trg vẫn = 1. Q bật sau bao lâu? (Đáp: 4 s nếu Ta được giữ; dòng 120 chỉ nói về ngõ ra, nên cần làm rõ.)
2. **Trg tạm ngắt làm timer "tạm dừng" thay vì reset.** Probe: On-delay T = 10 s. Trg = 1 trong 6 s, Trg = 0 trong 1 s, rồi Trg = 1 lại. Q bật sau bao lâu kể từ lần lên thứ hai? (Đáp: 10 s; dòng 173.)
3. **Retentive on-delay: Trg xuống làm Q tắt.** Probe: Trg giữ 1 đủ T rồi về 0. Sau đó R xung 1 rồi 0 trong khi Trg vẫn = 1. Q tắt khi nào, bật lại khi nào? (Đáp: Q vẫn = 1 khi Trg xuống; R = 1 làm Q = 0; sau khi R về 0, Q không bật lại vì không có cạnh Trg↑ mới; dòng 364–366.)
4. **Cạnh và mức: AND cạnh giữ được nhiều chu kỳ.** Probe: 4 ngõ vào AND giữ mức 1 trong 5 s. Ngõ ra AND cạnh bằng 1 bao nhiêu chu kỳ quét? (Đáp: 1; dòng 62.)
5. **Off-delay đếm từ cạnh lên.** Probe: Off-delay T = 5 s. Trg lên lúc 0, xuống lúc 2 s. Q tắt lúc nào? (Đáp: 7 s; T tính từ cạnh xuống, dòng 221–233.)
6. **Ưu tiên S/R bị hiểu là "ai đến trước thắng".** Probe: Latching relay có S = R = 1. Pulse relay với Par = RS và với Par = SR, cùng S = R = 1. Q bằng bao nhiêu? (Đáp: 0; 0; 1; dòng 1126, 1182, 1204.)
7. **Kênh lịch tuần được cộng OR.** Probe: No1 ON 08:00, OFF 17:00. No3 ON 12:00, OFF 13:00. Lúc 13:30 Q bằng bao nhiêu? (Đáp: 0; No3 ưu tiên và đang OFF, dòng 827.)
8. **Reset bộ đếm giờ xóa tổng giờ.** Probe: MI = 100 h, OT = 40 h, đã chạy thêm 30 h. Sau R↑, OT và MN bằng bao nhiêu? Sau đó Ral↑, OT bằng bao nhiêu? (Đáp: OT = 70, MN = 100; sau Ral, OT = 0; dòng 1016–1019, 1056–1058.)

## Vấn đề của tài liệu

- **Tên nhóm sai:** dòng 19 ghi "GF" trong khi tiêu đề là BF (47). Dòng 21 ghi "SF: danh sách các hàm cơ bản" nhưng SF là hàm đặc biệt (104).
- **Bảng chân trị bị mất:** các dòng 57, 70, 84, 90, 98 có tiêu đề "Bảng logic" nhưng không có nội dung. NOT (100–102) không có mô tả. Các ảnh tương ứng dung lượng dưới 300 byte, khả năng là placeholder (chưa kiểm tra bằng ảnh do đã dùng hết 5 ảnh).
- **Mâu thuẫn Off-delay:** dòng 233 nói Ta khởi động lại khi Trg xuống 0, còn dòng 235 nói cạnh lên Trg reset Ta. Hai câu không thể cùng đúng; cần đối chiếu manual.
- **Mô tả trùng lặp, sai:** dòng 269 lặp câu "delay-on"; vế thứ hai phải là delay-off TL (theo 286, 296).
- **Nhãn sai:** dòng 1060 dùng "Q0:R+En" cho cả hai trường hợp; trường hợp đầu (R hoặc Ral) phải là "Q0:R" (theo 1040).
- **Rem và retentive:** dòng 300 đặt hàm "On-delay có nhớ" và hình 31 có cột Rem cho hàm này, nhưng dòng 368 vẫn ghi "nếu retentive không được chọn thì reset khi mất nguồn". Không rõ tham số Rem có áp dụng cho hàm có tên "có nhớ" hay không.
- **Thiếu hành vi:** dòng 758 không nói cách thoát chế độ giữ liên tục của công tắc đa chức năng. Dòng 963–967 không nói Q khi Off ≤ Cnt < On, và không nói biên (Cnt = On hoặc Off) khi On < Off. Dòng 568 nói "thời gian Ta bị reset" cho bộ phát xung không đồng bộ, nhưng hàm này không có Ta; Q khi En = 0 cũng không nêu.
- **Ký hiệu có thể trùng:** dòng 192 và 454 dùng cùng file image43 (Off-delay và Edge wiping); dòng 394 và 594 dùng cùng image49 (Wiping relay và Random generator). Có thể là lỗi ký hiệu; chưa xác minh bằng ảnh.
- **Tần số và kênh:** dòng 923 ghi "2Khz" (sai đơn vị); dòng 924 "trong vòng 4Hz" không rõ nghĩa. Dòng 29 và 923 cùng áp dụng cho các model 12/24RC và 24/24o; cần kiểm tra datasheet số kênh I5/I6 (nhanh) và I7/I8 (analog).
- **Thế hệ:** chunk không nêu thế hệ LOGO! hay firmware. Tham số Ral, Par, RS/SR, Dir gợi ý LOGO! 8, chưa xác nhận. Không nêu model nào có AQ (33).
- **Thiếu nội dung:** hơn 10 hàm trong hình 31–38 không có mô tả. Dòng 62 chỉ nói cạnh cho AND và NAND, không nói OR, NOR, XOR.
- **Chính tả:** "Srt up" (35), "đươc" (nhiều dòng, 173–764), "Định gian" (859), "khời" (1068), "đượs" (1116).
