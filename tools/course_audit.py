#!/usr/bin/env python3
"""Read-only audit of a versioned course fixture and its declared answer keys."""
import argparse
import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.course_support.audit import audit_bundle, load_bundle
from tools.knowledge_registry import build_registry


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("course_folder", type=Path)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    try:
        course, sessions, profile, exams, hashes = load_bundle(args.course_folder)
        registry = build_registry(args.root)
        known = {r["id"] for r in registry["records"] if r.get("type") == "source"}
        result = audit_bundle(course, sessions, profile, exams, known_sources=known)
        result["input_hashes"] = hashes
        if registry["errors"]:
            result["errors"].extend("REGISTRY: " + e for e in registry["errors"])
            result["passed"] = False
    except (OSError, ValueError, UnicodeError) as exc:
        result = {"passed": False, "errors": [f"INPUT: {exc}"], "learning_effectiveness": "not_assessed"}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
