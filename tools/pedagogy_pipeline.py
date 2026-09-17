#!/usr/bin/env python3
"""Prepare draft manifests; apply explicitly without Git operations."""
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def main(argv=None):
    try:
        from tools.pipeline_support.cli import main as run
    except ImportError as error:
        print(f"Publication dependency unavailable: {error}. Install requirements.txt.", file=sys.stderr)
        return 2
    return run(argv)


if __name__ == "__main__":
    raise SystemExit(main())
