# Implementation status

## Executed course exercise, 17 September 2026

The [Vietnamese Grade 1 mathematics course](../courses/vi-vn-grade-1-math/README.md) now provides an actual 35-week/105-period authoring fixture, an independent 24-requirement map, per-period tasks/keys, eight detailed teaching examples and two sample assessments. The bounded audit recomputed 111 declared keys and identified 14 observational tasks for separate review. Twenty new tests plus the existing suite passed: 98 total. The registry contains 98 records and 350 resolved references, with no errors and 62 retained legacy warnings.

The [evaluation](../courses/vi-vn-grade-1-math/workflow-evaluation.md) separates these checks from subject/teacher review, textbook-page alignment, classroom timing and learner effectiveness, which remain unverified. The [course audit documentation](course-audit.md) records the executable scope and limitations. The older implementation snapshots below retain their original dates and counts.

Updated 17 September 2026. Current knowledge plan: [course-design foundation](../plans/20260917-knowledge-course-design/plan.md). The publication/rehearsal implementation record from 16 September is retained below.

## Knowledge update, 17 September 2026

The latest [completion report](../plans/20260917-knowledge-course-design/completion.md) records 78 passing software tests, 94 knowledge records, 346 resolved references and zero registry errors. Five source cards and three course/research records were added; seven existing records were repaired with original IDs retained. There are still 62 legacy records, seven unclassified records and no records marked independently reviewed.

The [course-design prompt](../90-agent-runtime/prompts/course-design-assistant.md), [blueprint](templates/course-blueprint.yaml), [coverage command](../tools/knowledge_coverage.py) and [knowledge roadmap](knowledge-roadmap.md) are available. Course acceptance scenarios are authored review specifications. No general course runtime, cross-model benchmark, expert appraisal or learner pilot was completed in this update.

## Prior implementation scope

The project contains a local Vietnamese rehearsal with three authored cases, a versioned registry, draft validation and explicit publication. Interrupted publication now records intent and exposes inspection/recovery. Acceptance depends on actual outputs, not source presence.

The original restart test uses a queue with an eight-second timeout. It differs from the select/readline helper audited in the partial folder view. That older defect must not be attributed to this checkout without matching evidence.

## Evidence

| Artifact under plans/20260916-reaudit-implementation | Scope |
| --- | --- |
| source-before.json | 182-file SHA-256 inventory before source edits; excludes session data/generated artifacts |
| baseline-tests.json | New native run: 52 tests passed before source edits |
| publication-existing-tests.json | 13 existing publication tests passed after journal/recovery implementation |
| consolidation-checks-r01.json | 67 tests passed; three operational path notices were still classified as errors |
| consolidation-checks-r02.json | One of 69 tests failed, exposing suppressed file-scheme links |
| link-parser-checks.json | All 11 provider/link tests passed after the parser correction |
| consolidation-checks-r03.json | Final suite and source hashes when produced; require all_passed=true |

Baseline: e4b14823c4532e121a1a889a5366beea53bc28a5. Changes are uncommitted; the source manifest, not the baseline alone, identifies tested code. No commit, push, deployment, external model call or real-user pilot is part of this change.

## Remaining gates

Legacy source appraisal, independent implementation review, named expert review and a real-user pilot remain pending unless separate artifacts record completion. AI-assisted arithmetic appraisal and review forms are in docs/fraction-pilot.md.

The consolidation review read publication, journal, recovery, filesystem transactions, registry, schema, the actual fraction pack and UI modules. A blocking FIFO import was reproduced using an isolated corpus and corrected with the existing bounded regular-file reader. Two import regression tests were added. Machine paths in operational prose remain visible as portability warnings; proposed modules still fail on those paths. Unsupported URL schemes are now extracted for audit instead of being silently hidden by renderer-oriented parsing.

This review was performed by the implementing assistant. Worker dispatch was unavailable, so no independent worker review is claimed. The fraction pack was preserved after checking the arithmetic and transfer keys; weak distractors still limit its use as an assessment. Historical browser results are retained, but new visual/browser acceptance is not implied by command-line tests.

See [Local workspace](local-workspace.md) and [Local delivery](local-delivery.md) for the machine, source bundle and evidence boundaries.

Pack migration, historical-pack replay, multiple accounts and changes to the latest-100 session listing are not introduced. Expansion remains conditional on pilot evidence.

## Changelog

16 September 2026: added journaled inspection and explicit recovery; retained canonical IDs, stages and session compatibility; documented CLI/API and review/pilot gates. Later tool failures do not invalidate earlier successful changes or tests.

16 September 2026, consolidation: bounded CLI imports reject special and linked files before draft creation. Link audits separate operational portability notices, retain draft restrictions and report unsupported schemes. Existing working-tree changes, corpus IDs, pack bytes and user session data are preserved.

17 September 2026: added source-traceable course-authoring guidance, research/acceptance protocols and read-only coverage reporting. Source checking remains distinct from appraisal. The implementing assistant performed verification; attempted worker conversations failed to start, so no independent worker review is claimed.
