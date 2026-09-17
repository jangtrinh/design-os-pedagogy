#!/usr/bin/env python3
"""Audit local Markdown links and headings; external URLs are not fetched."""
import argparse
import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def audit_repository(repo_root=None):
    from tools.link_support.audit import audit
    report = audit(repo_root or Path(__file__).resolve().parents[1])
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return not report["errors"]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path)
    args = parser.parse_args(argv)
    try:
        return 0 if audit_repository(args.root) else 1
    except ImportError as error:
        print(f"Link audit dependency unavailable: {error}. Install requirements.txt.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
