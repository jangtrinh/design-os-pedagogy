# Worker A: forward-reference management + learning from primary docs

Worktree: isolated worktree (removed after merge)
Branch: `worktree-agent-a69636e4ffb88ceb6`

## Not verified (read first)
- Ausubel (1960) advance organizers: APA PsycNet returned 403; Semantic Scholar record has no abstract. Bruner (spiral curriculum): publisher page returned empty. Both cited by name only as Tier 3 / Grade E lineage; **no evidence record created**.
- All 5 new evidence records rest on **PubMed abstracts only** (no full text, no effect sizes, no appraisal). Kept `review_status: unreviewed`.
- Karpicke & Blunt 2011 has a published comment (PMID 22034416); not read.
- No study of the full "flag + ledger + closure" protocol or the 4-pass docs protocol was found or read. Both modules are authored (`U`).
- Gate command deviation: the worktree guard refused to execute `the project venv python` (path outside worktree). Gates ran with system `python3` 3.14.6 plus `PYTHONPATH=<venv>/lib/python3.14/site-packages` (same Python minor as the venv). INFERENCE: equivalent interpreter + packages; not proven identical.
- Unit tests: worktree baseline is **98 tests** (11 test files), not 143. Main checkout has 16 test files (uncommitted/other state). Baseline 98 OK before edits = 98 OK after.

## Delivered (FACT, on disk)
| File | Kind |
| --- | --- |
| `30-pedagogy/instructional-methods/forward-reference-management.md` | new module, id `method-forward-reference-management` |
| `30-pedagogy/instructional-methods/learning-from-primary-docs.md` | new module, id `method-learning-from-primary-docs` |
| `60-evidence/sources/evidence-roediger-2006-test-enhanced-learning.md` | new source record |
| `60-evidence/sources/evidence-karpicke-2011-retrieval-vs-concept-mapping.md` | new source record |
| `60-evidence/sources/evidence-dunlosky-2013-learning-techniques.md` | new source record |
| `60-evidence/sources/evidence-cepeda-2006-distributed-practice.md` | new source record |
| `60-evidence/sources/evidence-kornell-2009-unsuccessful-retrieval.md` | new source record |
| `90-agent-runtime/workflows/pedagogical-state-machine.md` | added section "Forward-reference ledger" (states open/due/closing/closed/reopened + transitions) after assistance policies |
| `00-navigation/MOC-Instructional-Design.md` | items 12–13 in §2 link both modules |
| `plans/reports/research-261029-craft-of-selfteaching-adoption-proposal.md` | copied from main checkout (was missing) |

## Acceptance criteria check
1. Frontmatter: `schema_version: "2.0.0"`, unique ids (registry: 0 DUPLICATE_ID), `evidence_grade: U`, `claim_status: unreviewed`, `review_status: unreviewed`, `provenance.kind: authored` with citations only to pages opened 2026-10-29 (PubMed abstracts, Python Tutorial §4.5, Raymond & Moen "Before You Ask", book chapters as idea lineage). Book = Tier 4/5, no grade from it.
2. Archetype C sections 1–10 present in both (contract, problem + prediction, preconditions/contraindications, anatomy + think-aloud + I/We/You, worked transcript, pathological + misconceptions, hinge YAML with distractor map/probes/routing/insufficient-evidence, adaptation matrix incl. AI tutor, fidelity checklist + recovery, evidence & boundaries). Each has "Không lấy từ sách nguồn" (rereading main loop, delaying all practice, no spacing; + laziness attribution / read-only motor skills).
3. License: no translated/copied passages. Module 1 has one Chinese quote of 12 characters (the book's core rule, attributed, used as the thing corrected). Module 2 has no quote. Both credit title, author, repo URL `https://github.com/xiaolai/the-craft-of-selfteaching` (clone origin), CC BY-NC-ND 3.0.
4. Locale: **`vi`**. Siblings in `30-pedagogy/instructional-methods/`: 3 declare `locale: vi` (autonomy-supportive, peer-instruction, self-regulated-learning), 4 legacy files declare no locale (English bodies). Frontmatter majority among declared = vi; proposal is also vi. Evidence records are `locale: en`, matching the v2 precedent `evidence-bastani-2025-ai-guardrails.md`.
5. Gates: see below.
6. Commit on branch `worktree-agent-a69636e4ffb88ceb6` (≠ main), not pushed.

## Key correction vs book (FACT from sources opened)
- Closure/review = closed-book retrieval, not rereading. Roediger & Karpicke 2006 abstract: testing beat restudying at 2 days and 1 week (restudy better at 5 min); restudy raised confidence. Dunlosky 2013 abstract: rereading low utility; practice testing + distributed practice high.
- Spacing gap depends on retention interval (Cepeda 2006 abstract; 839 assessments / 317 experiments / 184 articles). No numeric schedule given in modules.
- Failed recall + answer still helps (Kornell 2009 abstract) → closure starts with recall even if learner may fail.
- `for…else` worked example verified by running Python 3.14: `[1,3,5]`→else runs; `[1,4,5]`→break, else skipped; `[]`→else runs; `return` skips else.

## Gate results (raw tails, after final edit)
```text
$ python3 tools/knowledge_registry.py   (LEGACY_UNREVIEWED warnings filtered from display)
{"edges": 366, "errors": 0, "records": 105, "unresolved_edges": 0, "unreviewed_records": 94, "warnings": 62}
registry_exit=0          # baseline before edits: records 98, edges 350, warnings 62
                         # 105 = 98 + 7 new files (2 modules + 5 evidence)

$ PYTHONPATH=<venv site-packages> python3 tools/verify_links.py .
  "files": 154,          # baseline 146; +7 corpus files +1 this report
  "errors": [  7 entries, all docs/course/grade-1-math/ (index.md:29 x3, teacher-guide.md:7 x3,
               workflow-evaluation.md:63) — identical to baseline ]
  "structural_errors": [],

$ PYTHONPATH=<venv site-packages> python3 -m unittest discover -s tests
Ran 98 tests in 15.860s
OK                       # baseline in this worktree: 98 OK

$ python3 scripts/self_check.py
ok: design-os-pedagogy self-check passed (design-os-pedagogy)
```

## Weakest link
Every evidence claim rests on abstracts only; transfer from verbal/prose-recall studies to technical-doc learning is INFERENCE, stated as such in both modules.

## Assumptions
- Evidence records kept `unreviewed` (not `source-checked`) because no named reviewer exists; confidence high; a named human extraction review would flip it.
- Stage tags S3–S6 chosen as authored scope; S1–S2 listed as contraindicated (prefer resequencing) in module 1; confidence medium.

## Follow-ups (not done, out of scope)
- MOC-Learning-Science still shows legacy effect sizes ($g = 0.74$, $d = 0.76$, etc.) without estimate records — pre-existing.
- 7 pre-existing link errors in `docs/course/grade-1-math/` unchanged.
- Read Ausubel 1960 / Luiten et al. 1980 full text via library access to upgrade the advance-organizer link from name-only lineage.

## Unresolved questions
- Should the 143-test acceptance number refer to the main checkout's uncommitted test files? The worktree branch has 98.
