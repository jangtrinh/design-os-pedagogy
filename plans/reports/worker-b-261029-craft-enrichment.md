# Worker B: craft-of-selfteaching enrichment (proposal items 3-5)

Date: 2026-10-29. Branch: `worktree-agent-ac6114ba4d2aaebc1`.

## Not verified
- Venv interpreter `<main checkout>/.venv/bin/python` could not be invoked: the worktree-isolation guard refused it as a command outside the worktree. Gates ran with system `python3` (3.14.6, the venv's own target: `.venv/bin/python3.14 -> /opt/homebrew/opt/python@3.14/bin/python3.14`) plus `PYTHONPATH=<venv>/lib/python3.14/site-packages`. Equivalent interpreter and packages; not byte-identical invocation.
- Unit tests: 98 ran OK, not 143. Baseline before any edit in this worktree was also 98 (11 test files here vs 16 in the main checkout). The 143 figure belongs to a newer main checkout state not on this branch.
- All five sources read at abstract/partial-chapter scope only; no methodological appraisal. Records stay `review_status: unreviewed`.
- Dunlosky & Rawson (2012) considered for the weakness ledger; abstract unavailable (publisher elided it in Crossref/Semantic Scholar) → not cited, no record.
- Autocomplete-off drill and the commit-trail mechanism have no supporting study opened → labelled authored/untested in the modules.

## Changes
Modules (subsection appended; only other change = frontmatter citation lists):
- `50-practice-library/interventions/worked-example-fading-protocol.md` → new §9 Summary Fading (4 tiers, worked example, non-example, hinge + distractor map YAML, protocol addendum, evidence & boundaries). Frontmatter has no citation list (only `evidence_basis` string) → untouched.
- `30-pedagogy/instructional-methods/self-regulated-learning.md` (vi) → new "Mở rộng: sổ điểm yếu". `provenance.citations` += Bjork & Bjork 2011 pp. 56-57.
- `40-disciplines/arts-professional/clinical-reasoning-and-deliberate-practice.md` → new §9: ledger→drill, paper trace + autocomplete-off as candidate desirable difficulties, boundary on variance explained (Macnamara 2014), quick hinge. Explicitly flags legacy §5 row 1 ("innate talent negligible") as overstated. No citation list → frontmatter untouched.
- `30-pedagogy/edtech-ai/process-based-assessment-viva.md` → new §7 Commit Trail (mechanism, signal-not-proof using git-commit docs, probe pairing, bulk-commit non-example, hinge table, ethics). `sources` += git-commit documentation.

New evidence records (v2 schema, `type: source`, `unreviewed`, URL + locator + access date + `source_check_scope`):
- `60-evidence/sources/evidence-bertsch-2007-generation-effect.md` (Europe PMC abstract)
- `60-evidence/sources/evidence-nesbit-2006-concept-maps.md` (Crossref publisher abstract)
- `60-evidence/sources/evidence-macnamara-2014-deliberate-practice.md` (Europe PMC abstract)
- `60-evidence/sources/evidence-xie-2018-program-tracing.md` (Semantic Scholar abstract)
- `60-evidence/sources/evidence-bjork-2011-desirable-difficulties.md` (author-lab PDF, pp. 55-58 read)

Volume/issue/pages for Bertsch (35(2) 201-210) and Macnamara (25(8) 1608-1618) checked against Crossref. Bjork chapter end page, editors and print year not verified → stated so in the record.

## Book handling
Credit once per file: title, author, `https://github.com/xiaolai/the-craft-of-selfteaching` (clone remote), CC BY-NC-ND 3.0 (README line 83 deed link). Zero quotes from the book; no translated passages. Ideas checked against the book markdown before use: Part.1.F (own summaries/tables, revised), S.whats-next (cheat sheets), Part.2.B lines 44-72 (where-to-practise, notes list, priorities, paper tracing, autocomplete off), 02.proof-of-work lines 53, 151-181 (fork, study branch, commits, records vs degrees). Not adopted: "talent irrelevant", records-outweigh-degrees, git proving "when".

## Gate tails (after final edit)
```
$ python3 tools/knowledge_registry.py
{"edges": 350, "errors": 0, "records": 103, "unresolved_edges": 0, "unreviewed_records": 92, "warnings": 62}
(warnings = same 62 LEGACY_UNREVIEWED lines as baseline)

$ PYTHONPATH=<venv site-packages> python3 tools/verify_links.py .
"files": 151 (incl. this report), "errors": [7 lines, all docs/course/grade-1-math/{index,teacher-guide,workflow-evaluation}.md — identical to baseline], "structural_errors": []

$ PYTHONPATH=<venv site-packages> python3 -m unittest discover -s tests
Ran 98 tests in 15.207s
OK

$ python3 scripts/self_check.py
ok: design-os-pedagogy self-check passed (design-os-pedagogy)
```
Baseline before edits: records 98, errors 0; links 145 files, same 7 errors; tests 98 OK; self-check ok.

## Weakest link
Generation-effect and concept-map evidence is about short verbal items and node-link maps; extending it to learner-built tables/summaries is an authored inference (stated in §9.6).

## Unresolved questions
- Should the legacy §5 row 1 of the clinical module ("innate talent negligible") be corrected? Out of scope here (existing content must stay unchanged); flagged in §9.3.
- Grade 1 link errors: links use `../../60-evidence` from `docs/course/grade-1-math/` (resolves to `docs/60-evidence`); files exist at repo root. Pre-existing; not touched.
