#!/usr/bin/env python3
"""Public corpus API and CLI; unresolved references remain visible errors."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from knowledge.frontmatter import parse_frontmatter
    from knowledge.registry import build_registry, validate_document
else:
    from .knowledge.frontmatter import parse_frontmatter
    from .knowledge.registry import build_registry, validate_document

__all__ = ["parse_frontmatter", "validate_document", "build_registry"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true", help="Print full registry and diagnostics")
    args = parser.parse_args()
    result = build_registry(args.root)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result["stats"], sort_keys=True))
        for label in ("errors", "warnings"):
            for item in result[label]:
                print(f"{label[:-1].upper()}: {item}")
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
