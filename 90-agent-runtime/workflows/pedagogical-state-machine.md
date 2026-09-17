---
schema_version: "2.0.0"
id: runtime-pedagogical-state-machine
title: "Pedagogical Control Loop: Specification and Validation Boundaries"
type: protocol
stage: [S2, S3, S4, S5, S6, S7]
axes: [AX-03, AX-07]
capabilities: [CAP-01, CAP-03, CAP-04]
context: [tutoring, teacher-rehearsal]
evidence_grade: U
claim_status: unreviewed
review_status: unreviewed
provenance: {kind: authored}
implementation_status: specification
prerequisites: [practice-ai-assistance-ladder, capability-learner-diagnostics]
leads_to: [eval-adaptive-oral-defense-viva]
---

# Pedagogical Control Loop

This document specifies intended behavior. It is not an implemented autonomous
engine, an executed benchmark or a clinical validation report. No answer-leak
rejection rate or delayed-transfer effect has been demonstrated here.

## Inputs and independent dimensions

Record the learning goal, context, prior-knowledge evidence, access needs and
learner response. Stage S0–S7 describes an educational setting or role. Assistance
AL0–AL7 describes help provided. Neither is a measure of domain competence.
Response latency is an observation to interpret with context, not an intelligence
measure or a reliable diagnosis by itself.

## States

1. **Observe:** capture the response and the evidence actually available.
2. **Form hypotheses:** distinguish possible slips, procedural gaps and
   misconceptions. Ask a discriminating probe when evidence is insufficient.
3. **Choose support:** select an explanation, worked example, representation,
   comparison or question consistent with the task and learner needs.
4. **Check the proposed turn:** ensure that it respects the active assistance
   policy, access needs and the boundary of the currently assessed task.
5. **Present the turn:** keep the learner's next action clear.
6. **Evaluate new evidence:** record reasoning, help used and performance on a
   new independent item. Adapt support; do not declare mastery from one answer.

## Assistance policy examples

```yaml
assistance_policies:
  AL0:
    purpose: independent-check
    actions: [present-item, collect-response]
    rule: "No content hints during the attempt; preserve agreed access accommodations"
  AL2:
    purpose: diagnostic-clue
    actions: [ask-probe, highlight-relevant-feature]
  AL3:
    purpose: partial-scaffold
    actions: [supply-subgoal, show-partial-structure]
    rule: "Leave meaningful work for the learner"
  AL4:
    purpose: contrasting-examples
    actions: [show-completed-example, compare-representations]
    rule: "Use separate examples; do not expose the answer to the assessed item"
```

These are authored policy examples. Any enforcement mechanism needs defined
answer boundaries, tests of false positives and false negatives, and an explicit
fallback when uncertain. A prompt, regular expression or semantic check cannot
be described as a guaranteed prevention mechanism without supporting evidence.

## Outcomes and reporting

Store observed attempts, assistance levels, explanations and independent-check
results. Do not manufacture calibrated mastery probabilities or epistemic-debt
points from this specification. Label simulation runs, preserve actual run IDs
only when they exist, and distinguish software-policy checks from human learning.
Independent and delayed transfer require separate observations. The former
78%, 100% and d = 0.64 benchmark claims had no attached study or run record and
have been withdrawn; they are not estimates available for runtime decisions.
