"""Coverage must expose gaps without converting graph connectivity into evidence."""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

from tools.knowledge.coverage import coverage_report, markdown_report


class KnowledgeCoverageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = Path(__file__).resolve().parents[1]
        (self.root / "00-system").mkdir()
        shutil.copyfile(self.project / "00-system/metadata-schema.yaml",
                        self.root / "00-system/metadata-schema.yaml")

    def write(self, identifier, *, kind="practice", folder="30-pedagogy", **fields):
        meta = dict(schema_version="2.0.0", id=identifier, type=kind, title=identifier,
                    stage=["S6"], axes=["AX-04"], capabilities=["CAP-02"], context=[],
                    evidence_grade="U", claim_status="unreviewed", review_status="unreviewed",
                    provenance={"kind": "authored"})
        meta.update(fields)
        path = self.root / folder / f"{identifier}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("---\n" + yaml.safe_dump(meta) + "---\n# Test record\n", encoding="utf-8")
        return path

    def source(self, identifier="source-one", **fields):
        return self.write(identifier, kind="source", folder="60-evidence/sources",
                          url="https://example.org/source", locator="Test locator", **fields)

    def test_empty_corpus_retains_zero_rows_and_no_readiness_claim(self):
        report = coverage_report(self.root)
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["selected"]["records"], 0)
        self.assertEqual(len(report["tagged_coverage"]["stage"]), 8)
        self.assertTrue(all(r["records"] == 0 for r in report["tagged_coverage"]["stage"]))
        self.assertEqual(report["learning_effectiveness"], "not_assessed")
        self.assertIn("not assessed", markdown_report(report))

    def test_filters_intersect_without_age_or_assistance_inference(self):
        self.write("adult", stage=["S6"], axes=["AX-04"], capabilities=["CAP-02"])
        self.write("adult-other-axis", stage=["S6"], axes=["AX-05"])
        self.write("child", stage=["S2"], axes=["AX-04"])
        report = coverage_report(self.root, stage="S6", axis="AX-04", capability="CAP-02")
        self.assertEqual([r["id"] for r in report["records"]], ["adult"])
        with self.assertRaises(ValueError):
            coverage_report(self.root, stage="AL2")

    def test_evidence_trails_follow_claims_but_not_prerequisites(self):
        self.source()
        self.write("claim-one", kind="claim", claim_statement="A test claim",
                   source_ids=["source-one"])
        self.write("connected", claim_ids=["claim-one"])
        self.write("navigation-only", prerequisites=["source-one"])
        report = coverage_report(self.root)
        self.assertEqual(report["errors"], [])
        records = {r["id"]: r for r in report["records"]}
        self.assertEqual(records["connected"]["traceable_source_ids"], ["source-one"])
        self.assertEqual(records["navigation-only"]["traceable_source_ids"], [])
        self.assertEqual(records["connected"]["review_status"], "unreviewed")

    def test_aliases_resolve_and_evidence_cycles_terminate(self):
        self.source()
        (self.root / "00-system/identifier-aliases.yaml").write_text(
            "aliases:\n  legacy-source: source-one\n", encoding="utf-8")
        self.write("claim-a", kind="claim", claim_statement="Test A",
                   claim_ids=["claim-b"], source_ids=["legacy-source"])
        self.write("claim-b", kind="claim", claim_statement="Test B", claim_ids=["claim-a"])
        report = coverage_report(self.root)
        self.assertEqual(report["errors"], [])
        claim = next(r for r in report["records"] if r["id"] == "claim-b")
        self.assertEqual(claim["traceable_source_ids"], ["source-one"])

    def test_legacy_validation_label_and_prose_do_not_confer_review(self):
        path = self.write("legacy")
        path.write_text('---\nid: legacy\ntitle: Legacy\ntype: practice\n'
                        'status: validated\nevidence_level: A\n---\nCited source in prose.\n',
                        encoding="utf-8")
        report = coverage_report(self.root)
        self.assertEqual(report["selected"]["legacy"], 1)
        self.assertEqual(report["selected"]["reviewed"], 0)
        self.assertEqual(report["records"][0]["evidence_grade"], "U")
        self.assertIn("legacy", report["untagged"]["stage"])
        self.assertIn("legacy", report["without_source_trail"])

    def test_inventory_is_read_only_and_deterministic(self):
        self.source()
        self.write("content", source_ids=["source-one"])
        def snapshot():
            return {str(p.relative_to(self.root)): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in self.root.rglob("*") if p.is_file()}
        before = snapshot()
        first = coverage_report(self.root)
        self.assertEqual(first, coverage_report(self.root))
        self.assertEqual(before, snapshot())

    def test_invalid_references_remain_visible_and_cli_fails(self):
        self.write("broken", source_ids=["absent"])
        result = subprocess.run([sys.executable, "-B", str(self.project / "tools/knowledge_coverage.py"),
                                 "--root", str(self.root), "--json"],
                                capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 1)
        report = json.loads(result.stdout)
        self.assertTrue(any("UNRESOLVED_REFERENCE" in e for e in report["errors"]))
        self.assertEqual(report["learning_effectiveness"], "not_assessed")

    def test_missing_root_reports_error_without_creation(self):
        target = self.root / "absent"
        report = coverage_report(target)
        self.assertTrue(report["errors"])
        self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
