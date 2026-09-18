# Đánh giá lượt thử course design: Toán lớp 1 Việt Nam

Ngày 17/09/2026. Đây là một lượt biên soạn thật trong hội thoại hiện tại bằng workflow đã đọc. Có sản phẩm lưu trong repo và kiểm tra chạy trên sản phẩm đó. Không có lượt gọi mô hình thứ hai, so sánh A/B, giáo viên phản biện độc lập hoặc học sinh tham gia.

## 1. Sản phẩm và cách kiểm tra

Gói gồm 24 yêu cầu được phân rã từ phần lớp 1, 12 chủ đề, 35 tuần/105 tiết, bài mẫu-luyện tập-đáp án-kiểm cuối tiết cho từng tiết, tám giáo án chi tiết và hai đề mẫu 10 điểm. Các mã chuẩn là do biên soạn tạo, không phải mã của Bộ. Bản đồ lưu bên ngoài nội dung khóa học để không thể tự cắt bớt mục tiêu rồi tuyên bố đủ.

Đã đọc phần lớp 1 và thời lượng của PDF chương trình, xem ảnh bảng; đọc quy định đánh giá và thông báo SGK. Các thẻ nguồn ghi rõ nguồn Bộ được trường lưu, toàn văn pháp lý tái đăng, và thông báo của nhà xuất bản. Chưa đọc trọn SGK, nên đối chiếu bài/trang vẫn chờ giáo viên xác nhận.

Kiểm tra tự động xác nhận 105 tiết, 3.675 phút, ánh xạ 24/24 mã yêu cầu và tính lại 111 đáp án khai báo trong tổng 125 tác vụ kiểm tra có cấu trúc (105 kiểm cuối tiết và 20 câu đề). Mười bốn tác vụ còn lại dùng tiêu chí quan sát; việc có tiêu chí không đồng nghĩa đã chấm được câu trả lời học sinh. Hai trong số đó là bản ghi vị trí tiết đề tổng hợp, không phải câu hỏi độc lập thêm vào đề.

Hai mươi phương thức unittest được bổ sung và đã chạy đạt ở lượt kiểm riêng. Chúng gồm gói dữ liệu thật và các biến thể cố ý sai: bỏ chuẩn khối/lịch, tham chiếu hỏng, chu trình tiên quyết, sai đáp án, cộng nhớ, trừ mượn, phép nhân, giờ rưỡi, xếp năm số, lệch thời lượng, yêu cầu đọc độc lập, thứ/ngày không khớp, điểm lẻ và gán hiệu quả học tập chưa có bằng chứng. Đây là phép thử phần mềm, không phải lỗi quan sát ở trẻ hay tỉ lệ lỗi của một mô hình nền.

## 2. Phát hiện từ chính workflow

| Phát hiện có căn cứ | Rủi ro đối với giáo trình | Thay đổi đã thực hiện |
| --- | --- | --- |
| Blueprint cũ chỉ có locale_and_curriculum dạng văn bản | Dễ bỏ sót một yêu cầu nhỏ nhưng bắt buộc | Thêm checklist độc lập và ánh xạ chuẩn-mục tiêu-tiết-luyện tập-đánh giá |
| S2 bao trùm nhiều lớp; tài liệu primary có ví dụ nhân/chia | Toán đúng nhưng vượt lớp 1 | Khóa quốc gia, lớp, phiên bản và giới hạn; thêm guide Việt Nam lớp 1 |
| Quy tắc hinge cũ đòi một đáp án và 3-4 nhiễu cho mọi câu | Ép hoạt động thao tác/nói thành bài kiểm tra đọc | Quy định riêng cho trắc nghiệm; cho phép quan sát với tiêu chí và câu hỏi tiếp |
| Chưa có kiểm tra được thực thi cho giáo trình cả năm | Nhầm số tiết, tiền đề, đáp án khó phát hiện trong tài liệu dài | Thêm bộ kiểm tra có phạm vi rõ và tests; không gọi là validator toàn năng |
| Chưa tách hoàn toàn lời cô, câu học sinh và đáp án | Có thể lộ đáp án hoặc bắt trẻ đọc chỉ dẫn dành cho người lớn | Dữ liệu và tài liệu phân tách từng phần; bản xuất được gắn nhãn giáo viên |
| Phạm vi SGK có thể thay đổi theo năm học | Tự gán một bộ sách/trang sách theo trí nhớ | Ghi nguồn hiện hành, giữ trường đối chiếu trang là pending khi chưa đọc |

## 3. Một lỗi nội dung mà kiểm tra cấu trúc không bắt được

Ở bản nháp tiết 85, lời hỏi học sinh nhắc dải 8 cm và 5 cm trong khi cm được giới thiệu ở tiết 87. Metadata của tiết vẫn gắn R16 (so sánh dài/ngắn), đáp án quan sát đúng nên checker đã cho qua. Khi đọc thực tế tiến trình, trợ lý phát hiện điểm này.

Đã sửa câu học sinh thành: “Đặt hai dải giấy chung một đầu. Dải nào dài hơn?”. Số đo 8/5 cm chỉ còn trong thông tin chuẩn bị của giáo viên. Đây là bằng chứng rằng phải kiểm tra sự phụ thuộc vào từ vựng/biểu diễn trong câu chữ, không chỉ mã chuẩn hoặc đáp án số.

Lưu ý khác đã xử lý khi thiết kế checker: 6+4 và 10-6 là kiến thức nhẩm trong phạm vi 10; 90+10 và 100-40 là số tròn chục. Không dùng kiểm tra nhớ/mượn theo chữ số một cách máy móc để loại các trường hợp hợp lệ này.

## 4. Đánh giá theo rubric đã có

| Tiêu chí | Kết luận của trợ lý trong lượt này | Còn thiếu |
| --- | --- | --- |
| Bối cảnh | Đã ghi quốc gia/lớp/tuổi giả định/ngôn ngữ/nguồn lực | Hồ sơ đầu vào lớp thật |
| Chính xác nội dung | Nguồn và đáp án có cấu trúc đã được kiểm; có sửa lỗi cm sớm | Giáo viên kiểm toàn bộ lời hỏi, học cụ và ý nghĩa toán |
| Alignment | 24/24 yêu cầu có tuyến bài-luyện tập-kiểm tra khai báo | Mức độ đại diện của từng tác vụ cần thẩm định nội dung |
| Tiến trình | Chuỗi đơn vị, lịch và tiên quyết dữ liệu nhất quán | Thời gian nắm bài của nhóm trẻ khác nhau |
| Khả năng dạy | Có 105 phiếu tiết và tám giáo án chi tiết | Dạy thử một số tiết để xem 35 phút có khả thi |
| Tiếp cận | Không bắt đọc thành thạo, có thao tác/nói/chỉ; không bắt dùng AI | Kiểm học cụ, phiếu in và nhu cầu cụ thể |
| Khả thi | 105 tiết và thời lượng khớp; không có bài nhà bắt buộc bị giấu | Điều chỉnh theo SGK và kế hoạch trường |
| Trung thực bằng chứng | Tách kiểm phần mềm, biên soạn, giáo viên và học sinh | Chưa có bằng chứng hiệu quả học tập |

Đây là self-review của trợ lý tạo sản phẩm. Không quy đổi thành điểm chất lượng tổng hợp hoặc ghi như chứng nhận độc lập.

## 5. Improve tiếp theo nên làm gì?

**P0, trước khi dạy:** giáo viên lớp 1 đối chiếu SGK đang dùng và kế hoạch trường; kiểm câu chữ, hình/vật, đáp án và ma trận đề; thử ít nhất các dạng thao tác số, chục/đơn vị, đo và đồng hồ. Các phiếu đề hiện ở dạng mẫu giáo viên với mô tả hình cần chuẩn bị; chưa phải toàn bộ workbook minh họa sẵn cho trẻ.

**P1, tăng độ chắc của workflow:** xây danh sách từ/biểu diễn tiên quyết trên từng nhiệm vụ để cảnh báo sớm trường hợp cm ở tiết 85; kiểm sự phù hợp giữa mã chuẩn và nội dung tác vụ thay vì chỉ kiểm liên kết; xuất phiếu học sinh tách khóa đáp án; thêm kiểm tra hình thước/đồng hồ/khối và sự tương đương hỗ trợ tiếp cận.

**P2, mở rộng có bằng chứng:** dùng thêm một khóa ở lớp hoặc lĩnh vực khác để thiết kế schema/plugin profile tổng quát. Hiện checker cố ý chỉ hỗ trợ case Việt Nam lớp 1; không dùng kết quả này để tuyên bố mọi khóa học đều đã được kiểm. Tiếp tục xử lý nội dung legacy có khẳng định quá mức theo ưu tiên sử dụng thực tế.

**Đo hiệu quả học tập:** cần quy trình nghiên cứu/đánh giá phù hợp của trường, minh chứng cá nhân, nhiệm vụ khác sau một thời gian và ghi hỗ trợ thực tế. Không thay bước này bằng hội thoại trẻ giả lập hoặc một bộ tests pass.

## 6. Bằng chứng máy và tái chạy

Lượt hồi quy cuối chạy đạt 98 tests (78 cũ và 20 mới). Registry ghi 98 records, 350 tham chiếu, không có lỗi hay liên kết chưa giải quyết; 62 cảnh báo legacy vẫn được giữ. Kiểm tra liên kết Markdown không có lỗi, sáu bản ghi kiến thức thêm/sửa được kiểm tra hợp lệ và bảy file Python mới/sửa được kiểm tra cú pháp. Báo cáo giữ nguyên trạng thái chưa có giáo viên độc lập hoặc học sinh thật.

Kết quả cuối và hash đầu vào được ghi ở plans/20260917-vietnam-grade1-course-test/final-checks.json. Lệnh tái chạy và phạm vi kiểm có tại [docs/course-audit.md](../../docs/course-audit.md). Nếu dữ liệu thay đổi, chạy lại checker và renderer; kết quả cũ chỉ áp dụng cho các hash đã lưu.
