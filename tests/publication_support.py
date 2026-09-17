"""Small input corpora for exercising the actual publication pipeline."""
import hashlib
import json
import shutil
import tempfile
from pathlib import Path
import yaml
from tools.pipeline_support.routing import classify_topic
from tools.pipeline_support.validation import SECTIONS

ROOT = Path(__file__).resolve().parents[1]


class CorpusFixture:
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root / "00-system").mkdir()
        shutil.copyfile(ROOT / "00-system/metadata-schema.yaml", self.root / "00-system/metadata-schema.yaml")
        (self.root / "README.md").write_text("# Publication test corpus\n")
        self.route = classify_topic("Classroom practice", "methods", stage="S2")
        self.moc = self.root / self.route["moc"]
        self.moc.parent.mkdir()
        self.moc.write_text("# Methods\n\n" + self.route["section"] + "\n\nExisting editorial note.\n")
        self.identifier, self.slug = "practice-classroom-practice", "classroom-practice"
        self.target = self.root / self.route["dir"] / f"{self.slug}.md"

    def module(self, **updates):
        metadata = dict(schema_version="2.0.0", id=self.identifier, type="practice", title="Classroom practice",
                        stage=["S2"], axes=["AX-03"], capabilities=["CAP-02"], context=["Fixture lesson"],
                        evidence_grade="U", claim_status="unreviewed", review_status="unreviewed",
                        provenance={"kind": "authored", "citations": [{"url": "https://example.org/fixture", "locator": "Test input only"}]})
        metadata.update(updates)
        prose = "Ask the learner to describe their method. Record an alternative explanation and select another task before drawing a conclusion."
        return "---\n" + yaml.safe_dump(metadata, sort_keys=False) + "---\n# Classroom practice\n\n" + "\n\n".join(
            f"## {name}\n\n{prose}" for name in SECTIONS) + "\n"

    def snapshot(self):
        return {str(p.relative_to(self.root)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in self.root.rglob("*") if p.is_file() and ".pedagogy-drafts" not in p.parts}

    def manifest(self, folder, **updates):
        path = folder / "manifest.json"
        data = json.loads(path.read_text())
        data.update(updates)
        path.write_text(json.dumps(data))
        return data
