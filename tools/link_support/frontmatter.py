"""Publication framing over the same metadata parser as the registry."""
from ..knowledge.frontmatter import load_mapping


def split_frontmatter(text: str, *, required: bool = False):
    """Return metadata, unchanged body and removed line count."""
    if not isinstance(text, str) or len(text.encode("utf-8")) > 4 * 1024 * 1024:
        raise ValueError("Document must be UTF-8 text below 4 MiB")
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "---":
        if required:
            raise ValueError("Document must start directly with YAML frontmatter")
        return {}, text, 0
    end = next((i for i in range(1, len(lines)) if lines[i].rstrip("\r\n") == "---"), None)
    if end is None:
        raise ValueError("YAML frontmatter has no closing --- delimiter")
    return load_mapping("".join(lines[1:end])), "".join(lines[end + 1:]), end + 1
