"""Validate metadata and record provenance without mutating the corpus."""
from __future__ import annotations
import math
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit
from .frontmatter import load_mapping


def read_schema(root: Path) -> dict:
    path = root / "00-system" / "metadata-schema.yaml"
    path.resolve().relative_to(root.resolve())
    return load_mapping(path.read_text(encoding="utf-8"))


def check(value, schema: dict, location: str = "$") -> list[str]:
    supported = {"$schema", "$id", "title", "description", "type", "required", "properties",
                 "items", "enum", "pattern", "additionalProperties", "minLength",
                 "minItems", "uniqueItems", "format"}
    unknown = set(schema) - supported
    if unknown:
        return [f"{location}: unsupported schema keywords {sorted(unknown)}"]
    kinds = {"object": lambda v: isinstance(v, dict), "array": lambda v: isinstance(v, list),
             "string": lambda v: isinstance(v, str), "boolean": lambda v: type(v) is bool,
             "number": lambda v: type(v) in (int, float) and math.isfinite(v),
             "integer": lambda v: type(v) is int, "null": lambda v: v is None}
    kind = schema.get("type")
    if kind is not None and (kind not in kinds or not kinds[kind](value)):
        return [f"{location}: expected {kind}"]
    errors = []
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{location}: value outside enum")
    if isinstance(value, dict):
        for field in schema.get("required", []):
            if field not in value:
                errors.append(f"{location}.{field}: required")
        for field, item in value.items():
            properties = schema.get("properties", {})
            if field in properties:
                errors.extend(check(item, properties[field], f"{location}.{field}"))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{location}.{field}: unknown field")
            elif isinstance(schema.get("additionalProperties"), dict):
                errors.extend(check(item, schema["additionalProperties"], f"{location}.{field}"))
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{location}: too few items")
        if schema.get("uniqueItems") and len(set(map(repr, value))) != len(value):
            errors.append(f"{location}: duplicate items")
        for index, item in enumerate(value):
            errors.extend(check(item, schema.get("items", {}), f"{location}[{index}]"))
    if isinstance(value, str):
        if len(value.strip()) < schema.get("minLength", 0):
            errors.append(f"{location}: empty or too short")
        if "pattern" in schema and not re.fullmatch(schema["pattern"], value):
            errors.append(f"{location}: invalid pattern")
        if schema.get("format") == "uri":
            parsed = urlsplit(value)
            if parsed.scheme not in ("https", "http") or not parsed.netloc:
                errors.append(f"{location}: expected HTTP(S) source URL")
        if schema.get("format") == "date":
            try:
                date.fromisoformat(value)
            except ValueError:
                errors.append(f"{location}: expected ISO date")
    return errors


def semantic_errors(meta: dict, body: str, generated: bool = False) -> list[str]:
    errors = []
    kind = meta.get("type")
    provenance = meta.get("provenance", {})
    provenance = provenance if isinstance(provenance, dict) else {}
    if meta.get("review_status", "unreviewed") != "unreviewed":
        for field in ("reviewer", "reviewed_at"):
            if not provenance.get(field):
                errors.append(f"provenance.{field}: required for reviewed metadata")
        if not provenance.get("citations") and not meta.get("source_ids") and kind != "estimate":
            errors.append("PROVENANCE: reviewed record requires citations or source_ids")
    if provenance.get("kind") == "observed" and not provenance.get("record_locator"):
        errors.append("PROVENANCE: observed case requires record_locator")
    if provenance.get("kind") == "simulation" and meta.get("claim_status") == "supported":
        errors.append("PROVENANCE: simulated success cannot mark a learning claim supported")
    required = {"source": ("url", "locator"), "claim": ("claim_statement",),
                "estimate": ("source_id", "claim_id", "metric", "population", "comparator",
                             "outcome", "timepoint", "locator")}
    for field in required.get(kind, ()):
        if not isinstance(meta.get(field), str) or not meta[field].strip():
            errors.append(f"{kind}.{field}: required")
    if kind == "claim" and meta.get("claim_status") in ("supported", "mixed", "not-supported", "refuted"):
        if not meta.get("source_ids"):
            errors.append("claim.source_ids: required for appraised claim")
    if kind == "estimate":
        if type(meta.get("value")) not in (int, float) or not math.isfinite(meta["value"]):
            errors.append("estimate.value: finite number required")
    if generated and kind not in ("estimate", "source"):
        if re.search(r"(?i)(?:effect[ -]size|cohen.?s|hedges.?)[^\n]{0,40}?\b[dg]\s*=\s*[-+]?\d", body) and not meta.get("estimate_ids"):
            errors.append("ESTIMATE: quantitative effect needs an estimate_ids locator")
    return errors
