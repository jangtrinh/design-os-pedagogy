#!/usr/bin/env python3
"""Build the interactive course website (student or teacher edition) after a passing audit."""
import argparse
import json
import shutil
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.course_support.vocational.audit import audit
from tools.course_support.vocational.content import check_content, load_content
from tools.course_support.vocational.model import load_bundle
from tools.course_support.vocational.site import Site

REPO = Path(__file__).resolve().parents[1]
STUDENT_OUT = REPO / "docs/course/plc-logo-zen"
ASSETS = ("course.css", "course.js")


def build(course_folder, schedule, sessions, audience):
    course, sched, plan, hashes = load_bundle(course_folder, schedule, sessions)
    content = load_content(course_folder, hashes)
    report = audit(course, sched, plan)
    errors = sorted(set(report["errors"]) | set(check_content(course, plan, content)))
    base_css = "../../assets/site.css" if audience == "student" else "assets/site.css"
    pages = Site(course, sched, plan, content, audience, base_css).build() if not errors else {}
    return pages, errors


def write(pages, out, audience):
    out = Path(out)
    if out.is_symlink() or (out.exists() and not out.is_dir()):
        raise ValueError("Output must be a real directory")
    for sub in ("bai", "tuan"):
        directory = out / sub
        if directory.is_dir():
            for stale in directory.glob("*.html"):
                if f"{sub}/{stale.name}" not in pages:
                    stale.unlink()
    for name, html in pages.items():
        target = out / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.is_symlink():
            raise ValueError(f"Refusing to write through a symlink: {name}")
        target.write_text(html, encoding="utf-8")
    if audience == "teacher":
        (out / "assets").mkdir(exist_ok=True)
        for asset in ASSETS:
            shutil.copyfile(STUDENT_OUT / "assets" / asset, out / "assets" / asset)
        shutil.copyfile(REPO / "docs/assets/site.css", out / "assets/site.css")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("course_folder", type=Path)
    parser.add_argument("--schedule", required=True)
    parser.add_argument("--sessions", required=True)
    parser.add_argument("--audience", choices=("student", "teacher"), default="student")
    parser.add_argument("--out", type=Path, help="output directory (student default: docs/course/plc-logo-zen)")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    out = args.out or (STUDENT_OUT if args.audience == "student" else REPO / ".data/teacher-site")
    try:
        pages, errors = build(args.course_folder, args.schedule, args.sessions, args.audience)
        result = {"passed": not errors, "errors": errors, "pages": len(pages), "audience": args.audience}
        if args.write and not errors:
            write(pages, out, args.audience)
            result["written"] = str(out)
    except (OSError, ValueError, UnicodeError, KeyError) as exc:
        result = {"passed": False, "errors": [f"INPUT: {type(exc).__name__}: {exc}"]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
