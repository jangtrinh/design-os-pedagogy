> **Ghi chú nguồn — Chương 2.2–3 — LOGO!Soft Comfort, lập trình trực tiếp, 4 bài ứng dụng**
> Trích xuất tự động bởi agent tầng **Sonnet** ngày 2026-11-01 từ tài liệu giảng dạy nội bộ "Chuyên đề Điều khiển lập trình cỡ nhỏ" (Trường CĐ Kiên Giang, 2025). Tài liệu gốc **không** lưu trong repo (lưu hành nội bộ). Số dòng (L…) tính theo chunk `C_ch2-3_logo_software_apps.md (dòng 2155–2912)` của bản chuyển .docx→Markdown bằng pandoc; ảnh `imageNNN` là ảnh nhúng trong .docx.
> Trạng thái: `unreviewed`. Mọi mục đánh dấu [SUY LUẬN]/[SUY RA] chưa được chạy thử trên thiết bị thật. Không dùng làm đáp án cho sinh viên trước khi giáo viên kiểm chứng trên kit.

# Phân tích chunk C: LOGO!Soft Comfort, lập trình trực tiếp, 4 bài lab (Chương 2.2–3.4)

Nguồn: chunk `C_ch2-3_logo_software_apps.md` (758 dòng). Quy ước: **[ĐỌC]** = có trong text/ảnh; **[SUY LUẬN]** = tôi tự suy ra, giáo viên phải kiểm chứng trên kit.

**Phát hiện quan trọng nhất:** chỉ 3.1.3 (dòng 557) có hình; mục 3.1.4, 3.2.3–3.2.4, 3.3.3–3.3.4, 3.4.3–3.4.4 (dòng 561–756) chỉ là các dòng chấm "......" để trống. Không có ảnh FBD/ladder nào cho 4 bài lab. Toàn bộ bảng I/O và logic bên dưới là **[SUY LUẬN]** từ lời đề bài, trừ phần ghi rõ [ĐỌC].

## 2.2 Phần mềm LOGO!Soft Comfort (dòng 1–105)

**Cài đặt (2.2.1) – checklist:**
- [ ] B1: Tải phần mềm từ internet, giải nén (không nêu nguồn/bản quyền).
- [ ] B2: Chạy `1_SetupLOGOSoftComfort7x..` (x86/x64); wizard "LOGO! Soft Comfort v7 Setup", bấm Next qua image73–75.
- [ ] B3: Mở LOGO!Soft Comfort V7 một lần, ghi "(bắt buộc)" (image76: Start menu V7.0).
- [ ] B4: Tắt phần mềm (image77, nút X).
- [ ] B5: Chạy `2_Setup_upgrades_update_v8.1x..`, chọn ngôn ngữ English, OK, chọn Program Group "Siemens LOGO!Soft", Install, Done (image78–83; ảnh đánh số đỏ tới bước 8).

**Sử dụng (2.2.2) – checklist:**
- [ ] Khởi động: Start > Siemens > LOGO!Soft Comfort; màn hình giới thiệu (image84).
- [ ] File > New, chọn FBD hoặc LAD; điền thông tin (Creator, Project name...) > OK (image85).
- [ ] Soạn chương trình: nhấp đúp hoặc kéo-thả từ thư viện trái; nhóm **Co** (vào/ra), **GF/BF** (hàm cơ bản), **SF** (hàm đặc biệt).
- [ ] Nối khối bằng **Connect (F5)**; mô phỏng **Tools > Simulation (F3)**.
- [ ] Lưu: File > Save as / Save (giữ password nếu có); mở: File > Open; thoát: File > Exit.

**So với lịch giảng V8.4:** tài liệu nói V7 rồi nâng lên **V8.1** (ảnh: "Version 8.1, © 2014–2016"). Không có V8.4. Ảnh màn hình làm việc (image85–86) là bản cũ (shortcut ghi V5.0, Windows XP, thiết bị 0BA5.Standard).

**Thiếu:** chọn model LOGO (0BA5/0BA7/0BA8) khi tạo project; truyền chương trình PC→LOGO (cáp, Tools > Transfer, Ethernet); chạy/giám sát online; mục "Soạn thảo FBD/LAD" (dòng 83–91) chỉ có tiêu đề, không có nội dung/ảnh; hướng dẫn nâng cấp V8.1 lên V8.4; kiểm tra lỗi (Tools > Check/Compile) và Simulation chi tiết.

## 2.3 Lập trình trực tiếp trên LOGO (dòng 107–526)

**Chung [ĐỌC]:** bàn phím gồm 4 phím mũi tên + ESC + OK. Ký hiệu 3 phím mũi tên ở dòng 111, 153, 171, 189, 363 bị **mất** khi chuyển đổi (chỉ còn ", và OK"). Trên LOGO 0BA5 chuẩn đó là ◄ ► + OK **[SUY LUẬN]**.

**Vào menu:** cấp nguồn > nếu "No Program / Press ESC" (image87) > nhấn đồng thời 3 phím (thường ◄ ► OK) > menu chính (image88/106): Program, PC/Card, Clock, Start.

**Chỉnh đồng hồ (Set Clock) – dòng 149–167:**
1. Chưa có chương trình: 3 phím > Program > OK > Set Clock > OK. Đã có chương trình: ESC + OK > Set Clock.
2. Chọn thứ DAY (SU, MO, TU, WE, TH, FR, SA) bằng phím mũi tên > OK.
3. Chọn giờ TIME hh.mm bằng phím mũi tên > OK.
4. Kết thúc: OK, màn hình trở lại.

**Xóa chương trình (Clear Prg) – dòng 169–185:** 3 phím > Program > OK > Clear Prg > OK > chọn YES (xóa) hoặc NO > OK. (Mục "Xóa một khối" dòng 173 thực ra lặp lại đúng quy trình xóa toàn bộ chương trình, xem mục lỗi.)

**Nhập chương trình (Edit Prg) – dòng 187–321:**
1. Program > Edit Prg > OK; hiện Q1 (có thể chọn Q2, Q3... bằng phím lên/xuống).
2. Lập trình **từ ngõ ra về ngõ vào** (từ phải sang trái). Con trỏ gạch chân = di chuyển; OK > con trỏ khối đậm nhấp nháy = chọn.
3. Chọn nhóm: **Co** (X, I1.., Q, M...), **BF** (AND, NAND, OR, NOR, XOR, NOT), **SF** (On-delay...). OK để chấp nhận; khối được gán số B01, B02...
4. Nối từng ngõ vào: OK > Co/BF/SF > chọn đích; ngõ vào không dùng = **X**.
5. Chèn khối: đặt con trỏ tại khối (ví dụ B01) > OK (menu BN) > chọn loại khối. Xóa khối: chọn khối kế sau trong menu BN. Xóa chuỗi phía trước: tại B02 > OK > Co > X > OK (xóa B02–B04, image102).
6. Xong: OK, màn hình về Q cuối; dùng phím mũi tên duyệt lại (image104 là chuỗi ví dụ I3 > B02 > B01 > Q1).

**Chạy (Start) – dòng 323–355:** ESC 2 lần > menu chính (con trỏ ">") > Start > OK > chế độ **Run** (hiển thị I/O, giờ). Card nhớ: có thì tự chép vào LOGO (ghi đè); LOGO nhớ trạng thái trước khi mất nguồn.

**Nguyên tắc vàng (2.3.7):**
1. 3 phím cùng lúc = vào soạn thảo; ESC + OK cùng lúc = chỉnh giờ/thông số.
2. Lập trình từ ngõ ra đến ngõ vào; 1 ngõ ra nối nhiều ngõ vào, **không** nối nhiều ngõ ra vào 1 ngõ vào.
3. Con trỏ gạch chân = di chuyển; OK chọn; ESC thoát. Con trỏ khối đậm = chọn khối/đầu nối; ESC lùi một bước.
4. LOGO chỉ lưu chương trình đã hoàn tất.

**Ví dụ 2.3.8 (dòng 399–526):** Ví dụ 1: mạch rơ-le S1//S2 điều khiển cuộn K1/đèn E1 (image107) chuyển thành khối **OR** (I1, I2, X) nối Q1 (image108). Dùng để dạy: (a) quy trình từng bước nhập OR; (b) ý nghĩa ký hiệu X; (c) nối dây S1→I1, S2→I2, tải→Q1 (image109). Chỉ có **1** ví dụ (tiêu đề "Các ví dụ" số nhiều); minh họa bằng ảnh màn hình LOGO image110–116. Phù hợp làm bài thực hành đầu tiên trên kit [SUY LUẬN].

## Lab specs

### LOGO-LAB-1 – Điều khiển động cơ điện (3.1, dòng 539–573)
- **Kiến thức liên quan [ĐỌC]:** lập trình bằng LOGO!Soft Comfort và trực tiếp trên LOGO; chỉ dẫn "xem lại phần hướng dẫn". Không có kiến thức về tự giữ/RS, rơ-le nhiệt.
- **Yêu cầu:** S1 = mở máy (nhấn thì động cơ chạy); S2 = dừng máy; khi quá tải, động cơ dừng và **đèn báo sáng**. Không có thời gian.
- **Bảng I/O:**

| Địa chỉ | Thiết bị | Mô tả | Nguồn |
|---|---|---|---|
| I1 | S1 (nút ON, NO) | Mở máy | text + image109 |
| I2 | S2 (nút OFF) | Dừng máy | text + image109 |
| I3 | F (tiếp điểm rơ-le nhiệt) | Quá tải | **[SUY LUẬN]** (ảnh không có) |
| Q1 | K/contactor động cơ | Chạy động cơ | image109 chỉ có "đèn" ở Q1 |
| Q2 | Đèn báo quá tải | Báo lỗi | **[SUY LUẬN]** |

- **Logic [SUY LUẬN]:** B1 = **RS (Latching relay)**: S = I1; R = OR(I2, NOT I3) (nếu F là tiếp điểm NC thì I3=1 khi bình thường). Q1 = B1. Q2 = NOT I3 (tùy chọn dùng Off-delay/Flasher cho đèn nháy). Cách thay thế dùng BF: Q1 = (I1 OR Q1) AND NOT I2 AND I3 (tự giữ bằng Q1).
- **Hàm cần dùng:** BF: OR, NOT, AND; SF: Latching relay (RS).
- **Tiêu chí đánh giá:** (1) nối dây đúng I/O, không hở/ chạm; (2) nhấn S1 động cơ chạy và giữ khi thả; (3) S2 dừng ngay; (4) quá tải (giả lập F) động cơ dừng + đèn sáng; (5) chương trình lưu, chạy lại sau mất nguồn đúng trạng thái; (6) thao tác đúng 2.3 (nếu thực hành trên bàn phím).
- **Biến thể:** (a) thêm đèn báo "đang chạy"; (b) khởi động sao-tam giác hoặc 2 hướng quay có khóa chéo (Q1/Q2); (c) tự khởi động lại sau 10 s khi hết quá tải, tối đa 3 lần (Up/Down counter + On-delay).
- **Sai hỏng – khắc phục:** nút OFF dùng NO nhưng viết logic NC (ngược) > kiểm tra loại tiếp điểm, dùng NOT; không tự giữ, thả S1 động cơ dừng > dùng RS hoặc feedback Q1; thứ tự ưu tiên set/reset sai (RS reset ưu tiên) > kiểm tra; I3 NC nối thành NO khiến động cơ không chạy > đo thông mạch; con trỏ nối sai ngõ vào "X" > duyệt lại bằng phím mũi tên.
- **An toàn điện:** cắt nguồn khi đấu dây; **nguồn LOGO 12/24RC là DC 12/24 V (image109 ghi "LOGO! 12/24 RC") nhưng ảnh nối L1/N 230 V AC**, phải xác nhận model (230RC) trước khi cấp nguồn; tiếp điểm rơ-le ≤ 10 A, động cơ dùng contactor trung gian; có CB, tiếp địa vỏ; không chạm đầu nối khi có điện.
- **Mức đầy đủ: 2/5.** Có yêu cầu và sơ đồ nối, nhưng sơ đồ trùng ví dụ 1 (xem mục Vấn đề), không có I3 quá tải, không có đáp án chương trình.

### LOGO-LAB-2 – Điều khiển đèn giao thông (3.2, dòng 575–653)
- **Kiến thức liên quan [ĐỌC]:** dùng Time (timer) trong LOGO; "xem phần lệnh cơ bản" (nhưng timer là SF, không phải BF).
- **Yêu cầu [ĐỌC]:** ngã tư, 6 đèn: X1 7 s, Đ2 10 s, V1 3 s, X2 7 s, Đ1 10 s, V2 3 s, lặp vô hạn. Lưu ý: 1 = sáng, 2 = tắt (bản gốc có thể là 1/0; hình bảng trạng thái bị mất).
- **Diễn giải [SUY LUẬN]:** nếu đọc tuần tự thì chu kỳ 40 s với từng đèn sáng một mình, vô lý (đường kia không có đèn). Hợp lý: **pha A** (0–10 s): X1 0–7 s, V1 7–10 s, Đ2 0–10 s; **pha B** (10–20 s): X2, V2, Đ1 tương tự; chu kỳ 20 s. Phải hỏi lại giáo viên biên soạn.
- **Bảng I/O [SUY LUẬN]:** I1 = công tắc Run/Enable (tùy chọn); Q1 = X1, Q2 = V1, Q3 = Đ1, Q4 = X2, Q5 = V2, Q6 = Đ2.
  **Cảnh báo:** LOGO 12/24RC (image109) chỉ có **Q1–Q4**; cần module mở rộng (ví dụ DM8 cho Q5–Q8) hoặc rút gọn còn 4 đèn.
- **Logic [SUY LUẬN]:** B1 = **Asynchronous pulse generator** T_H = 10 s, T_L = 10 s, Enable = I1 → P. Đ2 = P. B2 = **On-delay** 7 s, input P → T1; X1 = P AND NOT T1; V1 = T1 (hết khi P=0 sau 3 s). B3 = NOT P; Đ1 = NOT P; B4 = On-delay 7 s, input NOT P → T2; X2 = NOT P AND NOT T2; V2 = T2. Phương án khác: chuỗi 3–4 On-delay + RS.
- **Hàm cần dùng:** SF: Asynchronous pulse generator, On-delay; BF: NOT, AND.
- **Tiêu chí:** (1) 6 đèn nối đúng; (2) thời gian đo bằng đồng hồ: X 7 s, V 3 s, Đ 10 s (sai số ≤ 0,5 s); (3) không bao giờ có hai hướng cùng xanh; (4) Đ của một hướng = X + V của hướng kia; (5) chạy lặp liên tục ≥ 3 chu kỳ; (6) trình bày bảng trạng thái/giản đồ thời gian.
- **Biến thể:** (a) thêm công tắc ban đêm: vàng nhấp nháy (Flasher); (b) thay đổi thời gian bằng Set Param không nạp lại chương trình; (c) thêm đèn đi bộ + nút gọi người đi bộ và đếm lùi hiển thị.
- **Sai hỏng – khắc phục:** thiếu ngõ ra (Q5, Q6) > dùng module mở rộng DM8; (các đèn cùng màu ở hai chiều của cùng một hướng có thể nối song song vào một ngõ ra); timer chạy sai vì reset chưa cấu hình (On-delay không giữ) > kiểm tra giản đồ; đèn đỏ & xanh cùng sáng > kiểm tra phủ định NOT/điều kiện; lệch thời gian do đặt đơn vị s/m sai > kiểm tra Par.
- **An toàn điện:** tải đèn bằng đèn LED/ bóng 12/24 V trên kit; không nối trực tiếp đèn 230 V quá dòng tiếp điểm; cắt nguồn trước khi đấu.
- **Mức đầy đủ: 2/5.** Có thông số thời gian đầy đủ, nhưng không có sơ đồ nối, bảng I/O, chương trình; mô tả mơ hồ về đồng thời; hình bảng trạng thái thiếu.

### LOGO-LAB-3 – Đóng mở cửa tự động (3.3, dòng 655–706)
- **Kiến thức liên quan [ĐỌC]:** dùng ngõ vào/ngõ ra điều khiển; "xem lệnh cơ bản".
- **Yêu cầu [ĐỌC]:** S2 = mở; chạy lên đến công tắc hành trình mở thì dừng. S3 = đóng; đến công tắc hành trình đóng thì dừng. S1 = dừng giữa chừng, sau đó có thể mở hoặc đóng tùy ý. Trạng thái mở/đóng/dừng hiển thị bằng đèn. Không có thời gian.
- **Bảng I/O [SUY LUẬN]:** I1 = S1 Dừng (NC), I2 = S2 Mở, I3 = S3 Đóng, I4 = LS mở (hành trình trên), I5 = LS đóng; Q1 = contactor mở (đèn "đang mở" song song), Q2 = contactor đóng (đèn "đang đóng" song song), Q3 = đèn "dừng". Ngõ vào cần 5 (12/24RC có I1–I8; đủ); ngõ ra 3–5 (nếu đèn riêng cần Q4+, hạn chế 4).
- **Logic [SUY LUẬN]:** B1 = RS mở: S = I2; R = OR(I1, I4, I3). B2 = RS đóng: S = I3; R = OR(I1, I5, I2). Q1 = B1 AND NOT B2; Q2 = B2 AND NOT B1 (khóa chéo). Q3 = NOT Q1 AND NOT Q2. Nên thêm On-delay 1 s trước khi đảo chiều để bảo vệ motor.
- **Hàm cần dùng:** SF: Latching relay (RS); BF: OR, AND, NOT; tùy chọn On-delay.
- **Tiêu chí:** (1) S2 mở, dừng đúng tại LS mở; (2) S3 đóng, dừng đúng tại LS đóng; (3) S1 dừng bất kỳ lúc nào; (4) sau dừng, mở/đóng đều chạy được; (5) không bao giờ Q1 và Q2 cùng 1; (6) đèn 3 trạng thái đúng.
- **Biến thể:** (a) tự đóng sau 10 s khi mở xong (On-delay); (b) thêm cảm biến hồng ngoại chống kẹt: đang đóng gặp vật cản thì mở lại; (c) 1 nút bấm đổi trạng thái (Pulse relay) + đếm số lần mở + còi cảnh báo 3 s trước khi chạy.
- **Sai hỏng – khắc phục:** Q1 và Q2 cùng sáng do thiếu khóa chéo > thêm AND NOT; cửa không dừng ở LS do LS nối NO/NC nhầm > đo bằng đồng hồ, dùng NOT; đảo chiều đột ngột cháy contactor > thêm trễ + khóa cơ khí; nhiễu nút nhấn > kiểm tra dây.
- **An toàn điện:** khóa chéo phần cứng cho 2 contactor; LS dừng khẩn cấp độc lập phần mềm; che chắn khu vực cửa; cắt nguồn khi đấu dây; không đứng trong vùng chuyển động khi thử.
- **Mức đầy đủ: 1,5/5.** Chỉ có yêu cầu; không có định nghĩa I/O, sơ đồ, chương trình.

### LOGO-LAB-4 – Băng tải công nghiệp (3.4, dòng 707–756)
- **Kiến thức liên quan [ĐỌC]:** Counter để đếm sản phẩm; "xem lại phần Counter trong lệnh đặc biệt" (nội dung này nằm ngoài chunk).
- **Yêu cầu [ĐỌC]:** Start: băng chuyền hộp chạy. Hộp chạm công tắc hành trình **S3**: băng hộp dừng, băng táo chạy. Cảm biến **S2** đếm táo. Đủ **10 quả**: băng táo dừng, băng hộp chạy lại; reset bộ đếm; lặp lại cho đến khi nhấn **Stop**.
- **Bảng I/O [SUY LUẬN]:** I1 = Start (S1, không được nêu tên trong đề), I2 = Stop, I3 = S3 (công tắc hành trình hộp), I4 = S2 (cảm biến táo); Q1 = băng tải hộp, Q2 = băng tải táo.
- **Logic [SUY LUẬN]:** B1 = RS Run: S = I1, R = I2. B2 = RS "chế độ táo": S = **cạnh lên** của I3 AND B1 (dùng AND edge); R = OR(Cnt_Q, I2). B3 = **Up/Down counter**: Cnt = I4, R = NOT B2 (hoặc Q của B3 qua trễ ngắn), Par = 10. Q1 = B1 AND NOT B2; Q2 = B2.
- **Hàm cần dùng:** SF: Up/Down counter, Latching relay; BF: AND (Edge), NOT, OR.
- **Tiêu chí:** (1) Start chạy băng hộp; (2) S3 dừng hộp và chạy băng táo; (3) đếm đúng 10 (đưa từng quả qua S2); (4) đủ 10 thì băng táo dừng, băng hộp chạy; (5) bộ đếm reset và chu trình lặp; (6) Stop dừng cả hai ở mọi trạng thái.
- **Biến thể:** (a) số táo đặt qua Set Param (không sửa chương trình); (b) hiển thị số đếm hiện tại trên màn hình LOGO (text/Message); (c) 2 số lượng khác nhau (10 và 12) chọn bằng công tắc, đếm tổng số hộp, dừng sau 20 hộp.
- **Sai hỏng – khắc phục:** hộp còn đè S3 khi vừa chạy lại làm chu trình táo lặp ngay > dùng cạnh lên/ trễ; đếm dư do cảm biến rung > lọc bằng On-delay ngắn/ chỉnh cảm biến; không reset counter nên lần sau đếm tiếp > nối R; Stop không dừng khi đang đếm > R của mọi RS nối I2.
- **An toàn điện:** cảm biến PNP/NPN phải phù hợp nguồn 24 V; nút Stop/E-Stop dạng NC; che chắn băng tải; không đưa tay vào băng khi chạy.
- **Mức đầy đủ: 2/5.** Yêu cầu khá rõ (có số lượng, trình tự) nhưng thiếu I/O, sơ đồ, chương trình.

## Vấn đề của tài liệu

1. **Sơ đồ 3.1.3 sai bài (dòng 557):** dùng `image109.png`, đúng hình của ví dụ 1 (dòng 431): S1/S2 vào I1/I2, đèn ở Q1. Không có rơ-le nhiệt, contactor, dây động cơ, ngõ báo quá tải; ảnh cho mạch OR của ví dụ 1 chứ không phải start/stop có tự giữ.
2. **Ba bài lab còn trống:** 3.2.3, 3.2.4, 3.3.3, 3.3.4, 3.4.3, 3.4.4 và 3.1.4 chỉ là dòng chấm (dòng 561–756). Không ảnh nào; mọi lập luận trên là suy luận.
3. **Đề 3.2 mơ hồ (dòng 583–603):** liệt kê tuần tự, không nói đồng thời; lưu ý "1/2" thay vì 1/0 và bảng trạng thái mất. 6 đèn cần 6 ngõ ra > LOGO 12/24RC (image109) chỉ có Q1–Q4.
4. **Đề 3.3:** không nêu cho phép đảo chiều trực tiếp hay phải dừng; đèn "dừng" lúc nào; không nêu số lượng/loại đèn; chữ "điều được hiển thị" (đều), "nhấn nút nhấn".
5. **Đề 3.4 (dòng 715):** lỗi chính tả "dây chuyền hộp/dây chuyền táo/bằng chuyền", không đặt tên S1/S4 cho Start/Stop; "S3 = công tắc hành trình, S2 = cảm biến" nhưng S3 ở bài 3.3 lại là nút Đóng; tên thiết bị thiếu nhất quán.
6. **Model/nguồn LOGO không khớp:** image109 là LOGO! 12/24 RC (nguồn DC) nhưng nối L1/N AC; text nói ngõ vào "I1…I6" (dòng 277) trong khi thiết bị có I1–I8.
7. **Menu không khớp ảnh:** dòng 123 viết "Lock" (nên là Clock) và dòng 133 "Set Clock" nằm trong Program; image88/106 cho thấy Clock là mục menu chính, menu Program gồm Edit Prg, Prg Name, Clear Prg, Password. Dòng 173 "Xóa một khối chương trình" là bản sao quy trình xóa cả chương trình. Dòng 297–303 mâu thuẫn (nói xóa khối "giữa B02 và Q1" nhưng thao tác chọn B01).
8. **Ký hiệu phím mất** (dòng 111, 153, 171, 189, 363 "nhấn ,và OK"), phần thao tác 4 phím không thể xác nhận nếu không có thiết bị.
9. **Phần mềm lỗi thời và thiếu:** V7 > V8.1 (lịch dạy V8.4); ảnh image85–86 từ V5.0/Windows XP; image85 là hộp Properties chứ không phải chọn FBD/LAD (dòng 45); mục FBD (dòng 89–91) trống; không có hướng dẫn tải chương trình xuống LOGO; yêu cầu "mở V7 bắt buộc" không giải thích (nguy cơ vấn đề bản quyền/crack, ảnh đến từ blogspot).
10. **Tham chiếu chéo:** 3.2–3.4 yêu cầu "xem phần lệnh cơ bản / Counter" nhưng nội dung SF (On-delay, Counter, Pulse generator) không nằm trong chunk này; cần kiểm tra chunk chương 2.1.
11. Lỗi nhỏ: "Logo! Comfor" (dòng 543), "Seimen" (dòng 39), "thí dụ minh hoạ" lặp, dòng 403 thiếu hình khi cấp nguồn.
