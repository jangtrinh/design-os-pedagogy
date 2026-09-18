"""Referential, scheduling and coverage checks, independent of prose quality."""
from collections import Counter


def object_list(value, label, errors):
    if not isinstance(value, list) or not value or any(not isinstance(x, dict) for x in value):
        errors.append(f"SHAPE: {label} must be a nonempty list of objects")
        return []
    return value


def unique(records, label, errors):
    ids = [r.get("id") for r in records]
    if any(not isinstance(i, str) or not i for i in ids):
        errors.append(f"ID: {label} contains missing or invalid IDs")
    counts = Counter(i for i in ids if isinstance(i, str))
    if any(n > 1 for n in counts.values()):
        errors.append(f"DUPLICATE_ID: {label}")
    return {r["id"]: r for r in records if isinstance(r.get("id"), str)}


def ids(value):
    return value if isinstance(value, list) and all(isinstance(i, str) for i in value) else []


def check_structure(course, sessions, profile, exams):
    errors = []
    required = {f"R{i:02}" for i in range(1, 25)}
    outcomes = object_list(course.get("outcomes"), "outcomes", errors)
    units = object_list(course.get("units"), "units", errors)
    sessions = object_list(sessions, "sessions", errors)
    exam_groups = object_list(exams.get("groups"), "exam groups", errors)
    unique(outcomes, "outcomes", errors)
    unit_map = unique(units, "units", errors)
    unique(sessions, "sessions", errors)
    unique(exam_groups, "exam groups", errors)
    requirements = object_list(profile.get("requirements"), "profile requirements", errors)
    if set(unique(requirements, "requirements", errors)) != required:
        errors.append("PROFILE_REQUIREMENTS: expected the 24 checked requirements")
    if set(ids(course.get("curriculum_alignment", {}).get("requirement_ids"))) != required:
        errors.append("DECLARED_COVERAGE: curriculum requirement set differs")
    if course.get("audit_contract") != "course-audit-1.0":
        errors.append("CONTRACT: course-audit-1.0 required")
    if profile.get("profile_id") != "vn-grade1-math-2018-checked-20260917":
        errors.append("PROFILE: unsupported; no national-conformity conclusion")
    limits = {"weeks": 35, "periods_per_week": 3, "period_minutes": 35, "total_periods": 105}
    for key, expected in limits.items():
        if type(profile.get(key)) is not int or profile[key] != expected:
            errors.append(f"PROFILE_TIME: {key}")
        value = course.get("constraints", {}).get(key)
        if type(value) is not int or value != expected:
            errors.append(f"COURSE_TIME: {key}")
    periods = [s.get("period") for s in sessions]
    valid_periods = all(type(n) is int for n in periods)
    if not valid_periods or sorted(periods) != list(range(1, 106)):
        errors.append("PERIOD_SEQUENCE: exactly 1-105 once each required")
    practice, assessment, covered, first_taught = {}, {}, set(), {}
    total_minutes = 0
    for session in sessions:
        sid, period = session.get("id"), session.get("period")
        if type(period) is not int:
            continue
        if type(session.get("week")) is not int or session["week"] != (period + 2) // 3:
            errors.append(f"WEEK: {sid}")
        minutes, parts = session.get("minutes"), session.get("activity_minutes")
        if (type(minutes) is not int or minutes != 35 or not isinstance(parts, list)
                or not parts or any(type(n) is not int or n < 0 for n in parts)
                or sum(parts) != minutes):
            errors.append(f"TIME_BUDGET: {sid}")
        total_minutes += minutes if type(minutes) is int else 0
        if session.get("reading_required") is not False:
            errors.append(f"READING_DEPENDENCY: {sid}")
        if session.get("mandatory_homework_minutes") != 0:
            errors.append(f"HIDDEN_HOMEWORK: {sid}")
        tags = ids(session.get("standard_ids"))
        if not tags or set(tags) - required:
            errors.append(f"STANDARD_REFERENCE: {sid}")
        covered.update(tags)
        if period not in (53, 104):
            for rid in tags:
                first_taught[rid] = min(period, first_taught.get(rid, period))
        for field, target in (("practice", practice), ("exit_task", assessment)):
            task = session.get(field)
            if not isinstance(task, dict) or not isinstance(task.get("id"), str):
                errors.append(f"TASK_REFERENCE: {sid}/{field}")
                continue
            if task["id"] in target:
                errors.append(f"DUPLICATE_ID: {task['id']}")
            target[task["id"]] = set(tags)
            for key in ("prompt", "answer"):
                if task.get(key) is None or task.get(key) == "":
                    errors.append(f"TASK_CONTENT: {sid}/{field}/{key}")
        if not session.get("teacher_model") or session.get("unit_id") not in unit_map:
            errors.append(f"SESSION_CONTENT: {sid}")
    if total_minutes != 3675 or course.get("constraints", {}).get("contact_minutes") != total_minutes:
        errors.append("TOTAL_MINUTES: expected 3675")
    if covered != required:
        errors.append(f"COVERAGE: missing {sorted(required - covered)}")
    outcome_coverage = set()
    for outcome in outcomes:
        oid, tags = outcome.get("id"), set(ids(outcome.get("standard_ids")))
        outcome_coverage.update(tags)
        if not tags or tags - required:
            errors.append(f"OUTCOME_STANDARD: {oid}")
        for field, target in (("practice_ids", practice), ("assessment_ids", assessment)):
            refs = ids(outcome.get(field))
            if not refs or any(ref not in target or not tags <= target[ref] for ref in refs):
                errors.append(f"ALIGNMENT: {oid}/{field}")
        if not outcome.get("content_source_ids"):
            errors.append(f"OUTCOME_SOURCE: {oid}")
    if outcome_coverage != required:
        errors.append("OUTCOME_COVERAGE: standards missing from outcomes")
    active, done = set(), set()
    def visit(uid):
        if uid in active:
            errors.append(f"PREREQUISITE_CYCLE: {uid}")
            return
        if uid in done:
            return
        active.add(uid)
        for dep in ids(unit_map[uid].get("prerequisite_unit_ids")):
            if dep not in unit_map:
                errors.append(f"PREREQUISITE_UNKNOWN: {dep}")
            else:
                visit(dep)
                if (type(unit_map[dep].get("end_period")) is not int
                        or type(unit_map[uid].get("start_period")) is not int
                        or unit_map[dep]["end_period"] >= unit_map[uid]["start_period"]):
                    errors.append(f"PREREQUISITE_ORDER: {dep}->{uid}")
        active.remove(uid)
        done.add(uid)
    for uid, unit in unit_map.items():
        if not isinstance(unit.get("prerequisite_unit_ids"), list) or any(
                not isinstance(x, str) for x in unit.get("prerequisite_unit_ids", [])):
            errors.append(f"PREREQUISITE_SHAPE: {uid}")
        visit(uid)
        members = [s for s in sessions if s.get("unit_id") == uid]
        if set(ids(unit.get("session_ids"))) != {s.get("id") for s in members}:
            errors.append(f"UNIT_MEMBERS: {uid}")
        if unit.get("contact_minutes") != 35 * len(members):
            errors.append(f"UNIT_TIME: {uid}")
        if members and (unit.get("start_period") != min(s["period"] for s in members)
                        or unit.get("end_period") != max(s["period"] for s in members)):
            errors.append(f"UNIT_RANGE: {uid}")
    for group in exam_groups:
        items = object_list(group.get("items"), str(group.get("id")), errors)
        unique(items, str(group.get("id")), errors)
        if any(type(t.get("points")) is not int or t["points"] < 0 for t in items):
            errors.append("EXAM_POINTS: integer points required")
        elif sum(t["points"] for t in items) != 10:
            errors.append("EXAM_POINTS: total must be ten")
        for item in items:
            tags = ids(item.get("standard_ids"))
            if not tags or set(tags) - required:
                errors.append(f"EXAM_STANDARD: {item.get('id')}")
            for rid in tags:
                if rid not in first_taught or type(group.get("period")) is not int or first_taught[rid] >= group["period"]:
                    errors.append(f"ASSESSMENT_BEFORE_PRACTICE: {item.get('id')}/{rid}")
    return sorted(set(errors))
