# Agent Teacher (design-os-pedagogy) — findability + Pages ledger (2026-09-18, es:public-repo-pages run 4)

## Epistemic Ledger

| Claim | Type | Evidence |
|---|---|---|
| Repo indexed by Google (main page) | FACT | WebSearch `"design-os-pedagogy" jangtrinh` returns it first |
| Absent from `AI pedagogy agent open source github …` (education-agent-skills 775★, AI-Teaching-Agent, pyragogy rank) | FACT | WebSearch |
| 10 topics present, homepage empty, no Pages, no release, **no LICENSE file** (`licenseInfo: null`), no CI workflow | FACT | `gh repo view`, `gh api …/pages`, `gh release list`, tree |
| About oversold vs README ("Autonomous Pedagogical Operating System … RCTs … agent runtime") while README states "no external model calls" and "does not certify teaching competence"; README title is "Agent Teacher" | FACT | both read |
| `docs/` = 8 Markdown pages; 11 links from them point `../` into the knowledge tree; `.brv/context-tree` Markdown is tracked on purpose (.gitignore comment) | FACT | `ls`, grep, .gitignore |
| Rehearsal runs locally: `python3 run_rehearsal.py --port 4322` served the app; real captures of the home and a session taken | FACT | this run, port allocated in the registry |
| 92 knowledge Markdown records across the ten numbered areas; 98 `def test_` in 11 modules; 3 authored fraction cases; Grade 1 math course: 105 period plans / 35 weeks | FACT | grep/find, course README |
| Competitor: education-agent-skills 20 topics + homepage; the two others 0–1 topics | FACT | `gh repo view` |
| Orca: `repo_not_found` → plain `git worktree add` | FACT | this run |

**Conclusion:** indexed, not ranking; metadata is half-done (topics yes, About inflated, no homepage/Pages, no license). Reachable wins: honest About + homepage, a Pages landing with a REAL capture of the rehearsal, the eight docs on the layout, JSON-LD, sitemap, Search Console token.

## Applied

- Topics +5 (teacher-training, course-design, knowledge-base, vietnamese, python) → 15.
- About rewritten to the README's own scope (≤ 200 chars, no "autonomous", no "RCTs" claim).
- Pages: `docs/` on the Jekyll `/docs` shape (`_config.yml`, `_layouts/default.html`, `assets/site.css`, `index.html`), landing with the rehearsal captures, sitemap via jekyll-sitemap, Search Console token file. Homepage → Pages URL after enabling.
- `.project-agent.md` with `localhost_port: 4322`.

## Not done, owner decisions

- **LICENSE is missing.** A license badge would read "not identified"; the landing's FAQ says so. Adding one is a legal choice (MIT like the sibling repos?).
- No release/tag: the repo has no version; a v0.1.0 tag is the owner's call.
- Search Console: verify the property `https://jangtrinh.github.io/design-os-pedagogy/` with the token committed to `docs/`, submit `sitemap.xml`.

## Executed 2026-09-18

| Step | Result | Rollback |
|---|---|---|
| Topics 10 → 15; About rewritten to README scope (173 chars); homepage → Pages URL | FACT | `gh repo edit` |
| `docs/` Pages site: landing + layout + CSS + config + real rehearsal captures + GSC token; `.project-agent.md` port 4322 | PR #1 `f388ee0`, Pages built | `git revert f388ee0`, `DELETE /pages` |
| Live `ui gate`: landing PASS 0/0; 7 docs pages PASS (Rouge `container-nesting-depth` warnings only) | FACT | |
| Tells DOM (1280×800): h1 352 / lede 489 / action 629, no gradient, nav hairline 0, 0 keyframes, 7 font sizes, wordmark → jang.work | FACT | |
| 390: no overflow on landing and a docs page; sitemap lists 8 pages; token 200 | FACT | |
| `course-audit.html` 404 | FACT: `docs/course-audit.md` is untracked in the owner's checkout (with `tools/course_audit.py`, `tests/test_course_audit.py`); README on main already links to it. Owner commits it; the page then renders and enters the sitemap. | |

Owner-manual: Search Console verify + sitemap submit; LICENSE decision; release tag decision; commit the course-audit WIP.
