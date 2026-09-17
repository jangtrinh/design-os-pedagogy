"""Inspect or explicitly finish interrupted publication while preserving edits."""
import os
from pathlib import Path

from .publication_journal import finish, load, owned, pending, state, sync_directory
from .transactions import inside, publication_lock


def inspect_publication(root):
    root = Path(root).resolve()
    with publication_lock(root):
        if not pending(root):
            return {"state": "idle", "corpus_changed": False}
        try:
            record, _, _ = load(root)
            return {"state": state(root, record), "draft": record["draft"],
                    "paths": [record["target"], record["moc"]], "corpus_changed": False}
        except (ValueError, OSError, KeyError, TypeError) as error:
            return {"state": "conflict", "reason": str(error), "corpus_changed": False}


def recover_publication(root):
    root = Path(root).resolve()
    with publication_lock(root):
        if not pending(root):
            return {"state": "idle", "corpus_changed": False, "git_operations": False}
        record, manifest, _ = load(root)
        current = state(root, record)
        target, moc = inside(root, record["target"]), inside(root, record["moc"])
        if current != "published":
            from .publication import _validate
            after = _validate(root, record["target"], record["moc"], manifest["route"],
                              manifest["id"], record["module"], record["before"])
            if after != record["after"]:
                raise ValueError("Recovery validation changed the proposed navigation")
            if state(root, record) != current:
                raise ValueError("Publication changed during recovery")
            if current == "prepared":
                os.link(inside(root, record["target_stage"]), target)
                sync_directory(target.parent)
            owned(moc, record["moc_before_identity"], record["before"])
            os.replace(inside(root, record["moc_stage"]), moc)
            sync_directory(moc.parent)
        finish(root, record)
        return {"state": "recovered", "paths": [record["target"], record["moc"]],
                "corpus_changed": current != "published", "git_operations": False,
                "review_status": "unreviewed"}
