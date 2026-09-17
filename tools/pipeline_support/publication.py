"""Revalidate draft scope and derived navigation before each explicit apply."""
import json
import re
import shutil
import uuid
from pathlib import Path

from ..link_support.audit import audit, candidate_errors
from ..link_support.frontmatter import split_frontmatter
from ..link_support.markdown import parse_markdown
from .routing import classify_topic, slugify
from .transactions import digest, inside, install, json_object, publication_lock, read_text
from .validation import validate
from .publication_journal import require_idle


def updated_moc(text, link_target, title, section):
    _, body, offset = split_frontmatter(text)
    parsed = parse_markdown(body, offset)
    existing = {link.target.split("#", 1)[0].strip() for link in parsed.links if link.kind == "wiki"}
    if link_target in existing:
        raise ValueError("MOC already references this module")
    title = re.sub(r"[\[\]|\r\n]", " ", title).strip()
    entry = f"* [[{link_target}|{title}]]: Authored draft; review pending.\n"
    fallback = "Draft modules awaiting review"
    desired = section.removeprefix("## ").strip()
    headings = [(title, line) for level, title, line in parsed.headings if level == 2]
    start = next((line for title, line in headings if title == desired), None)
    if start is None:
        start = next((line for title, line in headings if title == fallback), None)
    if start is None:
        return text.rstrip() + f"\n\n## {fallback}\n\n" + entry
    lines = text.splitlines(keepends=True)
    end = next((line - 1 for _, line in headings if line > start), len(lines))
    lines.insert(end, entry + "\n")
    return "".join(lines)


def _scope(route, slug):
    if not isinstance(route, dict) or not isinstance(slug, str) or slugify(slug) != slug:
        raise ValueError("Invalid route or filename slug")
    expected = classify_topic("", route.get("archetype"), stage=route.get("stage"), domain=route.get("domain"))
    if expected != route:
        raise ValueError("Route differs from the current routing contract")
    return f"{route['dir']}/{slug}.md", route["moc"]


def _validate(root, relative, moc_relative, route, identifier, text, before):
    metadata = validate(root, relative, text, identifier)
    if metadata["type"] != route["type"] or route["stage"] not in metadata["stage"]:
        raise ValueError("Module type and stage must match the requested route")
    target, moc = inside(root, relative), inside(root, moc_relative)
    errors = candidate_errors(root, target, text)
    if errors:
        raise ValueError("Link validation failed: " + "; ".join(errors[:20]))
    after = updated_moc(before, relative.removesuffix(".md"), metadata["title"], route["section"])
    baseline = set(audit(root)["errors"])
    proposed = audit(root, {target: text, moc: after})
    introduced = sorted(set(proposed["errors"]) - baseline)
    if introduced:
        raise ValueError("Navigation introduces errors: " + "; ".join(introduced[:20]))
    return after


def prepare(root, route, identifier, slug, text):
    root = Path(root).resolve()
    relative, moc_relative = _scope(route, slug)
    target, moc = inside(root, relative), inside(root, moc_relative)
    with publication_lock(root):
        require_idle(root)
        if target.exists():
            raise ValueError("Target exists; existing content will not be overwritten")
        before = read_text(moc)
        after = _validate(root, relative, moc_relative, route, identifier, text, before)
        folder = inside(root, f".pedagogy-drafts/{uuid.uuid4()}")
        folder.mkdir(mode=0o700)
        manifest = {"version": 2, "id": identifier, "slug": slug, "route": route,
                    "target": relative, "moc": moc_relative, "scope": [relative, moc_relative],
                    "module_hash": digest(text), "moc_before_hash": digest(before),
                    "moc_after_hash": digest(after), "status": "draft"}
        try:
            (folder / "module.md").write_text(text, encoding="utf-8")
            (folder / "moc.md").write_text(after, encoding="utf-8")
            (folder / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        except BaseException:
            shutil.rmtree(folder)
            raise
    return folder


def apply(root, folder):
    root, folder = Path(root).resolve(), Path(folder).absolute()
    relative_folder = folder.relative_to(root)
    if len(relative_folder.parts) != 2 or relative_folder.parts[0] != ".pedagogy-drafts":
        raise ValueError("Apply expects one draft folder directly inside .pedagogy-drafts")
    folder = inside(root, relative_folder)
    with publication_lock(root):
        require_idle(root)
        manifest = json_object(read_text(inside(root, relative_folder / "manifest.json"), 65536))
        if type(manifest.get("version")) is not int or manifest["version"] != 2 or manifest.get("status") != "draft":
            raise ValueError("Unsupported manifest; prepare a new draft with this pipeline")
        relative, moc_relative = _scope(manifest["route"], manifest["slug"])
        if [manifest.get("target"), manifest.get("moc")] != [relative, moc_relative] or manifest.get("scope") != [relative, moc_relative]:
            raise ValueError("Invalid draft scope")
        target, moc = inside(root, relative), inside(root, moc_relative)
        if target.exists():
            raise ValueError("Target already exists; apply does not overwrite or repeat publication")
        text = read_text(inside(root, relative_folder / "module.md"))
        after = read_text(inside(root, relative_folder / "moc.md"))
        before = read_text(moc)
        if digest(text) != manifest["module_hash"] or digest(after) != manifest["moc_after_hash"]:
            raise ValueError("Draft changed; prepare a new draft")
        if digest(before) != manifest["moc_before_hash"]:
            raise ValueError("MOC changed; prepare a new draft")
        derived = _validate(root, relative, moc_relative, manifest["route"], manifest["id"], text, before)
        if derived != after:
            raise ValueError("Draft navigation differs from the permitted insertion")
        install(target, moc, text, before, after, root=root, folder=folder)
    return {"status": "applied", "paths": [relative, moc_relative],
            "git_operations": False, "review_status": "unreviewed"}
