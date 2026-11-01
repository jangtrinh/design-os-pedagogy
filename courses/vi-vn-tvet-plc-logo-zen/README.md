# Điều khiển lập trình cỡ nhỏ (PLC LOGO!, ZEN): khóa học nghề theo lịch trình

Trạng thái: `draft`. Đây là khung khóa học (pha P1). Chưa có giáo án hay phiếu học tập nào được sinh ra, và chưa có lời giải lab nào được giáo viên kiểm chứng. Nghiên cứu và thiết kế nằm ở [`plans/20261101-tvet-plc-teacher-agent/`](../../plans/20261101-tvet-plc-teacher-agent/plan.md).

## Tệp

| Tệp | Vai trò | Ai sửa |
|---|---|---|
| `course.yaml` | Chương trình mô đun: bài học, giờ chuẩn LT/TH, điều kiện tiên quyết, thiết bị, chuẩn đầu ra, bài thực hành (lab), đánh giá, chính sách thời gian, chấm điểm, sĩ số, giả định phần cứng, nguồn | Người soạn khóa học |
| `schedules/cd9-k5-2026.yaml` | Lịch trình của một lớp trong một học kỳ, kèm danh sách `exceptions` | Giáo viên, khi lịch thay đổi |
| `sessions/cd9-k5-2026.yaml` | Các buổi đã ghép (khối nội dung, số giáo án, bài học trước, khung phút theo pha giáo án). **Tệp sinh tự động** | `tools/plan_schedule.py` |

Các tệp `.yaml` thực chất là JSON (một tập con của YAML), đọc bằng bộ nạp nghiêm ngặt `tools/knowledge/frontmatter.py`.

## Quy trình

```bash
# Xếp lịch, xem thay đổi so với bản đã lưu, kiểm định; chỉ ghi khi audit qua
python3 tools/plan_schedule.py courses/vi-vn-tvet-plc-logo-zen \
  --schedule schedules/cd9-k5-2026.yaml --sessions sessions/cd9-k5-2026.yaml --write

# Kiểm định chỉ đọc
python3 tools/vocational_audit.py courses/vi-vn-tvet-plc-logo-zen \
  --schedule schedules/cd9-k5-2026.yaml --sessions sessions/cd9-k5-2026.yaml
```

### Khi lịch thay đổi

Thêm một mục vào `exceptions` của tệp lịch. Mỗi mục bắt buộc có `reason`. Sau đó chạy lại `plan_schedule.py`. Mục `changes` trong kết quả cho biết những buổi nào cần soạn lại giáo án.

| `kind` | Trường | Ý nghĩa |
|---|---|---|
| `cancel_session` | `week` | Nghỉ buổi của tuần đó |
| `set_hours` | `week`, `hours` | Đổi số giờ của buổi (bội số 0,25) |
| `add_session` | `start`, `hours`, `equipment_ids?` | Buổi học bù |
| `equipment_unavailable` | `week`, `equipment_ids` | Thiếu thiết bị trong tuần đó |
| `extend_lesson` | `lesson_id`, `block_kind`, `hours` | Thêm giờ cho một bài, ví dụ khi "Rút kinh nghiệm" ghi lớp chậm |

Quy tắc xếp:
- Giữ thứ tự khối của lịch gốc. Không có ngoại lệ thì kết quả trùng lịch gốc.
- Khối lý thuyết và thực hành được tách theo bước 15 phút. Bài kiểm tra không bị tách.
- Một bài chỉ bắt đầu khi các bài tiên quyết đã xong. Bài kiểm tra chỉ diễn ra sau khi phạm vi của nó đã dạy xong.
- Thi kết thúc mô đun được **ghim** vào tuần của lịch gốc. Kiểm tra định kỳ thì được dời theo nội dung.
- Thiếu giờ thì planner **không cắt bớt nội dung**. Nó liệt kê `unscheduled` và audit báo lỗi, để giáo viên chọn giữa thêm buổi bù và bỏ bớt nội dung.

## Bất biến audit (`course-audit-vocational-1.0`)

- Tổng giờ của lịch khớp chương trình mô đun: 14 LT, 42 TH (gồm KTĐK), 4 giờ thi. Giờ từng bài lệch chương trình thì chỉ cảnh báo `PROGRAM_DEVIATION`.
- Kế hoạch buổi phải được sinh từ đúng nội dung lịch hiện tại (`STALE_PLAN`). Mọi khối đều có chỗ (`UNSCHEDULED`, `COVERAGE`). Số giáo án và "bài học trước" khớp thứ tự buổi.
- Tổng phút các pha bằng thời lượng buổi theo `time_policy`: lý thuyết 45 phút/giờ, thực hành và kiểm tra 60 phút/giờ. Pha thuộc tập đóng và đúng thứ tự của mẫu giáo án. Phút kiểm tra bằng thời lượng bài kiểm tra.
- Thứ tự tiên quyết, phạm vi kiểm tra, thiết bị trong tuần, sức chứa của buổi.
- Bài có giờ thực hành phải có lab. Mỗi lab có yêu cầu, ít nhất 3 tiêu chí chấm, mục an toàn, cặp "sai hỏng – khắc phục", trạng thái kiểm chứng. Lời giải `inferred` không được đánh dấu đã kiểm chứng nếu không ghi người kiểm chứng.
- `learning_effectiveness` luôn là `not_assessed`.

Audit không chạy chương trình PLC, không đánh giá sơ đồ đấu dây đúng hay sai, và không đánh giá chất lượng văn bản.

## Giả định đang dùng (chờ giáo viên xác nhận)

- Phần cứng: LOGO! 12/24RCE + 1 DM8 12/24R; ZEN-10C1AR-A-V2. Xem `course.yaml → hardware_assumptions`.
- Kiểm tra định kỳ: 1 giờ thực hành mỗi lần, tách khỏi 4 giờ TH của tuần 10 và 14 (`duration_basis: assumed`).
- Xưởng có cả hai bộ kit suốt học kỳ (`calendar.available_equipment_ids`).
- Quy định đào tạo nghề tham chiếu theo trích đoạn. Các trang luật không truy cập được trong phiên nghiên cứu (xem `source-notes/06`).
