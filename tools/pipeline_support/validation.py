"""Validate draft structure and references; scientific review remains separate."""
import re
from pathlib import Path

from ..knowledge_registry import validate_document
from ..link_support.frontmatter import split_frontmatter
from ..link_support.markdown import parse_markdown

SECTIONS = ("Learning Contract", "Intuitive Dilemma", "Prediction Challenge", "Mental Model",
            "Worked Example", "Non-Example", "Misconceptions", "Diagnostic Question",
            "Practice and Transfer", "Implementation Protocol", "Evidence and Boundaries")


def validate(root, relative, text, identifier):
    if not isinstance(text, str) or len(text.encode("utf-8")) > 2097152:
        raise ValueError("Module must be UTF-8 text below 2 MiB")
    # Publication framing is stricter than the legacy adapter; both reject unsafe YAML.
    metadata, body, _ = split_frontmatter(text, required=True)
    if metadata.get("id") != identifier:
        raise ValueError("Module ID does not match the requested canonical identifier")
    if metadata.get("schema_version") != "2.0.0" or metadata.get("review_status") != "unreviewed":
        raise ValueError("Generated modules require schema_version 2.0.0 and unreviewed status")
    if metadata.get("claim_status") not in {"unreviewed", "not-applicable"}:
        raise ValueError("Publication cannot appraise a generated claim automatically")
    placeholder = r"(?im)(\bTODO\b|\bPLACEHOLDER\b|<Real empirical|MANDATORY GOVERNING INVARIANTS|Write the full, complete document|^TOPIC:|^MODULE ID:|^hook:|^tokens used)"
    if re.search(placeholder, text):
        raise ValueError("Output contains placeholder, prompt echo or runtime material")
    if metadata.get("type") not in {"source", "claim", "estimate"}:
        headings = [(title, line) for level, title, line in parse_markdown(body).headings if level == 2]
        names = [re.sub(r"^\d+[.)]?\s*", "", title).strip().casefold() for title, _ in headings]
        missing = [section for section in SECTIONS if section.casefold() not in names]
        if missing:
            raise ValueError("Missing instructional sections: " + ", ".join(missing))
        if len(names) != len(set(names)):
            raise ValueError("Instructional headings must not repeat")
        lines = body.splitlines()
        spans = ["\n".join(lines[line:headings[index + 1][1] - 1 if index + 1 < len(headings) else len(lines)])
                 for index, (_, line) in enumerate(headings)]
        if any(len(section.strip()) < 40 for section in spans):
            raise ValueError("Instructional sections must contain substantive prose")
        provenance = metadata.get("provenance", {})
        if not metadata.get("source_ids") and not (isinstance(provenance, dict) and provenance.get("citations")):
            raise ValueError("Instructional drafts require identified source references or URL locators")
    errors = validate_document(Path(root) / relative, text, root, generated=True)
    if errors:
        raise ValueError("Metadata/reference validation failed:\n" + "\n".join(errors[:20]))
    return metadata


def build_prompt(topic, route, identifier, schema):
    return ("Author an UNREVIEWED draft pedagogy module, not a claimed empirical result. "
            "Do not invent sources, effects, sample sizes, observations or learner outcomes. "
            "Diagnoses are hypotheses requiring discriminating probes. Several teaching moves may fit. "
            "Return only Markdown starting directly with closed YAML frontmatter. "
            "Use canonical source_ids already in the registry or provenance.citations with actual URLs and locators. "
            "Quantitative effects require typed estimate_ids. No automatic scientific verification is implied.\n"
            f"Requested title: {topic}\nCanonical id: {identifier}\nType: {route['type']}\n"
            f"Stage: {route['stage']}\nDomain: {route['domain']}\n"
            "Required instructional level-two headings, each with actual practice content:\n" +
            "\n".join(SECTIONS) + "\nMetadata contract:\n" + schema)
