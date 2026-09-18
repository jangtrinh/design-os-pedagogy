#!/usr/bin/env python3
"""Render teacher-facing Markdown from the audited course data; --write is explicit."""
import argparse
import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.course_support.audit import audit_bundle, load_bundle


def answer_text(task):
    value, kind = task["answer"], task["kind"]
    if kind == "calendar":
        days = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ nhật"]
        return f"{days[value['weekday']]}, ngày {value['day']}"
    if kind == "place":
        return f"{value[0]} chục và {value[1]} đơn vị"
    if kind == "measurement":
        return f"{value} cm"
    if kind == "clock":
        return f"{value} giờ"
    if isinstance(value, list):
        return ", ".join(map(str, value))
    return str(value)


def render_lessons(course, sessions, profile):
    lines = ["# Lịch 35 tuần và 105 phiếu tiết học", "",
             "Bản dành cho giáo viên, có đáp án. Được xuất từ dữ liệu khóa học; không phát nguyên bản cho học sinh.", "",
             "Phân phối là đề xuất biên soạn. Mỗi tiết 35 phút; kiểm tra và phản hồi đã nằm trong tổng 105 tiết.", "",
             "## Lịch theo tuần", "", "| Tuần | Tiết thứ nhất | Tiết thứ hai | Tiết thứ ba |",
             "| --- | --- | --- | --- |"]
    for week in range(1, 36):
        group = [s for s in sessions if s["week"] == week]
        lines.append(f"| {week} | " + " | ".join(f"{s['period']}. {s['title']}" for s in group) + " |")
    lines += ["", "## Bản đồ yêu cầu và minh chứng", "",
              "Các mã R là phân rã của người biên soạn, không phải mã chuẩn chính thức. Đủ mã không chứng minh chất lượng nhiệm vụ.", "",
              "| Mã | Yêu cầu | Tiết có cơ hội học/thực hành |", "| --- | --- | --- |"]
    for requirement in profile["requirements"]:
        periods = [str(s["period"]) for s in sessions if requirement["id"] in s["standard_ids"]
                   and s["period"] not in (53, 104)]
        lines.append(f"| {requirement['id']} | {requirement['expectation']} | {', '.join(periods)} |")
    for unit in course["units"]:
        lines += ["", f"## {unit['id']}. {unit['title']}", ""]
        for session in sessions:
            if session["unit_id"] != unit["id"]:
                continue
            task = session["exit_task"]
            lines += [f"### Tiết {session['period']}: {session['title']}", "",
                      f"Tuần {session['week']}; 35 phút; yêu cầu {', '.join(session['standard_ids'])}.", "",
                      f"**Học cụ:** {task.get('materials', 'Theo hướng dẫn giáo viên.')}", "",
                      f"**Bài mẫu của cô:** {session['teacher_model']}", "",
                      f"**Luyện tập:** {session['practice']['prompt']}", "",
                      f"**Đáp án luyện tập:** {session['practice']['answer']}", "",
                      f"**Nhiệm vụ cuối tiết:** {task['prompt']}", "",
                      f"**Đáp án/tiêu chí:** {answer_text(task)}", "",
                      "Đọc yêu cầu khi cần; ghi hành động/câu trả lời và hỗ trợ thực tế. Nếu chưa rõ, hỏi trẻ chỉ vào vật hoặc giải thích một bước, rồi kiểm lại bằng nhiệm vụ tương tự khác số/vật. Không gán nhãn từ một đáp án.", ""]
    return "\n".join(lines) + "\n"


def render_assessment(exams):
    lines = ["# Hai đề mẫu và hồ sơ đánh giá", "",
             "Bản giáo viên, có đáp án và mô tả hình cần chuẩn bị. Chưa phải đề chính thức và chưa có dữ liệu học sinh.", ""]
    for label, text in exams["instructions"].items():
        lines += [f"**{label}:** {text}", ""]
    lines += ["## Chuẩn bị hình cho phiếu học sinh", "",
              "HK1-09: bốn hình phẳng A tròn, B vuông, C tam giác, D chữ nhật không vuông. HK1-10: hai mẫu A lập phương và B hộp chữ nhật dài. CN-09: hình thước có vạch, dải từ 0 tới 7; yêu cầu đọc hình thước, không đo tỉ lệ bản in. CN-10: đồng hồ hai kim, kim phút 12, kim giờ 7. Giáo viên phải duyệt độ rõ của hình/vật trước khi phát; không phát mô tả có đáp án này cho học sinh.", ""]
    for group in exams["groups"]:
        lines += [f"## {group['title']}", "", f"Dự kiến tiết {group['period']}. 10 câu, tối đa 10 điểm.", "",
                  "| Câu | Yêu cầu đọc cho học sinh | Chuẩn | Mức đề xuất | Điểm |",
                  "| --- | --- | --- | ---: | ---: |"]
        for index, task in enumerate(group["items"], 1):
            visual = f" (cần hình {task['visual_id']})" if task.get("visual_id") else ""
            lines.append(f"| {index} | {task['prompt']}{visual} | {', '.join(task['standard_ids'])} | {task['level']} | {task['points']} |")
        lines += ["", "### Đáp án và tiêu chí", "", "| Câu | Đáp án | Tiêu chí |", "| --- | --- | --- |"]
        for index, task in enumerate(group["items"], 1):
            lines.append(f"| {index} | {answer_text(task)} | {task['criterion']} |")
        lines += ["", "Mỗi câu đúng theo tiêu chí được 1 điểm; chưa đáp ứng được 0 điểm và kèm nhận xét. Không suy ra kết quả môn/cả năm từ riêng tổng điểm. Các câu hình và biểu đạt cần giáo viên duyệt trước sử dụng.", ""]
    columns = exams["formative_record"]["columns"]
    lines += ["## Phiếu ghi minh chứng thường xuyên", "", "| " + " | ".join(columns) + " |",
              "| " + " | ".join("---" for _ in columns) + " |",
              "| " + " | ".join(" " for _ in columns) + " |", "",
              exams["formative_record"]["note"], "",
              "Các trạng thái theo dõi: " + "; ".join(exams["formative_record"]["states"]) + ".", "",
              "Giữa học kì: xem hồ sơ, kiểm thêm nội dung chưa rõ và cập nhật hỗ trợ. Đề mẫu không biến bài kiểm tra viết giữa kì thành bắt buộc lớp 1. Các điều chỉnh chính thức thuộc giáo viên và nhà trường."]
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("course_folder", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    course, sessions, profile, exams, _ = load_bundle(args.course_folder)
    result = audit_bundle(course, sessions, profile, exams)
    if not result["passed"]:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1
    outputs = {"lessons.md": render_lessons(course, sessions, profile), "assessment.md": render_assessment(exams)}
    if args.write:
        for name, text in outputs.items():
            path = args.course_folder / name
            if path.is_symlink():
                raise ValueError("Refusing linked output")
            path.write_text(text, encoding="utf-8")
    print(json.dumps({"written": args.write, "outputs": {k: len(v.encode('utf-8')) for k, v in outputs.items()}}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
