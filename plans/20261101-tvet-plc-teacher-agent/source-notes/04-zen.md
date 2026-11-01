> **Ghi chú nguồn — Chương 4–6 — PLC Omron ZEN**
> Trích xuất tự động bởi agent tầng **Sonnet** ngày 2026-11-01 từ tài liệu giảng dạy nội bộ "Chuyên đề Điều khiển lập trình cỡ nhỏ" (Trường CĐ Kiên Giang, 2025). Tài liệu gốc **không** lưu trong repo (lưu hành nội bộ). Số dòng (L…) tính theo chunk `D_ch4-6_zen.md (dòng 2913–4025)` của bản chuyển .docx→Markdown bằng pandoc; ảnh `imageNNN` là ảnh nhúng trong .docx.
> Trạng thái: `unreviewed`. Mọi mục đánh dấu [SUY LUẬN]/[SUY RA] chưa được chạy thử trên thiết bị thật. Không dùng làm đáp án cho sinh viên trước khi giáo viên kiểm chứng trên kit.

# D_zen: PLC Omron ZEN (Ch4-6, "Điều khiển lập trình cỡ nhỏ")

Nguồn: chunk `D_ch4-6_zen.md` (L = số dòng file). Ảnh: `media/imageNNN`. Nhãn: **[ĐỌC]** = có trong tài liệu/ảnh; **[SUY RA]** = tôi suy luận, chưa chạy thử trên ZEN.
**Phát hiện quan trọng nhất:** Mục 6.1.3-6.4.4 chỉ là các dòng chấm trống (L903-1107). Chương 6 chỉ có đúng 1 ảnh (image154, sơ đồ rơ-le 6.1). Toàn bộ sơ đồ nối dây và ladder cho bài lab phải do giáo viên tự soạn.

## Ch4 đơn vị nội dung

**4.1 Giới thiệu và ứng dụng (L11-61)**
- Khái niệm: ZEN là bộ điều khiển lập trình cỡ nhỏ, lập trình bậc thang (LAD) trực tiếp bằng phím (loại có LCD) hoặc bằng phần mềm; "nối mạch bằng logic thay vì đấu dây"; có module mở rộng, bảo vệ mật mã, hiển thị 6 ngôn ngữ (L21-31).
- Ứng dụng: máy giá thấp, bơm nước, máy khoan, máy bán hàng, thang cuốn, garage, rửa xe, cửa tự động, thông gió nhà kính, báo động, chiếu sáng, tưới tự động.
- Mã model, đọc từ ảnh (bài viết không nêu mã): CPU **ZEN-10C1AR-A** (AC 100-240V, ngõ ra rơ-le, có LCD, phím DEL/ALT/↑↓←→/ESC/OK), image117. Module mở rộng **8EAR** (AC 100-240V), image118. Hộp Property Settings: CPU Unit type "-V2", ZEN types "10C1A*-A-V2" (image122); thanh trạng thái "ZEN-10C1**-A" (image123). [ĐỌC, từ ảnh]
- Số I/O: "10 I/O" = 6 vào (I0-I5) + 4 ra (Q0-Q3). "20 I/O" = 12 vào (I0-Ib) + 8 ra (Q0-Q7) (L159-245). Mở rộng tối đa 3 module, 24 điểm (X0-Xb và Y0-Yb, 12+12) (L81, L176, L252).
- Thuật ngữ VI↔EN: bit trung gian = auxiliary relay (M); bit hold = holding relay (H); module mở rộng = expansion unit; khối CPU = CPU Unit.

**4.2 Lắp đặt và nối dây (L63-121)**
- Lắp lên ray DIN: 4 bước (L69-77). Mở rộng: tháo nắp CPU, đẩy module sang phải (L83-87). Thiếu bước tháo ray và cắt điện trước khi lắp.
- Nguồn AC 100-240VAC 50/60Hz, 30VA; L và N đúng chân, không đảo (L93-99). Nguồn DC 24VDC; "+"/"-" đúng cực; ngõ vào nối "-" vào COM, "+" qua công tắc (L109-113). I4, I5 là ngõ vào analog 0-10V (L115).
- Ngõ ra: 4 rơ-le độc lập, không phân cực. 4 transistor độc lập, có đầu cực nhưng đổi chiều nguồn/tải vẫn không sao (L119-121).
- Hình quan trọng: **image119**. Sơ đồ nối dây AC: nguồn L/N, công tắc SW1, SW2 nối I0, I1, kèm ladder I0 nối tiếp I1(NC) và chốt Q0 (đã xem).
- **An toàn khi đấu nối** (L101-107, L869-873):
  - Không đảo L/N.
  - Đối chiếu dòng định mức ZEN với nguồn cấp.
  - Không nối trực tiếp dây đôi xoay chiều vào ngõ vào CPU (ý chưa rõ, xem mục Vấn đề).
  - Trên model AC, công tắc ngõ vào nối vào pha L (image119), nghĩa là điện lưới tại nút nhấn. Dùng kit cách ly và cắt điện khi đấu dây. [SUY RA từ ảnh]
  - Kiểm tra dây nguồn/ngõ ra trước khi cấp điện, tháo tải ngõ ra khi chạy thử lần đầu, bảo đảm an toàn khu vực quanh thiết bị.

## Ch5 bảng lệnh

### Bảng loại bit (L135-294) [ĐỌC]
| Ký hiệu | Tên | Địa chỉ / số bit | Chức năng |
|---|---|---|---|
| I | Vào CPU | I0-I5 (6, loại 10 I/O); I0-Ib (12, loại 20 I/O) | Trạng thái thiết bị vào |
| X | Vào mở rộng | X0-Xb (12) | Vào của module mở rộng |
| B | Phím bấm | B0-B7 (8) | Phím trên CPU (loại LCD) |
| A | So sánh vào analog | A0-A3 (4) | Chỉ ZEN nguồn DC |
| P | So sánh | P0-Pf (16) | So sánh giá trị hiện thời T, #, C |
| Q | Ra CPU | Q0-Q3 (10 I/O); Q0-Q7 (20 I/O) | Trạng thái thiết bị ra |
| Y | Ra mở rộng | Y0-Yb (12) | Ra của module mở rộng |
| M | Trung gian | M0-Mf (16) | Dùng trong chương trình, không ra ngoài |
| H | Hold | H0-Hf (16) | Như M nhưng **giữ trạng thái khi mất điện** |
| T | Timer | T0-T5 (Pre-V1, 8 bit) / T0-Tf (-V1, 16) | 4 chế độ (bảng dưới) |
| # | Holding timer | #0-#3 (Pre-V1) / #0-#7 (-V1) | Giữ giá trị khi trigger OFF hoặc mất nguồn |
| @ | Weekly timer | @0-@7 / @0-@f | ON/OFF theo giờ, ngày trong tuần |
| * | Calendar timer | *0-*7 / *0-*f | ON/OFF theo giờ, tháng |
| C | Counter | C0-C7 / C0-Cf | Đếm thuận/ngược |

Dạng ngõ ra của cuộn dây (L296-363) [ĐỌC]:
| Ký hiệu | Tên | Hành vi |
|---|---|---|
| `[` | Normal | Ra theo vào |
| S | Set | Ra ON và giữ khi vào ON |
| R | Reset | Ra OFF khi vào ON |
| A | Alternate | Đổi trạng thái mỗi lần vào ON |

### Timer / Counter (L490-553) [ĐỌC; không có giản đồ thời gian]
| Ký hiệu | Chế độ | Hành vi | Ứng dụng (đề xuất) [SUY RA] |
|---|---|---|---|
| X | ON Delay | Trigger ON và giữ đủ thời gian đặt thì bit timer ON | Chuyển sao-tam giác sau 10 s (6.1), nối tầng đèn giao thông (6.2) |
| N | OFF Delay | Trigger ON thì bit ON; trigger OFF đủ thời gian đặt thì OFF | Quạt/đèn trễ tắt |
| O | One-shot pulse | Trigger ON thì bit ON trong khoảng đặt trước | Xung ngắn, che nhiễu công tắc hành trình |
| F | Flashing pulse | Trigger ON thì bit ON/OFF lặp lại | Đèn vàng nhấp nháy, chu kỳ 6.2 |
| # | Holding timer | Giữ giá trị khi mất trigger, chạy tiếp khi ON lại | Tích lũy thời gian vận hành |
| C | Counter | Đếm thuận/ngược (chân đếm, reset, hướng không được mô tả) | Đếm sản phẩm (6.4) |

Lưu ý: chữ "X" (chế độ ON delay) trùng chữ X của bit mở rộng; dễ nhầm khi dạy.

### Quy trình ZEN Support Software (L555-765, image120-142) [ĐỌC]
1. Cài: đưa CD, chọn ngôn ngữ, OK; nếu không tự chạy thì mở `Setup.exe`. Next, rồi Finish (L559-565).
2. Mở: Program/OMRON/ZEN Support Software. Chọn Create a new program / Load programs from files / Read program from ZEN (image121).
3. Hộp Property Settings: CPU Unit type (ví dụ -V2), ZEN types (10C1A*-A-V2), Expansion Unit 1-3, Project Name, Comment (image122).
4. Nhập contact: Enter hoặc nhấp đôi, hoặc Insert/Contact. Hộp Edit Contact: bit type, N.O./N.C., địa chỉ, comment. Nhập coil: nhấp đôi ô ngõ ra, chọn function (Normal/Set/Reset/Alternate), địa chỉ.
5. Nối: Insert Horizontal, Insert Vertical (đường dọc kéo xuống từ con trỏ).
6. Cáp **ZEN-CIF01** (RS232, cổng COM). File/Communications Settings: Port Name (COM1), Monitor Time (2 s) (image127-128).
7. File/Properties chọn đúng kiểu ZEN và mở rộng, bật nguồn, mở file, rồi Go Online (xác nhận OK, image129).
8. Transfer to ZEN. Tick "The settings are downloaded too". Tick Protection chỉ khi đã đặt mật khẩu. Kiểm tra an toàn trước khi truyền (image130).
9. ZEN/Change operating mode/RUN, kiểm tra thanh trạng thái STOP chuyển sang RUN.
10. Giám sát: Toggle Monitoring hoặc ZEN/Monitor. Mạch đóng chuyển **màu xanh** (image132).
11. Mô phỏng: Start/Stop Simulator, nền **vàng**, rồi RUN/STOP; có nút hiện hình ZEN và đồng hồ (image134, bảng L697-765).

### Lập trình trực tiếp bằng phím (L767-873, image143-153) [ĐỌC]
**Đổi ngôn ngữ** (6 ngôn ngữ, mặc định Anh; khuyến cáo không đổi):
1. Bật nguồn, OK vào Menu.
2. ↓ 4 lần đến LANGUAGE.
3. OK (chữ cuối nhấp nháy), OK lần nữa (cả từ nhấp nháy), ↑/↓ chọn, OK.

**Đặt đồng hồ:**
1. Menu, SET CLOCK, OK.
2. ↑↓ đổi số, ←→ đổi vị trí (thứ tự tự cập nhật).
3. OK, OK để xác nhận.
- Năm 2000-2099. Mất điện ≥2 ngày ở 25 °C thì về 00/1/1 00:00. Chỉ model có lịch (không rõ model nào).

**Nhập ladder** (phải ở STOP):
1. Menu, PROGRAM, EDIT PROGRAM, OK.
2. Màn hình chỉ hiện 2 dòng. Ô đầu nhấp nháy ở bit type.
3. **I0**: OK, chọn loại bit I bằng ↑↓, → sang địa chỉ, chọn 0, OK hai lần.
4. Đổi NO/NC bằng ALT.
5. **I1 nối tiếp I0**: sang vị trí kế, làm tương tự (image148).
6. **Ngõ ra Q0**: → đến vùng ngõ ra, chọn bit type Q và địa chỉ 0 (image150).
7. **Tiếp điểm tự giữ Q0 song song I0**: xuống dòng 2, đặt Q0, rồi nối nhánh.
8. **Đường nối (OR)**: ALT khi con trỏ giữa 2 vị trí, dùng phím mũi tên vẽ ngang/dọc, ↑ vẽ đồng thời dọc và ngang, OK hoặc ESC để thoát (image152-153).
9. **ESC về Menu trước khi tắt điện**, nếu không chương trình mất.
10. Không vẽ đường nối khép kín (vòng kín).
11. Chuyển RUN, thử với tải đã tháo.

## Đối chiếu LOGO ↔ ZEN (cho transfer)
Thông tin LOGO lấy từ chunk A/B/C. Cột ZEN [ĐỌC] trừ khi có ghi chú.
| Khái niệm | Siemens LOGO! | Omron ZEN | Lưu ý giảng dạy |
|---|---|---|---|
| Ngôn ngữ | FBD: khối nối từ trái sang phải đến Q | Ladder: tiếp điểm trái, cuộn dây phải; LCD chỉ hiện 2 dòng | Một mạch LOGO có nhiều khối thành vài rung ladder; đọc rung từ trái sang phải |
| AND / OR | Khối AND, OR | Nối tiếp = AND, song song = OR (đường nối ALT) | Dạy "khối AND = tiếp điểm nối tiếp" |
| NOT | Khối NOT | Tiếp điểm N.C. (ALT) | |
| Địa chỉ | I1.., Q1.. (bắt đầu từ 1, thập phân), M, AI1/AI2 (I7, I8) | I0.., Q0.. (bắt đầu từ 0), hex đến b/f; analog I4, I5 (DC) | **Lệch 1 so với LOGO** (I1 LOGO = I0 ZEN): lỗi chép nhầm phổ biến |
| Bit nhớ | M | M (mất khi cúp điện) và H (giữ khi cúp điện) | LOGO dùng tùy chọn Rem=on/off; ZEN chọn loại bit |
| On-delay | SF On-delay (Trg, T, Rem) | T mode X | Cùng khái niệm, khác biểu diễn: LOGO 1 khối, ZEN cuộn T + tiếp điểm T |
| Off-delay | SF Off-delay | T mode N | |
| Xung / nhấp nháy | Relay xung có trì hoãn; Bộ phát xung không đồng bộ | T mode O (one-shot); F (flashing) | Gần tương đương [SUY RA] |
| Chốt (latching) | Bộ chốt relay (S, R) | Coil S/R hoặc tự giữ Q0 song song I0 | ZEN có 2 cách: S/R hoặc tự giữ cổ điển (bài 6.1 dùng tự giữ) |
| Đảo trạng thái | Bộ relay xung | Coil A (Alternate) | |
| Bộ đếm | Bộ đếm lên xuống (Cnt, Dir, R) | C (đếm thuận/ngược) | Tài liệu ZEN thiếu mô tả chân đếm, reset |
| Đồng hồ | Bộ định ngày giờ tuần / năm | @ Weekly / * Calendar timer; SET CLOCK | |
| Giữ khi mất điện | Rem (retentive) | H, # (holding timer) | |
| Cờ khởi động | M8 (set 1 chu kỳ quét đầu) | Không đề cập | Bài cần xung khởi động phải tự tạo |
| Phần mềm | LOGO!Soft Comfort V8.4 (lịch) | ZEN Support Software; mô phỏng nền vàng | |
| Sửa trực tiếp | Phím con trỏ | ALT/DEL/ESC/OK + mũi tên; ESC về Menu trước khi tắt nguồn | |
| Chế độ | START | Phải STOP mới sửa chương trình | |

## Lab specs 6.1-6.4
Lịch: tuần 13-14 (mỗi tuần 1 LT + 3 TH). 6.1-6.3 trong lịch; **6.4 không**. Quy ước chung cho ladder bên dưới: nút dừng đấu NC nên trong ladder dùng tiếp điểm N.O. của ngõ vào đó; mọi địa chỉ là đề xuất.

### ZEN-LAB-1 (6.1) Điều khiển động cơ: sao-tam giác (tên "sao-tam giác" là [SUY RA])
- **Yêu cầu [ĐỌC L897]:** nhấn S2: K1, T1, K2 có điện, tự giữ; sau **10 s** tiếp điểm T1 thường đóng mở: K2 mất điện, K3 có điện. Tài liệu không nói K2/K3 là gì và không có đoạn dừng. Từ image154 (đã xem), S1 là nút dừng NC.
- **Sơ đồ rơ-le [ĐỌC image154]:** S1 NC nối tiếp (S2 NO // K1 tự giữ), cuộn K1 và T1 (trễ đóng). K1 cấp qua tiếp điểm chuyển mạch T1 vào hai nhánh: K2 (qua tiếp điểm K3 NC) và K3 (qua tiếp điểm K2 NC), khóa liên động chéo.
- **Bảng I/O [SUY RA]:** I0=S1 (dừng, NC), I1=S2 (chạy, NO); Q0=K1, Q1=K2 (sao), Q2=K3 (tam giác); T0 mode X, đặt 10.0 s.
- **Ladder [SUY RA]:**
  - R0: (I1 hoặc Q0) nối tiếp I0 thì Q0 (tự giữ, dừng ưu tiên).
  - R1: Q0 thì cuộn T0 (X, 10 s).
  - R2: Q0, T0(N.C.), Q2(N.C.) thì Q1.
  - R3: Q0, T0(N.O.), Q1(N.C.) thì Q2.
- **Lệnh cần:** I/Q, tiếp điểm NO/NC, tự giữ, timer mode X.
- **Tiêu chí (5):**
  1. Đấu dây đúng và an toàn.
  2. Chạy đúng chuỗi K1/K2, sau 10 s K2 tắt K3 bật.
  3. Q1/Q2 không bao giờ cùng ON.
  4. Nhấn S1 tắt tất cả.
  5. Nạp/giám sát bằng phần mềm đúng quy trình.
- **Biến thể:** (a) thêm đèn báo/nút dừng khẩn dùng I2; (b) đổi thời gian đặt, hoặc thêm trễ 0.5 s giữa K2 tắt và K3 bật.
- **Sai hỏng:**
  - Đảo ý NC của S1, nên động cơ không khởi động (khắc phục: kiểm tra N.O./N.C. trong ladder).
  - Lẫn I0/I1 giữa ladder và bảng I/O.
  - Quên khóa liên động.
  - Quên chuyển RUN.
  - Quên bấm ESC (mất chương trình).
- **Completeness: 3/5** (có sơ đồ rơ-le, nhưng thiếu I/O, nối dây, ladder).
- **So với LOGO 3.1: KHÔNG giống.** LOGO là chạy/dừng động cơ có đèn báo quá tải (S1=chạy, S2=dừng). ZEN đảo vai S1/S2 (S1=dừng NC, S2=chạy). Chuyển giao chỉ là khái niệm tự giữ.

### ZEN-LAB-2 (6.2) Đèn giao thông ngã tư
- **Yêu cầu [ĐỌC L949-969]:** X1 7 s, Đ2 10 s, V1 3 s, X2 7 s, Đ1 10 s, V2 3 s, lặp lại. Ghép pha [SUY RA]: (0-7 s) X1+Đ2; (7-10) V1+Đ2; (10-17) X2+Đ1; (17-20) V2+Đ1, chu kỳ **20 s**.
- **Bảng I/O [SUY RA]:** I0=RUN (tùy chọn); Q0=X1, Q1=V1, Q2=Đ1, Q3=X2, Q4=V2, Q5=Đ2. T0=7 s, T1=10 s, T2=17 s, T3=20 s (mode X).
- **Cảnh báo:** cần **6 ngõ ra**, trong khi ZEN 10 I/O chỉ có Q0-Q3 (4 ra). Phải dùng loại 20 I/O (Q0-Q7) hoặc module mở rộng (Y0-Y…). Kiểm tra kit thực tế.
- **Ladder [SUY RA]** (Q lấy RUN=I0 làm điều kiện chung):
  - T0, T1, T2, T3: cuộn trigger bởi RUN · T3(N.C.) (cả 4 cùng trigger, T3 hết 20 s thì reset toàn chu kỳ).
  - Q0 = RUN·T0(NC); Q1 = T0(NO)·T1(NC); Q5 = RUN·T1(NC); Q3 = T1(NO)·T2(NC); Q4 = T2(NO)·T3(NC); Q2 = T1(NO)·T3(NC).
  - Có thể xuất hiện 1 chu kỳ quét glitch ở mốc 20 s.
- **Lệnh:** timer X (nhiều timer chạy song song), tiếp điểm NO/NC.
- **Tiêu chí (5):** đúng thời gian từng pha; không có hai đèn xanh cùng sáng; lặp chu kỳ; nối dây nhiều ngõ ra đúng; ladder gọn, dùng ≤ 4 timer.
- **Biến thể:** (a) đèn vàng nhấp nháy mode F ban đêm hoặc theo Weekly timer @0; (b) chu kỳ khác (xanh 10 s) hoặc thêm pha đỏ toàn phần 1 s.
- **Sai hỏng:** thiếu ngõ ra (dùng sai model); cuộn T không reset nên chu kỳ không lặp; đặt thời gian sai đơn vị; không tắt đèn pha trước.
- **Completeness: 2/5** (yêu cầu đầy đủ, mọi thứ còn lại trống; không ghi rõ ghép pha).
- **So với LOGO 3.2: GIỐNG** (cùng văn bản yêu cầu, chunk C L581-603). Dạy chuyển giao: LOGO dùng khối timer/phát xung, ZEN dùng nhiều timer X.

### ZEN-LAB-3 (6.3) Cửa tự động
- **Yêu cầu [ĐỌC L1019-1021]:** S2 mở, chạy đến công tắc giới hạn mở thì dừng; S3 đóng, đến giới hạn đóng thì dừng; S1 dừng giữa chừng, sau đó chọn mở hoặc đóng; trạng thái mở/đóng/dừng hiển thị bằng đèn.
- **Bảng I/O [SUY RA]:** I0=S1 (dừng, NC), I1=S2 (mở), I2=S3 (đóng), I3=công tắc hành trình mở, I4=công tắc hành trình đóng (đấu NC, an toàn khi đứt dây); Q0=motor mở (+ đèn "đang mở" song song), Q1=motor đóng (+ đèn "đang đóng"), Q2=đèn "dừng". Chỉ 3 ngõ ra (đèn mở/đóng mắc song song cuộn contactor), vừa với model 10 I/O. Lưu ý I4 trên model DC là analog.
- **Ladder [SUY RA]:**
  - R0: (I1 hoặc Q0) · I0 · I3 · Q1(NC) thì Q0.
  - R1: (I2 hoặc Q1) · I0 · I4 · Q0(NC) thì Q1.
  - R2: Q0(NC) · Q1(NC) thì Q2.
  - Khóa chéo Q0/Q1 buộc phải nhấn S1 trước khi đảo chiều, khớp yêu cầu.
- **Lệnh:** tiếp điểm NO/NC, tự giữ, khóa liên động (không dùng timer).
- **Tiêu chí (5):** mở/đóng đúng tới giới hạn; S1 dừng giữa chừng và chạy lại được cả hai chiều; không chạy hai chiều cùng lúc; đèn đúng trạng thái; đấu dây công tắc hành trình đúng.
- **Biến thể:** (a) thêm cảm biến/nút chống kẹt (dừng và đảo chiều); (b) tự đóng sau thời gian đặt (T mode X).
- **Sai hỏng:** công tắc hành trình đấu NO nên chạy ngay lập tức hoặc không dừng; thiếu khóa liên động; hai contactor đảo chiều cùng ON (khắc phục: thêm khóa phần cứng); nhấn S2 và S3 liên tiếp không qua S1.
- **Completeness: 2/5.**
- **So với LOGO 3.3: GIỐNG** (cùng yêu cầu, chunk C L661-665).

### ZEN-LAB-4 (6.4) Băng tải (KHÔNG có trong lịch)
- **Yêu cầu:** mục 6.4.1-6.4.2 **để trống** (L1065-1067). Lấy yêu cầu từ LOGO 3.4 [chunk C L713-715]: Start thì băng hộp chạy; chạm công tắc hành trình S3 thì băng hộp dừng, băng táo chạy; cảm biến S2 đếm táo; đủ 10 quả thì băng táo dừng, băng hộp chạy lại; counter reset; lặp lại đến khi nhấn Stop.
- **Bảng I/O [SUY RA]:** I0=Start, I1=Stop (NC), I2=S3, I3=S2 (cảm biến táo); Q0=băng hộp, Q1=băng táo; M0=chạy, M1=pha táo; C0 đặt 10.
- **Ladder [SUY RA]:** (I0/M0 tự giữ, I1 dừng); Q0 = M0·M1(NC); S3 (I2) set M1; Q1 = M0·M1; C0 đếm I3 khi M1, reset khi M1 OFF; C0 ON thì reset M1.
- **Lệnh:** counter C, M bit, coil S/R.
- **Tiêu chí (5):** chuỗi hộp-táo-hộp đúng; đếm đúng 10; counter reset; Stop tắt hết; lặp ổn định.
- **Biến thể:** số táo thay đổi; thêm đèn báo/đếm hộp.
- **Sai hỏng:** S3 vẫn bị đè khi băng hộp chạy lại làm kích lại M1 (cần timer O che nhiễu); counter không reset; sensor nhiễu.
- **Completeness: 1/5.**
- **So với LOGO 3.4: có thể giống** (cùng chủ đề), nhưng phần ZEN trống nên không xác nhận được.

## Vấn đề của tài liệu
1. **Chương 6 gần như trống:** L903-1107 chỉ là dòng chấm; chỉ 1 ảnh (image154). Không có sơ đồ nối dây, ladder, bảng I/O.
2. **Đề 6.1 khác LOGO 3.1** (xem ZEN-LAB-1): không phải cùng bài; S1/S2 đảo vai. Cần cảnh báo sinh viên.
3. **Tên phần mềm không nhất quán:** "ZEN Soft" (L567), "ZEN Support Software" (L569), "ZEN-SOFT" (lịch giảng), splash image120 "ZEN-SOFT01". Chọn một tên khi soạn giáo án (khuyến nghị: ZEN Support Software).
4. **Phiên bản/model:** bảng bit phân biệt Pre-V1/-V1 (L403-477) nhưng ảnh phần mềm là **-V2** (image122). Không rõ -V2 có thêm bit gì. Bài viết không liệt kê mã model nào; mã chỉ thấy trong ảnh (10C1AR-A, 8EAR). Không nói model nào có đồng hồ/LCD.
5. **Lỗi bảng:** "T0 đến T5 (Pre-V1)" nhưng ghi 8 bit (L403-408), đáng ra T0-T7. Cột "Địa chỉ bit" của bảng timer 5.1.4 thực ra chứa tên chế độ (L503). Mô tả bit Q "nối với đầu vào khối CPU" (L245) nên là đầu ra. "công suất 6.5 Hz" (L109) sai đơn vị (W); "30VA (W)" (L93). Hình đánh số "Hình 1.1" trong Ch4 (L17).
6. **Câu khó hiểu về an toàn** (L107): "không nối trực tiếp dây đôi xoay chiều tới ngõ vào CPU" (không rõ nghĩa). Không có cảnh báo cắt điện khi đấu dây, không có nhãn model nối dây cụ thể cho DC.
7. **Thiếu nội dung kỹ thuật:** không có giản đồ thời gian cho X/N/O/F; không nói cách đặt giá trị và đơn vị thời gian timer; không nói cách dùng counter (chân đếm, reset, hướng) và bit P/A/B; không có bước nhập timer/counter trên phím (chỉ dạy contact/coil), trong khi bài 6.1, 6.2, 6.4 cần timer/counter.
8. **Cài đặt cũ:** cài từ CD-ROM (L559-561); cáp ZEN-CIF01 là RS232/COM (L629), máy tính hiện đại thường không có cổng COM (cần bộ chuyển USB-RS232, cần kiểm); không nêu phiên bản Windows hỗ trợ.
9. **Lệch lịch giảng:** lịch dùng "Bài 7-9", tuần 11-14, còn sách là Ch4-6. Lịch tuần 13-14 (9.1-9.3 + Kiểm tra định kỳ 2) khớp 6.1-6.3.
10. **Ảnh hộp thoại (image124-126)** chữ rất nhỏ; tôi không đọc được danh sách loại bit và chế độ timer trong hộp Edit Contact/Coil. Cần xác nhận với máy thật.
