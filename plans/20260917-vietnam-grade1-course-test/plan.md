# Thử nghiệm workflow: Toán lớp 1 Việt Nam

Ngày: 17/09/2026. Baseline Git quan sát: 2a52315; working tree sạch khi bắt đầu.

## Mục tiêu

Thực hiện một lượt thiết kế giáo trình cả năm bằng workflow hiện có, đối chiếu yêu cầu Việt Nam, lưu sản phẩm thật và kiểm tra các lỗi mà workflow chưa ngăn được. Sản phẩm là bản biên soạn thử nghiệm để giáo viên thẩm định, không phải sách giáo khoa được phê duyệt hay kết quả dạy thử trẻ em.

## Quyết định

Giả định lớp 1 khoảng 6 tuổi, đầu vào đọc và toán chưa đồng đều, dạy bằng tiếng Việt với giáo viên, đồ dùng rẻ và bản in. Không yêu cầu thiết bị hay AI cho học sinh. Quy mô lớp 30-35 em là giả định thiết kế. Khung cả năm: 35 tuần, 105 tiết, 35 phút/tiết. Phân phối bài và học kì là đề xuất, không gán là phân phối chương trình chính thức của một bộ sách.

Đọc trực tiếp Chương trình môn Toán và Chương trình tổng thể 2018 từ bản PDF của Bộ trên website trường thuộc mạng giáo dục; xem ảnh các trang bảng liên quan. Đọc Điều 6-8 TT27/2020 trên bản toàn văn tái đăng; TT17/2025 Điều 1; thông báo SGK 2026-2027 của NXBGDVN. Không suy diễn đã đọc toàn bộ SGK hay toàn bộ lịch sử sửa đổi văn bản.

## Các bước

- [x] Xác minh repo, đọc prompt, blueprint, rubric và context.
- [x] Nghiên cứu chuẩn, thời lượng, đánh giá và bối cảnh SGK hiện hành.
- [x] Lập bản đồ yêu cầu, giáo trình 105 tiết, hoạt động, đáp án, giáo án mẫu và đánh giá.
- [x] Kiểm tra độ phủ, tiên quyết, thời lượng, đáp án, phạm vi và khả năng học không cần đọc thành thạo.
- [x] Chạy thử đầu vào lỗi; sửa các thiếu sót workflow có bằng chứng.
- [x] Kiểm tra hồi quy; ghi nhận phần đã kiểm tra và phần cần giáo viên/học sinh thật.

## Phát hiện trực tiếp từ baseline

Blueprint 1.0 chỉ có locale_and_curriculum dạng văn bản và không có danh sách chuẩn độc lập, ánh xạ chuẩn-bài-tác vụ, lịch tiết hoặc quy tắc phạm vi môn học. Rubric chưa có tình huống vượt lớp do lấy ví dụ của cả cấp học. Tài liệu S2 hiện có ví dụ nhân/chia và phương trình dành cho bối cảnh rộng; không được đưa thẳng vào Toán lớp 1. Quy định mọi hinge phải có 3-4 đáp án nhiễu xung đột với đánh giá thao tác/nói phù hợp người mới học đọc; sẽ giới hạn quy định đó cho câu trắc nghiệm.

## Phạm vi thay đổi

Tạo gói khóa học riêng trong courses/vi-vn-grade-1-math, các thẻ nguồn Việt Nam và công cụ kiểm tra có phạm vi công bố rõ. Tái sử dụng bộ đọc YAML chặt chẽ; giữ nguyên runtime phân số và dữ liệu phiên. Không tái cấu trúc toàn bộ corpus. Các worker trước đó lỗi khởi động chưa được khắc phục; đánh giá lần này do trợ lý thực hiện, không gán là thẩm định độc lập.

## Kết quả

98 tests pass; 105 tiết, 24 yêu cầu, 111 đáp án khai báo được tính lại và 14 tác vụ có tiêu chí quan sát. Registry/link audit không có lỗi. Đã sửa một câu học sinh dùng cm trước khi dạy đơn vị này; đó là phát hiện nội dung ngoài khả năng kiểm của tham chiếu/số học. Xem [báo cáo workflow](../../courses/vi-vn-grade-1-math/workflow-evaluation.md) và final-checks.json. SGK/trang sách, giáo viên thẩm định, hình/phiếu dùng cho trẻ và hiệu quả học tập còn cần kiểm chứng thực tế; không trình bày là đã hoàn tất các bước đó.
