# 05 – Sự kiện phần cứng/phần mềm: LOGO! và Omron ZEN (ghi chú nguồn)

Ngày: 2026-11-01. Phương pháp và giới hạn: WebFetch bị chặn DNS cho toàn bộ miền Siemens, Omron, manualslib, vendor (không đọc được PDF gốc). Mọi dữ kiện dưới đây lấy từ bản tóm tắt/trích đoạn của công cụ WebSearch trên các trang gốc, KHÔNG phải đọc toàn văn tài liệu. Vì vậy độ tin cậy tối đa là "trung bình"; các điểm hành vi (mục 3) phải kiểm chứng bằng mô phỏng trong LOGO!Soft Comfort. Trang industrialmonitordirect.com bị loại (tự mâu thuẫn, số khối sai).

## 1. Các thế hệ LOGO! và thông số 12/24RCE, 230RCE

**Thế hệ**
- LOGO! 0BA6 (LOGO! 6) đã bị Siemens công bố phase-out từ 10/2016; màn hình 0BA6 kém hơn LOGO! 8 (LOGO! 8: 6 dòng x 16 ký tự, độ tương phản cao hơn). [nguồn: https://www.rs-online.com/designspark/siemens-logo-6-is-declared-a-phase-out-product-with-the-effect-from-october-2016]
- 0BA6/0BA7: không có Ethernet native, nối PC bằng cáp LOGO! (RS232/USB); LOGO! 8 có cổng RJ45 Ethernet tích hợp (12/24RCE) – lập trình bằng cáp mạng. [nguồn: https://mall.industry.siemens.com/mall/en/ww/Catalog/Product/6ED10521MD000BA8] (phần 0BA6/0BA7 do blog bên thứ ba, [CHƯA XÁC MINH]: https://industrialmonitordirect.com/blogs/knowledgebase/siemens-logo-ethernet-connectivity-options-and-solutions)
- Ký hiệu MLFB: 6ED1052-1MD00-0BA8 (thế hệ "0BA8") và 6ED1052-1MD08-0BA0/0BA1/0BA2/0BA3 (LOGO! 8.x). Ánh xạ chính xác 0BA0=8.0, 0BA1=8.2, 0BA2=8.3, 0BA3=8.4 [CHƯA XÁC MINH]; cách gọi "FS04/FS:08" không tìm thấy nguồn Siemens [CHƯA XÁC MINH]. Hướng dẫn xác định thực tế: đọc nhãn thiết bị. [nguồn: https://www.rowse-automation.co.uk/blog/post/siemens-logo-6-to-logo-8-conversion]
- Bản 0BA3 (LOGO! 8.4) có thêm MQTT, cloud; phần mềm cần LSC V8.4 trở lên; V8.4 bổ sung email, cloud (Azure, Alibaba), MQTT, tải datalog khi RUN, thêm bộ nhớ, web server nhanh hơn. [nguồn: https://www.automation-fair.com/which-operating-systems-does-logosoft-comfort-v8-4-support/ ; https://www.tme.com/Document/91f627304a0f3f155029dd01a7362394/6ED1052-2MD08-0BA3.pdf] (mức tin cậy trung bình, nguồn thương mại/mirror).
- Bộ nhớ chương trình: datasheet 12/24RCE liệt kê 400 khối; 800 khối cho bản mới (8.3/8.4) có chỗ ghi nhưng nguồn mâu thuẫn [CHƯA XÁC MINH]. [nguồn: https://mall.industry.siemens.com/mall/en/ww/Catalog/Product/6ED10521MD000BA8 ; https://www.tme.com/Document/91f627304a0f3f155029dd01a7362394/6ED1052-2MD08-0BA3.pdf]

**LOGO!Soft Comfort V8.4**
- Mã đặt hàng 6ED1058-0BA08-0YA1; Siemens Mall ghi hệ điều hành thử nghiệm Windows 7, 8, 10, 11 (cộng Mac OS, SUSE Linux). [nguồn: https://mall.industry.siemens.com/mall/en/uk/Catalog/Product/6ED1058-0BA08-0YA1 ; https://www.automation24.com/siemens-logo-soft-comfort-v8-6ed1058-0ba08-0ya1]
- Thiết bị 0BA8 (12/24RCE, 24RCE, 230RCE) được lập trình từ LSC V8.0 trở lên. LSC V8.4 đổi định dạng file FBD/LAD, không mở ngược bằng V8.3. [nguồn: https://industrialmonitordirect.com/blogs/knowledgebase/resolving-logo-soft-comfort-v84-file-compatibility-errors] [CHƯA XÁC MINH – bên thứ ba]
- Thiết bị 0BA6/0BA7 có được V8.4 hỗ trợ hay không: không có nguồn Siemens [CHƯA XÁC MINH]. Giáo trình nội bộ có ảnh chụp V7 → V8.1 nên chương trình cũ có thể cần chuyển đổi.
- V8.3 trên Windows 11 có báo lỗi khởi động (một blog) [CHƯA XÁC MINH]. [nguồn: https://industrialmonitordirect.com/blogs/knowledgebase/resolving-logo-soft-comfort-v83-splash-screen-failure]

**12/24RCE (LOGO! 8)**
- 8 ngõ vào số, trong đó 4 dùng được ở chế độ analog 0–10 V; 4 ngõ ra rơle; nguồn 10,8–28,8 V DC; 400 khối; mở rộng được; Ethernet. [nguồn: https://www.mouser.lt/datasheet/2/1412/1/6ED10521MD080BA2_datasheet_en-3450712.pdf ; https://sterowniki-plc.net/image/catalog/Produkty/Siemens/LOGO!/6ED1052-1MD08-0BA1.pdf]
- Các ngõ analog là I1, I2, I7, I8 (quy ước manual LOGO! 8). [nguồn: https://media.automation24.com/manual/pl/109826499_logo_system_manual_en-US_en-US.pdf]
- Rơle: tối đa 10 A tải trở, 3 A tải cảm; không có bảo vệ ngắn mạch (cần cầu chì ngoài). [nguồn: https://www.tme.com/Document/2626a91f65457e14b2210cea3c77d44b/6ED1052-1MD08-0BA3.pdf ; https://www.promelec.ru/fs/sources/8f/d6/b5/4b/0fdd03104ab2ee8a7b16ea81.pdf]
- Ngưỡng ngõ vào DC (mức 0 < 5 V DC; mức 1 > 8,5 V DC): chỉ thấy blog bên thứ ba nói ">8,5 V là HIGH", không trích được datasheet [CHƯA XÁC MINH]. [nguồn: https://industrialmonitordirect.com/blogs/knowledgebase/logo-hold-to-confirm-analog-button-press-timer-setup]

**230RCE**: 8 DI, 4 DO rơle, nguồn 115/230 V; rơle 10 A tải trở / 3 A tải cảm. [nguồn: https://www.tme.com/Document/a51fa35e7683f3fc84557c63e969b8e0/6ED1052-1FB08-0BA3.pdf] Ngưỡng ngõ vào AC (< 40 V / > 79 V AC) không trích được [CHƯA XÁC MINH]. Lưu ý an toàn: 230 V không dùng chung công tắc ELV; kiểm tra nhãn.

**Mở rộng**
- DM8 12/24R: 4 DI/4 DO, rơle, nguồn 10,8–28,8 V DC. [nguồn: https://sterowniki-plc.net/image/catalog/Produkty/Siemens/LOGO!/6ED1055-1MB00-0BA2.pdf]
- DM16 24 / DM16 24R: 8 DI/8 DO (chỉ 24 V DC); KHÔNG có DM16 12/24R. [nguồn: https://mall.industry.siemens.com/mall/de/be/Catalog/Products/10029112]
- Tối đa hệ thống LOGO! 8: 24 DI, 20 DO, 8 AI, 8 AO (nhiều nguồn nhưng có số lệch 16 DO). [nguồn: https://www.onninen.no/en/siemens-logo-dm8-12-24r-4-di-4-do-6ed1055-1mb00-0ba2-as/p/GCR523] [CHƯA XÁC MINH bằng manual chính thức]
- Tổng ngõ ra số: 4 (cơ sở) + 4 (một DM8) = 8; cơ sở + DM16 = 12.

## 2. Kit/mô hình LOGO! tại các trường nghề Việt Nam

- Không tìm được catalogue kit nội địa có thông số chi tiết (số nút nhấn, đèn). Chỉ thấy: bài báo "Xây dựng bộ thực hành PLC LOGO! 230RCE ... CDIO" (chỉ có tiêu đề/tóm tắt), nên bối cảnh Việt Nam có cả 230RCE. [nguồn: https://vjol.vista.gov.vn/tctbgd/en/article/view/106022]
- Các nhà bán lẻ VN (plcsiemens.vn, vnqtech.com, siemens-vn.com) chỉ bán PLC đơn, DM8, TDE; chưa phải kit đào tạo. [nguồn: https://plcsiemens.vn/danh-muc-san-pham/bo-lap-trinh-logo ; https://vnqtech.com/logo-siemens]
- Giáo trình VN trùng tên module: "Giáo trình điều khiển lập trình cỡ nhỏ - LOGO!". [nguồn: https://www.slideshare.net/slideshow/gio-trnh-iu-khin-lp-trnh-c-nh-logo/156181353] (chưa đọc nội dung).
- Kit quốc tế tham chiếu: plc4training "Logo8-Trainingsboard" cho 12/24RCE + DM8 12/24R [nguồn: https://www.plc4training.com/en/shop/logo8-trainingsboard/]; Christiani LOGO! Trainer Package 12/24 RCE (LOGO! 8) cho đào tạo nghề [nguồn: https://www.christiani-international.com/Vocational-Training-University/Automation-Technology-Electronics/Control-Technology/LOGO-Trainer-Package-12-24-RCE-LOGO-8.html].
- Cấu hình điển hình (8 DI / 4 DO, có/không DM8), nút nhấn, đèn, tải mô phỏng: [CHƯA XÁC MINH] (suy luận từ kit quốc tế).

## 3. Special functions của LOGO! (hành vi)

Trích đoạn lấy từ bản manual cũ (mirror), chưa phải bản LOGO! 8 – phải kiểm chứng mô phỏng.
- **Rem** = tham số "Retentivity": "/ = no retentivity, R = The status is retentive". Khi bật, sau mất điện timer không reset mà tiếp tục từ điểm dừng ("The timer is not reset, but resumes operation until the time-to-go has expired"). Tức Rem giữ trạng thái và thời gian đã trôi Ta qua mất điện, không phải lúc Trg tắt. [nguồn: https://www.manualslib.com/manual/1382742/Siemens-Logo.html?page=152 ; https://www.manualslib.com/manual/1382742/Siemens-Logo.html?page=136]
- **Off-delay (On-/Off-delay)**: "A negative edge (1 to 0 transition) at input Trg triggers the off-delay time"; Q giữ 1 trong lúc đếm; Q = 0 khi Ta = T; "You can set input R (Reset) to reset the time Ta and the output before Ta has expired." [nguồn: https://www.manualslib.com/manual/1382742/Siemens-Logo.html?page=150 ; https://www.manualslib.com/manual/1359132/Siemens-Logo.html?page=127]
  - Cạnh lên mới của Trg khi đang đếm: tài liệu trích "Ta is retriggered ... at Trg" nhưng câu rút gọn mơ hồ [CHƯA XÁC MINH]. Mặc định đề xuất: khi Trg lên 1, Q=1, đếm bị hủy; chu kỳ mới bắt đầu ở cạnh xuống kế tiếp (đúng với cách dạy phổ biến; cần test).
- **Retentive on-delay**: "A signal at input R resets the on-delay time and the output"; R ưu tiên hơn mọi ngõ vào ("R has priority over Trg"). [nguồn: https://cache.industry.siemens.com/dl/files/342/19623342/att_84037/v1/logo_e_96.pdf]
  - Sau R với Trg vẫn = 1: khối kích bằng cạnh lên 0→1 nên khả năng cao KHÔNG tự chạy lại nếu không có cạnh lên mới [CHƯA XÁC MINH].
  - Một nguồn nói Trg thêm trong lúc đếm "retriggers Ta", nguồn khác nói "không ảnh hưởng"; câu retrigger nằm trong danh sách cạnh Wiping relay nên có thể bị gán nhầm. [nguồn: https://www.libble.eu/siemens-siemens-logo!/online-manual-830177/?page=0155] [CHƯA XÁC MINH]

## 4. Omron ZEN

- ZEN-10C1AR-A-V2: nguồn 100–240 VAC, 6 vào AC, 4 ra rơle, LCD, đồng hồ thực; mở rộng tối đa 34 điểm I/O. [nguồn: https://industrial.omron.eu/en/products/zen-10c ; https://baoanjsc.com.vn/products/programmable-relay-omron-ZEN-10C1AR-A-V2_54772_en.aspx]
- ZEN-20C1AR-A-V2: 12 vào, 8 ra rơle, tối đa 44 điểm. [nguồn: https://uk.rs-online.com/web/p/logic-modules/6502978 ; https://baoanjsc.com.vn/products/programmable-relay-omron-ZEN-20C1AR-A-V2_54775_en.aspx]
- ZEN-8E1AR: 4 vào AC + 4 ra rơle 5 A; tối đa 3 khối mở rộng (trừ loại Economy); khối mở rộng ngõ vào AC không nối với CPU V2 nguồn DC. [nguồn: https://industrial.omron.eu/en/products/zen-8e ; https://baoanjsc.com.vn/TaiLieu/Bo%20dieu%20khien%20lap%20trinh%20logic%20OMRON%20ZEN%20series-%20Catalog%2030112015054726.pdf]
- V1 vs V2: V2 bỏ khe tản nhiệt, nối được ZEN-8E1 nửa kích thước (V1 nối ZEN-4E/8E), ngõ analog ±1,5% FS (V1 10% FS), dải DC rộng 10,8–28,8 V (V1 20,4–26,4 V); V2 bổ sung twin timer. [nguồn: https://www.ia.omron.com/support/faq/answer/66/faq04288/]
- Timer: 16 timer T0–Tf + holding timer #0–#7 (manual cũ nói 8, [CHƯA XÁC MINH] cho V2); chế độ ON-delay (X), OFF-delay (■), one-shot (O), flashing (F), twin (W, V2). Holding timer giữ giá trị khi RUN→STOP hoặc mất điện, chỉ kiểu ON-delay. [nguồn: https://files.omron.eu/downloads/latest/manual/en/z211_zen_v2_operation_manual_en.pdf ; https://edata.omron.com.au/eData/Programmable_relay/Zen_DS.pdf]
- Counter: 16 bộ C0–Cf, 0–9999, đếm cạnh OFF→ON, có reset; nguồn mâu thuẫn (blog nói chỉ C0–C7 ở 10C) [CHƯA XÁC MINH]; mã manual là Z211-E1-03 (không thấy "W385/W386").
- Ngừng sản xuất: ngày đặt cuối 30/03/2024, giao cuối 30/06/2024, hỗ trợ đến 30/06/2029; thay thế CP2E (ZEN-8E1 không có thay thế đề xuất, trang sản phẩm khác nhau). [nguồn: https://assets.omron.eu/downloads/latest/discontinuation_notice/en/2022006_zen-series_discontinuation_notice_en.pdf ; https://automation.omron.com/en/us/products/family/ZEN-10C]
- Phần mềm ZEN-SOFT01-V4 (bản Ver. 4.14): Omron liệt kê tới Windows 10 (64-bit trên Win7/10); Windows 11 không được liệt kê [CHƯA XÁC MINH khả năng chạy]. Cáp ZEN-CIF01 là RS-232C; cáp USB riêng của Omron cho ZEN không tìm thấy, dùng bộ chuyển USB-RS232 là suy luận [CHƯA XÁC MINH]. [nguồn: https://www.fa.omron.co.jp/product/tool/66/zen_versionup/download_en.html ; https://files.omron.eu/downloads/latest/manual/de/z184_zen_v2_support_software_operation_manual_de.pdf]

## 5. Đèn giao thông 6 đèn và bài mẫu

- Kit Christiani "LOGO!Learn Traffic Light Control" dùng 4 ngõ ra LOGO! cho 2 đèn xe 3 màu + 2 đèn người đi bộ (cấu hình khác bài 6 đèn). [nguồn: https://www.christiani-international.com/Vocational-Training-University/Automation-Technology-Electronics/Control-Technology/LOGO-Learn-Traffic-Light-Control.html]
- Không tìm thấy khuyến nghị chính thức Siemens/Omron cho 6 đèn trên 4 ngõ ra. Đề xuất kỹ thuật (lập luận, [CHƯA XÁC MINH bằng nguồn]): (a) thêm DM8 (LOGO!) hoặc ZEN-8E1AR (ZEN) để có 8 ngõ ra, mỗi đèn 1 ngõ; (b) ghép: dùng Q cho Xanh/Vàng mỗi hướng (4 ngõ) và đèn Đỏ lấy qua rơle trung gian ngoài; (c) dùng ZEN-20C (8 ra).
- Nguồn bài mẫu: Siemens SCE "Startup LOGO! 0BA8" tài liệu đào tạo [nguồn: https://www.automation.siemens.com/sce-static/learning-training-documents/additional/logo/sce-900-011-startup-logo-0ba8-r1603-zh.pdf]; chương ví dụ ứng dụng trong manual LOGO! (ví dụ Stairway lighting) [nguồn: https://www.manualslib.com/manual/1359132/Siemens-Logo.html?page=137]; thư mục Samples đi kèm LOGO!Soft Comfort; bài sao-tam giác LOGO! V8 [nguồn: https://myshare-cms.siemens.com/siemens-plc-logo-manual/star-delta-starter-motor-control-circuit-using-logo-v8-plc] (trang tổng hợp, độ tin cậy thấp); Siemens Support forum về trang application examples [nguồn: https://support.industry.siemens.com/forum/de/en/post/424798]. Ví dụ cửa tự động/băng tải đếm/khởi động-dừng có đèn quá tải: chưa tìm được nguồn công khai riêng [CHƯA XÁC MINH].

## Mặc định đề xuất cho agent

| Hạng mục | Mặc định | Tin cậy | Giáo viên xác nhận |
|---|---|---|---|
| LOGO! kit | LOGO! 8 12/24RCE (8 DI, trong đó I1, I2, I7, I8 analog; 4 DO rơle 10 A/3 A) + 1x DM8 12/24R (4 DI/4 DO) = 8 DO; ngõ vào ký hiệu I1–I12, ngõ ra Q1–Q8 | Trung bình (giáo trình nội bộ có 12/24RC) | Có DM8 không; có 230RCE không; mã MLFB/nhãn (0BA8 hay 0BA1-3) |
| Phần mềm | LOGO!Soft Comfort V8.4, FBD; cảnh báo định dạng file không mở ngược V8.3; ảnh V7/V8.1 trong giáo trình có thể khác giao diện | Trung bình | Phiên bản cài thực tế, Windows 10/11 |
| Ngưỡng ngõ vào | Nói "mức 0 dưới ~5 V, mức 1 trên ~8,5 V DC" kèm cảnh báo chưa xác minh datasheet | Thấp | Dẫn chiếu datasheet |
| Timer LOGO! | Off-delay: Trg 1→0 bắt đầu đếm, R hủy; Retentive on-delay: R ưu tiên, Rem = bật giữ trạng thái/thời gian qua mất điện; mọi tình huống biên (cạnh lên khi đang đếm, R xong Trg=1) bảo HS tự mô phỏng | Trung bình-thấp | Kiểm chứng trên simulation V8.4 |
| ZEN kit | ZEN-10C1AR-A-V2 (100–240 VAC: 6 vào, 4 ra rơle) + tùy chọn ZEN-8E1AR (4/4), tối đa 3 mở rộng (34 điểm); ZEN-SOFT01-V4 + cáp ZEN-CIF01 RS-232 (có thể cần USB-RS232) | Trung bình | Có V2 hay V1; có 20C không; AC hay DC; cáp; máy Win11 chạy được không |
| ZEN timer | Bốn chế độ X/■/O/F và holding timer #; counter C0–Cf (khẳng định số lượng sau khi xem Z211); thông báo ZEN đã ngừng sản xuất (CP2E thay thế) | Trung bình | Phiên bản manual nhà trường |
| Đèn giao thông | Mặc định: cần 6 ngõ ra, nên dùng DM8 (LOGO!) hoặc ZEN-8E1AR; nếu không có, dùng rơle trung gian | Thấp-trung bình | Kit có đèn thế nào, có mở rộng không |
| Điều chuẩn nhiệm vụ | Khi kit chưa rõ: agent hỏi lại 5 điều (MLFB, DM8, ngõ vào đèn/nút, phần mềm, ZEN V1/V2) trước khi ra đề | – | – |
