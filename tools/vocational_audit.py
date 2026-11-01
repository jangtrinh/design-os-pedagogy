#!/usr/bin/env python3
"""Read-only audit of a schedule-driven vocational course and its planned sessions."""
import argparse
import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.course_support.vocational.audit import audit
from tools.course_support.vocational.content import check_content, load_content
from tools.course_support.vocational.model import load_bundle


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("course_folder", type=Path)
    parser.add_argument("--schedule", required=True)
    parser.add_argument("--sessions")
    parser.add_argument("--content", action="store_true", help="also check content/ (lesson pages, lesson plans)")
    args = parser.parse_args(argv)
    try:
        course, schedule, sessions, hashes = load_bundle(args.course_folder, args.schedule, args.sessions)
        result = audit(course, schedule, sessions)
        if args.content:
            content = load_content(args.course_folder, hashes)
            content_errors = check_content(course, sessions, content)
            result["errors"] = sorted(set(result["errors"]) | set(content_errors))
            result["passed"] = not result["errors"]
            result["counts"].update({"lesson_pages": len(content["lessons"]), "lesson_plans": len(content["sessions"]),
                                     "glossary_terms": len((content["glossary"] or {}).get("terms", []))})
        result["input_hashes"] = hashes
    except (OSError, ValueError, UnicodeError) as exc:
        result = {"passed": False, "errors": [f"INPUT: {exc}"], "learning_effectiveness": "not_assessed"}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
