"""Crash real publisher processes at filesystem boundaries, then restart."""
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from publication_support import CorpusFixture, ROOT
from tools.pipeline_support.publication import apply, prepare
from tools.pipeline_support.recovery import inspect_publication, recover_publication

CRASH_PROGRAM = '''
import json, os, sys
from pathlib import Path
from tools.pipeline_support.publication import apply
from tools.pipeline_support.recovery import recover_publication
root, folder = Path(sys.argv[1]), Path(sys.argv[2])
boundary, operation = sys.argv[3:5]
manifest = json.loads((folder / 'manifest.json').read_text())
target, moc = root / manifest['target'], root / manifest['moc']
original_link, original_replace = os.link, os.replace
def link(source, destination, *args, **kwargs):
    if Path(destination) == target and boundary == 'before_link':
        os._exit(73)
    result = original_link(source, destination, *args, **kwargs)
    if Path(destination) == target and boundary == 'after_link':
        os._exit(73)
    return result
def replace(source, destination, *args, **kwargs):
    if Path(destination) == moc and boundary == 'before_moc':
        os._exit(73)
    result = original_replace(source, destination, *args, **kwargs)
    if Path(destination) == moc and boundary == 'after_moc':
        os._exit(73)
    return result
os.link, os.replace = link, replace
recover_publication(root) if operation == 'recover' else apply(root, folder)
raise SystemExit('Requested interruption was not reached')
'''


class PublicationRecoveryTests(CorpusFixture, unittest.TestCase):
    def draft(self):
        return prepare(self.root, self.route, self.identifier, self.slug, self.module())

    def crash(self, folder, boundary, operation="apply"):
        result = subprocess.run([sys.executable, "-B", "-c", CRASH_PROGRAM, str(self.root),
                                 str(folder), boundary, operation], cwd=ROOT,
                                capture_output=True, text=True, timeout=12)
        self.assertEqual(result.returncode, 73, result.stdout + result.stderr)

    def cli(self, flag):
        result = subprocess.run([sys.executable, "-B", str(ROOT / "tools/pedagogy_pipeline.py"),
                                 "--root", str(self.root), flag], cwd=ROOT,
                                capture_output=True, text=True, timeout=12)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def assert_recovery(self, boundary, expected):
        folder = self.draft()
        self.crash(folder, boundary)
        before_inspection = self.snapshot()
        self.assertEqual(self.cli("--inspect-publication")["state"], expected)
        self.assertEqual(self.snapshot(), before_inspection)
        self.assertEqual(self.cli("--recover-publication")["state"], "recovered")
        self.assertEqual(self.target.read_text(), self.module())
        self.assertEqual(self.moc.read_text(), (folder / "moc.md").read_text())
        self.assertEqual(self.target.stat().st_nlink, 1)
        after = self.snapshot()
        self.assertEqual(self.cli("--recover-publication")["state"], "idle")
        self.assertEqual(self.snapshot(), after)
        self.assertEqual(list(self.moc.parent.glob(".pedagogy-stage-*")), [])

    def test_restart_before_module_creation(self):
        self.assert_recovery("before_link", "prepared")

    def test_restart_after_module_creation(self):
        self.assert_recovery("after_link", "module_installed")

    def test_restart_before_navigation_replacement(self):
        self.assert_recovery("before_moc", "module_installed")

    def test_restart_after_navigation_replacement(self):
        self.assert_recovery("after_moc", "published")

    def test_recovery_can_be_interrupted_and_restarted(self):
        folder = self.draft()
        self.crash(folder, "before_link")
        self.crash(folder, "after_moc", operation="recover")
        self.assertEqual(inspect_publication(self.root)["state"], "published")
        self.assertEqual(recover_publication(self.root)["state"], "recovered")
        self.assertEqual(self.moc.read_text(), (folder / "moc.md").read_text())

    def assert_conflict_preserves_files(self):
        before = self.snapshot()
        self.assertEqual(inspect_publication(self.root)["state"], "conflict")
        with self.assertRaises((ValueError, OSError)):
            recover_publication(self.root)
        self.assertEqual(self.snapshot(), before)
        self.assertTrue((self.root / ".pedagogy-drafts/active-publication.json").exists())

    def test_edited_module_is_preserved(self):
        self.crash(self.draft(), "after_link")
        self.target.write_text("Teacher edited the interrupted module.\n")
        self.assert_conflict_preserves_files()

    def test_edited_navigation_is_preserved(self):
        self.crash(self.draft(), "after_link")
        self.moc.write_text(self.moc.read_text() + "\nLater editorial work.\n")
        self.assert_conflict_preserves_files()

    def test_same_content_replacement_does_not_inherit_ownership(self):
        self.crash(self.draft(), "after_link")
        replacement = self.root / "replacement.md"
        replacement.write_text(self.target.read_text())
        os.replace(replacement, self.target)
        self.assert_conflict_preserves_files()

    def test_changed_draft_blocks_recovery(self):
        folder = self.draft()
        self.crash(folder, "after_link")
        (folder / "module.md").write_text("A new draft version.\n")
        self.assert_conflict_preserves_files()

    def test_pending_transaction_blocks_another_publication(self):
        folder = self.draft()
        self.crash(folder, "before_link")
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "Unfinished publication"):
            self.draft()
        with self.assertRaisesRegex(ValueError, "Unfinished publication"):
            apply(self.root, folder)
        self.assertEqual(self.snapshot(), before)
        recover_publication(self.root)

    def test_catchable_navigation_failure_rolls_back_owned_module(self):
        folder = self.draft()
        before = self.snapshot()
        original_replace = os.replace
        def fail_navigation(source, destination, *args, **kwargs):
            if Path(destination) == self.moc:
                raise OSError("Navigation write failed")
            return original_replace(source, destination, *args, **kwargs)
        with patch("tools.pipeline_support.transactions.os.replace", side_effect=fail_navigation):
            with self.assertRaises(OSError):
                apply(self.root, folder)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(inspect_publication(self.root)["state"], "idle")


if __name__ == "__main__":
    unittest.main()
