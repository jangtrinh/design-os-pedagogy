"""Explicit routing and Unicode identifiers, independent of provider execution."""
from __future__ import annotations

from pathlib import Path
import re
import unicodedata

STAGE_DIRS = {
    "S0": "s0-prenatal-caregiver", "S1": "s1-early-childhood", "S2": "s2-primary",
    "S3": "s3-secondary", "S4": "s4-tertiary", "S5": "s5-postgraduate-doctoral",
    "S6": "s6-lifelong-adult", "S7": "s7-master-pedagogy",
}
ARCHETYPES = {"foundations": "A", "stages": "B", "methods": "C", "disciplines": "D",
              "cases": "E", "capabilities": "F", "runtime": "Runtime"}
TYPES = {"A": "concept", "B": "stage-guide", "C": "practice", "D": "discipline",
         "E": "case", "F": "capability", "Runtime": "protocol"}
MOC = "00-navigation/"


def slugify(text):
    value = unicodedata.normalize("NFKC", text).casefold()
    value = re.sub(r"[^\w\s-]", " ", value, flags=re.UNICODE)
    value = re.sub(r"[\s_-]+", "-", value).strip("-")
    if not value or len(value.encode("utf-8")) > 180:
        raise ValueError("Topic must yield a non-empty identifier of at most 180 UTF-8 bytes; provide a shorter title")
    return value


def classify_topic(topic, archetype="auto", *, stage=None, domain=None):
    allowed = {*ARCHETYPES, *ARCHETYPES.values(), "auto"}
    if archetype not in allowed:
        raise ValueError(f"Unknown archetype {archetype!r}; choose " + ", ".join(ARCHETYPES))
    if stage not in STAGE_DIRS:
        raise ValueError("Choose an explicit lifecycle --stage S0 through S7")
    arch = ARCHETYPES.get(archetype, archetype)
    words = set(re.findall(r"[^\W_]+", unicodedata.normalize("NFKC", topic).casefold()))
    if arch == "auto":
        if words & {"case", "transcript", "trial", "rct", "simulation"}:
            arch = "E"
        elif words & {"neuroscience", "memory", "retrieval", "cognition"}:
            arch = "A"
        elif words & {"ai", "llm", "agent", "synthetic", "offloading"}:
            arch, domain = "C", domain or "edtech-ai"
        else:
            raise ValueError("Topic has no unambiguous automatic route. Choose --archetype and --domain explicitly")
    if domain is not None and (slugify(domain) != domain or "/" in domain):
        raise ValueError("--domain must be a single lowercase domain slug")
    if arch in {"D", "F"} and not domain:
        raise ValueError("Discipline/capability routes require an explicit --domain directory")
    defaults = {"A": "learning-science", "B": "developmental-pedagogy", "C": "instructional-methods",
                "D": domain, "E": "clinical-case", "F": domain, "Runtime": "agent-runtime"}
    domain = domain or defaults[arch]
    routes = {
        "A": (f"10-foundations/{domain}", "MOC-Learning-Science.md", "## 1. Core Cognitive Foundations & Neurobiology"),
        "B": (f"20-stages/{STAGE_DIRS[stage]}", "MOC-Instructional-Design.md", "## 1. By Lifecycle Stage"),
        "C": (f"30-pedagogy/{domain}", "MOC-Instructional-Design.md", "## 2. Core Instructional Methods & Disciplinary Pedagogies"),
        "D": (f"40-disciplines/{domain}", "MOC-Instructional-Design.md", "## 2. Core Instructional Methods & Disciplinary Pedagogies"),
        "E": ("50-practice-library/cases", "MOC-Classroom-Practice.md", "## 2. Clinical Classroom Cases & Protocols"),
        "F": (f"70-capabilities/{domain}", "MOC-Assessment.md", "## 1. Classroom Assessment Instruments & Diagnostic Catalogs"),
        "Runtime": ("90-agent-runtime/evals", "MOC-Assessment.md", "## 2. Adaptive Protocols & AI Evaluation Rubrics"),
    }
    directory, moc, section = routes[arch]
    if arch == "C" and domain == "edtech-ai":
        section = "## 4. Cutting-Edge AI-Era Pedagogy & Epistemic Scaffolding"
    if arch == "C" and domain == "assessment-psychometrics":
        moc, section = "MOC-Assessment.md", "## 1. Classroom Assessment Instruments & Diagnostic Catalogs"
    return {"archetype": arch, "type": TYPES[arch], "dir": directory, "moc": MOC + moc,
            "section": section, "domain": domain, "stage": stage}


def find_repo_root(start=None):
    current = Path(start or __file__).resolve()
    for root in [current, *current.parents]:
        if (root / "00-system" / "metadata-schema.yaml").is_file() and (root / "README.md").is_file():
            return root
    raise ValueError("Cannot identify repository root; use --root with an existing Agent Teacher checkout")
