# Agent Teacher: re-audit implementation

Approved: 2026-09-16. Original checkout: /Users/jang/Products/Agent Teacher.
Observed Git baseline: e4b14823c4532e121a1a889a5366beea53bc28a5.
Existing uncommitted work must be preserved; the baseline alone does not identify it.

## Objective

Close the reproducible technical and documentation findings, review the fraction
pack, and prepare the human review/pilot handoff with source and test evidence.

## Decisions and current evidence

- Read and terminal initially reached the complete original checkout this turn.
  Later reads again reached the partial docs/tests tree. Every execution must
  verify the original root and required sources before running.
- The original process test uses a queue timeout, not the select/readline helper
  audited in the partial tree. Test the actual helper before deciding a fix.
- Retain explicit draft review and apply; never automatically commit, push,
  publish real corpus content, migrate session data or contact pilot participants.
- Publication recovery must preserve user edits and reject ambiguous ownership.
  Multiple files cannot be represented as one atomic filesystem transaction.
- Preserve canonical content IDs and current unreviewed labels. AI-assisted
  content appraisal is distinct from human expert review and a real-user pilot.
- Preserve the initial session/pack compatibility policy; portfolio expansion
  is conditional on pilot findings, not an implicit migration in this change.

## Work and acceptance

- [x] Read the re-audit and original publication/startup sources and callers.
- [x] Pin source inventory and local baseline checks to the same original checkout.
      source-before.json records 182 files; baseline-tests.json records 52 passes.
- [x] Check the actual queue-based startup deadline with partial output, cleanup,
      corrupt database preservation and real server restart in the native suite.
- [x] Add explicit inspection/recovery for interrupted publication; test crash
      boundaries and edited files using isolated temporary corpora.
      All 11 native recovery tests passed, including interruption of recovery itself.
- [x] Review registry, publication/recovery and the actual fraction pack.
      Arithmetic is consistent; authored transfer keys are not independent efficacy evidence.
- [x] Update README EN/VI, CLI and rehearsal contracts, operational recovery,
      changelog and expert/pilot materials to match the installed behavior.
- [x] Run affected tests, full suite, registry, local links, Python syntax and
      JavaScript syntax checks. Native final suite: 70 tests passed; Git whitespace check passed.
- [x] Save final output, source/pack hashes and delivery evidence locally in
      consolidation-checks-r03.json, delivery-manifest.json and completion.md.
- [ ] Complete independent visual/browser acceptance. The original browser JSON
      was read; no new browser run or pixel review is claimed.

## Local delivery

The complete MacBook checkout retains source, Git history, assets and session data.
The native archive Agent-Teacher-local-source-20260916.tar.gz contains 248 members
verified against the files on disk. delivery-manifest.json records its SHA-256,
size, source inventory and exclusions. The archive is a snapshot taken before this
completion-note update; subsequent plan notes are separate from tested source.
consolidation-checks-r01.json and r02.json remain as historical diagnostic runs;
r03.json is the final successful run. The original conversation ZIP download was
rejected before copying; its raw bytes are not claimed present on this machine.

## Human gates

Named expert review and observation of real teachers/tutors remain pending until
performed. A prepared checklist or automated content test does not close them.
Broader domains, lesson planning, transcript coaching, portfolios and agent
adapters remain conditional roadmap options.
