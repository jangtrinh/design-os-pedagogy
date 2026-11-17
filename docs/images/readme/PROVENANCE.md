# README images

| File | Size | What it is |
| :--- | :--- | :--- |
| `cover-dark.png`, `cover-light.png` | 1600x720 | README cover, dark and light |
| `flow-dark.png`, `flow-light.png` | 1600x1000 | "Library. Rehearsal. Course." overview, dark and light |
| `social-preview.png` | 1280x640 | Social preview candidate. Not uploaded to the repository settings |
| `rehearsal-cases.png` | 1440x900 | Real capture of the rehearsal app's case list |
| `rehearsal-session.png` | 1440x900 | Real capture of a rehearsal session at step 4 (check) |

- Covers, flows and the social preview were rendered from HTML with headless Chrome, set in Be Vietnam Pro (400, 600, 800), monochrome plus `#fca849`. The numbers on them come from `tools/knowledge_registry.py`, `tools/knowledge_coverage.py`, `tools/course_audit.py` and `rehearsal/` as of commit `1c6200a`.
- The mark is `design-os-pedagogy.webp` from the hub repository, `jangtrinh/jangtrinh.github.io`, at `assets/logos/` (sha256 `a9a25586a1d0cf8e3ef3eab97be45969845d26b11394470956189ebce87c12c4`). Its provenance is recorded in the hub's `assets/logos/SOURCES.txt`.
- The two rehearsal captures were taken from `python3 run_rehearsal.py` running locally on a throwaway data folder, with no edits beyond palette quantisation. The student lines are the authored lines from `rehearsal/data/fractions.vi.json`; the teacher text is test input.
- Every PNG is under 150 KB. Alt text and captions read "design:os by Jang".
