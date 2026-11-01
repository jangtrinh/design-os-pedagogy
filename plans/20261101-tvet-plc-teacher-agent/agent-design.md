# Thiết kế: Teacher agent soạn giáo án và tài liệu học viên theo lịch trình

Ngày: 2026-11-01. Trạng thái: **đề xuất**, chưa triển khai. Dựa trên [research.md](research.md).

## 1. Mục tiêu và phạm vi

Giáo viên đưa vào một **lịch trình giảng dạy**, cộng với **chương trình mô đun, giáo trình và mẫu giáo án** của trường. Agent tạo ra cho từng buổi:

| Đầu ra | Người dùng | Ghi chú |
|---|---|---|
| Giáo án theo đúng mẫu trường (GA20) | GV, Trưởng bộ môn | Xuất Markdown trước; docx theo mẫu là bước sau |
| Phiếu hướng dẫn thực hành / phiếu học tập | Sinh viên | Không chứa đáp án |
| Phiếu chấm sản phẩm (checklist + cổng an toàn) | GV | Dùng trong mục "Kết thúc vấn đề" |
| Đáp án / lời giải tham khảo | Chỉ GV | Kèm nhãn trạng thái kiểm chứng |
| Câu hỏi kiểm tra bài cũ, câu hỏi chẩn đoán | GV | Lấy từ ngân hàng câu hỏi theo bài |
| Đề KTĐK, đề thi kết thúc + đáp án, thang điểm | GV | Chỉ hỏi phần đã dạy tính đến tuần đó |

Khi lịch đổi (nghỉ đột xuất, dời tuần, đổi số giờ, thiếu kit, lớp chậm tiến độ theo "Rút kinh nghiệm"), agent **xếp lại**. Nó chỉ sinh lại các buổi bị ảnh hưởng và báo phần chênh lệch so với chương trình.

Không thuộc phạm vi: tự quyết định thay chương trình mô đun; phát lời giải chưa kiểm chứng cho sinh viên; tuyên bố hiệu quả học tập (theo quy ước repo: `learning_effectiveness: not_assessed`).

## 2. Mô hình dữ liệu

Ý chính: **nội dung** và **thời gian** là hai lớp riêng. Bộ xếp lịch ghép chúng thành **buổi học**.

```
schedule.json  ──┐
                 ├─► planner (tất định) ─► sessions/W{nn}.json ─► generators (LLM) ─► audit ─► render (md/docx)
course.yaml   ───┤                                                      ▲
content units ───┘                       feedback/W{nn}.md (Rút kinh nghiệm) ┘
```

| Tệp | Nội dung | Ổn định qua các khóa? |
|---|---|---|
| `schedule.json` | Lịch, các tuần, giờ LT/TH, ngoại lệ, thiết bị, mốc kiểm tra. Mẫu: [`schedule-cd9-k5.json`](schedule-cd9-k5.json) | Không (mỗi lớp, mỗi học kỳ) |
| `course.yaml` | Mục tiêu mô đun, danh sách bài, giờ chuẩn LT/TH, DAG điều kiện tiên quyết, chuẩn đầu ra ↔ đánh giá. Theo khuôn `docs/templates/course-blueprint.yaml` | Có |
| `units/*.yaml` | Đơn vị nội dung nguyên tử (ví dụ `LOGO-1.2.1`, `LOGO-SF-ONDELAY`, `LOGO-LAB-2`): khái niệm, thuật ngữ, mức Bloom, phút ước tính LT/TH, tiên quyết, hiểu lầm kèm câu hỏi chẩn đoán, nguồn (chương/mục) | Có |
| `labs/*.yaml` | Đặc tả lab: yêu cầu, bảng I/O, logic, tiêu chí chấm, biến thể, sai hỏng, an toàn, `verification: draft / teacher_verified / used_in_class`, tệp chương trình (.lsc, .zen) khi có | Có |
| `sessions/W{nn}.json` | Bản ghi buổi đã ghép: các khối nội dung, phút, các pha GA, liên kết lab và đánh giá | Không (sinh ra) |
| `feedback/W{nn}.md` | "III. Rút kinh nghiệm" GV ghi sau buổi, cộng tiến độ thực tế | Không |

Ví dụ bản ghi buổi (rút gọn) cho tuần 3:

```json
{"id":"W03","week":3,"date_range":["2026-09-21","2026-09-26"],"ga_number":3,
 "previous_lesson":"Bài 2: Các lệnh cơ bản lập trình cho PLC LOGO",
 "lesson_id":"B3","items":["3.1","3.2","3.3","3.4"],"minutes":{"theory":60,"practice":180},
 "objectives":{"knowledge":["..."],"skills":["..."],"attitude_safety":["..."]},
 "materials":["Máy vi tính","LOGO!Soft Comfort V8.4","Kit LOGO!"],
 "organization":"Tập trung lớp hướng dẫn ban đầu; chia nhóm theo số kit",
 "phases":[
  {"kind":"on_dinh_lop","minutes":10,"retrieval_check":"..."},
  {"kind":"dan_nhap","minutes":5,"teacher":"...","student":"..."},
  {"kind":"gioi_thieu_chu_de","minutes":5},
  {"kind":"giai_quyet_van_de","minutes":195,"steps":[
     {"mode":"i_do","minutes":20,"unit":"LOGO-LAB-1","worked_example":"full"},
     {"mode":"we_do","minutes":35,"hinge_question":"..."},
     {"mode":"you_do","minutes":140,"task":"LOGO-LAB-1.req","rubric":"LOGO-LAB-1.rubric","safety_gate":true}]},
  {"kind":"ket_thuc_van_de","minutes":20},
  {"kind":"huong_dan_tu_hoc","minutes":5}],
 "handout":"handouts/W03.md","answer_key":{"ref":"labs/LOGO-LAB-1.yaml","verification":"draft"}}
```

## 3. Quy trình và phân tầng model

| Giai đoạn | Việc | Ai làm | Lý do |
|---|---|---|---|
| 0. Nạp | .doc/.docx → Markdown, tách ảnh, chia chunk theo đề mục | Script (soffice, pandoc) | Tất định, không tốn token |
| 1. Trích lịch | Bảng lịch → `schedule.json` | **Haiku**, sau đó script kiểm tổng giờ | Bảng có cấu trúc. Script bắt lỗi |
| 2. Trích nội dung | Chunk → `units/*.yaml` (khái niệm, thuật ngữ, số liệu) | **Haiku**, song song theo chunk | Trích xuất, ít suy luận |
| 3. Đọc sơ đồ, soạn lab | Ảnh nối dây và chương trình → bảng I/O, logic, tiêu chí, biến thể, sai hỏng | **Sonnet** | Cần đọc ảnh và suy luận kỹ thuật |
| 4. Kiến trúc khóa | Mục tiêu, DAG, ánh xạ chuẩn đầu ra ↔ đánh giá, chiến lược làm mẫu rồi rút dần qua các lab, thiết kế đề | **Opus**, một lần mỗi mô đun | Quyết định có đánh đổi, ít lần gọi |
| 5. Xếp lịch | Ghép đơn vị nội dung vào buổi theo ràng buộc | **Script** (không LLM) | Lặp lại được, kiểm thử được |
| 6. Sinh buổi | Điền GA (hoạt động GV/SV, câu hỏi, chia pha), phiếu học tập, phiếu chấm | **Sonnet** mỗi buổi. Câu hỏi lấy từ ngân hàng ở bước 2 | Khối lượng lớn nhất, cần chất lượng sư phạm vừa đủ |
| 7. Kiểm định | Bất biến ở §4 | **Script** | Tất định |
| 8. Rà soát | Đọc chéo các lab `draft` và đề thi, đối chiếu với nguồn | **Opus**, chỉ ở chỗ rủi ro cao | Chỉ dùng khi có lỗi kỹ thuật hay an toàn |
| 9. Xếp lại lịch | Đọc `feedback/` và thay đổi lịch, đề xuất phương án | Script tính các phương án hợp lệ. **Sonnet** tóm tắt cho GV. **Opus** chỉ khi có xung đột phải đánh đổi (ví dụ cắt bài nào) | Đa số thay đổi là dời tuần thuần túy |
| 10. Xuất | Markdown → docx theo mẫu trường | Script (pandoc với reference.docx, hoặc python-docx) | Tất định |

Ước lượng một mô đun 15 buổi: bước 2–4 chạy **một lần** (tái dùng cho mọi lớp). Mỗi lớp mới chỉ tốn bước 1 (Haiku) cộng bước 6 (15 lần Sonnet). Mỗi lần xếp lại chỉ sinh lại các buổi bị ảnh hưởng.

## 4. Bất biến kiểm định (bản cho đào tạo nghề, tách khỏi audit lớp 1)

1. Tổng giờ LT và TH theo `schedule.json` khớp tổng các buổi. Mỗi buổi đúng `session_hours × 60` phút (240). Tổng phút các pha GA bằng thời lượng buổi.
2. Loại pha nằm trong tập đóng: `on_dinh_lop`, `dan_nhap`, `gioi_thieu_chu_de`, `giai_quyet_van_de`, `ket_thuc_van_de`, `huong_dan_tu_hoc`.
3. Thứ tự buổi tôn trọng DAG tiên quyết. Mọi bài kiểm tra chỉ hỏi đơn vị đã dạy trước tuần đó.
4. Mỗi pha thực hành có `rubric`, `safety_gate` và `sai_hong` (sai hỏng thường gặp).
5. Phiếu học viên không chứa đáp án. Lời giải `verification: draft` không xuất hiện trong tài liệu học viên.
6. "Bài học trước" và số giáo án khớp thứ tự buổi sau khi xếp lại.
7. Thiết bị yêu cầu của buổi nằm trong danh sách thiết bị của tuần đó (ví dụ không giao lab ZEN vào tuần chỉ có kit LOGO).
8. Phần chênh lệch giờ giữa lịch và chương trình mô đun được **báo cáo**, không tự sửa.

## 5. Tích hợp vào repo

Theo báo cáo kiến trúc: `tools/course_support/structure.py` và `render_course.py` đang gắn cứng cho lớp 1 (35 tuần, R01–R24, tiết 53/104). Đề xuất:

- **Không sửa** audit lớp 1 (`course-audit-1.0`). Thêm nhánh song song `tools/course_support/vocational/` với hợp đồng `course-audit-vocational-1.0`. Tái dùng các phần dùng chung: `load_mapping`, `transactions.inside/read_text`, băm sha256, kiểm DAG, kiểm ID trùng, mẫu báo cáo `limits` / `not_assessed`.
- Khóa học mới đặt tại `courses/vi-vn-tvet-plc-logo-zen/` (`course.yaml`, `requirements.yaml`, `schedules/cd9-k5.json`, `units/`, `labs/`, `assessments.yaml`).
- Công cụ mới: `tools/plan_schedule.py` (xếp lịch và xếp lại), `tools/render_giao_an.py` (`--week N`, `--write`), `tools/render_handout.py`. Kiểm thử `tests/test_vocational_course.py` theo mẫu `tests/test_course_audit.py` (fixture thật, rồi làm hỏng từng bản sao).
- Kiến thức mới qua `bin/pedagogy-pipeline`: đào tạo kỹ năng thực hành (psychomotor), an toàn xưởng điện, cấu trúc giáo án tích hợp GDNN. Cần thêm route trong `tools/pipeline_support/routing.py`. Các module liên quan đã có: `explicit-instruction-i-we-you`, `worked-example-fading-protocol`, `clinical-reasoning-and-deliberate-practice`, `rosenshine-10-principles`, `formative-hinge-questions`.
- Agent runtime: `90-agent-runtime/prompts/vocational-lesson-planner.md`. Cập nhật `skills/design-os-pedagogy/SKILL.md` và `llms.txt` để agent tìm thấy luồng `courses/`; hiện SKILL.md không nhắc đến nó.

## 6. Lộ trình

| Pha | Nội dung | Tiêu chí chấp nhận |
|---|---|---|
| P0 (xong) | Nghiên cứu nguồn, số hóa lịch, thiết kế | Thư mục này |
| P1 | Schema + `plan_schedule.py` + audit đào tạo nghề + test | Test đỏ khi: phút ≠ 240, thiếu rubric hoặc an toàn, kiểm tra trước khi dạy, sai thiết bị. Audit lớp 1 vẫn xanh |
| P2 | `course.yaml`, `units/`, `labs/` cho mô đun này. GV kiểm chứng 7 lab trong lịch trên kit | Mỗi lab có `verification: teacher_verified` và tệp chương trình |
| P3 | Sinh và xuất GA, phiếu học tập cho tuần 1–3, thử trên lớp thật | GV duyệt. docx khớp mẫu trường |
| P4 | Xếp lại lịch từ `feedback/` và `exceptions` | Kịch bản thử: nghỉ tuần 6, buổi rút còn 3 giờ, thiếu kit ZEN tuần 11 |
| P5 | Mở rộng sang mô đun khác của khoa | Chỉ thay `course.yaml`, `units/`, `labs/`, không đổi mã |

## 7. Câu hỏi cần giáo viên trả lời trước P2

1. Kit thực tế dùng model nào: LOGO! 12/24RC hay 230RC, thế hệ 0BA6, 0BA8 hay mới hơn, có module DM8 không? ZEN loại 10 hay 20 I/O, có module mở rộng không? Bài đèn giao thông cần 6 ngõ ra, nên câu trả lời quyết định lời giải.
2. Hình thức và thời lượng KTĐK 1, KTĐK 2 (lý thuyết, thực hành hay sản phẩm). Thang điểm và trọng số.
3. Lớp có bao nhiêu sinh viên và bao nhiêu kit, để chia nhóm.
4. Khoa có sẵn lời giải các bài lab (tệp .lsc/.zen) ngoài giáo trình không?
5. Có cần docx khớp từng ô theo mẫu trường, hay Markdown/PDF là đủ cho giai đoạn đầu?
6. Repo này công khai. Có được phép đưa trích đoạn giáo trình nội bộ vào không, hay chỉ giữ ở dạng tham chiếu như hiện nay?
