"""Load and audit one explicitly versioned course bundle without mutation."""
import hashlib
from collections import Counter
from pathlib import Path

from ..knowledge.frontmatter import load_mapping
from ..pipeline_support.transactions import inside, read_text
from .math_checks import check_task
from .structure import check_structure


def load_bundle(folder):
    folder = Path(folder)
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError("Course folder must exist and must not be a symlink")
    hashes = {}
    def load(name):
        if not isinstance(name, str):
            raise ValueError("Course file path must be a string")
        text = read_text(inside(folder, name))
        hashes[name] = hashlib.sha256(text.encode("utf-8")).hexdigest()
        return load_mapping(text)
    course = load("course.yaml")
    names = course.get("session_files")
    if (not isinstance(names, list) or not 1 <= len(names) <= 12
            or any(not isinstance(n, str) for n in names) or len(names) != len(set(names))):
        raise ValueError("One to twelve unique session file paths are required")
    sessions = []
    for name in names:
        value = load(name).get("sessions")
        if not isinstance(value, list):
            raise ValueError("Session files must contain a sessions list")
        sessions.extend(value)
    return course, sessions, load("requirements.yaml"), load("assessments.yaml"), hashes


def audit_bundle(course, sessions, profile, exams, *, known_sources=None):
    errors, warnings, verified, manual = [], [], [], []
    if not all(isinstance(x, dict) for x in (course, profile, exams)) or not isinstance(sessions, list):
        return {"passed": False, "errors": ["BUNDLE_SHAPE: objects and sessions list required"]}
    for field in ("outcomes", "units", "sources", "assessment_events"):
        value = course.get(field)
        if not isinstance(value, list) or not value or any(not isinstance(x, dict) for x in value):
            return {"passed": False, "errors": [f"BUNDLE_SHAPE: {field} must contain objects"]}
    for field in ("constraints", "curriculum_alignment", "learner_profile", "review"):
        if not isinstance(course.get(field), dict):
            return {"passed": False, "errors": [f"BUNDLE_SHAPE: {field} must be an object"]}
    if course["learner_profile"].get("stage") != "S2" or course["learner_profile"].get("grade") != 1:
        errors.append("LEARNER_SCOPE: this profile is for S2, grade 1")
    try:
        errors.extend(check_structure(course, sessions, profile, exams))
        source_rows = course.get("sources", [])
        if not isinstance(source_rows, list) or any(not isinstance(s, dict) for s in source_rows):
            raise ValueError("sources must be objects")
        source_map = {s.get("id"): s for s in source_rows}
        if len(source_map) != len(source_rows) or None in source_map:
            errors.append("SOURCE_IDS: missing or duplicate source IDs")
        for source in source_rows:
            if not all(source.get(k) for k in ("locator", "accessed_at", "scope_actually_read", "knowledge_source_id")):
                errors.append(f"SOURCE_LOCATOR: {source.get('id')}")
            if known_sources is not None and source.get("knowledge_source_id") not in known_sources:
                errors.append(f"UNKNOWN_KNOWLEDGE_SOURCE: {source.get('id')}")
        for outcome in course.get("outcomes", []):
            if any(s not in source_map for s in outcome.get("content_source_ids", [])):
                errors.append(f"OUTCOME_SOURCE: {outcome.get('id')}")
        if known_sources is None:
            warnings.append("Knowledge source IDs were not checked against a registry in this invocation.")
        tasks = [(s.get("id"), s.get("exit_task")) for s in sessions if isinstance(s, dict)]
        for group in exams.get("groups", []):
            tasks.extend((t.get("id"), t) for t in group.get("items", []))
        for name, task in tasks:
            failures, recomputed = check_task(task)
            errors.extend(f"{name}: {failure}" for failure in failures)
            if recomputed:
                verified.append(name)
            elif isinstance(task, dict) and task.get("kind") == "observation":
                manual.append(name)
        events = course.get("assessment_events", [])
        actual_groups = {(g.get("id"), g.get("period")) for g in exams.get("groups", [])}
        declared_groups = {(e.get("id"), e.get("period")) for e in events}
        if actual_groups != declared_groups or len(events) != 2 or len(actual_groups) != 2:
            errors.append("ASSESSMENT_EVENTS: two declared sample end-term events must match task groups")
        if any(e.get("kind") != "periodic-written" or e.get("max_score") != 10 for e in events):
            errors.append("ASSESSMENT_POLICY: expected ten-point sample end-term written tests")
        for group in exams.get("groups", []):
            if any(type(t.get("level")) is not int or t["level"] not in (1, 2, 3)
                   or not t.get("criterion") for t in group.get("items", [])):
                errors.append("EXAM_RUBRIC: level 1-3 and scoring criterion required")
        if course.get("review", {}).get("learning_effectiveness") != "not_assessed":
            errors.append("EFFECTIVENESS_CLAIM: this fixture has no learner-effectiveness evidence")
    except (KeyError, TypeError, ValueError, AttributeError, RecursionError) as exc:
        errors.append(f"INVALID_SHAPE: {type(exc).__name__}: {exc}")
    errors = sorted(set(errors))
    return {
        "audit_version": "1.0.0", "passed": not errors,
        "scope": "Structure, declared standards mapping and structured answer keys for the VN Grade 1 fixture",
        "profile": profile.get("profile_id"), "errors": errors, "warnings": warnings,
        "counts": {"sessions": len(sessions), "outcomes": len(course.get("outcomes", [])),
                   "keys_recomputed": len(verified), "observational_tasks": len(manual)},
        "strands": dict(Counter(s.get("strand") for s in sessions if isinstance(s, dict))),
        "mechanically_verified_task_ids": verified, "manual_content_review_task_ids": manual,
        "teacher_review": "not_run", "learner_pilot": "not_run", "learning_effectiveness": "not_assessed",
        "limits": [
            "A standard tag does not prove that a task adequately elicits that standard.",
            "Prose examples, mathematical meaning, visual clarity and student responses need separate review.",
            "Recomputed count/number keys check declared quantities, not photographed physical objects.",
            "Observation rubrics and reading support are checked for explicit fields, not real-world usability.",
            "The 24 requirement IDs are an authored decomposition of the checked curriculum, not official IDs.",
            "This is a bounded audit profile, not a validator for every subject, age or jurisdiction.",
        ],
    }
