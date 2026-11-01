# Nghiên cứu nguồn: mô đun "Điều khiển lập trình cỡ nhỏ" (PLC LOGO! / ZEN)

Ngày: 2026-11-01. Trạng thái: `unreviewed`. Đây là bản trích xuất và đối chiếu do AI làm. Chưa có chuyên gia PLC hay giáo viên phụ trách thẩm định.

## 1. Bộ nguồn và vai trò

| File tải lên | Loại | Vai trò đối với teacher agent | Ghi chú |
|---|---|---|---|
| `LichTrinh_DKLTCN_CD9_K5.doc` | Lịch trình giảng dạy HK I 2026–2027, lớp KTML&ĐHKK CĐ9+ K5 | **Đầu vào điều khiển thời gian** (time slots) | Đã số hóa thành [`schedule-cd9-k5.json`](schedule-cd9-k5.json) |
| `GA20.docx` | Giáo án số 20, môn Kỹ thuật lạnh (Gia công ống đồng – hàn nối ống), 4 giờ | **Mẫu biểu đầu ra** (form giáo án tích hợp của trường) | Nội dung thuộc môn khác. Dùng làm khuôn định dạng, không dùng làm nội dung |
| `TaiLieuGiangDay_DieuKhienLapTrinhCoNho.docx` | Tài liệu giảng dạy nội bộ, 6 chương, ~80 trang, 146 ảnh | **Nguồn nội dung** (content units) | Bản trích theo chương ở [`source-notes/`](source-notes/) |

Tài liệu gốc ghi "lưu hành nội bộ", lịch trình và giáo án có tên giáo viên. Vì vậy repo **không** lưu file gốc hay tên người, chỉ lưu bản phân tích, số liệu cấu trúc và vị trí trích dẫn.

### Cách xử lý (điều phối nhiều tầng model)

| Bước | Thực hiện | Lý do chọn tầng |
|---|---|---|
| Chuyển .doc/.docx sang Markdown và tách ảnh | `soffice` + `pandoc`, không gọi model | Việc tất định |
| Đọc lịch trình và mẫu GA20 (~21 KB) | Opus đọc trực tiếp | Ngắn. Cần hiểu cấu trúc để thiết kế schema |
| Ch.1 phần cứng LOGO; Ch.2.1 danh mục lệnh | 2 agent **Haiku** chạy song song | Trích xuất có cấu trúc, ít suy luận |
| Ch.2.2–3 phần mềm và 4 bài lab LOGO; Ch.4–6 ZEN | 2 agent **Sonnet** chạy song song, đọc 16 và ~27 ảnh | Phải đọc sơ đồ, suy luận logic chương trình, đánh giá sư phạm |
| Khảo sát kiến trúc repo `design-os-pedagogy` | 1 agent **Sonnet** (Explore) | Đọc nhiều file, chỉ cần kết luận |
| Kiểm chứng điểm then chốt, đối chiếu chéo, thiết kế agent | **Opus** | Quyết định kiến trúc và đánh đổi |

Lượng token của subagent: Haiku ~148k + ~164k; Sonnet ~111k + ~137k + ~120k. Phần Opus chỉ đọc kết quả đã nén (~11k từ) cùng hai file ngắn.

## 2. Lịch trình giảng dạy

- 15 tuần, từ thứ Hai 07/09/2026 đến thứ Bảy 19/12/2026. Mỗi tuần một buổi 4 giờ. Tổng 60 giờ, gồm **14 LT + 46 TH** (đã kiểm bằng script khi tạo JSON).
- Đơn vị lịch là "Bài 1–9", còn giáo trình đánh số "Chương 1–6". Ánh xạ:

| Lịch | Giáo trình | Tuần | LT/TH theo lịch | LT/TH theo chương trình mô đun |
|---|---|---|---|---|
| Giới thiệu mô đun + Bài 1 | Mở đầu + Ch.1 | 1 | 2/2 | 1/3 |
| Bài 2 | Ch.2 | 2 | 2/2 | 1/3 |
| Bài 3 Động cơ | 3.1 | 3–4 | 2/6 | 2/6 |
| Bài 4 Đèn giao thông | 3.2 | 5–6 | 2/6 | 2/6 |
| Bài 5 Cửa tự động | 3.3 | 7–8 | **1/7** | 2/6 |
| Bài 6 Băng tải + **KTĐK 1** | 3.4 | 9–10 | **1/7** | 2/6 |
| Bài 7 | Ch.4 | 11 | 1/3 | 1/3 |
| Bài 8 | Ch.5 | 12 | 1/3 | 1/3 |
| Bài 9 (9.1–9.3) + **KTĐK 2** | 6.1–6.3 (**không có 6.4**) | 13–14 | 2/6 | 2/6 |
| Thi kết thúc mô đun | — | 15 | 0/4 (ghi vào cột TH) | 4 giờ cột Kiểm tra |

Những điểm agent phải xử lý:
1. **Giờ từng bài không khớp chương trình**, dù tổng LT vẫn là 14. Lịch là ràng buộc cứng, chương trình là chuẩn tham chiếu. Agent nên báo chênh lệch thay vì tự sửa.
2. **Hai bài kiểm tra định kỳ không có thời lượng riêng.** Chúng nằm trong 4 giờ TH của tuần 10 và 14. Giáo án tuần đó phải cắt bớt phút thực hành, và agent phải hỏi giáo viên hình thức và thời lượng.
3. **Bài 6.4 (băng tải trên ZEN) bị bỏ** khỏi lịch. Đây là ví dụ thực tế cho việc lịch quyết định phạm vi.
4. Có lỗi chính tả ("cở nhỏ", "đóng mở của"). Thiết bị chia làm hai cụm: LOGO!Soft Comfort V8.4 + kit LOGO! (tuần 1–10) và ZEN-SOFT + kit ZEN (tuần 11–14).
5. Lịch không ghi ngày nghỉ hay buổi học bù. Trong khoảng 09–12/2026 không có ngày nghỉ lễ quốc gia, nhưng nghỉ đột xuất thì cần cơ chế `exceptions`.

## 3. Mẫu giáo án GA20

Phần tô vàng trong file gốc là **trường biến**. Phần còn lại là khung cố định:

```
Header : GIÁO ÁN SỐ {n} | Thời gian thực hiện {giờ} | Bài học trước: {tên} | Thực hiện từ {ngày} đến {ngày}
Tên bài: Bài {x}: {tên} (tt) / {mục}
MỤC TIÊU CỦA BÀI: "Sau khi học xong bài này người học có khả năng:" + 3–5 gạch đầu dòng (kiến thức / kỹ năng / thái độ–an toàn)
ĐỒ DÙNG VÀ TRANG THIẾT BỊ DẠY HỌC
HÌNH THỨC TỔ CHỨC DẠY HỌC          (ví dụ "Tập trung lớp hướng dẫn ban đầu; Chia nhóm thực tập")
I.  ỔN ĐỊNH LỚP HỌC — {phút}       (nhắc nội quy xưởng, kiểm tra bài cũ)
II. THỰC HIỆN BÀI HỌC — bảng: TT | NỘI DUNG | HĐ GIÁO VIÊN | HĐ HỌC SINH | THỜI GIAN
    1 Dẫn nhập · 2 Giới thiệu chủ đề · 3 Giải quyết vấn đề (A. Mục tiêu, B. Nội dung: kiến thức liên quan,
    an toàn, chuẩn bị, các bước công việc, sai hỏng & khắc phục, yêu cầu bài tập, phân nhóm, theo dõi)
    4 Kết thúc vấn đề (chấm sản phẩm, rút kinh nghiệm, giao bài, vệ sinh xưởng) · 5 Hướng dẫn tự học
III. RÚT KINH NGHIỆM TỔ CHỨC THỰC HIỆN  (để trống, GV ghi sau buổi)
Chữ ký: Trưởng bộ môn | Ngày … GIÁO VIÊN
```

- **Ngân sách phút** của GA20 là 10 (ổn định) + 3 + 2 + 205 + 15 + 5 = **240 phút**, đúng 4 giờ. Đây là một bất biến kiểm được tự động.
- Mỗi tuần một giáo án được đánh số liên tục. "Bài học trước" lấy từ buổi liền trước, nên khi xếp lại lịch thì trường này phải được tính lại.
- **Điểm yếu sư phạm của mẫu:** cột "Hoạt động học sinh" lặp lại "Lắng nghe, ghi nhận / Tham gia trả lời câu hỏi / Bổ sung" ~10 lần. 205 phút "Giải quyết vấn đề" là một khối duy nhất, không tách làm mẫu, thực hành có hướng dẫn và thực hành độc lập. Agent nên giữ đúng khung biểu mẫu, nhưng chia khối này thành các bước "GV làm mẫu → cả lớp cùng làm → SV tự làm" (`50-practice-library/lesson-patterns/explicit-instruction-i-we-you.md`), kèm câu hỏi kiểm tra hiểu và tiêu chí chấm.
- Mục "III. Rút kinh nghiệm" là **kênh phản hồi tự nhiên** để agent điều chỉnh các buổi sau.

## 4. Giáo trình: mức đầy đủ theo bài

| Bài (lịch) | Nội dung có trong giáo trình | Đầy đủ (1–5) | Thiếu hoặc sai đáng kể |
|---|---|---|---|
| B1 LOGO phần cứng | Ký hiệu model, bảng thông số, sơ đồ nối dây I/O relay và transistor, module mở rộng, địa chỉ | 3.5 | Mâu thuẫn số liệu: relay 10A/3A và 8A/2A; dòng vào 230RC 0.05 và 0.24 mA; ngưỡng 12 và 15 VDC; "16 DO" và 20. Không ghi thế hệ 0BA6/0BA8. Có câu "không cần dây nối đất" nguy hiểm |
| B2 Lệnh LOGO | Co, BF, 16 SF có mô tả, phần mềm V7→V8.1, thao tác phím, 1 ví dụ OR | 3 | Mất bảng chân trị BF. Off-delay mô tả mâu thuẫn. Hơn 10 SF chỉ có tên. Ảnh phần mềm từ V5.0/XP, lịch dạy V8.4. Thiếu nạp chương trình PC→LOGO. Ký hiệu phím mất khi chuyển đổi |
| B3–B6 Lab LOGO | Chỉ có "Kiến thức liên quan" và "Yêu cầu bài tập" | **1.5–2** | **Sơ đồ kết nối và "Lập trình theo yêu cầu" đều là dòng chấm trống** (đã kiểm trực tiếp). Hình duy nhất ở 3.1.3 là hình ví dụ OR, không phải mạch động cơ, và vẽ model 12/24RC (DC) nối L1/N. Đề 3.2 cần 6 ngõ ra, model cơ bản chỉ có 4 |
| B7 ZEN phần cứng | Ứng dụng, lắp ray DIN, nối dây AC/DC | 3 | Mã model chỉ có trong ảnh (ZEN-10C1AR-A, 8EAR). Lỗi đơn vị "6.5 Hz" |
| B8 Lệnh ZEN | Loại bit I/Q/M/H/T/#/@/*/C, kiểu cuộn dây S/R/A, phần mềm, nhập ladder bằng phím | 3 | Không có giản đồ thời gian X/N/O/F. Không hướng dẫn đặt timer, counter. Bảng ghi "T0–T5" cho 8 bit. Cáp RS232 ZEN-CIF01 đã lỗi thời |
| B9 Lab ZEN | Yêu cầu 6.1–6.3, có 1 sơ đồ rơ-le cho 6.1 | **2** | Cũng trống phần sơ đồ và chương trình. **6.1 trên ZEN là mạch sao–tam giác, khác 3.1 trên LOGO** (start/stop có báo quá tải). Hai bài đảo vai S1/S2 |

Các rủi ro khi giảng dạy mà agent phải nêu ra, không được im lặng:
- **Chuyển giao LOGO→ZEN dễ sai địa chỉ:** LOGO đánh từ 1 (I1, Q1), ZEN đánh từ 0 và dùng hex (I0…Ib). Chữ "X" vừa là bit mở rộng vừa là chế độ ON-delay của ZEN.
- **An toàn điện:** model AC đưa điện lưới ra tận nút nhấn ngõ vào. Mạch đảo chiều (cửa, động cơ) cần khóa liên động cả phần cứng lẫn phần mềm. Phải kiểm tra model kit trước khi cấp nguồn.
- **Phiên bản phần mềm và thiết bị** trong giáo trình đều cũ hơn lịch và kit thực tế.

Danh sách lỗi đầy đủ, có số dòng, nằm trong [`source-notes/`](source-notes/).

## 5. Hệ quả cho thiết kế teacher agent

1. **Agent không thể chỉ "tóm tắt giáo trình".** Với 8/8 bài thực hành, phần đáp án, sơ đồ nối dây và chương trình đều không có. Agent phải soạn mới, và mọi lời giải phải qua **cổng kiểm chứng của giáo viên trên kit** trước khi phát cho sinh viên. Lời giải chưa kiểm chứng chỉ được nằm trong tài liệu dành cho giáo viên, có gắn nhãn.
2. **Tách "đơn vị nội dung" khỏi "khung thời gian".** Nội dung (bài, mục, lab, mức đầy đủ, điều kiện tiên quyết) ổn định qua các khóa. Lịch thay đổi theo lớp và học kỳ. Agent ghép hai thứ này lại, và khi lịch đổi thì ghép lại, không viết lại từ đầu.
3. **Bất biến kiểm được:** tổng 240 phút mỗi buổi; tổng giờ LT/TH theo lịch; bài kiểm tra chỉ hỏi nội dung đã dạy; mỗi bài thực hành có tiêu chí chấm, mục an toàn và sai hỏng thường gặp; "Bài học trước" khớp thứ tự buổi.
4. **Cấu trúc lặp lại để giảm tải:** 4 lab có cùng khung 4 bước (kiến thức liên quan, yêu cầu, sơ đồ kết nối, lập trình), và cùng 3 chủ đề lặp lại trên ZEN. Đây là chỗ hợp với làm mẫu rồi rút dần (worked-example fading): LOGO-LAB-1 có lời giải đầy đủ, các lab sau giảm dần phần gợi ý. ZEN-LAB-2 và ZEN-LAB-3 đóng khung thành bài **chuyển giao** "cùng bài toán, khác nền tảng".
5. Repo hiện **chưa có** đầu vào lịch, chưa có cơ chế xếp lại lịch, chưa xuất được docx, và chưa có kiến thức về đào tạo kỹ năng thực hành, an toàn hay biểu mẫu GDNN (xem báo cáo kiến trúc trong [`agent-design.md`](agent-design.md#5-tích-hợp-vào-repo)).
