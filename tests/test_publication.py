"""Publication tests use real files and deliberate I/O failure injection."""
import json
import os
import subprocess
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch

from publication_support import CorpusFixture, ROOT
from tools.pipeline_support.publication import apply, prepare, updated_moc
from tools.pipeline_support.transactions import digest, json_object
from tools.pipeline_support.validation import validate


class PublicationTests(CorpusFixture, unittest.TestCase):
    def draft(self, **fields):
        return prepare(self.root, self.route, self.identifier, self.slug, self.module(**fields))

    def test_prepare_preserves_corpus_and_apply_changes_only_two_files(self):
        before = self.snapshot()
        folder = self.draft()
        self.assertEqual(self.snapshot(), before)
        result = apply(self.root, folder)
        self.assertEqual(result["status"], "applied")
        after = self.snapshot()
        changed = {p for p in after if before.get(p) != after[p]}
        self.assertEqual(changed, {str(self.target.relative_to(self.root)), self.route["moc"]})
        self.assertEqual(self.target.read_text(), self.module())
        self.assertIn(str(self.target.relative_to(self.root)).removesuffix(".md"), self.moc.read_text())

    def test_repeat_and_existing_target_preserve_user_content(self):
        folder = self.draft()
        apply(self.root, folder)
        before = self.snapshot()
        with self.assertRaises(ValueError):
            apply(self.root, folder)
        with self.assertRaises(ValueError):
            self.draft()
        self.assertEqual(self.snapshot(), before)

    def test_stale_moc_rejected(self):
        folder = self.draft()
        self.moc.write_text(self.moc.read_text() + "\nUser's later edit.\n")
        before = self.snapshot()
        with self.assertRaises(ValueError):
            apply(self.root, folder)
        self.assertEqual(self.snapshot(), before)

    def test_tampering_and_rehashed_navigation_injection_rejected(self):
        folder = self.draft()
        before = self.snapshot()
        (folder / "moc.md").write_text("# Replaced user's navigation\n")
        with self.assertRaises(ValueError):
            apply(self.root, folder)
        self.manifest(folder, moc_after_hash=digest((folder / "moc.md").read_text()))
        with self.assertRaises(ValueError):
            apply(self.root, folder)
        self.assertEqual(self.snapshot(), before)

    def test_route_scope_and_metadata_mismatch_rejected(self):
        folder = self.draft()
        self.manifest(folder, target="README.md", scope=["README.md", self.route["moc"]])
        with self.assertRaises(ValueError):
            apply(self.root, folder)
        for fields in ({"type": "concept"}, {"stage": ["S7"]}, {"claim_status": "supported"}):
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                self.draft(**fields)
        self.assertFalse(self.target.exists())

    def test_symlink_and_hardlink_draft_files_rejected(self):
        folder = self.draft()
        before = self.snapshot()
        module = folder / "module.md"
        original = module.read_text()
        module.unlink()
        module.symlink_to(self.root / "README.md")
        with self.assertRaises(ValueError):
            apply(self.root, folder)
        module.unlink()
        module.write_text(original)
        os.link(module, folder / "linked.md")
        with self.assertRaises(ValueError):
            apply(self.root, folder)
        self.assertEqual(self.snapshot(), before)

    def test_symlink_draft_folder_and_hardlinked_lock_rejected(self):
        folder = self.draft()
        alias = self.root / ".pedagogy-drafts/alias"
        alias.symlink_to(folder, target_is_directory=True)
        with self.assertRaises(ValueError):
            apply(self.root, alias)
        lock = self.root / ".pedagogy-drafts/publication.lock"
        os.link(lock, self.root / ".pedagogy-drafts/linked-lock")
        with self.assertRaises(ValueError):
            apply(self.root, folder)
        self.assertFalse(self.target.exists())

    def test_replace_failure_rolls_back_module_and_preserves_moc(self):
        folder = self.draft()
        before = self.snapshot()
        with patch("tools.pipeline_support.transactions.os.replace", side_effect=OSError("injected disk failure")):
            with self.assertRaises(OSError):
                apply(self.root, folder)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(self.target.parent.exists())
        self.assertEqual(list(self.moc.parent.iterdir()), [self.moc])

    def test_two_concurrent_applies_do_not_overwrite_each_other(self):
        folders = [self.draft(), self.draft()]
        def run(folder):
            try:
                return apply(self.root, folder)["status"]
            except ValueError:
                return "conflict"
        with ThreadPoolExecutor(max_workers=2) as executor:
            self.assertCountEqual(executor.map(run, folders), ["applied", "conflict"])
        self.assertEqual(self.moc.read_text().count("Authored draft; review pending."), 1)

    def test_instructional_gate_rejects_audit_counterexamples(self):
        valid = self.module()
        samples = ["---\nid: bad\n" + "placeholder\n" * 50,
                   valid.replace(self.identifier, "wrong-id", 1),
                   valid.replace("## Mental Model", "## MISSING"),
                   valid.split("# Classroom practice", 1)[0] + "```markdown\n" + valid.split("# Classroom practice", 1)[1] + "\n```\n",
                   valid + "\nWrite the full, complete document now.\n",
                   valid.replace("id: " + self.identifier, "id: other\nid: " + self.identifier)]
        for sample in samples:
            with self.subTest(sample=sample[:70]), self.assertRaises(ValueError):
                validate(self.root, str(self.target.relative_to(self.root)), sample, self.identifier)
        self.assertFalse(self.target.exists())

    def test_invalid_manifest_json_is_not_accepted(self):
        for text in ('[]', '{"version":2,"version":2}', '{"number":NaN}', '[' * 2000):
            with self.subTest(text=text[:40]), self.assertRaises(ValueError):
                json_object(text)

    def test_similar_moc_link_does_not_suppress_new_entry(self):
        before = "# Methods\n\n## Cases\n\n[[topic-advanced]]\n"
        after = updated_moc(before, "topic", "New topic", "## Cases")
        self.assertIn("[[topic|New topic]]", after)
        self.assertIn("[[topic-advanced]]", after)

    def test_real_cli_import_then_apply(self):
        source = self.root / "input.md"
        source.write_text(self.module())
        command = [sys.executable, "-B", str(ROOT / "tools/pedagogy_pipeline.py"), "--root", str(self.root)]
        before = self.snapshot()
        result = subprocess.run(command + ["Classroom practice", "--stage", "S2", "--archetype", "methods",
                                           "--input", str(source)], text=True, capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.snapshot(), before)
        folder = json.loads(result.stdout)["folder"]
        result = subprocess.run(command + ["--apply", folder], text=True, capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(json.loads(result.stdout)["git_operations"])
        self.assertTrue(self.target.is_file())

    def test_cli_rejects_fifo_input_without_waiting_for_a_writer(self):
        source = self.root / "input.md"
        os.mkfifo(source)
        command = [sys.executable, "-B", str(ROOT / "tools/pedagogy_pipeline.py"),
                   "--root", str(self.root), "Classroom practice", "--stage", "S2",
                   "--archetype", "methods", "--input", str(source)]
        result = subprocess.run(command, text=True, capture_output=True, timeout=3)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("Publication stopped:", result.stderr)
        self.assertFalse((self.root / ".pedagogy-drafts").exists())
        self.assertFalse(self.target.exists())

    def test_cli_rejects_linked_input_before_preparing_a_draft(self):
        original = self.root / "original.md"
        original.write_text(self.module(), encoding="utf-8")
        source = self.root / "input.md"
        command = [sys.executable, "-B", str(ROOT / "tools/pedagogy_pipeline.py"),
                   "--root", str(self.root), "Classroom practice", "--stage", "S2",
                   "--archetype", "methods", "--input", str(source)]
        for kind in ("symlink", "hardlink"):
            with self.subTest(kind=kind):
                source.symlink_to(original) if kind == "symlink" else os.link(original, source)
                try:
                    result = subprocess.run(command, text=True, capture_output=True, timeout=3)
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn("Publication stopped:", result.stderr)
                    self.assertFalse((self.root / ".pedagogy-drafts").exists())
                    self.assertEqual(original.read_text(encoding="utf-8"), self.module())
                finally:
                    source.unlink()


if __name__ == "__main__":
    unittest.main()
