"""Local child processes and actual Markdown parsing; no network or model calls."""
import sys
import time
import unittest
from publication_support import CorpusFixture
from tools.pipeline_support.process import run_provider
from tools.pipeline_support.routing import classify_topic, slugify
from tools.link_support.audit import audit, candidate_errors


class ProviderTests(unittest.TestCase):
    def child(self, script, **options):
        return run_provider([sys.executable, "-c", script], "test input", **options)

    def test_stdin_stdout_and_stderr_are_separate(self):
        result = self.child("import sys; s=sys.stdin.read(); sys.stderr.write('warning'); print(s)")
        self.assertEqual(result, "test input\n")

    def test_large_streams_are_drained_and_limit_enforced(self):
        code = "import sys; sys.stdout.write('x'*1048576); sys.stderr.write('y'*1048576)"
        self.assertEqual(len(self.child(code)), 1048576)
        with self.assertRaisesRegex(ValueError, "output limit"):
            self.child(code, max_bytes=1024)

    def test_nonzero_utf8_and_timeout_fail_without_partial_output(self):
        for code in ("print('---\\nid: fragment'); raise SystemExit(2)", "import os; os.write(1,b'\\xff')"):
            with self.subTest(code=code), self.assertRaises(ValueError):
                self.child(code)
        start = time.monotonic()
        with self.assertRaisesRegex(ValueError, "timed out"):
            self.child("import time; time.sleep(10)", timeout=0.1)
        self.assertLess(time.monotonic() - start, 5)

    def test_invalid_limits_and_explicit_routes(self):
        for timeout in (0, -1, float("nan"), float("inf"), True):
            with self.assertRaises(ValueError):
                self.child("print('x')", timeout=timeout)
        self.assertNotEqual(slugify("Learning (S2)"), slugify("Learning (S3)"))
        self.assertEqual(slugify("学习"), "学习")
        with self.assertRaises(ValueError):
            slugify("***")
        with self.assertRaises(ValueError):
            classify_topic("wait time", stage="S2")
        self.assertIn("s0-prenatal", classify_topic("prenatal", "stages", stage="S0")["dir"])


class LinkTests(CorpusFixture, unittest.TestCase):
    def document(self, text):
        path = self.root / "reference.md"
        path.write_text(text)
        return path

    def test_reference_html_and_anchor_targets_are_checked(self):
        for text in ('![image][pic]\n\n[pic]: absent.png\n', '<img src="absent.png">', '[jump](README.md#missing)'):
            self.document(text)
            self.assertTrue(audit(self.root)["errors"], text)

    def test_valid_alias_paths_and_encoded_targets(self):
        child = self.root / "A name.md"
        child.write_text('---\naliases: ["Friendly title"]\n---\n# A heading\n')
        self.document('[file](A%20name.md#a-heading)\n[[Friendly title]]\n[[A name#A heading]]\n')
        self.assertEqual(audit(self.root)["errors"], [])

    def test_fenced_examples_and_body_ids_are_not_parsed_as_links_or_metadata(self):
        self.document('```md\n[example](missing.md)\n[[missing]]\n```\n')
        self.assertEqual(audit(self.root)["errors"], [])
        (self.root / "body.md").write_text('# Body\nid: fake-id\n')
        self.document('[[fake-id]]\n')
        self.assertTrue(audit(self.root)["errors"])

    def test_missing_root_and_bad_frontmatter_fail_closed(self):
        self.assertTrue(audit(self.root / "absent")["errors"])
        self.document('---\nid: first\nid: second\n---\n# Broken metadata\n')
        self.assertTrue(candidate_errors(self.root, self.root / "candidate.md", '# New file\n'))

    def test_machine_paths_in_instructions_remain_visible_portability_warnings(self):
        text = '# Local instructions\n\n```sh\ncd /Users/example/Project\n```\n'
        path = self.document(text)
        report = audit(self.root)
        self.assertEqual(report["errors"], [])
        self.assertEqual(len(report["portability_warnings"]), 1)
        self.assertIn("machine-specific path", report["portability_warnings"][0])
        self.assertTrue(candidate_errors(self.root, path, text))

    def test_machine_specific_link_targets_still_fail_link_audit(self):
        for target in ('/Users/example/Project/missing.md',
                       'file:///Users/example/Project/missing.md'):
            with self.subTest(target=target):
                self.document(f'[Local document]({target})\n')
                self.assertTrue(audit(self.root)["errors"])

    def test_unsupported_schemes_are_reported_in_links_and_references(self):
        for text in ('[Unsupported](javascript:alert(1))\n',
                     '[Local][target]\n\n[target]: file:///example/missing.md\n',
                     '![Local image](file:///example/missing.png)\n'):
            with self.subTest(text=text):
                self.document(text)
                errors = audit(self.root)["errors"]
                self.assertTrue(any("unsupported URL scheme" in e for e in errors), errors)
        self.document('```md\n[Example](file:///example/missing.md)\n```\n')
        self.assertEqual(audit(self.root)["errors"], [])


if __name__ == "__main__":
    unittest.main()
