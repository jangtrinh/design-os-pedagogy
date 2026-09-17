# Agent Teacher: trust foundation and fraction rehearsal

Baseline: e4b14823c4532e121a1a889a5366beea53bc28a5. Roadmap approved 2026-09-15.

Deliver a validated content pipeline and a local Vietnamese fraction rehearsal for teachers. Learner responses and coaching are authored simulations, not evidence of learning efficacy.

## Decisions

- Preserve corpus and public IDs; use explicit compatibility mappings.
- Separate stages S0–S7, assistance AL0–AL7 and domain expertise.
- Separate study design, source verification, certainty and effect metrics.
- Validate drafts before explicit application; no automatic Git operations.
- Store revisioned session events separately from corpus; loopback-only service.
- Accept several reasonable teaching strategies; do not claim free-text semantic assessment.
- Keep transfer feedback unavailable until submission.
- No commits, pushes or deployment.

## Work

- [ ] Repair pipeline validation, process handling, staging and collision checks.
- [ ] Add regression tests for failures and preservation of existing work.
- [ ] Unify registry/schema and evidence policy; expose unresolved legacy data.
- [ ] Correct important sources and unsubstantiated runtime claims.
- [ ] Build fraction cases, probes, instructional choices, coaching and transfer.
- [ ] Implement save/reopen, replay, export and stale-write protection.
- [ ] Complete Vietnamese browser workflow and labelled fraction representations.
- [ ] Run technical and browser checks; record expert/pilot gates separately.

## Gates

G1: Invalid publication leaves corpus and Git unchanged; unresolved IDs return errors.
G2: Create, complete, reopen, replay and export a rehearsal; stale writes cannot overwrite events.
G3: Technical results remain separate from expert review and human learning outcomes.

## Continuation

The approved 2026-09-16 re-audit implementation is tracked in
`plans/20260916-reaudit-implementation/plan.md`. The original decisions above
remain in force. Earlier unchecked items are historical, not a current test result.
