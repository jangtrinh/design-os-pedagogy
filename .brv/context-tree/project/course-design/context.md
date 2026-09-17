---
title: "Agent Teacher course-design knowledge handoff"
summary: "Course-authoring foundation, verified inventory, evidence boundaries, continuation priorities and native delivery context."
tags: [agent-teacher, knowledge-base, course-design, assessment, provenance, roadmap]
keywords: [S0-S7, AL0-AL7, CAP-02, knowledge_coverage, rehearsal, source-checked]
related: []
createdAt: "2026-09-17"
updatedAt: "2026-09-17"
---

# Course-design knowledge handoff

## Goal and entry points

Help an assistant design a course for a specified age group, topic and context using reusable pedagogy, separately verified subject content and explicit review. The goal is broader than the existing fraction rehearsal.

Paths below are relative to the project root:

| Purpose | Path |
| --- | --- |
| Current product scope | `README.md` |
| Coverage gaps and ordered acceptance gates | `docs/knowledge-roadmap.md` |
| Learner intake, subject sources, alignment and unit design | `70-capabilities/design/instructional-system-design-protocol.md` |
| Assistant handoff | `90-agent-runtime/prompts/course-design-assistant.md` |
| Editable course contract | `docs/templates/course-blueprint.yaml` |
| Bounded knowledge research | `90-agent-runtime/workflows/knowledge-research-cycle.md` |
| Manual acceptance scenarios | `90-agent-runtime/evals/course-design-acceptance.md` |
| Audit and source/test evidence | `plans/20260917-knowledge-course-design/` |

Course workflow: learner goals, age, setting, proficiency, language, access and time; then subject-source map, prerequisites, outcome-assessment-practice alignment, usable units with checked answers, expert/access review, and appropriate learner evaluation.

## Verified snapshot from the completed knowledge run

`plans/20260917-knowledge-course-design/validation.json` records 78 passing tests, 94 knowledge records, 346 resolved references and zero registry errors. Coverage records 10 source records, 8 source-checked records across types, 86 unreviewed records, 62 legacy warnings, 7 unclassified records and no records marked reviewed. These are a dated inventory, not permanent expectations or a readiness percentage.

Five institutional source cards were added for CMU, NAEYC, CAST, UNESCO and IES. Each records reading scope and limitations. The IES extraction covers its official HTML summary, not the downloadable guide or underlying studies. Seven existing knowledge documents were repaired with canonical IDs preserved. Do not infer appraisal of the wider corpus from those corrections.

The application implements three authored Vietnamese fraction rehearsal cases, SQLite session persistence, replay and export. Feedback follows authored branches; free text is not semantically graded. The course blueprint is an authoring template, not an executable schema. The eight acceptance scenarios are authored review specifications, not passed model evaluations.

## Durable lesson

Keep structural validity, source connectivity and software success separate from subject accuracy, source appraisal, independent competence and learning effectiveness. Preserve the same distinction in metadata, retrieval, teaching claims and reports. Educational stage or role (S0-S7), actual age, subject proficiency and AI assistance (AL0-AL7) are separate attributes; S0 addresses caregiver learning and S7 educator development.

## Continuation priorities

First appraise consequential legacy claims and primary quotations and give the seven unclassified records justified types. Then implement a separate executable course schema with checks for missing outcomes, orphan assessments, duplicate IDs, prerequisite cycles and time-budget conflicts. Build complete representative domain packs and record actual course-generation/review results before expanding retrieval infrastructure. Subject experts, accessibility review and appropriate learner evidence remain separate acceptance gates.

Keep unknown-topic behavior explicit: obtain a bounded subject foundation or produce a provisional outline with unresolved dependencies. Do not generate generic pages simply to increase coverage counts.

## Local verification and preservation

Run from the complete Agent Teacher checkout:

```sh
.venv/bin/python -B tools/knowledge_coverage.py
.venv/bin/python -B tools/knowledge_coverage.py --stage S6 --axis AX-04 --capability CAP-02 --json
.venv/bin/python -B tools/knowledge_registry.py
.venv/bin/python -B tools/verify_links.py
.venv/bin/python -B -m unittest discover -s tests -v
git diff --check
```

Coverage is read-only and follows typed evidence links, not navigation or prerequisite proximity. Tag filters intersect metadata; inspect untagged material and bodies too. Verify physical cwd, host and Git root against `docs/local-workspace.md` before mutations. Preserve unrelated work, canonical IDs, session data, earlier evidence and local backups. Machine-local BRV config/cache, environments, session databases and generated source archives do not belong in commits.

The previous final supplementary documentation check was blocked and produced no file; the earlier successful validation remains scoped to its hashes. The commit/merge task must record its own results instead of retroactively inventing that missing check. Worker startup failed in the knowledge run; no independent worker review, expert appraisal or learner pilot was performed.

The subsequent commit-gate run passed all 78 tests and the current registry, link and syntax checks. Source commit `c2769bfcde8e0a1a53916c287b44c26429441f41` records the integrated implementation. See `plans/20260917-knowledge-course-design/commit-validation.md` for the observed checks and `git log` for the actual merge result. Source review status and learner-effectiveness limitations remain unchanged.

## Context storage provenance

The user requested saving context to BRV and committing/merging the project. ByteRover 2.1.3 initialized this project's local tree. Its `curate` command reported an HTTP 401 error (task `4126d336-b2b7-46e7-92cf-50f0d78c6ee0`), despite process exit code 0. This Markdown handoff was therefore written directly into the local context tree. It is not a successful remote curation or cloud-sync result. Read the actual Git log and task evidence for subsequent commit/merge outcomes; intent alone is not completion.
