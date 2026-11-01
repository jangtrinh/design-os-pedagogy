"""Deterministic binding of course content blocks to schedule slots.

The teacher's baseline schedule fixes an ordered queue of blocks (lesson x kind x hours).
Exceptions change the slots (cancel, shorten, add a make-up session, missing equipment)
or the queue (extra hours for a lesson). Planning is greedy list scheduling: each slot
takes the earliest queued block that is allowed there, splitting theory/practice blocks
on a quarter-hour grid and never splitting an assessment. With no exceptions the output
reproduces the baseline exactly. Nothing here calls a model.
"""
from datetime import timedelta

from . import BLOCK_KINDS
from .model import GRANULARITY, index, iso_date, to_minutes

FIXED_PHASES = ("on_dinh_lop", "dan_nhap", "gioi_thieu_chu_de")
CLOSING_PHASES = ("ket_thuc_van_de", "huong_dan_tu_hoc")
EXCEPTION_KINDS = ("cancel_session", "set_hours", "add_session", "equipment_unavailable", "extend_lesson")


def _block(raw, lessons, assessments):
    kind = raw.get("kind")
    if kind not in BLOCK_KINDS:
        raise ValueError(f"Unknown block kind: {kind!r}")
    block = {"kind": kind, "minutes": to_minutes(raw.get("hours"))}
    if block["minutes"] == 0:
        raise ValueError("Blocks must have positive hours")
    if kind == "assessment":
        aid = raw.get("assessment_id")
        if aid not in assessments:
            raise ValueError(f"Unknown assessment: {aid!r}")
        block["assessment_id"] = aid
    else:
        lid = raw.get("lesson_id")
        if lid not in lessons:
            raise ValueError(f"Unknown lesson: {lid!r}")
        block["lesson_id"] = lid
        items = raw.get("items", [])
        if not isinstance(items, list) or any(not isinstance(i, str) for i in items):
            raise ValueError("Block items must be strings")
        block["items"] = list(items)
    return block


def _equipment(block, lessons, assessments):
    if block["kind"] == "assessment":
        return set(assessments[block["assessment_id"]].get("equipment_ids", []))
    return set(lessons[block["lesson_id"]].get("equipment_ids", []))


def _slots(schedule):
    calendar = schedule.get("calendar", {})
    first = iso_date(calendar.get("first_week_start"))
    default = to_minutes(calendar.get("session_hours"))
    pool = calendar.get("available_equipment_ids")
    slots = {}
    for week in schedule.get("weeks", []):
        number = week.get("week")
        if type(number) is not int or number in slots:
            raise ValueError(f"Invalid or duplicate week number: {number!r}")
        start = iso_date(week.get("start"))
        if start != first + timedelta(weeks=number - 1):
            raise ValueError(f"Week {number} start does not follow the calendar")
        slots[number] = {"key": f"W{number:02}", "week": number, "start": start.isoformat(),
                         "end": week.get("end"), "capacity": default,
                         "equipment": set(week.get("equipment_ids", []) if pool is None else pool),
                         "notes": []}
    for exc in schedule.get("exceptions", []):
        kind = exc.get("kind")
        if kind not in EXCEPTION_KINDS:
            raise ValueError(f"Unknown exception kind: {kind!r}")
        if kind == "add_session":
            start = iso_date(exc.get("start"))
            number = (start - first).days // 7 + 1
            key = f"M{len([s for s in slots.values() if s['key'].startswith('M')]) + 1:02}"
            slots[key] = {"key": key, "week": number, "start": start.isoformat(),
                          "end": exc.get("end", start.isoformat()),
                          "capacity": to_minutes(exc.get("hours", calendar.get("session_hours"))),
                          "equipment": set(exc.get("equipment_ids", pool or [])),
                          "notes": [exc.get("reason", "add_session")]}
            continue
        if kind == "extend_lesson":
            continue
        slot = slots.get(exc.get("week"))
        if slot is None:
            raise ValueError(f"Exception refers to unknown week: {exc.get('week')!r}")
        slot["notes"].append(exc.get("reason", kind))
        if kind == "cancel_session":
            slot["capacity"] = 0
        elif kind == "set_hours":
            slot["capacity"] = to_minutes(exc.get("hours"))
        elif kind == "equipment_unavailable":
            slot["equipment"] -= set(exc.get("equipment_ids", []))
    return sorted(slots.values(), key=lambda s: (s["start"], s["key"]))


def _queue(course, schedule, lessons, assessments):
    queue = []
    for week in sorted(schedule.get("weeks", []), key=lambda w: w.get("week")):
        if to_minutes(sum(b.get("hours", 0) for b in week.get("blocks", []))) != to_minutes(
                schedule["calendar"]["session_hours"]):
            raise ValueError(f"Baseline week {week.get('week')} blocks must fill the session")
        for raw in week.get("blocks", []):
            block = _block(raw, lessons, assessments)
            if block["kind"] == "assessment" and _pinned(assessments[block["assessment_id"]]):
                block["pinned_week"] = week.get("week")
            queue.append(block)
    for exc in schedule.get("exceptions", []):
        if exc.get("kind") != "extend_lesson":
            continue
        extra = _block({**exc, "kind": exc.get("block_kind", "practice"),
                        "items": exc.get("items", ["Luyện tập bổ sung"])}, lessons, assessments)
        if extra["kind"] == "assessment":
            raise ValueError("extend_lesson cannot add assessment time")
        last = max((i for i, b in enumerate(queue) if b.get("lesson_id") == extra["lesson_id"]), default=None)
        if last is None:
            raise ValueError(f"extend_lesson for unscheduled lesson {extra['lesson_id']}")
        queue.insert(last + 1, extra)
    return queue


def _pinned(assessment):
    return assessment.get("placement", "pinned" if assessment.get("kind") == "final" else "floating") == "pinned"


def _allowed(position, queue, slot, lessons, assessments, done):
    block = queue[position]
    if "pinned_week" in block:
        return False  # placed only by the pinned pass
    if not _equipment(block, lessons, assessments) <= slot["equipment"]:
        return False
    earlier = queue[:position]
    if block["kind"] == "assessment":
        scope = assessments[block["assessment_id"]].get("scope_lesson_ids", [])
        return all(b.get("lesson_id") not in scope for b in earlier)
    lid = block["lesson_id"]
    if any(b.get("lesson_id") == lid for b in earlier):
        return False  # keep each lesson's own block order
    prereqs = lessons[lid].get("prerequisite_ids", [])
    return all(p in done and all(b.get("lesson_id") != p for b in earlier) for p in prereqs)


def phase_skeleton(blocks, policy):
    """Minutes per GA phase from the time policy; prose is filled by generators later."""
    rates = policy["minutes_per_hour"]
    teach = sum(b["minutes"] * rates[b["kind"]] // 60 for b in blocks if b["kind"] != "assessment")
    check = sum(b["minutes"] * rates["assessment"] // 60 for b in blocks if b["kind"] == "assessment")
    if not teach:
        return [{"kind": "kiem_tra", "minutes": check}] if check else []
    defaults = policy["default_phase_minutes"]
    fixed = [{"kind": k, "minutes": defaults[k]} for k in FIXED_PHASES]
    closing = [{"kind": k, "minutes": defaults[k]} for k in CLOSING_PHASES]
    core = teach - sum(p["minutes"] for p in fixed + closing)
    if core < GRANULARITY:
        raise ValueError("Session too short for the GA phase structure")
    middle = [{"kind": "giai_quyet_van_de", "minutes": core}]
    if check:
        middle.append({"kind": "kiem_tra", "minutes": check})
    return fixed + middle + closing


def plan(course, schedule):
    """Return {sessions, unscheduled, warnings} for one course and one schedule."""
    lessons = index(course.get("lessons"), "lessons")
    assessments = index(course.get("assessments"), "assessments")
    policy = course.get("time_policy")
    if not isinstance(policy, dict):
        raise ValueError("course.time_policy must be an object")
    queue, slots = _queue(course, schedule, lessons, assessments), _slots(schedule)
    sessions, done, warnings, previous = [], set(), [], None
    for slot in slots:
        remaining, placed = slot["capacity"], []
        for pin in [b for b in queue if b.get("pinned_week") == slot["week"] and slot["key"].startswith("W")]:
            if pin["minutes"] <= remaining:
                queue.remove(pin)
                placed.append({k: v for k, v in pin.items() if k != "pinned_week"})
                remaining -= pin["minutes"]
        while remaining > 0:
            position = next((i for i in range(len(queue))
                             if _allowed(i, queue, slot, lessons, assessments, done)
                             and (queue[i]["kind"] != "assessment" or queue[i]["minutes"] <= remaining)), None)
            if position is None:
                break
            block = queue[position]
            take = min(block["minutes"], remaining)
            piece = {**block, "minutes": take}
            if take < block["minutes"]:
                block["minutes"] -= take
            else:
                queue.pop(position)
                if block["kind"] != "assessment" and all(
                        b.get("lesson_id") != block["lesson_id"] for b in queue):
                    done.add(block["lesson_id"])
            if placed and placed[-1].get("lesson_id") == piece.get("lesson_id") \
                    and placed[-1]["kind"] == piece["kind"] and piece["kind"] != "assessment":
                placed[-1]["minutes"] += take
                placed[-1]["items"] += [i for i in piece["items"] if i not in placed[-1]["items"]]
            else:
                placed.append(piece)
            remaining -= take
        if remaining and slot["capacity"]:
            warnings.append(f"SPARE_TIME: {slot['key']} has {remaining} unplanned minutes")
        if not placed:
            continue
        needed = set().union(*(_equipment(b, lessons, assessments) for b in placed))
        taught = [b["lesson_id"] for b in placed if b["kind"] != "assessment"]
        phases = phase_skeleton(placed, policy)
        blocks = [{**{k: v for k, v in b.items() if k != "minutes"}, "hours": b["minutes"] / 60} for b in placed]
        sessions.append({
            "id": slot["key"], "week": slot["week"], "start": slot["start"], "end": slot["end"],
            "ga_number": len(sessions) + 1, "previous_lesson_id": previous,
            "blocks": blocks, "equipment_ids": sorted(needed), "notes": slot["notes"],
            "phases": phases, "status": "skeleton",
        })
        previous = taught[-1] if taught else previous
    unscheduled = [{**{k: v for k, v in b.items() if k not in ("minutes", "pinned_week")},
                    "hours": b["minutes"] / 60} for b in queue]
    for block in unscheduled:
        warnings.append(f"UNSCHEDULED: {block.get('lesson_id') or block.get('assessment_id')} "
                        f"{block['kind']} {block['hours']}h")
    return {"sessions": sessions, "unscheduled": unscheduled, "warnings": warnings}


def diff(old_sessions, new_sessions):
    """Session ids whose dates or content blocks changed between two plans."""
    key = lambda s: (s.get("start"), [(b.get("lesson_id"), b.get("assessment_id"), b.get("kind"), b.get("hours"))
                                      for b in s.get("blocks", [])])
    old = {s.get("id"): key(s) for s in old_sessions}
    new = {s.get("id"): key(s) for s in new_sessions}
    return {"added": sorted(set(new) - set(old)), "removed": sorted(set(old) - set(new)),
            "changed": sorted(i for i in set(old) & set(new) if old[i] != new[i])}
