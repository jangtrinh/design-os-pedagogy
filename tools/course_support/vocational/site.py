"""Static, dependency-free course website from course data and authored content.

Two audiences share one generator. The student build is safe to publish: it never contains
lesson plans, lab solution outlines or open technical issues. The teacher build adds them.
"""
import json
from html import escape

from markdown_it import MarkdownIt

PHASE_LABELS = {
    "on_dinh_lop": "Ổn định lớp", "dan_nhap": "Dẫn nhập", "gioi_thieu_chu_de": "Giới thiệu chủ đề",
    "giai_quyet_van_de": "Giải quyết vấn đề", "kiem_tra": "Kiểm tra", "ket_thuc_van_de": "Kết thúc vấn đề",
    "huong_dan_tu_hoc": "Hướng dẫn tự học",
}
STEP_LABELS = {"i_do": "GV làm mẫu", "we_do": "Cùng làm", "you_do": "Tự thực hành", "check": "Kiểm tra nhanh"}
KIND_LABELS = {"theory": "Lý thuyết", "practice": "Thực hành", "assessment": "Kiểm tra"}
_md = MarkdownIt("commonmark", {"html": False, "linkify": False}).enable("table")


def e(value):
    return escape("" if value is None else str(value), quote=True)


def md(text):
    return _md.render(text or "")


def hours(value):
    return f"{value:g} giờ"


def date_vi(iso):
    y, m, d = iso.split("-")
    return f"{d}/{m}/{y}"


class Site:
    def __init__(self, course, schedule, sessions_document, content, audience, base_css):
        if audience not in ("student", "teacher"):
            raise ValueError("audience must be student or teacher")
        self.course, self.schedule, self.content, self.audience = course, schedule, content, audience
        self.sessions = sessions_document["sessions"]
        self.lessons = {l["id"]: l for l in course["lessons"]}
        self.labs = {l["id"]: l for l in course["labs"]}
        self.assessments = {a["id"]: a for a in course["assessments"]}
        self.base_css = base_css
        self.teacher = audience == "teacher"

    # Shell -------------------------------------------------------------------

    def page(self, depth, current, title, body, toc=None):
        root = "../" * depth
        nav = [("index.html", "Tổng quan", "home"), ("lich.html", "Lịch học", "schedule"),
               ("tra-cuu.html", "Tra cứu", "glossary")]
        links = "".join(f'<a href="{root}{href}"{" aria-current=\"page\"" if key == current else ""}>{label}</a>'
                        for href, label, key in nav)
        badge = ('<span class="c-badge" data-kind="teacher">Bản giáo viên</span>' if self.teacher
                 else '<span class="c-badge" data-kind="draft">Bản nháp</span>')
        aside = f'<aside class="c-toc"><nav aria-label="Mục lục"><ol>{toc}</ol></nav></aside>' if toc else ""
        robots = '<meta name="robots" content="noindex">' if self.teacher else ""
        return f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{robots}<title>{e(title)} · Điều khiển lập trình cỡ nhỏ</title>
<link rel="stylesheet" href="{root}{self.base_css}">
<link rel="stylesheet" href="{root}assets/course.css">
</head>
<body class="c-body" data-audience="{self.audience}">
<a class="ds-skip-link" href="#main">Bỏ qua điều hướng</a>
<header class="c-top"><a class="c-brand" href="{root}index.html">PLC LOGO! · ZEN</a><nav class="c-nav" aria-label="Chính">{links}</nav>{badge}</header>
<div class="c-layout">{aside}<main id="main" class="c-main">
{body}
</main></div>
<footer class="c-foot"><p>Mô đun Điều khiển lập trình cỡ nhỏ · nội dung do AI soạn từ lịch trình và tài liệu giảng dạy của khoa, <strong>chưa được giáo viên duyệt</strong>. Lời giải bài thực hành chỉ có trong bản giáo viên.</p></footer>
<script src="{root}assets/course.js" defer></script>
</body>
</html>
"""

    @staticmethod
    def callout(tone, title, html):
        return f'<div class="c-callout" data-tone="{tone}"><p class="c-callout-title">{e(title)}</p>{html}</div>'

    @staticmethod
    def items(values):
        return "<ul>" + "".join(f"<li>{e(v)}</li>" for v in values) + "</ul>" if values else ""

    def mcq(self, item):
        options = "".join(
            f'<li><button type="button" class="c-mcq-option" data-index="{i}">{e(o)}</button>'
            f'<div class="c-mcq-feedback" hidden>{e(f)}</div></li>'
            for i, (o, f) in enumerate(zip(item["options"], item["feedback"])))
        return (f'<div class="c-mcq" id="{e(item["id"])}" data-answer="{item["answer"]}">'
                f'<p class="c-mcq-prompt">{e(item["prompt"])}</p><ol class="c-mcq-options">{options}</ol></div>')

    def quiz(self, key, items, title=None):
        if not items:
            return ""
        head = f"<h3>{e(title)}</h3>" if title else ""
        return (f'<div class="c-quiz" data-key="{e(key)}">{head}{"".join(self.mcq(i) for i in items)}'
                f'<p class="c-quiz-score" aria-live="polite"></p>'
                f'<button type="button" class="c-quiz-reset">Làm lại</button></div>')

    @staticmethod
    def table(table):
        head = "".join(f"<th scope=\"col\">{e(c)}</th>" for c in table["columns"])
        rows = "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>" for r in table["rows"])
        caption = f"<caption>{e(table.get('caption'))}</caption>" if table.get("caption") else ""
        return f'<table class="c-table">{caption}<thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>'

    @staticmethod
    def widget(widget, wid):
        spec = json.dumps(widget["spec"], ensure_ascii=False).replace("</", "<\\/")
        return (f'<div class="c-sim" id="{e(wid)}"><h3>{e(widget.get("title", "Mô phỏng"))}</h3>'
                f'<script type="application/json" class="c-sim-spec">{spec}</script>'
                f'<p class="c-sim-note">Mô phỏng minh họa trên trình duyệt, không thay cho thử trên kit.</p></div>')

    def checklist(self, key, values):
        lis = "".join(f'<li><label><input type="checkbox"><span>{e(v)}</span></label></li>' for v in values)
        return (f'<div class="c-checklist" data-key="{e(key)}"><ul>{lis}</ul>'
                f'<p class="c-checklist-progress" aria-live="polite"></p></div>')

    # Pages -------------------------------------------------------------------

    def lesson_sessions(self, lid):
        return [s for s in self.sessions if any(b.get("lesson_id") == lid for b in s["blocks"])]

    def index(self):
        c = self.course
        program = c["module_program"]
        cards = []
        for lid, lesson in self.lessons.items():
            ready = lid in self.content["lessons"]
            weeks = ", ".join(str(s["week"]) for s in self.lesson_sessions(lid))
            cards.append(f'<a class="c-card" href="bai/{lid}.html"><span class="c-card-kicker">{lid} · tuần {e(weeks)}</span>'
                         f'<h3>{e(lesson["title"])}</h3><p>{e(lesson["source_locator"])} · '
                         f'{hours(lesson["program_hours"]["theory"])} LT, {hours(lesson["program_hours"]["practice"])} TH</p>'
                         f'<span class="c-status" data-status="{"ready" if ready else "skeleton"}">'
                         f'{"Có nội dung" if ready else "Đang soạn"}</span></a>')
        outcomes = "".join(f'<li><strong>{e(o["id"])}</strong> {e(o["text"])}</li>' for o in c["outcomes"])
        g = c["grading_policy"]
        hw = c["hardware_assumptions"]
        body = f"""<div class="c-hero"><p class="c-kicker">Mô đun cao đẳng · {e(self.schedule["class"]["name"])}</p>
<h1>{e(c["course"]["title"])}</h1>
<p class="c-lede">Giáo trình tương tác: đọc ngắn, thử ngay trên mô phỏng, tự kiểm tra, rồi mang phiếu thực hành ra kit.</p>
<dl class="c-meta"><dt>Thời lượng</dt><dd>{program["total_hours"]} giờ</dd><dt>Lý thuyết</dt><dd>{program["theory_hours"]} giờ</dd>
<dt>Thực hành</dt><dd>{program["practice_hours"]} giờ</dd><dt>Thi</dt><dd>{program["exam_hours"]} giờ</dd>
<dt>Học kỳ</dt><dd>{e(self.schedule["class"]["semester"])} · {e(self.schedule["class"]["school_year"])}</dd></dl></div>
{self.callout("draft", "Bản nháp do AI soạn", "<p>Nội dung được viết lại từ tài liệu giảng dạy và lịch trình của khoa, chưa được giáo viên duyệt. Thông số kỹ thuật theo bộ kit giả định bên dưới; khi lớp dùng thiết bị khác, giáo viên sẽ cập nhật.</p>")}
<section class="c-section" id="tuan-nay"><h2>Tuần này</h2><p data-today>Mở trang Lịch học để xem buổi hiện tại.</p><p><a href="lich.html">Xem toàn bộ lịch 15 tuần →</a></p></section>
<section class="c-section" id="bai-hoc"><h2>Bài học</h2><div class="c-cards">{"".join(cards)}</div></section>
<section class="c-section" id="muc-tieu"><h2>Sau mô đun, bạn có thể</h2><div class="c-prose"><ul>{outcomes}</ul></div></section>
<section class="c-section" id="danh-gia"><h2>Đánh giá</h2><div class="c-prose">
<p>Hai bài kiểm tra định kỳ (tuần 10 và 14) và thi kết thúc mô đun (tuần 15), đều là bài thực hành chấm theo phiếu.</p>
<p><strong>Điểm mô đun</strong> = {g["test_average_share"]:g} × điểm trung bình kiểm tra + {g["final_exam_share"]:g} × điểm thi (thang {g["scale"]}, làm tròn {g["rounding_decimals"]} chữ số thập phân). Kiểm tra định kỳ hệ số {g["periodic_weight"]}, thường xuyên hệ số {g["continuous_weight"]}. Đạt khi từ {g["pass_mark"]:g} điểm.</p>
<p>Điều kiện dự thi: tham gia ít nhất {round(g["exam_eligibility"]["min_attendance"] * 100)}% thời gian học và điểm trung bình kiểm tra từ {g["exam_eligibility"]["min_test_average"]:g}.</p></div></section>
<section class="c-section" id="thiet-bi"><h2>Thiết bị giả định</h2>{self.callout("info", "Chờ giáo viên xác nhận", self.items([hw["logo"]["base"], hw["logo"]["expansion"], hw["logo"]["software"], hw["zen"]["base"], hw["zen"]["software"]]))}</section>"""
        return self.page(0, "home", "Tổng quan", body)

    def schedule_page(self):
        rows = []
        for s in self.sessions:
            parts = []
            for b in s["blocks"]:
                if b["kind"] == "assessment":
                    parts.append(f'<span class="c-pill" data-tone="warn">{e(b["assessment_id"])}</span> {hours(b["hours"])}')
                else:
                    parts.append(f'<a href="bai/{b["lesson_id"]}.html">{e(b["lesson_id"])}</a> '
                                 f'{KIND_LABELS[b["kind"]].lower()} {hours(b["hours"])}'
                                 + (f' <small>({e(", ".join(b["items"]))})</small>' if b["items"] else ""))
            label = f"Tuần {s['week']}" if s["id"].startswith("W") else f"Học bù (tuần {s['week']})"
            rows.append(f'<tr data-start="{s["start"]}" data-end="{s["end"]}"><th scope="row">{e(label)}</th>'
                        f'<td>{date_vi(s["start"])} – {date_vi(s["end"])}</td><td>{"<br>".join(parts)}</td>'
                        f'<td><a href="tuan/{s["id"]}.html">Chi tiết</a></td></tr>')
        body = f"""<div class="c-hero"><p class="c-kicker">Lịch học</p><h1>Lịch 15 tuần</h1>
<p class="c-lede" data-today>Mỗi tuần một buổi 4 giờ. Giờ lý thuyết 45 phút, giờ thực hành 60 phút.</p></div>
<table class="c-sched c-table"><caption>{e(self.schedule["class"]["name"])} · HK {e(self.schedule["class"]["semester"])} {e(self.schedule["class"]["school_year"])}</caption>
<thead><tr><th scope="col">Tuần</th><th scope="col">Ngày</th><th scope="col">Nội dung</th><th scope="col"></th></tr></thead>
<tbody>{"".join(rows)}</tbody></table>"""
        return self.page(0, "schedule", "Lịch học", body)

    def lab_block(self, lab, lesson_doc):
        practice = (lesson_doc or {}).get("practice", {})
        parts = [f'<p class="c-kicker">{e(lab["id"])}</p><h3>{e(lab["title"])}</h3>',
                 f'<div class="c-prose">{md(practice.get("brief_md") or lab["requirement"])}</div>']
        if lab.get("io_table"):
            rows = [[r["address"], r["device"], r["description"]] for r in lab["io_table"]]
            parts.append('<div class="c-io">' + self.table({"caption": "Gán địa chỉ đề xuất (chờ giáo viên xác nhận trên kit)",
                                                           "columns": ["Địa chỉ", "Thiết bị", "Mô tả"], "rows": rows}) + "</div>")
        parts.append(self.callout("safety", "An toàn", self.items(lab["safety"])))
        if practice.get("steps"):
            parts.append("<h4>Các bước</h4><ol>" + "".join(f"<li>{e(s)}</li>" for s in practice["steps"]) + "</ol>")
        parts.append("<h4>Tự kiểm trước khi gọi giáo viên chấm</h4>"
                     + self.checklist(f"{lab['id']}-check", practice.get("self_check") or lab["rubric"]))
        faults = [[f["fault"], f["remedy"]] for f in lab["common_faults"]]
        parts.append("<h4>Sai hỏng thường gặp</h4>" + self.table({"columns": ["Hiện tượng", "Cách khắc phục"], "rows": faults}))
        if lab.get("variants"):
            parts.append("<h4>Mở rộng (làm thêm khi xong sớm)</h4>" + self.items(lab["variants"]))
        if self.teacher:
            teacher = [f'<p><strong>Trạng thái:</strong> {e(lab["verification"])} · cơ sở lời giải: {e(lab["solution_basis"])}</p>']
            if lab.get("solution_outline"):
                teacher.append(f'<p><strong>Lời giải tham khảo:</strong> {e(lab["solution_outline"])}</p>')
            teacher.append("<p><strong>Tiêu chí chấm:</strong></p>" + self.items(lab["rubric"]))
            if lab.get("open_issues"):
                teacher.append("<p><strong>Cần xác nhận:</strong></p>" + self.items(lab["open_issues"]))
            parts.append(self.callout("draft", "Chỉ giáo viên", "".join(teacher)))
        return '<div class="c-lab">' + "".join(parts) + "</div>"

    def lesson(self, lid):
        lesson, doc = self.lessons[lid], self.content["lessons"].get(lid)
        sessions = self.lesson_sessions(lid)
        weeks = ", ".join(f'<a href="../tuan/{s["id"]}.html">tuần {s["week"]}</a>' for s in sessions)
        toc, body = [], []
        outcomes = [o for o in self.course["outcomes"] if lid in o["lesson_ids"]]
        if doc:
            body.append(f'<div class="c-hero"><p class="c-kicker">{lid} · {e(lesson["source_locator"])}</p><h1>{e(lesson["title"])}</h1>'
                        f'<p class="c-lede">{e(doc["summary"])}</p><dl class="c-meta"><dt>Lịch</dt><dd>{weeks}</dd>'
                        f'<dt>Lý thuyết</dt><dd>{hours(lesson["program_hours"]["theory"])}</dd>'
                        f'<dt>Thực hành</dt><dd>{hours(lesson["program_hours"]["practice"])}</dd></dl></div>')
            body.append('<section class="c-section" id="muc-tieu"><h2>Mục tiêu</h2><div class="c-prose">'
                        + self.items(doc["objectives"]) + "</div></section>")
            toc.append('<li><a href="#muc-tieu">Mục tiêu</a></li>')
            for section in doc["sections"]:
                toc.append(f'<li><a href="#{e(section["id"])}">{e(section["title"])}</a></li>')
                inner = [f'<h2>{e(section["title"])}</h2><div class="c-prose">{md(section["body_md"])}</div>']
                if section.get("table"):
                    inner.append(self.table(section["table"]))
                if section.get("widget"):
                    inner.append(self.widget(section["widget"], f'{section["id"]}-sim'))
                inner.append(self.quiz(f"{section['id']}-checks", section.get("checks", []), "Kiểm tra nhanh"))
                body.append(f'<section class="c-section" id="{e(section["id"])}">{"".join(inner)}</section>')
            if doc.get("worked_examples"):
                toc.append('<li><a href="#vi-du">Ví dụ mẫu</a></li>')
                examples = []
                for ex in doc["worked_examples"]:
                    steps = []
                    for n, step in enumerate(ex["steps"]):
                        if step.get("blank"):
                            steps.append(f'<li class="c-we-step is-blank"><p class="c-we-prompt">{e(step["prompt"])}</p>'
                                         f'<textarea class="c-we-input" data-key="{e(ex["id"])}-{n}" rows="3" '
                                         f'aria-label="Bước bạn tự viết"></textarea><details class="c-we-reveal">'
                                         f'<summary>Xem bước mẫu</summary><div>{e(step["text"])}</div></details></li>')
                        else:
                            steps.append(f'<li class="c-we-step">{e(step["text"])}</li>')
                    examples.append(f'<div class="c-we" data-fading="{e(ex["fading"])}"><h3>{e(ex["title"])}</h3>'
                                    f'<p class="c-we-problem">{e(ex["problem"])}</p><ol class="c-we-steps">{"".join(steps)}</ol></div>')
                body.append('<section class="c-section" id="vi-du"><h2>Ví dụ mẫu</h2>'
                            '<p>Ví dụ đầu có lời giải đầy đủ. Ví dụ sau để trống vài bước: tự viết trước, rồi mới mở bước mẫu.</p>'
                            + "".join(examples) + "</section>")
        else:
            body.append(f'<div class="c-hero"><p class="c-kicker">{lid} · {e(lesson["source_locator"])}</p><h1>{e(lesson["title"])}</h1>'
                        f'<p class="c-lede">Bài này đang được soạn. Trang hiện chỉ có mục tiêu và nhiệm vụ thực hành.</p>'
                        f'<dl class="c-meta"><dt>Lịch</dt><dd>{weeks}</dd></dl></div>')
            body.append('<section class="c-section" id="muc-tieu"><h2>Chuẩn đầu ra liên quan</h2><div class="c-prose">'
                        + self.items([o["text"] for o in outcomes]) + "</div></section>")
            toc.append('<li><a href="#muc-tieu">Mục tiêu</a></li>')
        toc.append('<li><a href="#thuc-hanh">Thực hành</a></li>')
        labs = "".join(self.lab_block(self.labs[l], doc if doc and doc["practice"]["lab_id"] == l else None)
                       for l in lesson["lab_ids"])
        body.append(f'<section class="c-section" id="thuc-hanh"><h2>Thực hành</h2>{labs}</section>')
        if doc and doc.get("self_test"):
            toc.append('<li><a href="#tu-kiem-tra">Tự kiểm tra</a></li>')
            body.append('<section class="c-section" id="tu-kiem-tra"><h2>Tự kiểm tra cuối bài</h2>'
                        + self.quiz(f"{lid}-self-test", doc["self_test"]) + "</section>")
        return self.page(1, "lesson", lesson["title"], "\n".join(body), "".join(toc))

    def timeline(self, phases):
        return '<div class="c-timeline">' + "".join(
            f'<span class="c-tl-seg" data-kind="{p["kind"]}" style="--min: {p["minutes"]}">'
            f'{e(PHASE_LABELS[p["kind"]])} · {p["minutes"]}′</span>' for p in phases) + "</div>"

    def session(self, s):
        doc = self.content["sessions"].get(s["id"])
        blocks = []
        for b in s["blocks"]:
            if b["kind"] == "assessment":
                a = self.assessments[b["assessment_id"]]
                blocks.append(f'<li><span class="c-pill" data-tone="warn">{e(a["id"])}</span> {hours(b["hours"])} · {e(a["format"])}</li>')
            else:
                lesson = self.lessons[b["lesson_id"]]
                blocks.append(f'<li><a href="../bai/{b["lesson_id"]}.html">{e(b["lesson_id"])} · {e(lesson["title"])}</a> · '
                              f'{KIND_LABELS[b["kind"]].lower()} {hours(b["hours"])}'
                              + (f' · mục {e(", ".join(b["items"]))}' if b["items"] else "") + "</li>")
        label = f"Tuần {s['week']}" if s["id"].startswith("W") else f"Buổi học bù (tuần {s['week']})"
        body = [f'<div class="c-hero"><p class="c-kicker">{e(label)} · buổi {s["ga_number"]}</p>'
                f'<h1>{date_vi(s["start"])} – {date_vi(s["end"])}</h1>'
                f'<p class="c-lede">{e(doc["title_line"]) if doc else "Nội dung buổi theo lịch."}</p></div>',
                '<section class="c-section" id="noi-dung"><h2>Nội dung buổi học</h2><div class="c-prose"><ul>'
                + "".join(blocks) + "</ul></div>" + self.timeline(s["phases"]) + "</section>"]
        equipment = {x["id"]: x["name"] for x in self.course["equipment"]}
        body.append('<section class="c-section" id="chuan-bi"><h2>Chuẩn bị</h2><div class="c-prose">'
                    + self.items([equipment[x] for x in s["equipment_ids"]]) + "</div></section>")
        if doc:
            self_study = next((p for p in doc["phases"] if p["kind"] == "huong_dan_tu_hoc"), None)
            if self_study:
                body.append('<section class="c-section" id="tu-hoc"><h2>Sau buổi học</h2><div class="c-prose">'
                            + self.items(self_study["content"]) + "</div></section>")
        if s["notes"]:
            body.append(self.callout("warn", "Thay đổi lịch", self.items(s["notes"])))
        if self.teacher:
            body.append(f'<p><a class="c-pill" data-tone="info" href="{s["id"]}-giao-an.html">Mở giáo án số {s["ga_number"]} →</a></p>')
        return self.page(1, "schedule", label, "\n".join(body))

    def giao_an(self, s):
        doc = self.content["sessions"].get(s["id"])
        previous = self.lessons.get(s["previous_lesson_id"], {}).get("title", "Không có (buổi đầu)")
        total_hours = sum(b["hours"] for b in s["blocks"])
        head = (f'<table class="c-ga c-ga-head"><tr><th>GIÁO ÁN SỐ: {s["ga_number"]}</th>'
                f'<td>Thời gian thực hiện: {total_hours:g} giờ<br>Bài học trước: <strong>{e(previous)}</strong><br>'
                f'Thực hiện từ ngày {date_vi(s["start"])} đến ngày {date_vi(s["end"])}</td></tr></table>')
        if not doc:
            rows = "".join(f'<tr><td>{n}</td><td>{e(PHASE_LABELS[p["kind"]])}</td><td></td><td></td><td>{p["minutes"]}</td></tr>'
                           for n, p in enumerate(s["phases"], 1))
            body = (head + self.callout("draft", "Chưa soạn", "<p>Khung phút đã có từ lịch; nội dung giáo án chưa được sinh.</p>")
                    + f'<table class="c-ga"><thead><tr><th>TT</th><th>NỘI DUNG</th><th>HOẠT ĐỘNG GIÁO VIÊN</th>'
                      f'<th>HOẠT ĐỘNG HỌC SINH</th><th>THỜI GIAN</th></tr></thead><tbody>{rows}</tbody></table>')
            return self.page(1, "schedule", f"Giáo án số {s['ga_number']}", body)
        o = doc["objectives"]
        first, rest = doc["phases"][0], doc["phases"][1:]
        rows = []
        for n, p in enumerate(rest, 1):
            rows.append(f'<tr><td>{n}</td><td><strong>{e(PHASE_LABELS[p["kind"]])}</strong>{self.items(p["content"])}</td>'
                        f'<td>{self.items(p["teacher"])}</td><td>{self.items(p["student"])}</td><td>{p["minutes"]}</td></tr>')
            for step in p.get("steps", []):
                refs = ", ".join(step.get("lesson_section_ids", []) + step.get("check_ids", []) + ([step["lab_id"]] if step.get("lab_id") else []))
                rows.append(f'<tr class="c-ga-step"><td></td><td><em>{e(STEP_LABELS[step["mode"]])}</em>: {e(step["title"])}'
                            + (f'<br><small>{e(refs)}</small>' if refs else "")
                            + f'</td><td>{self.items(step["teacher"])}</td><td>{self.items(step["student"])}</td><td>{step["minutes"]}</td></tr>')
        retrieval = first.get("retrieval_questions", [])
        body = f"""{head}
<p><strong>{e(doc["title_line"])}</strong></p>
<p><strong>MỤC TIÊU CỦA BÀI:</strong> <em>Sau khi học xong bài này người học có khả năng:</em></p>
{self.items(o["knowledge"] + o["skills"] + o["attitude"])}
<p><strong>ĐỒ DÙNG VÀ TRANG THIẾT BỊ DẠY HỌC:</strong> {e("; ".join(doc["materials"]))}</p>
<p><strong>HÌNH THỨC TỔ CHỨC DẠY HỌC:</strong> {e(doc["organization"])}</p>
<p><strong>I. ỔN ĐỊNH LỚP HỌC:</strong> Thời gian: {first["minutes"]} phút</p>
{self.items(first["content"] + first["teacher"] + ["Kiểm tra bài cũ: " + q for q in retrieval])}
<p><strong>II. THỰC HIỆN BÀI HỌC</strong></p>
{self.timeline(s["phases"])}
<table class="c-ga"><thead><tr><th>TT</th><th>NỘI DUNG</th><th>HOẠT ĐỘNG GIÁO VIÊN</th><th>HOẠT ĐỘNG HỌC SINH</th><th>THỜI GIAN (phút)</th></tr></thead>
<tbody>{"".join(rows)}</tbody></table>
<p><strong>III. RÚT KINH NGHIỆM TỔ CHỨC THỰC HIỆN:</strong></p>
<div class="c-ga-blank" aria-label="Để trống cho giáo viên ghi"></div>
{self.callout("safety", "Ghi chú cho giáo viên (không in kèm giáo án nộp)", self.items(doc.get("teacher_notes", [])))}
<table class="c-ga c-ga-sign"><tr><td><strong>TRƯỞNG BỘ MÔN</strong></td><td>Ngày … tháng … năm …<br><strong>GIÁO VIÊN</strong></td></tr></table>
<p><button type="button" data-print>In giáo án</button></p>"""
        return self.page(1, "schedule", f"Giáo án số {s['ga_number']}", body)

    def glossary(self):
        terms = sorted((self.content["glossary"] or {}).get("terms", []), key=lambda t: t["vi"].lower())
        platform = {"logo": "LOGO!", "zen": "ZEN", "chung": "Chung"}
        rows = "".join(
            f'<div class="c-term" data-platform="{e(t["platform"])}" data-search="{e((t["vi"] + " " + t.get("en", "")).lower())}">'
            f'<dt>{e(t["vi"])}' + (f' <span lang="en">({e(t["en"])})</span>' if t.get("en") else "")
            + f' <span class="c-pill">{platform[t["platform"]]}</span></dt><dd>{e(t["definition"])} '
            + " ".join(f'<a href="bai/{l}.html">{l}</a>' for l in t["lesson_ids"]) + "</dd></div>" for t in terms)
        body = f"""<div class="c-hero"><p class="c-kicker">Tra cứu</p><h1>Thuật ngữ</h1>
<p class="c-lede">Gõ tiếng Việt có dấu hoặc không dấu, hoặc tên tiếng Anh.</p></div>
<p><label>Tìm <input type="search" class="c-search" data-target="#gl" placeholder="ví dụ: tu giu, on-delay"></label>
<label>Nền tảng <select class="c-filter" data-target="#gl"><option value="">Tất cả</option><option value="logo">LOGO!</option>
<option value="zen">ZEN</option><option value="chung">Chung</option></select></label></p>
<p class="c-search-count" aria-live="polite"></p>
<dl id="gl" class="c-glossary">{rows}</dl>"""
        return self.page(0, "glossary", "Thuật ngữ", body)

    def build(self):
        """Return {relative path: html} for the whole site."""
        pages = {"index.html": self.index(), "lich.html": self.schedule_page(), "tra-cuu.html": self.glossary()}
        for lid in self.lessons:
            pages[f"bai/{lid}.html"] = self.lesson(lid)
        for s in self.sessions:
            pages[f"tuan/{s['id']}.html"] = self.session(s)
            if self.teacher:
                pages[f"tuan/{s['id']}-giao-an.html"] = self.giao_an(s)
        return pages
