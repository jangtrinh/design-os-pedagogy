"""Durable publication intent and exact ownership of staged files."""
import json
import os
import stat
from pathlib import Path

from .transactions import _stage, digest, inside, json_object, read_text

JOURNAL = ".pedagogy-drafts/active-publication.json"
LIMIT = 16 * 1024 * 1024


def sync_directory(path):
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def pending(root):
    return inside(root, JOURNAL).exists()


def require_idle(root):
    if pending(root):
        raise ValueError("Unfinished publication; use --inspect-publication, then --recover-publication")


def identity(path):
    info = path.stat(follow_symlinks=False)
    return [info.st_dev, info.st_ino, stat.S_IMODE(info.st_mode)]


def owned(path, expected, text, links=1):
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, "rb") as stream:
        info = os.fstat(stream.fileno())
        actual = [info.st_dev, info.st_ino, stat.S_IMODE(info.st_mode)]
        if not stat.S_ISREG(info.st_mode) or actual != expected or info.st_nlink != links:
            raise ValueError(f"Publication file ownership changed: {path.name}")
        content = text.encode("utf-8")
        if len(content) > 2097152 or stream.read(len(content) + 1) != content:
            raise ValueError(f"Publication file content changed: {path.name}")


def encoded(record):
    return json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def begin(root, folder, target, moc, text, before, after, target_stage, moc_stage):
    require_idle(root)
    relative = lambda path: str(path.relative_to(root))
    record = {"version": 1, "draft": relative(folder), "target": relative(target), "moc": relative(moc),
              "module": text, "before": before, "after": after,
              "target_stage": relative(target_stage), "moc_stage": relative(moc_stage),
              "target_identity": identity(target_stage), "moc_before_identity": identity(moc),
              "moc_after_identity": identity(moc_stage),
              "manifest_hash": digest(read_text(folder / "manifest.json", 65536))}
    payload = encoded(record)
    if len(payload.encode("utf-8")) > LIMIT:
        raise ValueError("Publication journal exceeds size limit")
    path = inside(root, JOURNAL)
    temporary = _stage(path.parent, payload, 0o600, prefix=".pedagogy-journal-")
    try:
        os.replace(temporary, path)
        sync_directory(path.parent)
    finally:
        temporary.unlink(missing_ok=True)
    return record


def load(root):
    raw = read_text(inside(root, JOURNAL), LIMIT)
    record = json_object(raw)
    fields = {"version", "draft", "target", "moc", "module", "before", "after", "target_stage",
              "moc_stage", "target_identity", "moc_before_identity", "moc_after_identity", "manifest_hash"}
    identities = {"target_identity", "moc_before_identity", "moc_after_identity"}
    if set(record) != fields or type(record["version"]) is not int or record["version"] != 1:
        raise ValueError("Unsupported publication journal")
    if raw != encoded(record):
        raise ValueError("Publication journal was edited; manual inspection required")
    for field in fields - identities - {"version"}:
        if not isinstance(record[field], str):
            raise ValueError(f"Invalid publication journal field: {field}")
    for field in identities:
        value = record[field]
        if not isinstance(value, list) or len(value) != 3 or any(type(x) is not int or x < 0 for x in value):
            raise ValueError("Invalid publication file identity")
    draft = Path(record["draft"])
    if len(draft.parts) != 2 or draft.parts[0] != ".pedagogy-drafts":
        raise ValueError("Invalid journal draft scope")
    folder = inside(root, draft)
    manifest_text = read_text(inside(root, draft / "manifest.json"), 65536)
    if digest(manifest_text) != record["manifest_hash"]:
        raise ValueError("Draft manifest changed since publication started")
    manifest = json_object(manifest_text)
    from .publication import _scope, updated_moc
    from ..link_support.frontmatter import split_frontmatter
    target, moc = _scope(manifest["route"], manifest["slug"])
    if type(manifest.get("version")) is not int or manifest["version"] != 2 or manifest.get("status") != "draft":
        raise ValueError("Unsupported draft manifest")
    if (manifest.get("scope") != [target, moc] or [manifest.get("target"), manifest.get("moc")] != [target, moc]
            or [record["target"], record["moc"]] != [target, moc]):
        raise ValueError("Journal scope differs from the permitted route")
    for source, key, filename in (("module", "module_hash", "module.md"), ("after", "moc_after_hash", "moc.md")):
        if digest(record[source]) != manifest[key] or read_text(inside(root, draft / filename)) != record[source]:
            raise ValueError("Draft content changed since publication started")
    metadata, _, _ = split_frontmatter(record["module"])
    if digest(record["before"]) != manifest["moc_before_hash"] or metadata.get("id") != manifest["id"]:
        raise ValueError("Invalid journal source snapshot")
    derived = updated_moc(record["before"], target.removesuffix(".md"), metadata["title"], manifest["route"]["section"])
    if derived != record["after"]:
        raise ValueError("Journal navigation differs from the permitted insertion")
    for stage, destination in (("target_stage", "target"), ("moc_stage", "moc")):
        path = inside(root, record[stage])
        if path.parent != inside(root, record[destination]).parent or not path.name.startswith(".pedagogy-stage-"):
            raise ValueError("Invalid publication staging path")
    return record, manifest, folder


def state(root, record):
    target, moc, target_stage, moc_stage = [inside(root, record[k]) for k in ("target", "moc", "target_stage", "moc_stage")]
    linked = target.exists() and target_stage.exists()
    if target.exists():
        owned(target, record["target_identity"], record["module"], 2 if linked else 1)
    if target_stage.exists():
        owned(target_stage, record["target_identity"], record["module"], 2 if linked else 1)
    if identity(moc) == record["moc_before_identity"]:
        owned(moc, record["moc_before_identity"], record["before"])
        if not target_stage.exists() or not moc_stage.exists():
            raise ValueError("Required publication stage is missing")
        owned(moc_stage, record["moc_after_identity"], record["after"])
        return "module_installed" if target.exists() else "prepared"
    owned(moc, record["moc_after_identity"], record["after"])
    if not target.exists() or moc_stage.exists():
        raise ValueError("Published files do not match the recorded transaction")
    return "published"


def clear(root, record):
    path = inside(root, JOURNAL)
    if read_text(path, LIMIT) != encoded(record):
        raise ValueError("Publication journal changed during recovery")
    path.unlink()
    sync_directory(path.parent)


def finish(root, record):
    if state(root, record) != "published":
        raise ValueError("Publication has not finished")
    stage = inside(root, record["target_stage"])
    if stage.exists():
        stage.unlink()
        sync_directory(stage.parent)
    clear(root, record)


def abort(root, record):
    current = state(root, record)
    if current == "published":
        raise ValueError("Publication already committed; explicit recovery is required")
    target = inside(root, record["target"])
    if current == "module_installed":
        target.unlink()
        sync_directory(target.parent)
    clear(root, record)
    for key in ("target_stage", "moc_stage"):
        inside(root, record[key]).unlink(missing_ok=True)
