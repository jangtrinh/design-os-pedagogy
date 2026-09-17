---
schema_version: "2.0.0"
id: protocol-knowledge-research-cycle
type: protocol
title: "Knowledge research cycle: question, extraction, appraisal and revision"
stage: [S0, S1, S2, S3, S4, S5, S6, S7]
axes: [AX-04, AX-05, AX-07, AX-08]
capabilities: [CAP-02, CAP-06]
context: [knowledge-maintenance, course-research]
locale: en
evidence_grade: U
claim_status: unreviewed
review_status: unreviewed
provenance: {kind: authored}
---

# Knowledge research cycle

This protocol is executed by a user-invoked agent with appropriate tools. It does not install a scheduler, autonomous crawler or publication service. Each run has a bounded question and a saved research record.

## Contract and decision puzzle

The researcher can trace a consequential claim to a source passage, distinguish extraction from appraisal, record contradictory or missing evidence, and improve an operational teaching document without overstating what is known.

**Predict:** A university page recommends a method. Is that enough to assign Grade A, attach a large effect size and recommend it for every age? No. The institution, recommendation, empirical claim and applicable population are separate pieces of evidence.

## Run sequence

1. **Select the gap.** Inspect coverage and the course request. Prioritize unsupported claims in active entry points, missing prerequisite/topic knowledge, and decisions affecting assessment or accessibility. Record the exact question, population, context and intended use. Avoid adding documents merely to increase a count.
2. **Search existing knowledge.** Resolve canonical IDs and aliases, inspect bodies and source trails, and check for duplicate studies or a source already represented. Metadata searches are not sufficient for untagged legacy material.
3. **Search primary material.** Prefer the original study, official standard/framework or publisher/author text. Record queries, date, selected sources and rejected candidates with reasons. Include plausible null or conflicting evidence; several summaries of one study are not independent replications.
4. **Read and extract.** Record URL/local locator, title, edition/revision, publication date when visible, access date, exact section/page and reading scope. Distinguish full text, official abstract and secondary summary. Inspect tables/figures when a claim depends on them. A search snippet or inaccessible PDF is not a full-text reading.
5. **Appraise the claim.** Identify population, comparator, outcome, timing, design, limitations and applicability. For quantitative results, use separate source, claim and estimate records with the required metric and locator. Do not convert incomparable metrics into a ranking or months-of-progress promise. Document why evidence supports a claim, not merely where it was found.
6. **Author the teaching implication.** Mark your adaptation as authored. Add target context, preconditions, worked example, an error/non-example, a diagnostic follow-up, practice, feedback, transfer and a usable protocol. Distinguish the source's recommendation from the local design decision.
7. **Validate and review.** Validate metadata, references and local links. Check content accuracy and pedagogical anatomy separately. Keep new generated practice records unreviewed. Source-checked records need a real extraction identity/date/locator; independent expert review must identify the actual reviewer and artifact.
8. **Record the result.** Save changed IDs, hashes or diff, accepted/rejected sources, unresolved claims and checks. Use the existing draft/import/apply process for new generated modules; applying a draft is separate from scientific approval. Preserve evidence and earlier revisions when correcting a claim.

## Research record

For each run save: question; why it matters; search date and queries; existing IDs inspected; candidate URLs; accepted/rejected rationale; scope actually read; extracted statements and locators; counterevidence; methodological/applicability limits; authored implications; changed paths; validation results; pending human review.

Prefer a source's stable version or DOI when available. Recheck a source when its edition changes, a material contradiction appears, or a new course relies on it outside the previously checked context. Choose maintenance frequency from volatility and usage; a classic theory and a changing technical specification need different treatment.

## Worked example and non-example

**Authored scenario:** A legacy guide assigns a universal effect size to curriculum alignment. Read the official teaching-center guidance and inspect whether it actually reports a controlled comparison. When it does not, retain the alignment recommendation with a framework source and remove the unsupported numerical claim. Record that this correction does not prove alignment ineffective or establish a replacement effect.

**Non-example:** Repeating the number from several blogs, citing a university homepage and marking the practice reviewed. More links do not repair the missing comparison and locator.

## Diagnostic and practice

Choose the justified result after reading only an official abstract: A. Full methodological appraisal. B. Checked extraction of what the abstract states, with full-text limits. C. Automatic Grade A. D. Proof that the same result holds for all ages.

**Key: B.** A confuses reading scope with appraisal; request methods and limitations. C confuses authority with quality; request design-specific evidence. D overgeneralizes; request population and context correspondence. Ask for reasoning before treating a choice as a diagnosis.

Practice with one claim in the active course: record its exact support and one applicability limit. Transfer to a source that is inaccessible or conflicts with the first; preserve an unresolved state and explain the decision it prevents. Successful completion means a traceable research record, not a predetermined positive result.

## Boundaries

This is a repository maintenance procedure derived from the [epistemic policy](../../00-system/epistemic-policy.md). It is not an empirical intervention. No new permissions, paid calls, external publication or learner-data collection follow from the protocol itself.
