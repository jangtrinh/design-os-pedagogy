"""Filesystem boundaries and journaled two-file publication."""
import fcntl
import hashlib
import json
import os
import stat
import tempfile
from contextlib import contextmanager
from pathlib import Path


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def inside(root, relative):
    path = Path(relative)
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise ValueError("A nonempty relative path inside the repository is required")
    current = Path(root)
    for part in path.parts:
        current /= part
        if current.is_symlink():
            raise ValueError("Publication paths must not contain symlinks")
    current.resolve().relative_to(Path(root).resolve())
    return current


def read_text(path, limit=2097152):
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_size > limit:
            raise ValueError("Expected a bounded regular file without hardlinks")
        content = stream.read(limit + 1)
        if len(content) > limit:
            raise ValueError("Publication file exceeds size limit")
        return content.decode("utf-8")


def json_object(text):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f"Duplicate manifest key: {key}")
            result[key] = value
        return result
    def reject(value):
        raise ValueError(f"Invalid JSON number: {value}")
    try:
        result = json.loads(text, object_pairs_hook=pairs, parse_constant=reject)
    except RecursionError:
        raise ValueError("Manifest nesting is too deep") from None
    if not isinstance(result, dict):
        raise ValueError("Manifest must be a JSON object")
    return result


@contextmanager
def publication_lock(root):
    drafts = inside(root, ".pedagogy-drafts")
    drafts.mkdir(mode=0o700, exist_ok=True)
    path = inside(root, ".pedagogy-drafts/publication.lock")
    descriptor = os.open(path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600)
    with os.fdopen(descriptor, "r+b") as lock:
        info = os.fstat(lock.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise ValueError("Invalid publication lock file")
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield


def _stage(parent, text, mode, prefix=".pedagogy-stage-"):
    path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=parent, prefix=prefix, delete=False) as stream:
            path = Path(stream.name)
            stream.write(text)
            stream.flush()
            os.fchmod(stream.fileno(), mode)
            os.fsync(stream.fileno())
        return path
    except BaseException:
        if path is not None:
            path.unlink(missing_ok=True)
        raise


def install(target, moc, text, before, after, *, root, folder):
    """Record intent before changing corpus files; the caller holds the lock."""
    from .publication_journal import begin, abort, finish, owned, pending, sync_directory
    if target.exists() or read_text(moc) != before:
        raise ValueError("Target or MOC changed; no files were applied")
    new_dirs = []
    parent = target.parent
    while not parent.exists():
        new_dirs.append(parent)
        parent = parent.parent
    target_temp = moc_temp = record = None
    try:
        for directory in reversed(new_dirs):
            directory.mkdir()
        target_temp = _stage(target.parent, text, 0o644)
        moc_temp = _stage(moc.parent, after, stat.S_IMODE(moc.stat().st_mode))
        record = begin(root, folder, target, moc, text, before, after, target_temp, moc_temp)
        os.link(target_temp, target)
        sync_directory(target.parent)
        owned(moc, record["moc_before_identity"], before)
        os.replace(moc_temp, moc)
        moc_temp = None
        sync_directory(moc.parent)
        finish(root, record)
    except BaseException:
        if record is not None:
            try:
                abort(root, record)
            except (ValueError, OSError):
                pass  # Preserve the journal and stages for explicit inspection.
        raise
    finally:
        if not pending(root):
            for temporary in (target_temp, moc_temp):
                if temporary is not None:
                    temporary.unlink(missing_ok=True)
            for directory in new_dirs:
                try:
                    directory.rmdir()
                except OSError:
                    pass
