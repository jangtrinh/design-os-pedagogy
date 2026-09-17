"""Build a deterministic registry; unresolved edges remain visible errors."""
from __future__ import annotations
from pathlib import Path
from .adapter import VERSION, normalize, references
from .frontmatter import load_mapping, parse_frontmatter
from .schema import check, read_schema, semantic_errors

ROOTS = ("00-navigation", "10-foundations", "20-stages", "30-pedagogy",
         "40-disciplines", "50-practice-library", "60-evidence",
         "70-capabilities", "80-professor-development", "90-agent-runtime")
TARGET_TYPES = {"source_ids": "source", "source_id": "source",
                "claim_ids": "claim", "claim_id": "claim", "estimate_ids": "estimate"}


def _relative(path: Path, root: Path) -> Path:
    return path.resolve().relative_to(root.resolve())


def _build(root: Path, overrides: dict[Path, str] | None = None,
           generated: bool = False) -> dict:
    root = root.resolve()
    overrides = overrides or {}
    result = {"schema_version": VERSION, "records": [], "aliases": {},
              "edges": [], "errors": [], "warnings": [], "stats": {}}
    errors, warnings = result["errors"], result["warnings"]
    if not root.is_dir():
        errors.append("REGISTRY: root does not exist")
        return result
    try:
        schema = read_schema(root)
    except (OSError, ValueError) as exc:
        errors.append(f"REGISTRY: cannot load schema: {exc}")
        return result
    paths = set(overrides)
    for folder in ROOTS:
        paths.update((root / folder).rglob("*.md"))
    for extension in ("*.yaml", "*.yml"):
        paths.update((root / "60-evidence").rglob(extension))
    by_id, duplicates = {}, set()
    for path in sorted(paths):
        try:
            relative = _relative(path, root)
            if not relative.parts or relative.parts[0] not in ROOTS:
                raise ValueError("document is outside the curated corpus")
            text = overrides[path] if path in overrides else path.read_text(encoding="utf-8")
            meta, body = (load_mapping(text), "") if path.suffix in (".yaml", ".yml") else parse_frontmatter(text)
            record, adapted_warnings = normalize(meta, relative)
            warnings.extend(adapted_warnings)
            identifier = meta.get("id")
            if not isinstance(identifier, str) or not identifier:
                errors.append(f"{relative}: ID_REQUIRED (no ID was invented)")
            elif identifier in by_id:
                duplicates.add(identifier)
                errors.append(f"{relative}: DUPLICATE_ID {identifier}")
                errors.append(f"{by_id[identifier]['path']}: DUPLICATE_ID {identifier}")
            else:
                by_id[identifier] = record
            if meta.get("schema_version") == VERSION:
                errors.extend(f"{relative}: {e}" for e in check(meta, schema))
                errors.extend(f"{relative}: {e}" for e in semantic_errors(meta, body, generated and path in overrides))
            else:
                if path in overrides and generated:
                    errors.append(f"{relative}: SCHEMA_VERSION_REQUIRED {VERSION}")
                for key in ("id", "title", "stage", "axes", "capabilities", "context"):
                    if key in record:
                        errors.extend(f"{relative}: {e}" for e in check(
                            record[key], schema.get("properties", {}).get(key, {}), key))
                if meta.get("schema_version") not in (None, "1.0.0"):
                    errors.append(f"{relative}: UNSUPPORTED_SCHEMA_VERSION {meta['schema_version']}")
            result["records"].append(record)
        except (OSError, ValueError, TypeError) as exc:
            errors.append(f"{path}: PARSE_OR_PATH_ERROR {exc}")
    aliases, alias_collisions = {}, set()
    alias_path = root / "00-system" / "identifier-aliases.yaml"
    if alias_path.exists():
        try:
            _relative(alias_path, root)
            alias_doc = load_mapping(alias_path.read_text(encoding="utf-8"))
            configured = alias_doc.get("aliases", {})
            if not isinstance(configured, dict):
                raise ValueError("aliases must be an object")
            aliases.update(configured)
        except (OSError, ValueError) as exc:
            errors.append(f"REGISTRY: ALIAS_FILE_ERROR {exc}")
    for record in result["records"]:
        declared = record.get("aliases", [])
        if not isinstance(declared, list) or any(not isinstance(a, str) or not a for a in declared):
            errors.append(f"{record['path']}: ALIASES must be a list of nonempty strings")
            continue
        for alias in declared:
            if alias in aliases and aliases[alias] != record.get("id"):
                alias_collisions.add(alias)
                errors.append(f"REGISTRY: ALIAS_COLLISION {alias}")
            else:
                aliases[alias] = record.get("id")
    for alias, target in sorted(aliases.items()):
        if alias in alias_collisions:
            continue
        if not isinstance(target, str) or target not in by_id or target in duplicates:
            errors.append(f"REGISTRY: ALIAS_TARGET_UNKNOWN {alias} -> {target}")
        elif alias in by_id and alias != target:
            errors.append(f"REGISTRY: ALIAS_COLLISION {alias}")
        else:
            result["aliases"][alias] = target
    for record in result["records"]:
        for field, target, malformed in references(record):
            canonical = None
            if malformed:
                errors.append(f"{record['path']}: {field}: {malformed}")
            elif target in duplicates:
                errors.append(f"{record['path']}: AMBIGUOUS_REFERENCE {field}: {target}")
            else:
                canonical = target if target in by_id else result["aliases"].get(target)
                if canonical is None:
                    errors.append(f"{record['path']}: UNRESOLVED_REFERENCE {field}: {target}")
                elif field in TARGET_TYPES and by_id[canonical].get("type") != TARGET_TYPES[field]:
                    errors.append(f"{record['path']}: WRONG_REFERENCE_TYPE {field}: {target}")
            result["edges"].append({"source": record.get("id"), "field": field,
                                    "target": target, "resolved_to": canonical})
    result["errors"] = sorted(set(errors))
    result["warnings"] = sorted(set(warnings))
    result["stats"] = {"records": len(result["records"]), "edges": len(result["edges"]),
                       "unresolved_edges": sum(e["resolved_to"] is None for e in result["edges"]),
                       "unreviewed_records": sum(r.get("review_status") == "unreviewed" for r in result["records"]),
                       "errors": len(result["errors"]), "warnings": len(result["warnings"])}
    return result


def build_registry(root: str | Path) -> dict:
    """Return records, explicit aliases, edges, errors and warnings; no writes."""
    return _build(Path(root))


def validate_document(path: str | Path, text: str, root: str | Path,
                      generated: bool = False) -> list[str]:
    """Validate a candidate and edges; unrelated legacy errors remain in full registry."""
    root = Path(root).resolve()
    path = Path(path)
    path = (path if path.is_absolute() else root / path).resolve()
    try:
        relative = _relative(path, root)
    except ValueError:
        return ["PATH_OUTSIDE_ROOT: candidate is not inside the corpus"]
    result = _build(root, {path: text}, generated)
    prefix = relative.as_posix() + ":"
    return [e for e in result["errors"]
            if e.startswith(prefix) or e.startswith("REGISTRY:") or e.startswith(str(path) + ":")]
