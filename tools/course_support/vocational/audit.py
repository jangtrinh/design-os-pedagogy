"""Invariant checks for a schedule-driven vocational course; prose quality is out of scope."""
import hashlib
import json
from collections import defaultdict

from . import BLOCK_KINDS, CONTRACT, PHASE_KINDS, VERIFICATION_STATES
from .model import index, to_minutes
from .planner import EXCEPTION_KINDS, _slots

HOUR_COLUMNS = ("theory", "practice", "exam")
SOLUTION_BASES = ("textbook", "inferred", "teacher")


def schedule_digest(schedule):
    """Stable digest of the schedule content a session plan was derived from."""
    text = json.dumps(schedule, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _nonempty_strings(value):
    return isinstance(value, list) and value and all(isinstance(x, str) and x.strip() for x in value)


def check_course(course, errors, warnings):
    if course.get("audit_contract") != CONTRACT:
        errors.append(f"CONTRACT: {CONTRACT} required")
    if course.get("review", {}).get("learning_effectiveness") != "not_assessed":
        errors.append("EFFECTIVENESS_CLAIM: no learner-effectiveness evidence exists")
    lessons = index(course.get("lessons"), "lessons")
    labs = index(course.get("labs"), "labs")
    assessments = index(course.get("assessments"), "assessments")
    outcomes = index(course.get("outcomes"), "outcomes")
    equipment = index(course.get("equipment"), "equipment")
    sources = index(course.get("sources"), "sources")
    policy = course.get("time_policy", {})
    rates = policy.get("minutes_per_hour", {})
    if any(type(rates.get(k)) is not int or not 0 < rates[k] <= 60 for k in BLOCK_KINDS):
        errors.append("TIME_POLICY: minutes_per_hour needs theory/practice/assessment in 1..60")
    defaults = policy.get("default_phase_minutes", {})
    if any(type(defaults.get(k)) is not int or defaults[k] < 0 for k in
           ("on_dinh_lop", "dan_nhap", "gioi_thieu_chu_de", "ket_thuc_van_de", "huong_dan_tu_hoc")):
        errors.append("TIME_POLICY: default_phase_minutes incomplete")
    for source in sources.values():
        if not all(source.get(k) for k in ("locator", "accessed_at", "scope_actually_read")):
            errors.append(f"SOURCE_LOCATOR: {source['id']}")
    for lid, lesson in lessons.items():
        hours = lesson.get("program_hours", {})
        if any(type(hours.get(k)) not in (int, float) or hours[k] < 0 for k in ("theory", "practice")):
            errors.append(f"PROGRAM_HOURS: {lid}")
        for ref, pool, label in ((lesson.get("prerequisite_ids", []), lessons, "PREREQUISITE_REF"),
                                 (lesson.get("equipment_ids", []), equipment, "EQUIPMENT_REF"),
                                 (lesson.get("lab_ids", []), labs, "LAB_REF"),
                                 ([lesson.get("source_id")], sources, "SOURCE_REF")):
            if any(r not in pool for r in ref):
                errors.append(f"{label}: {lid}")
        if hours.get("practice") and not lesson.get("lab_ids"):
            errors.append(f"PRACTICE_WITHOUT_TASK: {lid}")
    state, order = {}, []
    def visit(lid):
        if state.get(lid) == 1:
            errors.append(f"PREREQUISITE_CYCLE: {lid}")
            return
        if state.get(lid) == 2:
            return
        state[lid] = 1
        for p in lessons[lid].get("prerequisite_ids", []):
            if p in lessons:
                visit(p)
        state[lid] = 2
        order.append(lid)
    for lid in lessons:
        visit(lid)
    for lab_id, lab in labs.items():
        if lab.get("lesson_id") not in lessons or lab_id not in lessons[lab["lesson_id"]].get("lab_ids", []):
            errors.append(f"LAB_LESSON: {lab_id}")
        if not isinstance(lab.get("requirement"), str) or not lab["requirement"].strip():
            errors.append(f"LAB_REQUIREMENT: {lab_id}")
        rubric = lab.get("rubric")
        if not _nonempty_strings(rubric) or len(rubric) < 3:
            errors.append(f"LAB_RUBRIC: {lab_id} needs at least three criteria")
        if not _nonempty_strings(lab.get("safety")):
            errors.append(f"LAB_SAFETY: {lab_id}")
        faults = lab.get("common_faults")
        if (not isinstance(faults, list) or not faults
                or any(not isinstance(f, dict) or not f.get("fault") or not f.get("remedy") for f in faults)):
            errors.append(f"LAB_FAULTS: {lab_id} needs fault/remedy pairs")
        if lab.get("verification") not in VERIFICATION_STATES:
            errors.append(f"LAB_VERIFICATION: {lab_id}")
        if lab.get("solution_basis") not in SOLUTION_BASES:
            errors.append(f"LAB_SOLUTION_BASIS: {lab_id}")
        if lab.get("solution_basis") == "inferred" and lab.get("verification") != "draft" \
                and not lab.get("verified_by"):
            errors.append(f"LAB_VERIFIER: {lab_id} verified without a recorded verifier")
    for aid, item in assessments.items():
        if item.get("placement", "pinned") not in ("pinned", "floating"):
            errors.append(f"ASSESSMENT_PLACEMENT: {aid}")
        if item.get("kind") not in ("periodic", "final") or item.get("hour_column") not in HOUR_COLUMNS:
            errors.append(f"ASSESSMENT_KIND: {aid}")
        scope = item.get("scope_lesson_ids")
        if not isinstance(scope, list) or not scope or any(s not in lessons for s in scope):
            errors.append(f"ASSESSMENT_SCOPE: {aid}")
        if not item.get("format") or not item.get("duration_basis"):
            errors.append(f"ASSESSMENT_FORMAT: {aid}")
        if item.get("duration_basis") == "assumed":
            warnings.append(f"ASSUMED_DURATION: {aid} duration is a default, not a confirmed school rule")
        if any(e not in equipment for e in item.get("equipment_ids", [])):
            errors.append(f"EQUIPMENT_REF: {aid}")
    covered, assessed = set(), set()
    for oid, outcome in outcomes.items():
        if outcome.get("domain") not in ("knowledge", "skill", "autonomy") or not outcome.get("text"):
            errors.append(f"OUTCOME_SHAPE: {oid}")
        refs, checks = outcome.get("lesson_ids", []), outcome.get("assessment_ids", [])
        if not refs or any(r not in lessons for r in refs):
            errors.append(f"OUTCOME_LESSONS: {oid}")
        if not checks or any(a not in assessments for a in checks):
            errors.append(f"OUTCOME_ASSESSMENT: {oid}")
        for a in checks:
            if a in assessments and not set(refs) & set(assessments[a].get("scope_lesson_ids", [])):
                errors.append(f"ALIGNMENT: {oid} is assessed by {a} outside its lessons")
        covered.update(refs)
        assessed.update(checks)
    if set(lessons) - covered:
        errors.append(f"OUTCOME_COVERAGE: lessons without outcomes {sorted(set(lessons) - covered)}")
    return lessons, assessments, order


def baseline_totals(course, schedule, lessons, assessments, errors, warnings):
    if schedule.get("course_id") != course.get("course", {}).get("id"):
        errors.append("SCHEDULE_COURSE: schedule belongs to another course")
    totals, per_lesson = defaultdict(int), defaultdict(lambda: defaultdict(int))
    for week in schedule.get("weeks", []):
        wid, available = week.get("week"), set(week.get("equipment_ids", []))
        for block in week.get("blocks", []):
            kind, minutes = block.get("kind"), to_minutes(block.get("hours"))
            if kind == "assessment":
                item = assessments.get(block.get("assessment_id"))
                if item is None:
                    errors.append(f"SCHEDULE_ASSESSMENT_REF: week {wid}")
                    continue
                totals[item.get("hour_column")] += minutes
                needed = set(item.get("equipment_ids", []))
            elif kind in ("theory", "practice") and block.get("lesson_id") in lessons:
                totals[kind] += minutes
                per_lesson[block["lesson_id"]][kind] += minutes
                needed = set(lessons[block["lesson_id"]].get("equipment_ids", []))
            else:
                errors.append(f"SCHEDULE_BLOCK: week {wid}")
                continue
            if not needed <= available:
                errors.append(f"SCHEDULE_EQUIPMENT: week {wid} lacks {sorted(needed - available)}")
    program = course.get("module_program", {})
    for column, key in (("theory", "theory_hours"), ("practice", "practice_hours"), ("exam", "exam_hours")):
        if totals[column] != to_minutes(program.get(key, -1) if program.get(key) is not None else 0):
            errors.append(f"MODULE_HOURS: schedule {column} {totals[column] / 60}h != program {program.get(key)}h")
    for lid, lesson in lessons.items():
        planned = {k: per_lesson[lid][k] / 60 for k in ("theory", "practice")}
        expected = {k: lesson.get("program_hours", {}).get(k) for k in ("theory", "practice")}
        if planned != expected:
            warnings.append(f"PROGRAM_DEVIATION: {lid} schedule {planned} vs program {expected}")
    for exc in schedule.get("exceptions", []):
        if exc.get("kind") not in EXCEPTION_KINDS or not exc.get("reason"):
            errors.append(f"EXCEPTION_SHAPE: {exc.get('kind')!r} needs a known kind and a reason")
    return totals, per_lesson


def check_sessions(course, schedule, document, lessons, assessments, errors, warnings):
    if document.get("schedule_sha256") != schedule_digest(schedule):
        errors.append("STALE_PLAN: sessions were not planned from this schedule; rerun plan_schedule")
    if document.get("unscheduled"):
        errors.append(f"UNSCHEDULED: {len(document['unscheduled'])} block(s) found no slot")
    sessions = document.get("sessions")
    if not isinstance(sessions, list) or not sessions:
        errors.append("SESSIONS_SHAPE: nonempty sessions list required")
        return {}
    index(sessions, "sessions")
    rates = course["time_policy"]["minutes_per_hour"]
    slots = {s["key"]: s for s in _slots(schedule)}
    position, placed, previous = {}, defaultdict(int), None
    if [s.get("start") for s in sessions] != sorted(s.get("start") for s in sessions):
        errors.append("SESSION_ORDER: sessions must be in date order")
    for n, session in enumerate(sessions):
        sid = session.get("id")
        if session.get("ga_number") != n + 1:
            errors.append(f"GA_NUMBER: {sid}")
        if session.get("previous_lesson_id") != previous:
            errors.append(f"PREVIOUS_LESSON: {sid}")
        slot = slots.get(sid)
        if slot is None or slot["start"] != session.get("start"):
            errors.append(f"SLOT: {sid} does not match a scheduled session date")
            continue
        blocks = session.get("blocks", [])
        if not blocks or any(b.get("kind") not in BLOCK_KINDS for b in blocks):
            errors.append(f"BLOCK_KIND: {sid}")
            continue
        minutes = [to_minutes(b.get("hours")) for b in blocks]
        if sum(minutes) > slot["capacity"]:
            errors.append(f"CAPACITY: {sid} uses {sum(minutes)} of {slot['capacity']} minutes")
        needed = set()
        for k, (block, used) in enumerate(zip(blocks, minutes)):
            if block["kind"] == "assessment":
                aid = block.get("assessment_id")
                if aid not in assessments:
                    errors.append(f"ASSESSMENT_REF: {sid}")
                    continue
                if aid in position:
                    errors.append(f"ASSESSMENT_REPEAT: {aid}")
                position[aid] = (n, k)
                placed[(aid, "assessment")] += used
                needed |= set(assessments[aid].get("equipment_ids", []))
            elif block.get("lesson_id") in lessons:
                lid = block["lesson_id"]
                position.setdefault(("first", lid), (n, k))
                position[("last", lid)] = (n, k)
                placed[(lid, block["kind"])] += used
                needed |= set(lessons[lid].get("equipment_ids", []))
            else:
                errors.append(f"LESSON_REF: {sid}")
        if not needed <= slot["equipment"]:
            errors.append(f"EQUIPMENT: {sid} needs {sorted(needed - slot['equipment'])}")
        taught = [b["lesson_id"] for b in blocks if b["kind"] != "assessment" and b.get("lesson_id")]
        previous = taught[-1] if taught else previous
        phases = session.get("phases", [])
        kinds = [p.get("kind") for p in phases]
        if any(k not in PHASE_KINDS for k in kinds) or kinds != sorted(kinds, key=PHASE_KINDS.index):
            errors.append(f"PHASE_ORDER: {sid}")
        expected = sum(m * rates[b["kind"]] // 60 for b, m in zip(blocks, minutes))
        if sum(p.get("minutes", 0) if type(p.get("minutes")) is int else 10**9 for p in phases) != expected:
            errors.append(f"PHASE_MINUTES: {sid} phases must total {expected}")
        checking = sum(m * rates["assessment"] // 60 for b, m in zip(blocks, minutes) if b["kind"] == "assessment")
        if sum(p["minutes"] for p in phases if p.get("kind") == "kiem_tra" and type(p.get("minutes")) is int) != checking:
            errors.append(f"PHASE_ASSESSMENT: {sid} kiem_tra minutes must equal assessment time")
    for lid, lesson in lessons.items():
        if ("first", lid) not in position:
            continue
        for p in lesson.get("prerequisite_ids", []):
            if ("last", p) not in position or position[("last", p)] >= position[("first", lid)]:
                errors.append(f"PREREQUISITE_ORDER: {lid} starts before {p} is finished")
    for aid, item in assessments.items():
        if aid not in position:
            errors.append(f"ASSESSMENT_MISSING: {aid}")
            continue
        for lid in item.get("scope_lesson_ids", []):
            if ("last", lid) not in position or position[("last", lid)] > position[aid]:
                errors.append(f"ASSESSED_BEFORE_TAUGHT: {aid} covers {lid}")
    return placed


def required_minutes(schedule, lessons):
    need = defaultdict(int)
    for week in schedule.get("weeks", []):
        for block in week.get("blocks", []):
            key = block.get("assessment_id") if block.get("kind") == "assessment" else block.get("lesson_id")
            need[(key, block.get("kind"))] += to_minutes(block.get("hours"))
    for exc in schedule.get("exceptions", []):
        if exc.get("kind") == "extend_lesson":
            need[(exc.get("lesson_id"), exc.get("block_kind", "practice"))] += to_minutes(exc.get("hours"))
    return need


def audit(course, schedule, sessions_document=None):
    errors, warnings = [], []
    counts = {}
    try:
        lessons, assessments, _ = check_course(course, errors, warnings)
        totals, _ = baseline_totals(course, schedule, lessons, assessments, errors, warnings)
        counts.update({f"{k}_hours": v / 60 for k, v in sorted(totals.items())})
        if sessions_document is not None:
            placed = check_sessions(course, schedule, sessions_document, lessons, assessments, errors, warnings)
            for key, minutes in required_minutes(schedule, lessons).items():
                if placed.get(key, 0) != minutes:
                    errors.append(f"COVERAGE: {key[0]} {key[1]} planned {placed.get(key, 0) / 60}h "
                                  f"of {minutes / 60}h")
            counts["sessions"] = len(sessions_document.get("sessions", []))
        counts.update({"lessons": len(lessons), "assessments": len(assessments),
                       "labs": len(course.get("labs", [])),
                       "labs_teacher_verified": sum(l.get("verification") != "draft" for l in course.get("labs", []))})
    except (KeyError, TypeError, ValueError, AttributeError, RecursionError) as exc:
        errors.append(f"INVALID_SHAPE: {type(exc).__name__}: {exc}")
    return {
        "audit_version": "vocational-1.0.0", "contract": CONTRACT, "passed": not errors,
        "scope": "Schedule arithmetic, ordering, equipment, GA time budget and declared lab fields",
        "errors": sorted(set(errors)), "warnings": sorted(set(warnings)), "counts": counts,
        "teacher_review": "not_run", "learner_pilot": "not_run", "learning_effectiveness": "not_assessed",
        "limits": [
            "Checks declared structure only; it does not run PLC programs or judge wiring correctness.",
            "A lab marked draft has an AI-inferred solution that no teacher has tested on a kit.",
            "Rubric, safety and fault lists are checked for presence, not adequacy.",
            "Minutes-per-hour and assessment durations come from course.time_policy; confirm them locally.",
            "This is a bounded profile for schedule-driven vocational modules, not a general validator.",
        ],
    }
