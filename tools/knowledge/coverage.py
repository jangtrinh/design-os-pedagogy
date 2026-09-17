"""Read-only coverage inventory. Metadata coverage never establishes effectiveness."""
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path

from .registry import build_registry

DIMENSIONS = {
    "stage": tuple(f"S{i}" for i in range(8)),
    "axes": tuple(f"AX-{i:02}" for i in range(1, 9)),
    "capabilities": tuple(f"CAP-{i:02}" for i in range(1, 7)),
}
EVIDENCE_FIELDS = {"source_ids", "source_id", "claim_ids", "claim_id",
                   "estimate_ids", "evidence_claims"}
EVIDENCE_TYPES = {"source", "claim", "estimate"}


def _tags(record: dict, field: str) -> list[str]:
    value = record.get(field, [])
    return [v for v in value if isinstance(v, str)] if isinstance(value, list) else []


def _source_trails(registry: dict) -> dict[str, list[str]]:
    records = {r.get("id"): r for r in registry["records"] if isinstance(r.get("id"), str)}
    adjacency = defaultdict(set)
    for edge in registry["edges"]:
        target = edge.get("resolved_to")
        if (edge["field"] in EVIDENCE_FIELDS and target in records
                and records[target].get("type") in EVIDENCE_TYPES):
            adjacency[edge["source"]].add(target)
    trails = {}
    for identifier in records:
        pending, visited, sources = [identifier], set(), set()
        while pending:
            node = pending.pop()
            if node in visited:
                continue
            visited.add(node)
            if records[node].get("type") == "source":
                sources.add(node)
            pending.extend(adjacency[node] - visited)
        trails[identifier] = sorted(sources)
    return trails


def _counts(records: list[dict]) -> dict:
    reviews = Counter(r.get("review_status", "unreviewed") for r in records)
    return {
        "records": len(records),
        "source_records": sum(r.get("type") == "source" for r in records),
        "source_checked": reviews["source-checked"],
        "reviewed": reviews["reviewed"],
        "unreviewed": reviews["unreviewed"],
        "legacy": sum(r.get("origin_schema") != "2.0.0" for r in records),
        "non_source_with_source_trail": sum(
            r.get("type") != "source" and bool(r["traceable_source_ids"]) for r in records),
    }


def coverage_report(root: str | Path, *, stage: str | None = None,
                    axis: str | None = None, capability: str | None = None) -> dict:
    """Intersect metadata filters; retain registry errors and zero-count dimensions."""
    filters = {"stage": stage, "axes": axis, "capabilities": capability}
    for field, value in filters.items():
        if value is not None and value not in DIMENSIONS[field]:
            raise ValueError(f"Unknown {field} filter: {value}")
    registry = build_registry(root)
    trails = _source_trails(registry)
    selected = []
    for original in registry["records"]:
        if any(value is not None and value not in _tags(original, field)
               for field, value in filters.items()):
            continue
        record = {key: original.get(key) for key in
                  ("id", "path", "type", "title", "origin_schema", "review_status",
                   "evidence_grade", "claim_status")}
        record.update({field: _tags(original, field) for field in DIMENSIONS})
        record["traceable_source_ids"] = trails.get(record["id"], [])
        selected.append(record)
    selected.sort(key=lambda r: r["path"])
    groups = {
        field: [{"id": identifier, **_counts([r for r in selected if identifier in r[field]])}
                for identifier in identifiers]
        for field, identifiers in DIMENSIONS.items()
    }
    disciplines = Counter()
    for record in selected:
        parts = Path(record["path"]).parts
        if len(parts) > 2 and parts[0] == "40-disciplines":
            disciplines[parts[1]] += 1
    return {
        "report_version": "1.0.0",
        "filters": filters,
        "registry_stats": registry["stats"],
        "selected": _counts(selected),
        "types": dict(sorted(Counter(r["type"] for r in selected).items())),
        "tagged_coverage": groups,
        "discipline_folders": dict(sorted(disciplines.items())),
        "untagged": {field: [r["id"] for r in selected if not r[field]] for field in DIMENSIONS},
        "without_source_trail": [r["id"] for r in selected
                                 if r["type"] != "source" and not r["traceable_source_ids"]],
        "unclassified": [r["id"] for r in selected if r["type"] == "unclassified"],
        "learning_effectiveness": "not_assessed",
        "interpretation": [
            "Counts describe declared tags and source trails, not complete curricula or learning gains.",
            "Tags overlap. Missing tags may reflect missing metadata rather than absent prose.",
            "Source trails follow evidence references, never navigation or prerequisite proximity.",
            "A source trail does not establish support, applicability or independent appraisal.",
            "Legacy prose citations are not silently converted into verified source records.",
            "Any registry error prevents structural acceptance; review the full diagnostics.",
        ],
        "records": selected,
        "errors": registry["errors"],
        "warnings": registry["warnings"],
    }


def markdown_report(report: dict) -> str:
    counts = report["selected"]
    lines = ["# Knowledge coverage inventory", "",
             f"Matching records: {counts['records']}. Source records: {counts['source_records']}.",
             f"Unreviewed: {counts['unreviewed']}; source-checked: {counts['source_checked']}; "
             f"reviewed: {counts['reviewed']}; legacy: {counts['legacy']}.", "",
             "Filters: " + ", ".join(f"{k}={v or 'all'}" for k, v in report["filters"].items()), "",
             "| Dimension | ID | Records | Source-checked | Reviewed | Legacy |",
             "| --- | --- | ---: | ---: | ---: | ---: |"]
    for field, groups in report["tagged_coverage"].items():
        for group in groups:
            lines.append(f"| {field} | {group['id']} | {group['records']} | "
                         f"{group['source_checked']} | {group['reviewed']} | {group['legacy']} |")
    lines += ["", f"Records without a typed source trail: {len(report['without_source_trail'])}.",
              f"Unclassified records: {len(report['unclassified'])}.", "",
              "Learning effectiveness: not assessed.", ""]
    lines.extend(report["interpretation"])
    lines += ["", f"Registry errors: {len(report['errors'])}; warnings: {len(report['warnings'])}."]
    lines.extend(f"ERROR: {error}" for error in report["errors"])
    lines += ["", "Use --json for record paths, source trails, missing tags and all diagnostics."]
    return "\n".join(lines) + "\n"
