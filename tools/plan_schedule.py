#!/usr/bin/env python3
"""Bind a vocational course to a teaching schedule; print the plan, optionally write it."""
import argparse
import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.course_support.vocational.audit import audit, schedule_digest
from tools.course_support.vocational.model import load_bundle
from tools.course_support.vocational.planner import diff, plan
from tools.pipeline_support.transactions import inside


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("course_folder", type=Path)
    parser.add_argument("--schedule", required=True, help="schedule file, relative to the course folder")
    parser.add_argument("--sessions", help="sessions file to compare against and, with --write, replace")
    parser.add_argument("--write", action="store_true", help="write the plan to --sessions if it passes audit")
    args = parser.parse_args(argv)
    if args.write and not args.sessions:
        parser.error("--write requires --sessions")
    try:
        target = inside(args.course_folder, args.sessions) if args.sessions else None
        existing = args.sessions if target is not None and target.exists() else None
        course, schedule, old, _ = load_bundle(args.course_folder, args.schedule, existing)
        result = plan(course, schedule)
        document = {"sessions_version": "tvet-sessions-1.0", "course_id": course["course"]["id"],
                    "schedule_file": args.schedule, "schedule_sha256": schedule_digest(schedule),
                    "unscheduled": result["unscheduled"], "sessions": result["sessions"]}
        report = audit(course, schedule, document)
        output = {"warnings": result["warnings"], "audit": {k: report[k] for k in ("passed", "errors", "warnings")},
                  "changes": diff(old.get("sessions", []), result["sessions"]) if old else None,
                  "sessions": [{"id": s["id"], "start": s["start"], "ga_number": s["ga_number"],
                                "blocks": [f"{b.get('lesson_id') or b.get('assessment_id')}:{b['kind']}:{b['hours']}h"
                                           for b in s["blocks"]]} for s in result["sessions"]],
                  "unscheduled": result["unscheduled"]}
        if args.write:
            if not report["passed"]:
                output["written"] = False
            else:
                if target.is_symlink():
                    raise ValueError("Refusing to write through a symlink")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                output["written"] = str(args.sessions)
    except (OSError, ValueError, UnicodeError, KeyError) as exc:
        output = {"audit": {"passed": False, "errors": [f"INPUT: {exc}"]}}
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if output["audit"]["passed"] and output.get("written", True) is not False else 1


if __name__ == "__main__":
    raise SystemExit(main())
