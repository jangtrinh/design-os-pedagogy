# Publication and interruption recovery

The publisher installs one new module and one derived MOC insertion after explicit review. It rejects existing module targets and performs no Git operations. These commands describe the CLI, not a report of publication into this repository.

## Draft contract

Run tools/pedagogy_pipeline.py with --dry-run, an explicit stage and a suitable archetype to inspect the target, canonical ID, route and schema. Import accepts --input with UTF-8 Markdown below 2 MiB. An explicitly selected --provider executable reads the prompt on stdin and writes Markdown on stdout, with bounded output and timeout.

Import requires a regular file without symlinks or extra hardlinks. Special files, including named pipes, are rejected before content is read. The size limit is enforced on the opened file and on the bytes read. Copy an intended linked input to an ordinary file before importing it.

A draft contains module.md, moc.md and manifest.json under .pedagogy-drafts. Version 2 manifests bind the route, target, navigation path and content hashes. Instructional modules require strict closed YAML, the requested ID, schema_version 2.0.0, unreviewed status, source references or URL locators, and the eleven parsed instructional sections printed by the preview. Code fences do not count as headings. Structural acceptance does not establish scientific validity.

Review the exact module, navigation insertion and manifest before --apply. Changed drafts or navigation must be prepared again. An existing target is a conflict, including repeated apply after success. Version 1 manifests must be prepared again.

## Interrupted publication

The publisher holds a filesystem lock. Before installing a module it records active-publication.json with intended snapshots, the draft manifest hash, file identities and staging paths. It links the module exclusively and replaces navigation only while the recorded original still matches.

| State from --inspect-publication | Meaning |
| --- | --- |
| idle | No active journal; this does not certify the corpus. |
| prepared | Intent and stages exist; the module is not installed. |
| module_installed | The owned module exists; navigation still matches the original. |
| published | Both intended files exist; final cleanup remains. |
| conflict | Files, draft or journal cannot be reconciled with recorded ownership/content. |

Inspection leaves corpus files unchanged, although it may create the local lock directory/file. A pending journal blocks another prepare or apply.

## Operator procedure

1. Stop editing the affected module, MOC and draft. Preserve a project copy including .pedagogy-drafts before manual intervention.
2. Run .venv/bin/python -B tools/pedagogy_pipeline.py --inspect-publication and inspect the state and paths.
3. For an unchanged prepared, module_installed or published transaction, explicitly run the CLI with --recover-publication. It checks the recorded draft, permitted navigation insertion, content and identity before finishing the original intent.
4. Inspect resulting files and run registry/link checks. A second recovery without a pending transaction returns idle without publishing again.

A conflict stops recovery and preserves files. Do not delete the lock or journal to force apply. Compare original snapshots, current files and draft, then reconcile edits manually with their owner. There is no automatic rollback command for ambiguous or edited transactions. Implementation tests use separate temporary corpora.

## Guarantees and limits

A catchable failure before navigation commits rolls back an unchanged owned module. Edited files or already-committed navigation retain the journal for inspection. An identical-content replacement still has a different identity and is rejected. Symlinks, extra hardlinks, changed stages and altered manifests are not silently accepted.

The lock coordinates publishers and releases when their process exits. It does not coordinate arbitrary editors. A journal does not make two files one atomic transaction. Process-interruption tests do not simulate every power loss, filesystem failure or hostile local race. Failure before journal creation can leave unreferenced temporary stages; do not infer ownership from filenames or delete unknown files automatically.

Tests are in tests/test_publication.py and tests/test_publication_recovery.py. Recorded outputs belong in plans/20260916-reaudit-implementation.

## Link and portability diagnostics

The repository link audit reports broken targets, anchors and invalid metadata as errors. Machine-specific paths quoted in prose or command examples are retained separately as `portability_warnings`; they do not themselves imply a broken link. Actual machine-specific link targets still fail the link checks. Draft validation treats portability warnings on the proposed module as blocking diagnostics, so generated teaching modules cannot acquire machine-specific paths through this distinction.
