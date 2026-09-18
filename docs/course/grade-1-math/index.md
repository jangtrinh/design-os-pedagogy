# Giáo trình thử nghiệm Toán lớp 1 Việt Nam

Phiên bản biên soạn: 17/09/2026. Dùng để kiểm tra course-design workflow của Agent Teacher. Đây là giáo trình mẫu dành cho giáo viên thẩm định và điều chỉnh, không phải SGK đã được Bộ phê duyệt, không thay kế hoạch giáo dục của trường.

> Bản chụp ngày 17/09/2026 của `courses/vi-vn-grade-1-math` để đọc trên web. Dữ liệu có cấu trúc (YAML) nằm trong repository.

## Bộ tài liệu

| Tài liệu | Công dụng |
| --- | --- |
| [Hướng dẫn giáo viên](teacher-guide.md) | Mục tiêu, tổ chức lớp, 12 chủ đề, tám giáo án minh họa và hỗ trợ phân hóa |
| [Lịch 35 tuần và 105 phiếu tiết học](lessons.md) | Mỗi tiết có bài mẫu, luyện tập, đáp án, câu kiểm tra và đồ dùng |
| [Hai đề mẫu và hồ sơ đánh giá](assessment.md) | Đề HKI, cuối năm, đáp án/tiêu chí, nhận xét và điều kiện sử dụng |
| [Bản đồ yêu cầu cần đạt](https://github.com/jangtrinh/design-os-pedagogy/blob/main/courses/vi-vn-grade-1-math/requirements.yaml) | 24 mã phân rã do người biên soạn tạo, với trang nguồn và giới hạn nội dung |
| [Course blueprint](https://github.com/jangtrinh/design-os-pedagogy/blob/main/courses/vi-vn-grade-1-math/course.yaml) | Đầu vào, giả định, ánh xạ yêu cầu-mục tiêu-luyện tập-đánh giá và tiên quyết |
| [Dữ liệu học kì I](https://github.com/jangtrinh/design-os-pedagogy/blob/main/courses/vi-vn-grade-1-math/sessions-sem1.yaml), [học kì II](https://github.com/jangtrinh/design-os-pedagogy/blob/main/courses/vi-vn-grade-1-math/sessions-sem2.yaml), [đề kiểm tra](https://github.com/jangtrinh/design-os-pedagogy/blob/main/courses/vi-vn-grade-1-math/assessments.yaml) | Dữ liệu có cấu trúc để kiểm tra và tái xuất bản |
| [Đánh giá workflow](workflow-evaluation.md) | Phát hiện thực tế, điều đã sửa, kết quả kiểm tra và phần chưa được kiểm chứng |

## Phạm vi và giả định

35 tuần, 3 tiết/tuần, 35 phút/tiết: tổng 105 tiết, 3.675 phút. Dự kiến học kì I 54 tiết và học kì II 51 tiết; phân phối học kì/tuần là đề xuất để trường điều chỉnh. Các giờ ôn, đánh giá, phản hồi, vận dụng đã nằm trong 105 tiết.

Người học là học sinh lớp 1 khoảng 6 tuổi, chưa giả định biết đọc thành thạo hay đã biết phép tính. Giáo viên đọc yêu cầu; học sinh có thể chỉ, nói, thao tác hoặc viết số tùy mục tiêu. Lớp 30-35 em là giả định thiết kế. Đồ dùng gồm que/bó chục, thẻ, khung mười ô, hình/khối, thước cm, đồng hồ và lịch mẫu. Không yêu cầu thiết bị, internet hoặc tài khoản AI cho học sinh.

Không có bài tập bắt buộc ngoài lớp. Hoạt động gia đình ngắn, nếu có, là tự chọn và không được dùng làm điều kiện học bài sau.

## Căn cứ

Đối chiếu [Chương trình môn Toán lớp 1](../../60-evidence/sources/evidence-vn-2018-grade1-mathematics.md), [TT27/2020 về đánh giá](../../60-evidence/sources/evidence-vn-2020-primary-assessment.md) và [thông báo SGK năm học 2026-2027](../../60-evidence/sources/evidence-vn-2026-textbook-context.md). Các thẻ nguồn ghi rõ URL, trang/điều, phiên bản và phần đã đọc. Chưa đối chiếu trang/bài với toàn bộ SGK đang dùng ở một trường; không có số trang SGK được tự điền.

Nội dung lõi gồm số đến 100; cộng/trừ không nhớ trong phạm vi quy định, nhẩm đến 10 và nhẩm số tròn chục; tình huống cộng/trừ; hình phẳng, khối, vị trí; đo độ dài, giờ đúng, tuần và lịch tờ; thực hành/trải nghiệm. Không biến nhân, chia, phân số, phương trình x, cộng nhớ/trừ mượn hoặc đọc phút thành yêu cầu bắt buộc lớp 1.

## Chạy kiểm tra

Tại gốc repo:

```sh
.venv/bin/python -B tools/course_audit.py courses/vi-vn-grade-1-math
.venv/bin/python -B -m unittest discover -s tests -p 'test_course_audit.py' -v
```

Công cụ kiểm tra lịch, tham chiếu, phạm vi đã mã hóa và các đáp án có cấu trúc. Nó không kiểm chứng toàn bộ ý nghĩa câu chữ/hình ảnh hoặc kết quả học của trẻ. Giáo viên và người học thật chưa tham gia đánh giá trong lần biên soạn này.
