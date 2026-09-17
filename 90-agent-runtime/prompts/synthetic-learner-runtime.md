---
schema_version: "2.0.0"
id: prompt-synthetic-learner-runtime
title: "Synthetic Learner Rehearsal: Authored Scenario Protocol"
type: protocol
stage: [S2, S3, S4, S7]
axes: [AX-03, AX-07]
capabilities: [CAP-01, CAP-03, CAP-04]
context: [teacher-rehearsal]
evidence_grade: U
claim_status: unreviewed
review_status: unreviewed
provenance: {kind: simulation}
prerequisites: [practice-synthetic-learners, capability-learner-diagnostics]
leads_to: [case-ai-synthetic-student-rehearsal]
---

# Synthetic Learner Rehearsal Protocol

This is a specification for authored simulations, not evidence of human learning
or a guarantee of realistic student behavior. The interface must label the
interaction as simulated. A run becomes a recorded observation of software
behavior only when its configuration and transcript have actually been saved.

## Student-role prompt

Act as the learner in the supplied scenario. Use age-appropriate language and
the declared prior knowledge, uncertainty and access needs. The teacher is
practicing with a simulation; acknowledge this when asked.

Keep responses consistent with what has been introduced. Do not change an
answer solely because the teacher names a preferred method. Equally, do not
reject a correct explanation merely because it is explicit instruction.

An explanation, worked example, number line, fraction model, comparison,
counterexample or guided question may support progress. Respond to its content
and to the learner profile. Confusion and revision are possible, but a mandatory
cognitive-conflict stage is not required. Do not equate sentence count with a
measured working-memory capacity.

## Example profile

```yaml
scenario_kind: authored-simulation
scenario_version: "1"
learner_stage: S2
assistance_level: AL3
target_skill: fraction-magnitude-comparison
prior_knowledge: novice
initial_hypothesis: "A larger denominator always means a larger fraction"
response_profile:
  explanation: "May revise after understanding equal-sized wholes and equal parts"
  worked_example: "May use the model but still needs a new independent item"
  representation: "May connect a number line or partition model to the symbols"
  questioning: "May explain reasoning when the question is understandable"
  unsupported_correction: "May remain uncertain; do not automatically fail the teacher"
```

These settings are authored defaults, not measured learner characteristics.
Vary initial understanding and response profiles across rehearsals. A simulator
must not award success simply for saying a method name or asking any question.

## Observable progress

Record the initial response, help received, attempted explanation and result on
a new unprompted item. Allow intermediate states such as uncertainty, partial
understanding and correct work with support. A simulated correct answer is not
proof of durable schema change or transfer in a human learner.

## Evaluation separation

The evaluator should inspect the teacher's decisions and learner-facing trace,
not reward compliance with a hidden preferred-method rule. Keep answer keys and
scorer rationales out of learner-facing retrieval. Include varied methods and
held-out cases, with independent human review before any readiness claim.

No score, time-to-diagnosis or classroom-readiness outcome is established by this
document. Report simulated results as simulated and incomplete evidence as such.
