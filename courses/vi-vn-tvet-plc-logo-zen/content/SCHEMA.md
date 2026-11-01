# Hợp đồng nội dung `tvet-content-1.0`

Nội dung do agent soạn nằm trong `content/`. Bộ dựng `tools/render_course_site.py` biến nó thành trang web: bản **học viên** (công khai) và bản **giáo viên** (có giáo án, đáp án). `tools/vocational_audit.py --content` kiểm các ràng buộc dưới đây.

Mọi tệp là JSON hợp lệ (đuôi `.yaml` giống phần còn lại của khóa học), UTF-8, không có khóa trùng. Văn bản viết bằng tiếng Việt; thuật ngữ tiếng Anh để trong ngoặc. Trường `*_md` là Markdown thuần, **không có HTML thô**. Không chép nguyên văn giáo trình nội bộ, mà viết lại và dẫn mục nguồn.

## 1. `content/lessons/<lesson_id>.yaml`: một bài trong giáo trình web

```json
{
  "content_version": "tvet-content-1.0",
  "lesson_id": "B1",
  "status": "draft",
  "authoring": {"model_tier": "sonnet", "date": "2026-11-01", "source_notes": ["source-notes/01-logo-hardware.md"]},
  "summary": "1–2 câu: bài này giúp người học làm được gì.",
  "objectives": ["Câu bắt đầu bằng động từ đo được, góc nhìn người học."],
  "sections": [
    {
      "id": "B1-s1",
      "title": "Tiêu đề mục",
      "items": ["1.1"],
      "body_md": "Giải thích ngắn, chia đoạn. Có ví dụ cụ thể và số liệu kỹ thuật kèm điều kiện.",
      "table": {"caption": "…", "columns": ["Cột 1", "Cột 2"], "rows": [["…", "…"]]},
      "widget": {"kind": "logic-sim", "title": "…", "spec": {}},
      "checks": [
        {"id": "B1-c1", "kind": "mcq", "prompt": "…", "options": ["…", "…", "…"], "answer": 1,
         "feedback": ["Vì sao A sai…", "Vì sao B đúng…", "Vì sao C sai…"], "misconception": "tùy chọn"}
      ]
    }
  ],
  "worked_examples": [
    {"id": "B1-we1", "title": "…", "problem": "…", "fading": "full",
     "steps": [{"text": "Bước đầy đủ."}, {"text": "Bước người học tự làm.", "blank": true, "prompt": "Gợi ý cho bước trống"}]}
  ],
  "practice": {
    "lab_id": "LOGO-PRAC-1",
    "brief_md": "Nhiệm vụ thực hành, viết cho người học.",
    "steps": ["Bước an toàn trước tiên", "…"],
    "self_check": ["Tiêu chí tự kiểm (diễn đạt lại rubric của lab cho người học)"]
  },
  "self_test": [{"id": "B1-t1", "kind": "mcq", "prompt": "…", "options": ["…"], "answer": 0, "feedback": ["…"]}]
}
```

Ràng buộc:
- `id` duy nhất trong toàn khóa. `items` lấy từ nhãn mục trong lịch (ví dụ `"1.1"`, `"2.3"`).
- `table`, `widget`, `checks` là tùy chọn. Mỗi mục nên có ít nhất 1 câu `checks`. `self_test` có 4–6 câu.
- MCQ: 3–4 lựa chọn; `answer` là chỉ số hợp lệ; `feedback` có đúng một câu giải thích cho mỗi lựa chọn. Đáp án sai phải là lỗi hiểu thật sự hay gặp, không phải lựa chọn vô lý.
- `worked_examples[].fading`: `full` (mọi bước có lời giải) hoặc `completion` (có ít nhất một bước `blank: true` kèm `prompt`). Theo thứ tự bài, ví dụ đầu nên `full`, các ví dụ sau `completion`.
- `practice.lab_id` phải là một lab của bài trong `course.yaml`. **Không** đưa lời giải hay logic chương trình của lab vào phần học viên. Lời giải chỉ nằm trong `course.yaml → labs[].solution_outline`, và chỉ hiện ở bản giáo viên.

### Widget `logic-sim`

Mô phỏng khối FBD kiểu LOGO! chạy trong trình duyệt. Chỉ dùng cho ví dụ minh họa, **không** dùng cho lời giải lab.

```json
{"inputs": [{"id": "I1", "label": "S1 – nút nhấn", "mode": "momentary"}, {"id": "I2", "label": "S2", "mode": "toggle"}],
 "blocks": [{"id": "B001", "type": "OR", "in": ["I1", "I2"]},
            {"id": "B002", "type": "ONDELAY", "in": ["B001"], "T": 3}],
 "outputs": [{"id": "Q1", "label": "Đèn H1", "from": "B002"}],
 "chart": ["I1", "B001", "Q1"]}
```

- Loại khối: `AND`, `OR`, `NAND`, `NOR`, `XOR` (danh sách `in`); `NOT` (`in` một phần tử); `RS` (`S`, `R`; R ưu tiên); `ONDELAY`, `OFFDELAY` (`in` một phần tử, `T` tính bằng giây); `PULSE` (bật/tắt luân phiên ở mỗi cạnh lên của `in`).
- Tham chiếu được: id ngõ vào, id khối, id ngõ ra (dùng giá trị của chu kỳ trước, để tự giữ), `"hi"`, `"lo"`.
- `chart` là tùy chọn: các tín hiệu vẽ giản đồ thời gian khoảng 15 giây gần nhất.

## 2. `content/sessions/<session_id>.yaml`: giáo án một buổi (chỉ hiện ở bản giáo viên)

```json
{
  "content_version": "tvet-content-1.0",
  "session_id": "W01",
  "status": "draft",
  "authoring": {"model_tier": "sonnet", "date": "2026-11-01"},
  "title_line": "Bài 1: Giới thiệu chung về PLC LOGO",
  "lesson_section_ids": ["B1-s1", "B1-s2"],
  "objectives": {"knowledge": ["…"], "skills": ["…"], "attitude": ["…"]},
  "materials": ["…"],
  "organization": "Tập trung lớp hướng dẫn ban đầu; chia nhóm theo số kit (tối đa 18 người/nhóm thực hành)",
  "phases": [
    {"kind": "on_dinh_lop", "minutes": 10, "content": ["Nhắc nội quy xưởng"], "teacher": ["…"], "student": ["…"],
     "retrieval_questions": ["Câu hỏi kiểm tra bài cũ (buổi đầu: kiểm tra kiến thức nền Khí cụ điện/Trang bị điện)"]},
    {"kind": "dan_nhap", "minutes": 5, "content": ["…"], "teacher": ["…"], "student": ["…"]},
    {"kind": "gioi_thieu_chu_de", "minutes": 5, "content": ["…"], "teacher": ["…"], "student": ["…"]},
    {"kind": "giai_quyet_van_de", "minutes": 175, "content": ["…"], "teacher": ["…"], "student": ["…"],
     "steps": [
       {"mode": "i_do", "minutes": 20, "title": "GV làm mẫu …", "teacher": ["…"], "student": ["…"], "lesson_section_ids": ["B1-s1"]},
       {"mode": "check", "minutes": 5, "title": "Câu hỏi bản lề", "teacher": ["…"], "student": ["…"], "check_ids": ["B1-c1"]},
       {"mode": "we_do", "minutes": 30, "title": "…", "teacher": ["…"], "student": ["…"]},
       {"mode": "you_do", "minutes": 120, "title": "…", "teacher": ["…"], "student": ["…"], "lab_id": "LOGO-PRAC-1"}
     ]},
    {"kind": "ket_thuc_van_de", "minutes": 15, "content": ["Chấm sản phẩm theo phiếu", "…"], "teacher": ["…"], "student": ["…"]},
    {"kind": "huong_dan_tu_hoc", "minutes": 5, "content": ["…"], "teacher": ["…"], "student": ["…"]}
  ],
  "teacher_notes": ["An toàn, hiểu lầm cần để ý, điều phải tự kiểm trên kit trước giờ dạy"]
}
```

Ràng buộc:
- Dãy `phases` (kind, minutes) phải **trùng khít** với `sessions/cd9-k5-2026.yaml → phases` của buổi đó. Phút đã tính theo quy tắc 45/60.
- Tổng `steps[].minutes` bằng `minutes` của pha `giai_quyet_van_de`. `mode` thuộc `i_do`, `we_do`, `you_do`, `check`. Phải có ít nhất một bước `you_do` gắn `lab_id` khi buổi có giờ thực hành.
- `lesson_section_ids`, `check_ids`, `lab_id` phải tồn tại.
- `teacher` và `student` là danh sách hành động cụ thể. Cột học sinh không được chỉ là "Lắng nghe, ghi nhận". Mỗi pha có ít nhất một hoạt động chủ động (làm, trả lời, đo, giải thích, kiểm tra chéo).

## 3. `content/glossary.yaml`

```json
{"content_version": "tvet-content-1.0", "terms": [
  {"vi": "Ngõ vào số", "en": "digital input", "definition": "…", "lesson_ids": ["B1"], "platform": "logo|zen|chung"}]}
```
