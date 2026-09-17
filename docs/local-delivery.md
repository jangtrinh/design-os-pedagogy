# Local delivery

The complete MacBook checkout is identified in [Local workspace](local-workspace.md). It retains Git history, uncommitted changes, corpus, assets, tests, documentation and session data. The partial Mac Studio tree was not used to replace implementation files.

## Consolidated changes

The local rehearsal, registry, publication journal and recovery implementation remain in place. This consolidation adds bounded file import, FIFO and linked-input regression tests, explicit portability diagnostics and unsupported-scheme detection. Both READMEs link to the local workspace instructions. The authored fraction pack is unchanged.

## Evidence in plans/20260916-reaudit-implementation

| Record | Scope |
| --- | --- |
| baseline-tests.json | 52-test baseline before the re-audit implementation |
| consolidation-checks-r01.json | 67 tests passed; operational path diagnostics remained |
| consolidation-checks-r02.json | One of 69 tests failed on a suppressed file-scheme link |
| link-parser-checks.json | All 11 provider/link tests passed after correction |
| consolidation-checks-r03.json | Final suite, registry, links and source hashes; require all_passed=true |
| delivery-manifest.json | Archive path, hash and verified member hashes after successful packaging |

Failed records are retained. A filename in this table does not establish that a later record has been produced.

## Source archive

The packaging command creates `Agent-Teacher-local-source-20260916.tar.gz` in the evidence directory only after the final checks pass. It includes current working source, curated content, assets, tests, documentation and available local evidence. Member hashes are compared with the tested source before the delivery manifest is written. Existing archives are not overwritten.

Git internals, virtual environments, session databases, active publication drafts, credentials and older compressed archives are excluded. Nothing is removed from the working checkout: Git history and sessions remain on the MacBook. Recreate an environment from requirements.txt when moving to another machine.

## Run

From the complete project folder:

```sh
python3 -B run_rehearsal.py --port 0
```

Open the loopback address printed by the launcher. Test servers use temporary storage and are stopped after checks; no persistent server is claimed by this document.

## Remaining boundaries

The raw conversation re-audit ZIP was not copied because the attachment tool rejected its download host. Earlier findings and current corrections are documented locally, but this does not imply the original ZIP bytes are present. The native source archive is generated from the checkout, not recreated from that conversation attachment.

The original browser report remains historical evidence. Command-line tests exercise actual server behavior, persistence, replay and export. Named expert review, real-user pilot and independent implementation review remain separate, uncompleted activities. Weak transfer distractors and unreviewed legacy claims retain their existing limitations.
