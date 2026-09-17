"""Strict YAML frontmatter parsing without modifying source documents."""
from __future__ import annotations

from datetime import date, datetime
from typing import Any

import yaml
import math


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate mappings instead of accepting the last value."""

    def compose_node(self, parent, index):
        if self.check_event(yaml.AliasEvent):
            raise ValueError("YAML aliases are not supported in metadata")
        return super().compose_node(parent, index)


def _mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict:
    loader.flatten_mapping(node)
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise ValueError("YAML mapping keys must be strings")
        if key in result:
            raise ValueError(f"Duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def _plain(value: Any, active: set[int] | None = None) -> Any:
    active = set() if active is None else active
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, (dict, list)):
        if id(value) in active:
            raise ValueError("Recursive YAML aliases are not supported")
        active.add(id(value))
        try:
            if isinstance(value, dict):
                return {key: _plain(item, active) for key, item in value.items()}
            return [_plain(item, active) for item in value]
        finally:
            active.remove(id(value))
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("YAML numbers must be finite")
    if value is not None and not isinstance(value, (str, bool, int, float)):
        raise ValueError("YAML metadata must contain JSON-compatible values")
    return value


def load_mapping(text: str) -> dict:
    """Load a YAML object, with safe tags and unique string keys."""
    if not isinstance(text, str) or len(text.encode("utf-8")) > 4 * 1024 * 1024:
        raise ValueError("Metadata input must be UTF-8 text below 4 MiB")
    try:
        value = yaml.load(text, Loader=UniqueKeyLoader)
    except (yaml.YAMLError, RecursionError) as exc:
        raise ValueError(f"Invalid YAML: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("YAML document must contain an object")
    return _plain(value)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return metadata and unchanged body; malformed headers raise ValueError."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    lines = text.lstrip("\ufeff").splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return {}, text
    for end in range(1, len(lines)):
        if lines[end].strip() in ("---", "..."):
            metadata = load_mapping("".join(lines[1:end]))
            return metadata, "".join(lines[end + 1:])
    raise ValueError("Unterminated YAML frontmatter")
