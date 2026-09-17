---
schema_version: "2.0.0"
id: realtime-formative-adaptation-protocol
title: "CAP-04: Adjust instruction from observable learner evidence"
type: capability
capability_id: CAP-04
stage: [S1, S2, S3, S4, S5, S6, S7]
axes: [AX-05]
capabilities: [CAP-04]
context: [classroom, teacher-rehearsal]
evidence_grade: U
claim_status: unreviewed
review_status: unreviewed
provenance:
  kind: authored
  citations:
    - url: https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.03087/full
      locator: "Wisniewski, Zierer and Hattie (2020), Abstract and Discussion"
prerequisites: [practice-formative-hinge-questions, capability-learner-diagnostics]
leads_to: [instructional-coaching-observation-protocol, runtime-pedagogical-state-machine, case-kmofap-formative-assessment-wiliam]
source_ids: [evidence-wisniewski-2020-feedback]
---

# CAP-04: Adjust instruction from observable evidence

## Learning Contract
Select a next teaching move using the current response, an explanation and the task
context. Distinguish observations from hypotheses and test whether the next move helps.

## Intuitive Dilemma
Authored scenario: a learner gives the correct fraction comparison after a long pause.
The pause alone does not establish overload, guessing, expertise or motivation.

## Prediction Challenge
Before advancing the difficulty, record what explanation would distinguish a sound
comparison from a memorized rule. Decide how to collect that explanation without pressure.

## Mental Model
Correctness, reasoning and task familiarity are separate observations. Correctness on
one item does not establish mastery. Missing input is an explicit state, not an error diagnosis.

## Worked Example
The learner selects 1/5 over 1/8. Ask what the denominator represents, then request
a different comparison. If the explanation is unclear, model another example and retry.

## Non-Example
Do not convert response latency into a cognitive label. Advancing because a response
took less than 45 seconds, or withholding help because it took more, is unsupported here.

## Misconceptions
A distractor can suggest several hypotheses. A group percentage can help choose the
next classroom activity but does not validate each student's understanding or a cause of error.

## Diagnostic Question
"What tells you that this comparison is correct?" Retain more than one possible
interpretation when the explanation is incomplete; ask a discriminating follow-up.

## Practice and Transfer
Apply the decision table to a correct answer without reasoning, a wrong answer with
reasoning, and missing input. Then test the same decisions with a different topic.

## Implementation Protocol
This is a proposed decision table, not an executable diagnosis engine. Read rows in
order; the final row covers incomplete, inconsistent or unsupported input. Latency may
be recorded for usability analysis but is never used to infer a learner condition.

```yaml
algorithm: CAP04-OBSERVE-PROBE-ADAPT
status: authored-specification
selection: first-matching-row
rows:
  - when: response_not_available
    action: clarify_task_or_offer_accessible_response_mode
  - when: correct_and_reasoning_observed_and_checked
    action: request_independent_transfer_before_considering_fading
  - when: correct_but_reasoning_not_checked
    action: ask_for_explanation_or_another_representation
  - when: incorrect_with_candidate_misconception
    action: ask_discriminating_probe_then_choose_support
  - when: incorrect_without_candidate_misconception
    action: clarify_prerequisites_then_offer_worked_example_if_needed
  - when: otherwise
    action: retain_uncertainty_and_collect_missing_evidence
```

All valid timings, including exactly 45, 60 or 90 seconds, use the same table.
Preserve the selected hypothesis, move, learner response and next observation. Stop
or simplify when the learner asks to pause; do not treat distress as a necessary goal.

## Evidence and Boundaries
The linked feedback synthesis motivates considering information and context, not this
specific decision table or a fixed success threshold. This protocol remains unreviewed.
Software tests, teacher rehearsal completion and learning effectiveness are separate gates.
