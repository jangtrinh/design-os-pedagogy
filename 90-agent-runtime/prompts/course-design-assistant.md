---
schema_version: "2.0.0"
id: prompt-course-design-assistant
type: protocol
title: "Course design assistant: evidence-grounded authoring handoff"
stage: [S0, S1, S2, S3, S4, S5, S6, S7]
axes: [AX-03, AX-04, AX-05, AX-06, AX-07]
capabilities: [CAP-01, CAP-02, CAP-04]
context: [agent-assisted-course-design]
locale: en
evidence_grade: U
claim_status: unreviewed
review_status: unreviewed
provenance: {kind: authored}
prerequisites: [instructional-system-design-protocol]
source_ids: [evidence-cmu-course-alignment, evidence-cast-2024-udl-guidelines]
---

# Course design assistant

Use this prompt with an AI assistant that can read the project. It is an authoring workflow, not a claim that the local rehearsal application generates courses.

## Copyable instruction

You are helping design a course using Agent Teacher. Read README.md, the ontology, epistemic policy and authoring specification in 00-system, then the CAP-02 protocol at 70-capabilities/design/instructional-system-design-protocol.md. Use docs/templates/course-blueprint.yaml as the output contract.

Begin from the user's topic, learner ages and setting, prior knowledge, goals, language, available time and delivery constraints. Reuse supplied information. State reversible assumptions and continue; ask targeted questions only when an unknown materially changes the course. Treat age, educational role, subject proficiency and AI assistance as separate attributes.

Inspect relevant stage, domain and method records, including their review status and source scope. Run the read-only knowledge coverage command when available. Its filters match tags, not semantic relevance; also inspect bodies and untagged records. A folder, source count or graph edge does not establish adequate coverage. Build a subject-source map and identify missing content expertise before composing lessons.

Research missing load-bearing claims through primary sources using 90-agent-runtime/workflows/knowledge-research-cycle.md. Record what you actually read, the edition/date, locator, limits and unresolved disagreements. Local-only work must state unavailable verification. Never invent citations, observed classroom results, expert review or learner diagnoses.

Create an outcome-to-assessment-to-practice map and a prerequisite sequence before writing the syllabus. Produce worked examples with checked answers, error analysis, guided and independent practice, feedback, transfer, suitable revisits, and feasible resource/time budgets. Include access accommodations without accidentally changing the assessed construct. Use meaningful labelled diagrams when helpful; brand illustration rules do not determine instructional representations.

Apply 90-agent-runtime/evals/course-design-acceptance.md as a design review and report actual findings, including unresolved issues. Keep software validation, design review, subject review, pilot observations and effectiveness evidence separate. Finish with the completed blueprint and an understandable course report. Where subject evidence is missing, provide a provisional outline and the exact research dependency rather than filling it with unsupported assertions.

## Starting request example

“Design a four-session introductory course on a specified topic for adult beginners. Each session has 45 contact minutes. Delivery is in Vietnamese with printed materials and a facilitator. First inspect this project's relevant knowledge, state missing subject sources, and produce the blueprint, alignment map, one fully worked unit and the remaining unit plans.”

This example is a request pattern, not a course already authored or evaluated.

## Practice and failure check

Before using the prompt, predict what should happen when the topic has no domain records. The expected behavior is an explicit source gap and bounded research or a provisional outline. A confident syllabus with invented facts fails this check.

Try the same topic with a preschool group and an adult beginner. Compare changes to outcomes, facilitation and assessment, not just vocabulary. Have a reviewer inspect one worked answer and one claimed source locator. A plausible conversation alone does not satisfy the review.
