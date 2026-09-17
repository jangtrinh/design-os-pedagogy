"""Check local Markdown links and headings without fetching external URLs."""
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

from .frontmatter import split_frontmatter
from .markdown import parse_markdown, heading_slug

EXCLUDED = {".git", ".venv", ".data", ".pedagogy-drafts", "node_modules", "__pycache__"}


def audit(root, overrides=None):
    root = Path(root).resolve()
    result = {"files": 0, "errors": [], "structural_errors": [], "portability_warnings": [],
              "scope": "Local Markdown files and anchors; external HTTP links are not fetched."}
    if not root.is_dir():
        result["errors"].append("Root does not exist")
        return result
    overrides = {Path(k).resolve(): v for k, v in (overrides or {}).items()}
    paths = {p for p in root.rglob("*.md") if not any(x in EXCLUDED for x in p.relative_to(root).parts)} | set(overrides)
    documents, names = {}, {}
    for path in sorted(paths):
        try:
            relative = path.resolve().relative_to(root)
            if any(p.is_symlink() for p in (path, *path.parents) if p != root):
                raise ValueError("Markdown symlinks are not accepted")
            text = overrides[path] if path in overrides else path.read_text(encoding="utf-8")
            metadata, body, offset = split_frontmatter(text)
            parsed = parse_markdown(body, offset)
            documents[path.resolve()] = parsed
            aliases = metadata.get("aliases", [])
            if not isinstance(aliases, list) or any(not isinstance(a, str) or not a for a in aliases):
                raise ValueError("Aliases must be an array of nonempty strings")
            for name in [path.stem, metadata.get("id"), metadata.get("title"), *aliases]:
                if isinstance(name, str) and name:
                    names.setdefault(name.casefold(), set()).add(path.resolve())
            for line_number, line in enumerate(body.splitlines(), offset + 1):
                if re.search(r"(?:file://)?/(?:Users|home)/[^/\s]+/", line):
                    result["portability_warnings"].append(f"{relative}:{line_number}: machine-specific path")
        except (ValueError, OSError, TypeError) as error:
            diagnostic = f"{path}: {error}"
            result["errors"].append(diagnostic)
            result["structural_errors"].append(diagnostic)
    result["files"] = len(documents)
    if not documents:
        result["errors"].append("No Markdown documents found")
    for path, parsed in documents.items():
        for link in parsed.links:
            try:
                raw, wiki = link.target, link.kind.startswith("wiki")
                if wiki:
                    name, _, anchor = raw.partition("#")
                    if not name:
                        target = path
                    elif "/" not in name and name.casefold() in names:
                        matches = names[name.casefold()]
                        if len(matches) != 1:
                            raise ValueError(f"ambiguous wikilink: {raw}")
                        target = next(iter(matches))
                    else:
                        candidates = [path.parent / name, root / name]
                        candidates += [p.with_suffix(".md") for p in candidates if not p.suffix]
                        matches = {p.resolve() for p in candidates if p.resolve() in documents or p.is_file()}
                        if len(matches) != 1:
                            raise ValueError(f"unresolved or ambiguous wikilink: {raw}")
                        target = next(iter(matches))
                else:
                    url = urlsplit(raw)
                    if url.scheme in {"http", "https", "mailto", "tel", "data"}:
                        continue
                    if url.scheme or url.netloc:
                        raise ValueError(f"unsupported URL scheme: {raw}")
                    name, anchor = unquote(url.path), unquote(url.fragment)
                    target = root / name.lstrip("/") if name.startswith("/") else path.parent / name if name else path
                    target = target.resolve()
                target.relative_to(root)
                if target not in documents and not target.exists():
                    raise ValueError(f"missing local target: {raw}")
                if anchor and target in documents:
                    anchors = documents[target].anchors
                    if anchor not in anchors and not (wiki and heading_slug(anchor) in anchors):
                        raise ValueError(f"missing heading: {raw}")
            except (ValueError, OSError) as error:
                result["errors"].append(f"{path.relative_to(root)}:{link.line}: {error}")
    result["errors"] = sorted(set(result["errors"]))
    result["portability_warnings"] = sorted(set(result["portability_warnings"]))
    return result


def candidate_errors(root, path, text):
    root, path = Path(root).resolve(), Path(path).resolve()
    report = audit(root, {path: text})
    prefixes = (str(path) + ":", str(path.relative_to(root)) + ":")
    diagnostics = report["errors"] + report["portability_warnings"]
    return sorted(set(report["structural_errors"] + [error for error in diagnostics
                      if error.startswith(prefixes) or error in {"Root does not exist", "No Markdown documents found"}]))
