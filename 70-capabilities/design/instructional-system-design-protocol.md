---
schema_version: "2.0.0"
id: instructional-system-design-protocol
title: "Course and unit design: learner context, alignment, practice and review"
type: capability
category: design
capability_id: "CAP-02"
stage: [S0, S1, S2, S3, S4, S5, S6, S7]
axes: [AX-03, AX-04, AX-05, AX-06]
capabilities: [CAP-01, CAP-02, CAP-04]
context: [course-design, unit-design, caregiver-education, adult-learning]
locale: en
evidence_grade: U
claim_status: unreviewed
review_status: unreviewed
provenance: {kind: authored}
prerequisites: [practice-backward-design-ubd, concept-cognitive-load-theory]
leads_to: ["socratic-and-explicit-facilitation-protocol", "realtime-formative-adaptation-protocol", "pedagogical-state-machine"]
source_ids: [evidence-cmu-course-alignment, evidence-naeyc-developmentally-appropriate-practice, evidence-cast-2024-udl-guidelines, evidence-unesco-2015-adult-learning, evidence-ies-2007-organizing-instruction]
---

# Course and unit design

This is an authored planning protocol. It produces a reviewable course proposal. It is not an implemented course generator, accreditation standard or demonstration of learning gains. Use the [course blueprint](../../docs/templates/course-blueprint.yaml) and [assistant prompt](../../90-agent-runtime/prompts/course-design-assistant.md).

## 0. Capability contract and prediction

The designer can identify missing learner and subject information, map outcomes to assessment and preparation, justify sequence and support, and identify what remains unverified.

**Puzzle:** Two beginners want to learn the same topic. One is ten, the other sixty. Is changing the reading level of a single syllabus sufficient? Predict three other decisions that could change before reading the intake table.

Possible differences include purpose, prior knowledge, available time, context, language and access needs. Age alone does not establish any of these. The same adult may be advanced in one domain and a novice in another.

## 1. Intake and scope

| Input | Record explicitly | Decision it informs |
| --- | --- | --- |
| Goal | A task the learner wants to perform; purpose and exclusions | Course scope and final evidence |
| Learner | Actual age range, educational setting/role, relevant experience and diagnostic evidence | Suitable content, examples and support |
| Context | Language, locale, curriculum jurisdiction, group size, delivery mode | Topic standards, participation and assessment |
| Constraints | Contact time, independent work, devices/materials, bandwidth, facilitator availability | Feasible sequence and resources |
| Access | Requested accommodations, communication and sensory/motor access needs | Participation options that preserve the intended skill |
| Knowledge gaps | Known facts, explicit assumptions, unresolved questions | Whether to draft, research, narrow scope or obtain expert review |

Use S0-S7 for setting/role, AL0-AL7 for AI assistance, and separate fields for age and proficiency. S0 planning addresses caregiver learning, not assessed prenatal learners. S7 addresses educator development. Neither is an age-based step after the other stages. A university qualification is not a prerequisite for adult education.

Proceed with labelled assumptions for reversible planning choices. Ask only for missing information that materially changes the course; never fabricate learner observations, a diagnosis, local curriculum requirements or access to equipment.

## 2. Build the subject foundation before writing the syllabus

Create a topic map with prerequisite skills, important representations, likely errors, domain standards and evidence of competent performance. Read the actual relevant sources and record the edition, section/page and applicability. Pedagogical knowledge does not establish the accuracy of medicine, history, engineering or any other subject content.

For an unfamiliar topic, use the [research cycle](../../90-agent-runtime/workflows/knowledge-research-cycle.md). Deliver an outline with unresolved content dependencies when necessary; do not silently convert an empty search into invented expertise. Independently check worked answers, quotations, units, diagrams and practical procedures. Domain-sensitive activities need appropriate supervision and review before learner use.

## 3. Align outcomes, assessment and practice

Write each outcome as a performance under stated conditions with an observable success criterion. Assign stable local IDs such as O1, A1 and P1. Every outcome must have assessment evidence and preparation; every assessed criterion must correspond to an outcome that learners had an opportunity to practice.

Select the format from the construct: recognition, explanation, calculation, performance, critique or creation. Multiple-choice items can be suitable for some goals; a project is not automatically superior. Distinguish individual competence from the quality of a group artifact.

Include answer keys or performance exemplars, criteria, plausible alternative explanations for errors, and a follow-up probe. Allow an insufficient-evidence judgment. Independent assessment can retain access accommodations while limiting assistance that supplies the skill being assessed.

## 4. Sequence, practice and adaptation

Order units by actual skill dependencies. Check for cycles and unmet prerequisites. A diagnostic may justify a shorter path, additional preparation or a different support level; one answer does not certify broad mastery.

For each unit provide a worked example, an error/non-example, guided practice, an independent attempt, feedback and a transfer task. Explain which parts are suitable for this cohort. Young-child activities may use caregiver observation and physical play; expert seminars may use competing interpretations and critique. Do not force every goal into the same lesson pattern.

Plan revisits and a delayed check where useful, stating the proposed interval and practical rationale. Budget contact time, breaks, assessment, independent work and follow-up separately. Check their sums. No fixed number of cognitive chunks, lesson-minute cutoff or universal spacing interval is used as an acceptance rule.

## 5. Worked design example

**Authored example, not classroom data:** An adult beginner wants to compare fractions of the same whole. Proposed duration: one 30-minute session plus a five-minute revisit the following week. Confirm fraction notation and equal partitioning first.

| Outcome | Assessment and key | Preparation and reasoning |
| --- | --- | --- |
| O1: Compare fractions of an equal whole and justify the result | A1: Compare 3/4 and 2/3. Key: 3/4 is greater because 9/12 exceeds 8/12, or an equivalent valid model | P1: Demonstrate equal-size fraction strips, then compare 1/2 with 2/3 together. Keeping the whole constant makes the comparison interpretable |
| O2: Identify when whole sizes are needed to compare actual quantities | A2: Is half of one cake more food than three quarters of another? Key: cake sizes are needed | P2: Contrast equal-size and unequal-size drawings. This tests the boundary of O1 |

Time proposal: intake 3 + demonstration 6 + guided work 8 + independent work 5 + feedback 4 + exit check 4 = 30 minutes. The later five-minute revisit is additional. Recheck with 3/5 versus 2/3; the latter is greater because 10/15 exceeds 9/15. These keys are arithmetic, not measurements of learning effectiveness.

For an S2 learner, retain the mathematical criterion when appropriate but adapt language, examples and facilitation from the actual profile. For a preschool child, fair-sharing play may require a different outcome and observational evidence; shortening this adult lesson is insufficient.

## 6. Diagnostic decision and practice

**Commit before reading the key:** A course promises that learners will repair a process independently. Which assessment best matches this outcome?

A. Name its components. B. Repair a new fault and explain the checks performed. C. Watch an expert repair it. D. Submit an attractive poster about it.

**Key: B**, subject to a verified, appropriately supervised task and rubric. A may substitute vocabulary for performance; probe whether the learner can execute the steps. C may confuse exposure with independent capability; request an independent attempt. D may prioritize presentation; ask which repair criteria the artifact actually demonstrates. A choice alone does not diagnose a learner's reasoning.

**Guided practice:** Replace A in a draft course with an aligned assessment, retaining any vocabulary check as a prerequisite probe. **Independent practice:** Design a one-unit blueprint in another domain and identify one content claim needing a source. **Transfer:** Adapt it for a different age/setting and explain which outcome, assessment or support changes and which stays constant.

## 7. Review and delivery

Deliver the completed brief, subject-source map, dependency sequence, alignment table, unit materials, assessment keys/rubrics, accessibility decisions, time/resource budget and unresolved issues. Use the [acceptance scenarios](../../90-agent-runtime/evals/course-design-acceptance.md) for a documented design review. Record a reviewer's identity and actual findings; a synthetic walkthrough is not a learner pilot.

The [CMU alignment note](../../60-evidence/sources/evidence-cmu-course-alignment.md) supports the alignment principle. [NAEYC](../../60-evidence/sources/evidence-naeyc-developmentally-appropriate-practice.md), [CAST](../../60-evidence/sources/evidence-cast-2024-udl-guidelines.md) and [UNESCO](../../60-evidence/sources/evidence-unesco-2015-adult-learning.md) inform context and access decisions. The [IES summary](../../60-evidence/sources/evidence-ies-2007-organizing-instruction.md) informs practice planning within its stated reading limits. The combined workflow and example remain authored and unreviewed; no effectiveness estimate is assigned.
