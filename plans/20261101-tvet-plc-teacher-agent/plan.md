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
- [x] Research các câu hỏi mở (phần cứng/phần mềm, quy định đào tạo nghề): [`source-notes/05`](source-notes/05-hardware-software-facts.md), [`source-notes/06`](source-notes/06-tvet-regulations.md), tóm tắt ở [agent-design §7](agent-design.md#7-câu-hỏi-mở-đã-research-chờ-giáo-viên-xác-nhận).
- [x] P1: khóa học [`courses/vi-vn-tvet-plc-logo-zen/`](../../courses/vi-vn-tvet-plc-logo-zen/README.md), `tools/course_support/vocational/` (planner + audit `course-audit-vocational-1.0`), `tools/plan_schedule.py`, `tools/vocational_audit.py`, `tests/test_vocational_course.py` (22 test). Toàn bộ suite: 120 test qua.
- [x] P3 (thử nghiệm): giáo trình web tại `docs/course/plc-logo-zen/` (bản học viên) và bản giáo viên dựng ra `.data/`; nội dung B1–B3, giáo án W01–W03, 88 thuật ngữ; audit nội dung `tvet-content-1.0`; 16 test site. Toàn bộ suite: 136 test qua. Rà soát kỹ thuật đã sửa 3 lỗi của agent: thao tác menu LOGO! 8 (ESC, không phải tổ hợp ba phím), điện áp "ma" do đồng hồ số trở kháng cao, và tiêu chí chấm "động cơ chạy lại sau mất nguồn" (đổi thành không tự khởi động).
- [ ] P2 (giáo viên kiểm chứng lab trên kit), P3 cho các bài B4–B9, P4 xếp lại lịch từ "Rút kinh nghiệm", P5 mở rộng mô đun khác.

## Acceptance

Bộ nguồn được mô tả có vị trí trích dẫn. Chênh lệch giữa lịch và chương trình được nêu rõ. Mức đầy đủ của giáo trình theo từng bài có bằng chứng. Thiết kế tách nội dung khỏi thời gian, có bất biến kiểm được và phân tầng model có lý do. Không có nội dung suy luận nào được trình bày như đã kiểm chứng.

## Limits

Các bản trích xuất là đầu ra AI, chưa có chuyên gia PLC hay giáo viên duyệt. Agent tầng Haiku và Sonnet chỉ mở một số ảnh có giới hạn. Một số hộp thoại phần mềm ZEN (image124–126) không đọc được. Tên tiếng Anh đánh dấu `*` trong ghi chú Ch.2 lấy từ hiểu biết chung về LOGO! Manual, chưa đối chiếu manual. P1 chỉ kiểm cấu trúc, thứ tự, thời lượng và thiết bị. Chưa có giáo án hay phiếu học tập nào được sinh (P3), và chưa có lab nào được giáo viên kiểm chứng (P2). `schedule-cd9-k5.json` là bản số hóa đầu tiên; bản dùng thật là `courses/vi-vn-tvet-plc-logo-zen/schedules/cd9-k5-2026.yaml`. Lỗi trong dữ liệu lab do Haiku soạn (ZEN-LAB-2 thiếu đường reset timer) đã được phát hiện khi rà soát và sửa lại.
