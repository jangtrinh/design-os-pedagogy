#!/usr/bin/env python3
"""Read-only audit of a schedule-driven vocational course and its planned sessions."""
import argparse
import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.course_support.vocational.audit import audit
from tools.course_support.vocational.model import load_bundle


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("course_folder", type=Path)
    parser.add_argument("--schedule", required=True)
    parser.add_argument("--sessions")
    args = parser.parse_args(argv)
    try:
        course, schedule, sessions, hashes = load_bundle(args.course_folder, args.schedule, args.sessions)
        result = audit(course, schedule, sessions)
        result["input_hashes"] = hashes
    except (OSError, ValueError, UnicodeError) as exc:
        result = {"passed": False, "errors": [f"INPUT: {exc}"], "learning_effectiveness": "not_assessed"}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
