"""Checks for authored lesson pages and lesson-plan content (contract tvet-content-1.0)."""
from pathlib import Path

from .model import index, load_file

CONTENT_VERSION = "tvet-content-1.0"
STEP_MODES = ("i_do", "we_do", "you_do", "check")
WIDGET_BLOCKS = {"AND", "OR", "NAND", "NOR", "XOR", "NOT", "RS", "ONDELAY", "OFFDELAY", "PULSE"}
PASSIVE = {"lắng nghe", "ghi nhận", "lắng nghe, ghi nhận", "lắng nghe và ghi nhận", "ghi chép"}


def load_content(folder, hashes):
    """Return {lessons: {id: doc}, sessions: {id: doc}, glossary: doc|None} from content/."""
    folder = Path(folder)
    result = {"lessons": {}, "sessions": {}, "glossary": None}
    for kind in ("lessons", "sessions"):
        directory = folder / "content" / kind
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.yaml")):
            doc = load_file(folder, f"content/{kind}/{path.name}", hashes)
            key = doc.get("lesson_id") if kind == "lessons" else doc.get("session_id")
            if key != path.stem:
                raise ValueError(f"content/{kind}/{path.name} must declare id {path.stem}")
            result[kind][key] = doc
    if (folder / "content" / "glossary.yaml").is_file():
        result["glossary"] = load_file(folder, "content/glossary.yaml", hashes)
    return result


def _strings(value):
    return isinstance(value, list) and bool(value) and all(isinstance(x, str) and x.strip() for x in value)


def _no_html(text):
    return isinstance(text, str) and "<" not in text.replace("<=", "").replace("< ", "")


def check_mcq(item, label, errors):
    options, answer, feedback = item.get("options"), item.get("answer"), item.get("feedback")
    if item.get("kind") != "mcq" or not item.get("prompt"):
        errors.append(f"MCQ_SHAPE: {label}")
        return
    if not _strings(options) or not 3 <= len(options) <= 4:
        errors.append(f"MCQ_OPTIONS: {label} needs 3-4 options")
        return
    if type(answer) is not int or not 0 <= answer < len(options):
        errors.append(f"MCQ_ANSWER: {label}")
    if not _strings(feedback) or len(feedback) != len(options):
        errors.append(f"MCQ_FEEDBACK: {label} needs one explanation per option")


def check_widget(widget, label, errors):
    if widget.get("kind") != "logic-sim" or not isinstance(widget.get("spec"), dict):
        errors.append(f"WIDGET_KIND: {label}")
        return
    spec = widget["spec"]
    try:
        inputs, blocks, outputs = index(spec.get("inputs"), "inputs"), index(spec.get("blocks"), "blocks"), \
            index(spec.get("outputs"), "outputs")
    except ValueError as exc:
        errors.append(f"WIDGET_SHAPE: {label}: {exc}")
        return
    known = set(inputs) | set(blocks) | set(outputs) | {"hi", "lo"}
    for bid, block in blocks.items():
        kind = block.get("type")
        if kind not in WIDGET_BLOCKS:
            errors.append(f"WIDGET_BLOCK: {label}/{bid} type {kind!r}")
            continue
        refs = [block.get("S"), block.get("R")] if kind == "RS" else block.get("in", [])
        if not isinstance(refs, list) or not refs or any(r not in known for r in refs):
            errors.append(f"WIDGET_REF: {label}/{bid}")
        if kind in ("NOT", "ONDELAY", "OFFDELAY", "PULSE") and len(refs) != 1:
            errors.append(f"WIDGET_ARITY: {label}/{bid}")
        if kind in ("ONDELAY", "OFFDELAY") and (type(block.get("T")) not in (int, float) or not 0 < block["T"] <= 60):
            errors.append(f"WIDGET_TIME: {label}/{bid}")
    for oid, output in outputs.items():
        if output.get("from") not in known:
            errors.append(f"WIDGET_REF: {label}/{oid}")
    if any(c not in known for c in spec.get("chart", [])):
        errors.append(f"WIDGET_CHART: {label}")


def check_lesson(doc, course, labs, ids, errors):
    lid = doc.get("lesson_id")
    lessons = {l["id"]: l for l in course.get("lessons", [])}
    if doc.get("content_version") != CONTENT_VERSION or lid not in lessons:
        errors.append(f"LESSON_CONTENT: {lid}")
        return
    if doc.get("status") not in ("draft", "teacher_reviewed"):
        errors.append(f"CONTENT_STATUS: {lid}")
    if not doc.get("summary") or not _strings(doc.get("objectives")):
        errors.append(f"LESSON_INTRO: {lid}")
    sections = doc.get("sections")
    if not isinstance(sections, list) or not sections:
        errors.append(f"LESSON_SECTIONS: {lid}")
        sections = []
    for section in sections:
        sid = section.get("id")
        if not isinstance(sid, str) or sid in ids:
            errors.append(f"CONTENT_ID: {lid}/{sid}")
        ids.add(sid)
        if not section.get("title") or not _no_html(section.get("body_md")) or not section.get("body_md"):
            errors.append(f"SECTION_BODY: {sid}")
        table = section.get("table")
        if table is not None and (not _strings(table.get("columns")) or not isinstance(table.get("rows"), list)
                                  or any(len(r) != len(table["columns"]) for r in table["rows"])):
            errors.append(f"SECTION_TABLE: {sid}")
        if section.get("widget") is not None:
            check_widget(section["widget"], sid, errors)
        for check in section.get("checks", []):
            if check.get("id") in ids:
                errors.append(f"CONTENT_ID: {check.get('id')}")
            ids.add(check.get("id"))
            check_mcq(check, f"{sid}/{check.get('id')}", errors)
    for example in doc.get("worked_examples", []):
        steps = example.get("steps")
        if example.get("fading") not in ("full", "completion") or not isinstance(steps, list) or not steps:
            errors.append(f"WORKED_EXAMPLE: {example.get('id')}")
            continue
        blanks = [s for s in steps if s.get("blank")]
        if (example["fading"] == "completion") != bool(blanks) or any(not s.get("prompt") for s in blanks):
            errors.append(f"FADING: {example.get('id')} completion needs blank steps with prompts")
    practice = doc.get("practice", {})
    if practice.get("lab_id") not in lessons[lid].get("lab_ids", []):
        errors.append(f"PRACTICE_LAB: {lid}")
    elif not practice.get("brief_md") or not _strings(practice.get("steps")) or not _strings(practice.get("self_check")):
        errors.append(f"PRACTICE_BRIEF: {lid}")
    else:
        outline = labs.get(practice["lab_id"], {}).get("solution_outline", "")
        student_text = " ".join([practice["brief_md"], *practice["steps"]])
        if labs.get(practice["lab_id"], {}).get("verification") == "draft" and outline and outline[:60] in student_text:
            errors.append(f"SOLUTION_LEAK: {lid} student brief repeats a draft solution")
    tests = doc.get("self_test", [])
    if not 4 <= len(tests) <= 6:
        errors.append(f"SELF_TEST: {lid} needs 4-6 questions")
    for test in tests:
        if test.get("id") in ids:
            errors.append(f"CONTENT_ID: {test.get('id')}")
        ids.add(test.get("id"))
        check_mcq(test, f"{lid}/{test.get('id')}", errors)


def check_session(doc, planned, labs, ids, errors):
    sid = doc.get("session_id")
    if doc.get("content_version") != CONTENT_VERSION or planned is None:
        errors.append(f"SESSION_CONTENT: {sid} has no planned session")
        return
    expected = [(p["kind"], p["minutes"]) for p in planned["phases"]]
    phases = doc.get("phases", [])
    if [(p.get("kind"), p.get("minutes")) for p in phases] != expected:
        errors.append(f"GA_PHASES: {sid} must match the planned phases {expected}")
    obj = doc.get("objectives", {})
    if not all(_strings(obj.get(k)) for k in ("knowledge", "skills", "attitude")) or not _strings(doc.get("materials")):
        errors.append(f"GA_HEADER: {sid}")
    if any(r not in ids for r in doc.get("lesson_section_ids", [])) or not doc.get("lesson_section_ids"):
        errors.append(f"GA_SECTION_REF: {sid}")
    has_practice = any(b["kind"] == "practice" for b in planned["blocks"])
    lab_steps = 0
    for phase in phases:
        kind = phase.get("kind")
        for side in ("teacher", "student"):
            if not _strings(phase.get(side)):
                errors.append(f"GA_ACTIVITY: {sid}/{kind}/{side}")
        student = phase.get("student") or []
        if student and all(s.strip().lower().rstrip(".") in PASSIVE for s in student):
            errors.append(f"PASSIVE_STUDENT: {sid}/{kind}")
        if kind != "giai_quyet_van_de":
            continue
        steps = phase.get("steps")
        if not isinstance(steps, list) or not steps:
            errors.append(f"GA_STEPS: {sid}")
            continue
        if sum(s.get("minutes", 0) for s in steps if type(s.get("minutes")) is int) != phase.get("minutes") \
                or any(type(s.get("minutes")) is not int or s["minutes"] <= 0 for s in steps):
            errors.append(f"GA_STEP_MINUTES: {sid}")
        for step in steps:
            if step.get("mode") not in STEP_MODES or not step.get("title"):
                errors.append(f"GA_STEP_MODE: {sid}")
            if not _strings(step.get("teacher")) or not _strings(step.get("student")):
                errors.append(f"GA_STEP_ACTIVITY: {sid}/{step.get('title')}")
            refs = step.get("lesson_section_ids", []) + step.get("check_ids", [])
            if any(r not in ids for r in refs):
                errors.append(f"GA_STEP_REF: {sid}/{step.get('title')}")
            if step.get("lab_id") is not None:
                if step["lab_id"] not in labs:
                    errors.append(f"GA_LAB_REF: {sid}")
                elif step.get("mode") == "you_do":
                    lab_steps += 1
    if has_practice and not lab_steps:
        errors.append(f"GA_PRACTICE: {sid} needs a you_do step tied to a lab")


def check_glossary(doc, lessons, errors):
    terms = doc.get("terms")
    if doc.get("content_version") != CONTENT_VERSION or not isinstance(terms, list) or not terms:
        errors.append("GLOSSARY_SHAPE")
        return
    seen = set()
    for term in terms:
        key = (term.get("vi", "").lower(), term.get("platform"))
        if not term.get("vi") or not term.get("definition") or key in seen \
                or term.get("platform") not in ("logo", "zen", "chung") \
                or not term.get("lesson_ids") or any(l not in lessons for l in term["lesson_ids"]):
            errors.append(f"GLOSSARY_TERM: {term.get('vi')}")
        seen.add(key)


def check_content(course, sessions_document, content):
    errors = []
    labs = {l["id"]: l for l in course.get("labs", [])}
    lessons = {l["id"] for l in course.get("lessons", [])}
    planned = {s["id"]: s for s in (sessions_document or {}).get("sessions", [])}
    ids = set()
    for doc in content["lessons"].values():
        check_lesson(doc, course, labs, ids, errors)
    for doc in content["sessions"].values():
        check_session(doc, planned.get(doc.get("session_id")), labs, ids, errors)
    if content["glossary"] is not None:
        check_glossary(content["glossary"], lessons, errors)
    return sorted(set(errors))
