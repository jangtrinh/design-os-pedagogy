"""Read-only loading of a vocational course bundle and its schedule files."""
import hashlib
from datetime import date
from pathlib import Path

from ...knowledge.frontmatter import load_mapping
from ...pipeline_support.transactions import inside, read_text

GRANULARITY = 15  # minutes; schedule hours must be multiples of a quarter hour


def load_file(folder, name, hashes):
    if not isinstance(name, str):
        raise ValueError("Course file path must be a string")
    text = read_text(inside(Path(folder), name))
    hashes[name] = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return load_mapping(text)


def load_bundle(folder, schedule_name, sessions_name=None):
    """Return course, schedule, sessions document (or None) and input hashes."""
    folder = Path(folder)
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError("Course folder must exist and must not be a symlink")
    hashes = {}
    course = load_file(folder, "course.yaml", hashes)
    schedule = load_file(folder, schedule_name, hashes)
    sessions = load_file(folder, sessions_name, hashes) if sessions_name else None
    return course, schedule, sessions, hashes


def to_minutes(hours):
    """Convert schedule hours (giờ) to whole minutes on a quarter-hour grid."""
    if isinstance(hours, bool) or not isinstance(hours, (int, float)) or hours < 0:
        raise ValueError(f"Hours must be a non-negative number: {hours!r}")
    minutes = round(hours * 60)
    if abs(minutes - hours * 60) > 1e-6 or minutes % GRANULARITY:
        raise ValueError(f"Hours must be multiples of 0.25: {hours!r}")
    return minutes


def iso_date(value):
    if not isinstance(value, str):
        raise ValueError(f"ISO date string required: {value!r}")
    return date.fromisoformat(value)


def index(records, label):
    if not isinstance(records, list) or any(not isinstance(r, dict) for r in records):
        raise ValueError(f"{label} must be a list of objects")
    result = {}
    for record in records:
        rid = record.get("id")
        if not isinstance(rid, str) or not rid:
            raise ValueError(f"{label} contains a missing or invalid id")
        if rid in result:
            raise ValueError(f"{label} contains duplicate id {rid}")
        result[rid] = record
    return result
