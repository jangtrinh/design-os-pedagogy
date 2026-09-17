---
schema_version: "2.0.0"
id: eval-course-design-acceptance
type: eval
title: "Course design acceptance scenarios and review rubric"
stage: [S0, S1, S2, S3, S4, S5, S6, S7]
axes: [AX-04, AX-05, AX-06, AX-07]
capabilities: [CAP-01, CAP-02, CAP-04]
context: [course-design-review, authored-evaluation]
locale: en
evidence_grade: U
claim_status: unreviewed
review_status: unreviewed
provenance: {kind: authored}
prerequisites: [instructional-system-design-protocol, prompt-course-design-assistant]
source_ids: [evidence-cmu-course-alignment, evidence-cast-2024-udl-guidelines]
---

# Course design acceptance

These are authored acceptance scenarios and a manual review rubric. They are not executed benchmarks, validated psychometrics or evidence that generated courses improve learning.

## Review contract

For each scenario, save the input, actual course output, model/tool/version information when relevant, source IDs, reviewer identity, criterion decisions and reasons. Use pass, revise, not run or not applicable with justification. An aggregate score cannot override a missing subject source or an incorrect answer key.

| Scenario | Input variation | Required evidence in the output |
| --- | --- | --- |
| Age and proficiency | Same introductory topic for a primary learner and an adult novice | Separate intake, purposeful adaptations and suitable assessment; adult age does not imply prior mastery |
| Early childhood | Preschool fair-sharing play with caregiver facilitation | Observable play-based goal and adult observation; no fixed attention-span diagnosis or compulsory child-AI conversation |
| Caregiver setting | S0 request for a prenatal course | The caregiver is the learner; no claims of fetal curricular mastery |
| Accessibility | Learner uses screen reader or requests spoken responses | Accessible material plan and assessment conditions that preserve the target skill; required accommodations retained |
| Unfamiliar domain | Topic absent from the repository | Explicit content-source gap, bounded research and provisional status until load-bearing facts are checked |
| Limited resources | Printed materials, no internet, short sessions | Feasible activities and separate contact/independent/follow-up budgets; no assumed unavailable software |
| Assessment mismatch | Stated goal is independent performance; supplied quiz checks vocabulary | Mismatch identified and repaired with preparation and suitable evidence of performance |
| Conflicting sources | Two credible sources differ in recommendation or scope | Differences explained with locators; uncertainty retained; no selective omission or automatic vote counting |

## Criteria

| Criterion | Evidence required | Revise when |
| --- | --- | --- |
| Context | Goals, age, setting, prior knowledge, language, access and constraints are explicit | Assumptions masquerade as observations |
| Subject accuracy | Load-bearing content has readable sources; answers, quotations and units have been checked | A pedagogy source is used as authority for unrelated subject facts |
| Alignment | Each outcome maps to assessment criteria and preparation tasks | Assessed skills were not practiced, or an outcome has no evidence |
| Progression | Dependencies, entry diagnostics and supported alternatives are explicit | Prerequisites are cyclic, omitted, or inferred from age alone |
| Teaching usability | Examples, error analysis, practice, feedback, transfer and materials are sufficiently specified | The product is only a topic list or slide outline |
| Access and fairness | Available response routes and accommodations preserve the assessed construct | Support is removed solely to make assessment “unassisted” |
| Feasibility | Time sums, resources and facilitation are plausible and checked | Hidden homework or unavailable resources make the plan infeasible |
| Evidence honesty | Extraction, design review, expert review, pilot and effectiveness are separate | A passing software check or synthetic learner is presented as educational validation |

## Practice and calibration

Before reading a draft, predict its most likely failure from the brief. Inspect one complete outcome-assessment-practice chain, one worked answer and one source locator; then inspect the remaining chains. For a vocabulary quiz attached to a repair-performance outcome, classify alignment as revise and specify the missing performance evidence. Do not discard a useful vocabulary prerequisite check.

Two reviewers can independently classify a sample and discuss disagreements using the saved artifacts. Record agreement only when actually measured. A reviewer may mark a topic not assessable without subject expertise; that is a pending review, not a fabricated pass.

## Boundary

Design acceptance supports a decision to prepare a supervised pilot. Learning claims require real, appropriate evidence about learner performance and transfer. The existing fraction rehearsal and its software tests do not execute this evaluation set.
