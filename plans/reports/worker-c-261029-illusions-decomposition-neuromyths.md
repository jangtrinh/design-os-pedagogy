# Worker C — illusions, two-axis decomposition, self-help neuromyths (2026-10-29)

## Not verified (read first)
- Test gate: worktree has 98 tests (baseline, before and after edits); acceptance said 143. Main checkout `tests/` has 16 files / 143 `def test_` vs 11 / 98 here, i.e. main working tree holds tests not in this branch (HEAD 47b59e7). 143 not reproducible in this worktree.
- All 9 sources: abstract only (Scherer: abstract + first page of publisher PDF via a mirror). No full-text appraisal, no typed estimate records.
- Row 14 (difficulty illusion) and the two-axis decomposition procedure: no source opened; labelled authored/untested.
- Proposal file `plans/reports/research-261029-craft-of-selfteaching-adoption-proposal.md` read from main checkout path; not copied into this worktree (outside allowed files).

## Changes
| File | Change |
|---|---|
| `50-practice-library/misconceptions/catalog-stem-and-humanities-misconceptions.md` | +§4 metacognitive misconceptions, rows 13–16 (time, difficulty, felt-need, fluency/rereading) in existing matrix columns + Replacement Model; §4.1 evidence notes; frontmatter `source_ids` added (4) |
| `70-capabilities/design/instructional-system-design-protocol.md` | +§4.1 two-axis decomposition (horizontal/vertical table, CLT segmenting/element-interactivity link, regex worked example, diagnostic, non-examples, alignment check). Frontmatter unchanged |
| `10-foundations/cognitive-neuroscience/neuromyths-debunked.md` | +§9 self-help claims non-example set (5 claims), prediction challenge, hinge + distractor map; frontmatter `source_ids` added (6) |
| `60-evidence/sources/` | 9 new v2 source records (source-checked = extraction only; claim_status not-applicable; grade U) |

New evidence: `evidence-hulleman-2009-utility-value`, `evidence-macnamara-2014-deliberate-practice`, `evidence-melby-lervag-2013-working-memory-training`, `evidence-dunlosky-2013-learning-techniques`, `evidence-karpicke-2009-student-study-strategies`, `evidence-buehler-1994-planning-fallacy`, `evidence-hickok-2009-mirror-neurons`, `evidence-sala-2017-far-transfer`, `evidence-scherer-2019-programming-transfer`.

## Claims (labelled)
- FACT (abstract, Scherer 2019): programming meta-analysis reports moderate far transfer (g = 0.47) to specific cognitive measures, larger with untreated controls. So "programming trains general thinking" is written as **contested**, not refuted; "life thinking" was not an outcome. This corrects the extraction report's "mostly near transfer" framing.
- FACT (abstract, Macnamara 2014): DP explains a minority of variance; abstract does not attribute remainder to talent — module says so.
- FACT (book text, grep in clone): book's talent claim is mainly "first-pass failure is not evidence of low talent"; module presents the general version as the myth risk.
- FACT (abstract, Melby-Lervåg 2013): scope = WM training programs only; mnemonic/domain memory untested — stated as limit.
- FACT (local run): regex dialect facts checked with Python 3.14 (`(?P<y>)` ok, `(?<y>)` rejected), Node (`(?<y>)` ok), BSD grep 2.6.0 (BRE needs `\{4\}`).
- INFERENCE: applying planning-fallacy findings to multi-week skill budgets — labelled authored extrapolation.
- Numbers kept in source records; modules state direction only (avoids untyped quantitative claims in modules).
- License: book credited once per file (title, author, repo URL, CC BY-NC-ND 3.0); 0 quotes, no translated passages.

## Gates (after final edit, worktree root, venv python via space-free symlink)
```
$ python tools/knowledge_registry.py    # exit=0
{"edges": 360, "errors": 0, "records": 107, "unresolved_edges": 0, "unreviewed_records": 87, "warnings": 62}
# 107 = 98 baseline + 9 new evidence; edges 350 -> 360 (new source_ids)
$ python tools/verify_links.py .        # exit=1, pre-existing only
files 154 / errors 7 (all docs/course/grade-1-math/) / structural_errors 0
non-grade-1-math errors: []
$ python -m unittest discover -s tests
Ran 98 tests in 15.295s
OK
$ python3 scripts/self_check.py
ok: design-os-pedagogy self-check passed (design-os-pedagogy)
```
Diff: 81 insertions, 0 deletions across the 3 files (existing content unchanged).

## Weakest link
Abstract-only reading; Hickok 2009 critiques action understanding, not observational learning broadly — extension to the book's social-motivation claims is inference.

## Unresolved questions
- Which branch/state holds the 143-test suite? This branch has 98.
- Controller dedupe: other workers may also add Dunlosky/Macnamara/Hulleman records under other ids.
