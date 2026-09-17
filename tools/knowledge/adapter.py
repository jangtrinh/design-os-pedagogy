"""Normalize legacy metadata for inspection, without granting it new trust."""
from __future__ import annotations
from pathlib import Path

VERSION = "2.0.0"
STAGES = {
    "S0-prenatal": "S0", "S1-early-childhood": "S1", "S2-primary": "S2",
    "S3-secondary": "S3", "S4-tertiary": "S4", "S5-postgraduate": "S5",
    "S6-adult": "S6", "S7-master-pedagogy": "S7",
}
TYPES = {
    "foundation": "concept", "method": "practice", "intervention": "practice",
    "pattern": "practice", "discipline-guide": "discipline",
    "professor-guide": "faculty", "prompt-spec": "protocol",
    "runtime-spec": "protocol", "eval-spec": "eval",
}
RELATIONS = ("prerequisites", "leads_to", "supports", "clinical_cases",
             "evidence_claims", "source_ids", "claim_ids", "estimate_ids")


def normalize(meta: dict, relative: Path) -> tuple[dict, list[str]]:
    record = dict(meta)
    warnings = []
    record["raw_metadata"] = dict(meta)
    record["path"] = relative.as_posix()
    record["origin_schema"] = meta.get("schema_version", "legacy")
    record["schema_version"] = VERSION
    if meta.get("schema_version") == VERSION:
        return record, warnings
    warnings.append(f"{relative}: LEGACY_UNREVIEWED (metadata adapted; claims not verified)")
    raw_type = meta.get("type")
    if relative.parts[0] == "60-evidence" and "sources" in relative.parts:
        record["type"] = "source"
    elif raw_type == "evidence":
        record["type"] = "synthesis"
    else:
        record["type"] = TYPES.get(raw_type, raw_type or "unclassified")
    raw_stages = meta.get("stage", meta.get("stage_applicability", []))
    record["stage"] = [STAGES.get(s, s) for s in raw_stages] if isinstance(raw_stages, list) else raw_stages
    raw_axes = meta.get("axes", [])
    record["axes"] = [a.split(":", 1)[0].strip() if isinstance(a, str) else a
                      for a in raw_axes] if isinstance(raw_axes, list) else raw_axes
    record["capabilities"] = [meta["capability_id"]] if meta.get("capability_id") else []
    record["context"] = meta.get("context", [])
    record["locale"] = meta.get("locale", "und")
    record["legacy_evidence_grade"] = meta.get("evidence_level", meta.get("evidence_basis"))
    record["evidence_grade"] = "U"
    record["claim_status"] = "unreviewed"
    record["review_status"] = "unreviewed"
    declared = meta.get("provenance", {})
    record["provenance"] = dict(declared) if isinstance(declared, dict) else {}
    record["provenance"].setdefault("kind", "unreviewed")
    return record, warnings


def references(meta: dict):
    """Return declared graph edges; prose bibliographies remain legacy text."""
    for field in RELATIONS:
        values = meta.get(field, [])
        if not isinstance(values, list):
            yield field, values, "expected a list of IDs"
            continue
        for value in values:
            if value == "none":
                continue
            yield field, value, None if isinstance(value, str) and value else "expected a nonempty ID"
    for field in ("source_id", "claim_id"):
        if field in meta:
            value = meta[field]
            yield field, value, None if isinstance(value, str) and value else "expected a nonempty ID"
