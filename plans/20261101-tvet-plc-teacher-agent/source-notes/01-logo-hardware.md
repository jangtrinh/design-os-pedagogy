> **Ghi chú nguồn — Chương 1 — PLC LOGO: phần cứng, nối dây, mở rộng**
> Trích xuất tự động bởi agent tầng **Haiku** ngày 2026-11-01 từ tài liệu giảng dạy nội bộ "Chuyên đề Điều khiển lập trình cỡ nhỏ" (Trường CĐ Kiên Giang, 2025). Tài liệu gốc **không** lưu trong repo (lưu hành nội bộ). Số dòng (L…) tính theo chunk `A_ch1_logo_hardware.md (dòng 411–949 của bản chuyển đổi)` của bản chuyển .docx→Markdown bằng pandoc; ảnh `imageNNN` là ảnh nhúng trong .docx.
> Trạng thái: `unreviewed`. Mọi mục đánh dấu [SUY LUẬN]/[SUY RA] chưa được chạy thử trên thiết bị thật. Không dùng làm đáp án cho sinh viên trước khi giáo viên kiểm chứng trên kit.

## Đơn vị nội dung (one block per section 1.1, 1.1.1, 1.1.2, 1.2, 1.2.1, 1.2.2)

### LOGO-1.1 · Giới thiệu sơ lược ứng dụng · dòng 11–17
- Khái niệm: LOGO! là mô-đun logic (logic module) của Siemens cho ứng dụng đơn giản (băng tải, chiếu sáng, bơm, chuông báo); giảm chi phí, dây và không gian tủ (L13). Cấu hình bằng LOGO!Soft Comfort (L15). Mở rộng tới 24 DI, 16 DO, 8 AI, 2 AO; có AS-i và KNX (L17).
- Thuật ngữ: logic module ↔ mô-đun logic; expansion module ↔ module mở rộng.
- Hình: không có.
- Lưu ý: tài liệu không nói LOGO! không thay thế mạch dừng khẩn cấp.
- Bloom: Hiểu. Nêu được ba nhóm ứng dụng và lợi ích so với mạch relay cứng.

### LOGO-1.1.1 · Phân loại và kết cấu phần cứng · dòng 19–39
- Khái niệm: điện áp vào 12VDC, 24VAC, 24VDC, 230VAC; ngõ ra transistor hoặc relay (L21). Tích hợp nguồn, màn hình (loại có), cổng nối PC, hàm thời gian, tạo xung, đồng hồ ngày/tuần/tháng/năm, vùng nhớ trung gian (L23–39).
- Thuật ngữ: timer ↔ bộ định thời; real-time clock ↔ đồng hồ thời gian thực.
- Hình: không có.
- Lưu ý: cấp sai điện áp (230VAC vào model 24V) làm hỏng ngõ vào; kiểm tra nhãn trước khi cấp nguồn.
- Bloom: Nhớ. Liệt kê được bốn mức điện áp vào và các chức năng tích hợp.

### LOGO-1.1.2 · Ký hiệu trên vỏ và bảng thông số · dòng 41–337
- Khái niệm: 12 (12VDC); 24 (24VDC/24VAC); 230 (115/230VAC); R (relay, không R là transistor); O (không màn hình); L (dài, xem vấn đề 8); C (định thời 7 ngày); DM/AM (mở rộng số/tương tự) (L43–59).
- Bảng (L63–337): 12/24RC: 8 DI + 2 AI (0–10V), 4 relay. 24: 8 DI + 2 AI, 4 transistor 0.3A. 24RC: 6 DI, 20.4–28.8VAC, 4 relay. 230RC: 6 DI, 85–256VAC, 4 relay. Relay 10A thuần trở / 3A tải cảm. Cáp 1.5–2.5 mm²; 0 đến +55 °C; 72×90×55 mm.
- Thuật ngữ: resistive/inductive load ↔ tải thuần trở/tải cảm; external fuse ↔ cầu chì ngoài.
- Hình: không có (bảng).
- Lưu ý: relay của 12/24RC, 24RC, 230RC cần cầu chì ngoài (L238–247). Đọc nhầm R/không R dẫn đến chọn sai loại tải.
- Bloom: Hiểu. Giải mã được mã model và chọn model theo điện áp vào và loại tải.

### LOGO-1.2 · Sơ đồ nối dây PLC LOGO · dòng 339–340
- Khái niệm: chỉ là tiêu đề; nội dung ở 1.2.1 và 1.2.2.
- Thuật ngữ: wiring diagram ↔ sơ đồ nối dây; terminal ↔ đầu nối.
- Hình: không có.
- Lưu ý: thiếu trình tự đấu nối chung (ngắt nguồn, đo điện áp, đối chiếu sơ đồ).
- Bloom: Hiểu. Nêu được trình tự đấu nối an toàn.

### LOGO-1.2.1 · Ngõ vào, ngõ ra và kết nối theo chủng loại · dòng 341–375
- Khái niệm:
  - 230R/230RC: ngõ vào I, mức 0 ≤ 40V, mức 1 ≥ 79V, dòng tối đa 0.24 mA, thay đổi trạng thái tối thiểu 50 ms (L353–355).
  - 24/24R: mức 0 ≤ 5VDC, mức 1 ≥ 15VDC, dòng tối đa 3 mA (L357–359).
  - Relay: tiếp điểm cách ly với nguồn và ngõ vào, tải có thể dùng nguồn khác (L365). Transistor (24): 0.3A, dùng chung nguồn 24VDC, bảo vệ quá tải và ngắn mạch (L371).
- Thuật ngữ: isolation ↔ cách ly; common (M) ↔ cực chung; load ↔ tải.
- Hình:
  - image3.png (Hình 1.1): LOGO!230, L1 và N, công tắc nối từ L1 vào I1–I6.
  - image5.png (Hình 1.2): LOGO! relay, Q1–Q4 có hai đầu tiếp điểm, nguồn L1/L+ và N/M.
  - image6.png (Hình 1.3, ảnh đầu): LOGO!24 transistor, các Q dùng chung M, tải nối giữa Q1 và M.
  - image7.png (Hình 1.3, ảnh thứ hai): LOGO!24L với 6 ngõ ra Q1–Q6, không khớp "4 transistor" ở 1.1.2.
- Lưu ý an toàn/lỗi: không đưa 230V vào ngõ vào 24V hoặc ngược lại. Tải trên transistor vượt 0.3A gây quá tải, cần relay trung gian. Tải cảm cần dập xung (kiến thức bổ sung). Ngõ vào 230V dòng nhỏ nên đèn báo song song dễ gây đọc sai.
- Bloom: Vận dụng. Đấu nối đúng ngõ vào và ngõ ra relay/transistor theo Hình 1.1–1.3.

### LOGO-1.2.2 · Khả năng mở rộng · dòng 377–535
- Khái niệm:
  - Ghép module vào LOGO! cơ bản (L379). DM8 230R: 4 DI 120/230VAC, 4 relay 5A. DM8 24: 4 DI 24VDC, 4 transistor 0.3A. DM8 12/24VDC và DM8 24R: 4 DI, 4 relay 5A (L391–421).
  - AM2: 2 AI, 0–10V hoặc 0–20mA. AM2 PT100: 2 ngõ vào PT100, 2 hoặc 3 dây, −50 đến 200 °C (L427–439).
  - Địa chỉ (L445–535): cơ bản I1–I6/I8; DM8 lần lượt I9–I12, I13–I16, I17–I20, I21–I24; AM là AI3–AI8.
- Thuật ngữ: PT100 ↔ cảm biến nhiệt điện trở platin; addressing ↔ đánh địa chỉ.
- Hình: image10.png (Hình 1.4): các khối module mở rộng, mô tả theo chú thích (chưa mở ảnh).
- Lưu ý: relay module 5A thấp hơn relay cơ bản 10A. Tài liệu không nói module có cùng họ nguồn với LOGO! cơ bản hay không.
- Bloom: Vận dụng. Tính số module để đủ I/O yêu cầu (xem câu 8).

## Câu hỏi kiểm tra gợi ý — 8 questions

1. [LOGO-1.1.2 · Nhớ] Giải thích ký hiệu trong mã LOGO! 230RCo.
   Đáp án: 230 = nguồn và ngõ vào 115/230VAC; R = relay; C = định thời 7 ngày; o = không màn hình.

2. [LOGO-1.1.2 · Nhớ] LOGO! 24 có bao nhiêu ngõ ra, loại gì, dòng tối đa mỗi ngõ?
   Đáp án: 4 transistor, 0.3A mỗi ngõ (L204, L222).

3. [LOGO-1.1.2 · Hiểu] So sánh LOGO! 24RC và 230RC về số ngõ vào số và dòng relay.
   Đáp án: Cùng 6 ngõ vào số; relay 10A thuần trở, 3A tải cảm (L225–230).

4. [LOGO-1.2.1 · Hiểu — Hình 1.1, image3] Công tắc nối giữa L1 và I3 đóng. Mức logic của I3 là gì, vì sao, và N nối với đâu?
   Đáp án: Mức 1, vì điện áp I3–N khoảng 230V, lớn hơn ngưỡng 79V. N là dây trung tính, nối với cực N của nguồn để khép mạch.

5. [LOGO-1.2.1 · Vận dụng — Hình 1.3, image6] Tải nối giữa Q1 và M của LOGO!24 transistor. M là cực nào của nguồn? Tải 0.5A có ổn không?
   Đáp án: M là cực chung 0V của nguồn 24VDC. 0.5A vượt 0.3A, cần relay hoặc contactor trung gian.

6. [LOGO-1.2.1 · Vận dụng — Hình 1.2, image5] Dùng LOGO! relay đóng cắt contactor 230VAC và đèn 24VDC có dùng chung một nguồn không?
   Đáp án: Được, vì tiếp điểm cách ly với nguồn và ngõ vào (L365). Kiểm tra dòng cuộn contactor so với 2A (văn bản) hoặc 3A (bảng L230).

7. [LOGO-1.2.1 · Phân tích — chẩn đoán lỗi] LOGO!230RC: I3 đóng nhưng màn hình hiển thị I3 = 0. VOM kim đo giữa I3 và N được khoảng 230V. Nêu ba nguyên nhân và cách kiểm tra.
   Đáp án mẫu: (a) Điện áp giả do VOM trở kháng cao; đo lại có tải (đèn thử hoặc điện trở), nếu điện áp sụt thì không có điện áp thật. (b) Đầu nối I3 lỏng hoặc đấu nhầm; siết lại và đo thông mạch khi công tắc đóng. (c) Chương trình không dùng I3 hoặc gán sai địa chỉ; kiểm tra trong LOGO!Soft Comfort. 230V đã vượt ngưỡng nên không phải do ngưỡng.

8. [LOGO-1.2.2 · Vận dụng] LOGO! 230RC cơ bản (6 DI, 4 relay) cần thêm 10 ngõ vào 230VAC và 6 ngõ ra relay. Chọn module và số lượng?
   Đáp án: DM8 230R. 10 DI cần 3 module (12 DI); 6 DO cần 2 module (8 DO). Tổng sau mở rộng: 18 DI, 16 DO. Số module tối đa phải kiểm tra theo catalogue.

## Vấn đề của tài liệu

1. Số I/O (L17): "16 đầu ra số" không khớp cấu hình 4 ngõ ra cơ bản + 4 DM8 × 4 = 20. "2 đầu ra tương tự" không có module ngõ ra tương tự nào ở 1.2.2.
2. Dòng relay mâu thuẫn: 10A/3A (L218–230) với 8A/2A (L365).
3. 230RC mâu thuẫn: 85–256VAC (L142) với 85–264V (L353). Mức 0/1 là "max 40VDC / min 79VDC" (L159, L176) nhưng văn bản ghi 40VAC / 79VAC (L355). Dòng vào 0.05 mA (L193) với 0.24 mA (L355).
4. Ngưỡng 24: bảng mức 1 min 12VDC (L170, L173), văn bản 15VDC (L359).
5. Sai khái niệm (L355, L359): "ngõ ra ở mức 1 khi công tắc đóng" phải là ngõ vào.
6. Lẫn tên model: văn bản "24R", "230R" (L353, L357, L365), bảng "24RC", "230RC". "12/24Rco" (L77) phải là 12/24RCo.
7. Đơn vị sai: "Tổn hao năng lượng 0.2–0.5V" (L277) phải là W.
8. "L: I/O gấp đôi" (L53) không khớp image7 (6 ngõ ra, không phải 8). Cần làm rõ.
9. "8/10 giờ" (L292–299): không rõ là điển hình hay tối thiểu.
10. Công thức vỡ ở L357 (`4 [ảnh image4.wmf] 0.3A`): ký hiệu nhân không hiển thị.
11. "Không cần dây nối đất" (L343): nguy hiểm nếu dạy như quy tắc chung. Cần đối chiếu manual về cực nối đất chức năng (FE).
12. Bảng 1.2.2: bảng "không có ngõ vào tương tự" (L489–535) gần như giống bảng trên, vẫn có AI3–AI8, câu mô tả lặp (L443, L491). Ô "AM8" (L480, L528) không khớp "AM2" (L427).
13. "Số đầu vào liên tục" (L97–98) không nói rõ có trùng với 8 ngõ vào số hay không.
14. DM8 230R ghi "120/230 VAC/DC" (L393), trong khi LOGO! 230 ghi 115/230 VAC (L47, L125).
15. Thiếu thế hệ và mã đặt hàng (0BA6, 0BA7, 0BA8 hay hiện hành) và phiên bản Soft Comfort. Không rõ bảng áp dụng cho thế hệ nào, đây là rủi ro lớn nhất khi dạy.
16. Thiếu: sơ đồ nguồn theo model, giá trị cầu chì ngoài (L238), số module tối đa, thứ tự ghép, đánh địa chỉ ngõ ra mở rộng, định thời theo năm (L35).
17. Lỗi gõ: "Lọai" (L27, L53), "digil" (L57), "tảI" (L219), "năm,." (L35), L15 thiếu động từ, "oC" (L316–317). Chú thích "<!-- -->" (L389, L425) làm hỏng danh sách.
