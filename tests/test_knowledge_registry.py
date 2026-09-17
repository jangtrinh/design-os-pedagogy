"""Trust checks using small corpora, including deliberately invalid records."""
import shutil
import tempfile
import unittest
from pathlib import Path
import yaml
from tools.knowledge_registry import build_registry, parse_frontmatter, validate_document


class KnowledgeRegistryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "00-system").mkdir()
        schema = Path(__file__).resolve().parents[1] / "00-system" / "metadata-schema.yaml"
        shutil.copyfile(schema, self.root / "00-system" / "metadata-schema.yaml")

    def metadata(self, identifier="concept-example", kind="concept", **fields):
        meta = dict(schema_version="2.0.0", id=identifier, type=kind, title="Example",
                    stage=["S2"], axes=["AX-01"], capabilities=[], context=[],
                    evidence_grade="U", claim_status="unreviewed", review_status="unreviewed",
                    provenance={"kind": "authored"})
        meta.update(fields)
        return meta

    def text(self, meta, body="# Example\n"):
        return "---\n" + yaml.safe_dump(meta, sort_keys=False) + "---\n" + body

    def write(self, name, meta, body="# Example\n"):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.text(meta, body), encoding="utf-8")
        return path

    def test_frontmatter_preserves_body_and_rejects_duplicate_keys(self):
        body = "# Header\n\n---\nLiteral body\n"
        self.assertEqual(parse_frontmatter(self.text({"id": "concept-x"}, body)),
                         ({"id": "concept-x"}, body))
        self.assertEqual(parse_frontmatter("Plain body"), ({}, "Plain body"))
        for text in ("---\nid: a\nid: b\n---\n", "---\nid: a\n",
                     "---\n- list\n---\n", "---\na: &x [*x]\n---\n"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_frontmatter(text)

    def test_valid_candidate_does_not_write_to_the_corpus(self):
        before = sorted(self.root.rglob("*"))
        errors = validate_document("10-foundations/new.md", self.text(self.metadata()), self.root, True)
        self.assertEqual(errors, [])
        self.assertEqual(sorted(self.root.rglob("*")), before)

    def test_generated_requires_v2_and_separate_assistance_namespace(self):
        for fields in ({"schema_version": "1.0.0"}, {"stage": ["AL2"]},
                       {"assistance_level": "S2"}, {"type": "mystery"}):
            self.assertTrue(validate_document("10-foundations/new.md",
                                             self.text(self.metadata(**fields)), self.root, True))
        self.assertEqual(validate_document("10-foundations/new.md",
                                          self.text(self.metadata(assistance_level="AL2")), self.root, True), [])

    def test_legacy_grade_and_validated_flag_do_not_become_review(self):
        self.write("10-foundations/legacy.md",
                   dict(id="legacy", title="Legacy", type="concept", stage=["S2-primary"],
                        axes=["AX-01: Learning Sciences"], evidence_level="A", status="validated"))
        result = build_registry(self.root)
        record = result["records"][0]
        self.assertEqual(record["id"], "legacy")
        self.assertEqual(record["stage"], ["S2"])
        self.assertEqual(record["evidence_grade"], "U")
        self.assertEqual(record["review_status"], "unreviewed")
        self.assertEqual(record["raw_metadata"]["evidence_level"], "A")
        self.assertTrue(result["warnings"])

    def test_unresolved_id_is_not_resolved_by_filename(self):
        self.write("10-foundations/named-node.md", self.metadata("canonical-node"))
        self.write("10-foundations/ref.md", self.metadata("reference-node", prerequisites=["named-node"]))
        result = build_registry(self.root)
        self.assertTrue(any("UNRESOLVED_REFERENCE" in e for e in result["errors"]))
        self.assertIsNone(result["edges"][0]["resolved_to"])
        (self.root / "00-system" / "identifier-aliases.yaml").write_text(
            "aliases:\n  named-node: canonical-node\n", encoding="utf-8")
        result = build_registry(self.root)
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["edges"][0]["resolved_to"], "canonical-node")

    def test_missing_id_duplicate_id_and_bad_alias_are_errors(self):
        meta = self.metadata()
        del meta["id"]
        self.write("10-foundations/missing.md", meta)
        self.write("10-foundations/a.md", self.metadata("duplicate"))
        self.write("10-foundations/b.md", self.metadata("duplicate"))
        (self.root / "00-system" / "identifier-aliases.yaml").write_text(
            "aliases:\n  ghost: does-not-exist\n", encoding="utf-8")
        errors = build_registry(self.root)["errors"]
        for code in ("ID_REQUIRED", "DUPLICATE_ID", "ALIAS_TARGET_UNKNOWN"):
            self.assertTrue(any(code in e for e in errors), errors)

    def test_alias_cannot_shadow_another_canonical_id(self):
        self.write("10-foundations/a.md", self.metadata("node-a"))
        self.write("10-foundations/b.md", self.metadata("node-b"))
        (self.root / "00-system" / "identifier-aliases.yaml").write_text(
            "aliases:\n  node-a: node-b\n", encoding="utf-8")
        self.assertTrue(any("ALIAS_COLLISION" in e for e in build_registry(self.root)["errors"]))

    def test_review_and_observation_require_provenance(self):
        for fields in ({"review_status": "source-checked"},
                       {"provenance": {"kind": "observed"}},
                       {"provenance": {"kind": "simulation"}, "claim_status": "supported"}):
            self.assertTrue(validate_document("50-practice-library/cases/new.md",
                                             self.text(self.metadata(kind="case", **fields)), self.root, True))

    def test_estimate_requires_typed_source_and_specific_comparison(self):
        self.write("60-evidence/sources/study.md", self.metadata(
            "source-study", "source", url="https://example.org/study", locator="Abstract"))
        self.write("60-evidence/claims/claim.md", self.metadata(
            "claim-study", "claim", claim_statement="A bounded test claim", source_ids=["source-study"]))
        estimate = self.metadata("estimate-study", "estimate", source_id="source-study",
                                 claim_id="claim-study", metric="hedges_g", value=0.48,
                                 population="School mathematics", comparator="No worked examples",
                                 outcome="Mathematics performance", timepoint="Study posttests", locator="Abstract")
        candidate = "60-evidence/estimates/result.md"
        self.assertEqual(validate_document(candidate, self.text(estimate), self.root, True), [])
        for key, value in (("source_id", "claim-study"), ("value", float("nan")),
                           ("value", True), ("metric", "g"), ("locator", "")):
            self.assertTrue(validate_document(candidate, self.text(dict(estimate, **{key: value})), self.root, True))

    def test_unrelated_legacy_errors_remain_in_full_registry(self):
        self.write("10-foundations/old.md", self.metadata("old", leads_to=["absent-node"]))
        self.assertTrue(build_registry(self.root)["errors"])
        self.assertEqual(validate_document("10-foundations/new.md",
                                          self.text(self.metadata()), self.root, True), [])

    def test_generated_effect_claim_requires_estimate_link(self):
        errors = validate_document("10-foundations/new.md",
                                   self.text(self.metadata(), "Effect size d = 0.64."), self.root, True)
        self.assertTrue(any("ESTIMATE:" in error for error in errors))
        self.assertEqual(validate_document("10-foundations/new.md",
                                          self.text(self.metadata(), "Gravity: g = 9.81."), self.root, True), [])

    def test_path_escape_and_unsupported_schema_cannot_pass(self):
        self.assertTrue(validate_document("../escape.md", self.text(self.metadata()), self.root, True))
        schema_path = self.root / "00-system" / "metadata-schema.yaml"
        schema = yaml.safe_load(schema_path.read_text())
        schema["anyOf"] = [{"type": "string"}]
        schema_path.write_text(yaml.safe_dump(schema))
        self.assertTrue(validate_document("10-foundations/new.md",
                                          self.text(self.metadata()), self.root, True))


if __name__ == "__main__":
    unittest.main()
