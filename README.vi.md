# Agent Teacher

DESIGN:OS Pedagogy gồm kho tri thức sư phạm, ứng dụng luyện dạy cục bộ và công cụ chuẩn bị, kiểm tra, áp dụng module theo các bước riêng.

![Không gian tri thức Agent Teacher](assets/pedagogy_hero_console_1789438819020.jpg)

[English](README.md) · [Bản đồ tri thức](00-navigation/MOC-Master.md) · [Contract ứng dụng](docs/rehearsal-contract.md) · [Xuất bản và phục hồi](docs/publication.md)

[Thư mục chạy cục bộ](docs/local-workspace.md) ghi cách xác nhận đúng checkout, khởi động ứng dụng và tìm bằng chứng kiểm thử.

## Phần đã triển khai

Vòng luyện dạy có ba tình huống phân số tiếng Việt: so sánh độ lớn, kiểm tra lý do phía sau đáp án đúng, và ký hiệu khác với lời giải thích. Người tham gia chọn hành động dạy, ghi lời mình sẽ nói, đọc phản hồi gắn với transcript, làm bài chuyển giao và lưu phản tư.

Phiên và sự kiện được lưu bằng SQLite, có kiểm revision, xử lý yêu cầu gửi trùng, mở lại, replay và xuất Markdown/JSON. Lời học sinh và coaching theo nhánh biên soạn. Câu chữ tự viết được lưu nhưng chưa chấm ngữ nghĩa. Ứng dụng không gọi model ngoài và không chứng nhận năng lực giảng dạy.

Registry kiểm tra metadata, ID chuẩn, alias tường minh và kiểu tham chiếu. Publisher kiểm tra bản nháp trước một lệnh áp dụng riêng. Review nguồn, review chuyên gia có danh tính và pilot người dùng thật vẫn chưa hoàn tất. Tests đạt hoặc graph sạch chưa xác nhận hiệu quả dạy học.

## Mở ứng dụng

Chạy từ thư mục project:

~~~sh
python3 run_rehearsal.py --port 0
~~~

Mở địa chỉ cục bộ được in ra. Port 0 chọn cổng trống; mặc định là 8876. Dữ liệu nằm tại .data/rehearsal.sqlite3. Dùng --data-dir với thư mục riêng cho kiểm thử hoặc pilot. Đây là dịch vụ cục bộ cho một người dùng, chưa phải hệ thống public nhiều tài khoản.

Luồng: hỏi thêm → diễn giải → chọn cách dạy → kiểm tra → review → chuyển giao → phản tư → hoàn thành. Phiên giữ version và fingerprint của pack. Khi pack đổi, phiên cũ vẫn xem/xuất được nhưng không tiếp tục hoặc replay bằng nội dung khác. Danh sách trả 100 phiên gần nhất; URL đã biết của phiên cũ hơn vẫn mở được.

## Tra cứu kho tri thức

Bắt đầu tại [bản đồ tổng quan](00-navigation/MOC-Master.md). Mô hình soạn thảo kết nối tri thức, trải nghiệm, chẩn đoán, thực hành, phản hồi, chuyển giao và quy trình áp dụng.

| Khu vực | Nội dung |
| --- | --- |
| 00-system | Ontology, schema, chính sách bằng chứng và contract soạn thảo |
| 10-foundations và 20-stages | Nền tảng và hướng dẫn theo giai đoạn giáo dục |
| 30-pedagogy và 40-disciplines | Phương pháp, đánh giá và thực hành chuyên ngành |
| 50-practice-library và 60-evidence | Tình huống, hồ sơ nguồn, claim và estimate |
| 70-capabilities và 80-professor-development | Năng lực dạy và phát triển nghề nghiệp |
| 90-agent-runtime | Đặc tả runtime, prompt và đề xuất đánh giá |
| rehearsal | Ứng dụng luyện dạy phân số đã triển khai |
| tools và tests | Registry, publication, link auditor và tests thực thi |

Giai đoạn giáo dục dùng S0 đến S7; hỗ trợ AI dùng AL0 đến AL7. Ontology/schema có phiên bản là contract chuẩn. Giai đoạn, hỗ trợ và năng lực là thuộc tính khác nhau. Tutor runtime rộng hơn trong 90-agent-runtime vẫn là đặc tả.

Đọc riêng trạng thái xác minh, claim, loại chỉ số tác động, điều kiện áp dụng và review. Ví dụ biên soạn không phải kết quả lớp học đã quan sát. Grade cũ hoặc cờ validated không thay cho review chuyên gia. [ART-DIRECTION.md](ART-DIRECTION.md) mô tả hình nhận diện; hình giảng dạy có thể dùng nhãn và tỷ lệ chính xác khi cần.

## Chuẩn bị và áp dụng module

Registry/publication cần package trong requirements.txt. Dùng .venv đang có; chỉ tạo môi trường khi chưa có rồi cài dependency. Publisher dùng khóa file POSIX.

~~~sh
.venv/bin/python -B tools/pedagogy_pipeline.py "Fraction teaching routine" --stage S2 --archetype methods --dry-run
~~~

Preview in route, ID và contract đầy đủ, chưa ghi draft hoặc gọi model. Soạn module đáp ứng contract rồi import:

~~~sh
.venv/bin/python -B tools/pedagogy_pipeline.py "Fraction teaching routine" --stage S2 --archetype methods --input /path/to/module.md
~~~

Review module.md, moc.md và manifest.json trong thư mục được trả về. Thay DRAFT_ID dưới đây bằng đúng tên thư mục đó:

~~~sh
.venv/bin/python -B tools/pedagogy_pipeline.py --apply .pedagogy-drafts/DRAFT_ID
~~~

Metadata phải giữ unreviewed; import không phải nghiệm thu khoa học. File đích đã có, draft đổi hoặc điều hướng đổi đều gây conflict. Tên file hỗ trợ Unicode; truyền --id ASCII chuẩn khi cần. Provider là tùy chọn, phải chọn tường minh bằng --provider. Không tự Git add, commit hoặc push. Các lệnh -m và -p cũ đã lỗi thời.

## Kiểm tra publication bị ngắt

~~~sh
.venv/bin/python -B tools/pedagogy_pipeline.py --inspect-publication
.venv/bin/python -B tools/pedagogy_pipeline.py --recover-publication
~~~

Recovery hoàn tất giao dịch dở dang còn nguyên vẹn. File đã sửa hoặc thay thế gây conflict. Giữ journal, draft và staging files; không xóa để ép apply. [Quy trình phục hồi](docs/publication.md) mô tả kiểm tra ownership và xử lý conflict thủ công. Hai lần ghi file không phải một giao dịch atomic; tests ngắt process không bao phủ mọi lỗi thiết bị hoặc mất điện.

## Kiểm tra và các cổng còn lại

~~~sh
.venv/bin/python -B -m unittest discover -s tests -v
.venv/bin/python -B tools/knowledge_registry.py
.venv/bin/python -B tools/verify_links.py
~~~

Tests dùng corpus và database tạm riêng. Link auditor kiểm tra đường dẫn/anchor cục bộ, không kiểm HTTP bên ngoài hay nguồn nghiên cứu có hỗ trợ claim không. Cần đọc diagnostics đúng phạm vi.

[Trạng thái triển khai](docs/implementation-status.md) ghi vị trí bằng chứng và giới hạn. [Review phân số và pilot](docs/fraction-pilot.md) mô tả công việc còn cần con người. Soạn bài, coaching transcript, portfolio, agent adapters và domain mới vẫn là lựa chọn mở rộng có điều kiện.
