---
schema_version: "2.0.0"
id: practice-ai-assistance-ladder
title: "AI Assistance Ladder AL0–AL7: Support and Independent Competence"
type: practice
stage: [S2, S3, S4, S5, S6, S7]
axes: [AX-03, AX-07]
capabilities: [CAP-02, CAP-03, CAP-04]
context: [tutoring, teacher-rehearsal]
evidence_grade: U
claim_status: unreviewed
review_status: unreviewed
provenance: {kind: authored}
prerequisites: [practice-ai-epistemic-partner, concept-cognitive-load-theory]
leads_to: [capability-learner-diagnostics, runtime-pedagogical-state-machine]
source_ids: [evidence-bastani-2025-ai-guardrails]
---

# AI Assistance Ladder AL0–AL7

This is an authored design framework. It distinguishes the help provided from
independent competence; it is not a validated scale or an empirical effect-size
ladder. Stage S0–S7 remains reserved for educational setting or role.

| Level | Form of assistance | Learner action to preserve |
| :--- | :--- | :--- |
| AL0 | Independent attempt without tutoring hints | Produce and explain an answer independently |
| AL1 | Metacognitive prompt | State a goal, uncertainty or strategy |
| AL2 | Diagnostic clue or targeted question | Continue reasoning and explain the relevant relation |
| AL3 | Partial scaffold or subgoal structure | Complete meaningful remaining work |
| AL4 | Contrasting worked examples or representations | Compare, explain and apply to a separate item |
| AL5 | Candidate draft or solution for critique | Identify limitations, correct errors and defend revisions |
| AL6 | Collaborative inquiry | Direct choices and explain contributions |
| AL7 | Delegated task completion | Independently verify the result where competence is claimed |

AL7 output is not evidence that a learner has acquired the target skill. Choose
the help level using the task, prior knowledge, current response and access
needs. More help is not inherently failure, and less help is not inherently
learning. Worked examples and clear explanations can be appropriate support.

## Authored example

A learner repeatedly fails a fraction comparison and cannot explain the meaning
of the denominator. Use a partition model, worked example or understandable
question, then ask for an explanation and a different independent comparison.
Record the assistance provided and the new evidence. A correct supported answer
does not establish unassisted mastery; a slow answer does not prove incapacity.

## Assistance record

```yaml
learner_stage: S2
target_skill: fraction-magnitude-comparison
assistance_level: AL3
prior_knowledge_status: uncertain
independent_check_status: not-yet-observed
```

Do not assign an empirically calibrated epistemic-debt score without a defined,
validated measurement model. Use direct records of help and independent
performance instead. Checkpoint frequency is a design decision that needs
evaluation in context, not a universal every-three-sessions or every-five-items
scientific rule.

## Evidence boundary

The linked Bastani source distinguishes assisted task performance from subsequent
independent performance in one study. It does not validate these eight levels,
their ordering, a fixed fading threshold or a particular debt formula. The
previous unnamed synthesis and numerical claims about this ladder have been
removed pending identifiable sources and methodological review.
