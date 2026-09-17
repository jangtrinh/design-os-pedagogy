# Agent Teacher knowledge and course-design audit

Completed 17 September 2026 in the verified native project. The work includes a full registry/software baseline, a focused content audit of course-design entry points, targeted primary-source research, knowledge repairs, reusable authoring artifacts and a prioritized roadmap. It is not a claim that every statement in the corpus has been appraised.

## Verified before and after

| Measure | Before | After |
| --- | ---: | ---: |
| Passing software tests | 70 | 78 |
| Knowledge records | 86 | 94 |
| Resolved references | 326 | 346 |
| Source records | 5 | 10 |
| Source-checked records, all types | 3 | 8 |
| Unreviewed records | 83 | 86 |
| Legacy records/warnings | 69 | 62 |
| Registry errors | 0 | 0 |
| Unclassified records | 7 | 7 |
| Records marked reviewed | 0 | 0 |

Unreviewed records increased because three authored operational records were added. Seven migrated records remain unreviewed. Source checking is an extraction status; it is not independent methodological appraisal.

## What changed

Five source cards document official guidance from CMU, NAEYC, CAST, UNESCO and IES/WWC. The cards include exact URLs, locators, revision/access information and reading limits. The IES extraction is from the official HTML summary, not its downloadable guide or underlying studies.

Seven existing knowledge documents were repaired: the CAP-02 design protocol; early-childhood and adult-learning stage guides; UDL and backward-design practices; and the master/instructional-design navigation maps. Original IDs were preserved. Their exact previous content is saved in content-before.json. Unsupported numerical claims and fixed learner assumptions were removed within these audited paths; other legacy content still requires review.

New authoring artifacts are the [course-design assistant](../../90-agent-runtime/prompts/course-design-assistant.md), [research cycle](../../90-agent-runtime/workflows/knowledge-research-cycle.md), [acceptance scenarios](../../90-agent-runtime/evals/course-design-acceptance.md) and [blueprint template](../../docs/templates/course-blueprint.yaml). The [CAP-02 guide](../../70-capabilities/design/instructional-system-design-protocol.md) now connects intake, subject sources, prerequisites, assessment, practice, adaptation and review.

The new coverage implementation is tools/knowledge/coverage.py with CLI tools/knowledge_coverage.py. It intersects canonical tags, retains zero-count dimensions and diagnostics, exposes untagged/unclassified records, and traces typed evidence references without treating navigation or prerequisites as evidence. It performs no network requests or corpus writes.

The README and implementation-status document now expose these entry points while retaining the prior implementation history. Their pre-edit content is saved in documentation-before.json.

## Validation

validation.json records an actual native run of all 78 tests, including eight new coverage tests. The added tests cover empty inventories, intersecting filters, evidence versus navigation, aliases/cycles, legacy trust labels, deterministic read-only behavior, unresolved references and missing roots.

All 15 added or revised knowledge records passed generated-candidate validation. The registry had zero errors. The local-link audit had zero errors; five operational machine-path portability notices remained visible. The blueprint parsed as YAML and retained draft/not-run markers. This is not equivalent to having an executable blueprint validator.

The baseline source-hash comparison found no unrelated changes before closing documentation was updated. A final supplementary terminal command was blocked by the platform because it could not determine the request's safety status. post-documentation-checks.json was not produced; a subsequent native read confirmed the file was absent. The last completed automated link audit preceded the closing README, status and report edits. Those closing edits do not have a new automated verification result. The successful 78-test run and its saved source hashes remain the evidence for the tested implementation.

coverage.json and [coverage.md](coverage.md) preserve the inventory with paths, tag counts, source trails and limitations. baseline.json contains the original counts, hashes and full baseline test output. validation.json includes full final test output and hashes for tested changes.

## Scope of acceptance

The software and structural checks passed. The implementing assistant performed the content/code review. Worker startup failed, so there was no independent worker review. No named subject expert, human pedagogy reviewer, learner pilot or cross-model course benchmark was completed. No commit, push, deployment or external model call was made.

The course blueprint and prompt are authored aids. Their presence does not mean the fraction rehearsal can execute arbitrary courses. Eight manual acceptance scenarios are specified; they are not recorded as passed model runs. The broader body of 62 legacy records and seven unclassified records remains visible.

## Next work

The [roadmap](../../docs/knowledge-roadmap.md) prioritizes remaining claim/quotation appraisal, justified metadata migration, a separate executable course contract, complete representative domain packs, actual prompt evaluations, source-aware retrieval and appropriate expert/learner review. These are acceptance-gated work packages rather than a claim of readiness for every age and topic.
