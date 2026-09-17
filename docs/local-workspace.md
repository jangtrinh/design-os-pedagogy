# Local workspace

The requested checkout is `/Users/jang/Products/Agent Teacher`. Native commands have identified the complete checkout on `jangtrinhs-MacBook-Pro-2.local`. A different tool endpoint has returned `/Users/jangtrinh/Products/Agent Teacher` on `Jangs-Mac-Studio.local`, containing only two documents and an older process test. These observations do not establish that either tree was deleted or synchronized.

## Select the complete checkout

Check the physical directory before running the project:

```sh
cd "/Users/jang/Products/Agent Teacher"
pwd -P
hostname
git rev-parse --show-toplevel
test -f run_rehearsal.py
test -f tools/pipeline_support/recovery.py
test -f rehearsal/data/fractions.vi.json
```

Do not install dependencies, run tests or copy over source when these checks identify the partial tree. Its `tests/test_rehearsal_process.py` uses an older select/readline helper. The complete checkout uses a queue timeout and has additional startup and publication recovery tests. Copying the older helper over it would discard verified work.

## Run locally

```sh
python3 -B run_rehearsal.py --port 0
```

Open the address printed by the launcher. The default session database is `.data/rehearsal.sqlite3`; use `--data-dir` with a separate directory for testing. Existing user sessions are not part of a source consolidation operation.

## Verification

Run from the complete checkout with the existing environment:

```sh
.venv/bin/python -B -m unittest discover -s tests -v
.venv/bin/python -B tools/knowledge_registry.py
.venv/bin/python -B tools/verify_links.py
git diff --check
```

The Git baseline is `e4b14823c4532e121a1a889a5366beea53bc28a5`; current implementation changes are uncommitted. Identify tested source with a source manifest as well as the baseline. A prior test result is not a substitute for checking a subsequently edited tree.

## Evidence locations and transfer boundaries

`plans/20260915-trust-and-fraction-rehearsal/` holds the original runtime and browser evidence. `plans/20260916-reaudit-implementation/` holds the re-audit plan and local verification artifacts. See `docs/implementation-status.md` for the scope of each artifact.

Conversation attachments are separate files until a local copy has been saved and verified. In the consolidation attempt on 16 September 2026, the attachment download tool rejected its file host before copying the re-audit archive. Do not mark that archive as present based on its conversation link. Do not manually bypass the download host restriction.

Preserve the complete working tree, existing Git history and session data. Source backups should include the current uncommitted files, corpus, assets, tests, documentation and verification reports. Python environments are machine-specific and should be recreated from `requirements.txt` when moving between machines. Do not copy an older partial tree over the complete checkout, discard existing files or migrate session databases implicitly.

Named expert review and a real-user pilot remain separate acceptance activities described in `docs/fraction-pilot.md`.
