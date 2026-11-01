# Teacher agent cho mô đun nghề: nghiên cứu nguồn PLC LOGO!/ZEN

Ngày: 1 November 2026. Project: Agent Teacher.

## Objective

Nghiên cứu ba tài liệu thật của một mô đun cao đẳng nghề: lịch trình giảng dạy, mẫu giáo án và tài liệu giảng dạy "Điều khiển lập trình cỡ nhỏ". Từ đó thiết kế một teacher agent soạn giáo án và tài liệu học viên bám theo lịch trình, và xếp lại khi lịch thay đổi.

## Decisions

- Điều phối nhiều tầng model. Việc tất định (chuyển đổi, kiểm tổng giờ) do script làm. Haiku trích xuất có cấu trúc. Sonnet đọc sơ đồ, suy luận lab và khảo sát repo. Opus kiểm chứng, đối chiếu và thiết kế.
- Không lưu tài liệu gốc (lưu hành nội bộ) và tên giáo viên trong repo. Chỉ lưu bản phân tích, có vị trí trích dẫn.
- Không sửa audit lớp 1. Đào tạo nghề sẽ có hợp đồng audit riêng (xem [agent-design §5](agent-design.md#5-tích-hợp-vào-repo)).
- Mọi lời giải lab do AI suy luận đều gắn nhãn `[SUY LUẬN]` / `[SUY RA]`, và chỉ được dùng cho học viên sau khi giáo viên kiểm chứng trên kit.

## Work

- [x] Chuyển .doc/.docx sang Markdown, tách 146 ảnh, chia giáo trình thành 4 chunk.
- [x] Trích xuất song song bằng 5 subagent (2 Haiku, 3 Sonnet), lưu ở [`source-notes/`](source-notes/).
- [x] Kiểm chứng trực tiếp phát hiện then chốt: các mục sơ đồ và chương trình của lab 3.x đúng là dòng chấm trống.
- [x] Số hóa lịch trình thành [`schedule-cd9-k5.json`](schedule-cd9-k5.json). Script đã kiểm 14 LT + 46 TH, 15 tuần, mỗi tuần 4 giờ, kết thúc 19/12/2026.
- [x] Tổng hợp [research.md](research.md) và thiết kế [agent-design.md](agent-design.md).
- [ ] P1–P5 theo lộ trình trong agent-design §6. Cần giáo viên trả lời các câu hỏi ở §7 trước P2.

## Acceptance

Bộ nguồn được mô tả có vị trí trích dẫn. Chênh lệch giữa lịch và chương trình được nêu rõ. Mức đầy đủ của giáo trình theo từng bài có bằng chứng. Thiết kế tách nội dung khỏi thời gian, có bất biến kiểm được và phân tầng model có lý do. Không có nội dung suy luận nào được trình bày như đã kiểm chứng.

## Limits

Các bản trích xuất là đầu ra AI, chưa có chuyên gia PLC hay giáo viên duyệt. Agent tầng Haiku và Sonnet chỉ mở một số ảnh có giới hạn. Một số hộp thoại phần mềm ZEN (image124–126) không đọc được. Tên tiếng Anh đánh dấu `*` trong ghi chú Ch.2 lấy từ hiểu biết chung về LOGO! Manual, chưa đối chiếu manual. Chưa có mã, schema hay test nào được thêm. Đây là pha nghiên cứu và thiết kế.
