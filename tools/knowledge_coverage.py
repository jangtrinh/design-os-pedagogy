#!/usr/bin/env python3
"""Inspect knowledge coverage without writing files, fetching sources or granting review."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.knowledge.coverage import DIMENSIONS, coverage_report, markdown_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--stage", choices=DIMENSIONS["stage"])
    parser.add_argument("--axis", choices=DIMENSIONS["axes"])
    parser.add_argument("--capability", choices=DIMENSIONS["capabilities"])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    report = coverage_report(args.root, stage=args.stage, axis=args.axis, capability=args.capability)
    print(json.dumps(report, ensure_ascii=False, indent=2) if args.json else markdown_report(report),
          end="\n" if args.json else "")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
