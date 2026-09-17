#!/usr/bin/env python3
"""Run the local Vietnamese teacher rehearsal without an external model."""

import argparse
import sqlite3
from pathlib import Path

from rehearsal.catalog import Catalog
from rehearsal.http_server import create_server
from rehearsal.store import Store

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8876)
    parser.add_argument("--data-dir", type=Path, default=ROOT / ".data")
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error("--port must be between 0 and 65535; 0 selects a free port")
    data_dir = args.data_dir.resolve()
    if data_dir == ROOT or any(data_dir.is_relative_to(p) for p in ROOT.iterdir()
                               if p.is_dir() and p.name[:2].isdigit()):
        parser.error("Session data must be separate from the content directories")
    try:
        catalog = Catalog()
        store = Store(data_dir / "rehearsal.sqlite3", catalog)
        server = create_server(store, catalog, ROOT / "rehearsal" / "static", args.port)
    except (ValueError, OSError, sqlite3.Error) as exc:
        parser.exit(1, f"Cannot start rehearsal: {exc}\n")
    print(f"Agent Teacher: http://127.0.0.1:{server.server_address[1]}", flush=True)
    print("Authored rehearsal; expert review and real-user learning evaluation pending.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
