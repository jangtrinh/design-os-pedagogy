# Vietnamese fraction rehearsal

The participant practises being the teacher. Student replies, coaching and transfer feedback are authored branches. The application makes no model calls and does not semantically assess free text, infer mental states or certify teaching competence. Expert review and a real-user pilot remain pending.

## Workflow

probe → interpret → teach → check → review → transfer → reflect → complete

Cases cover fraction magnitude, a correct answer with an insufficient reason, and notation conflicting with the learner's explanation. Number-line instruction, worked examples and short explicit explanation are available. Check responses depend on the teaching choice. There is no universal cognitive-conflict requirement.

Coaching cites a recorded teacher turn and comments on the selected action. Leading/trailing whitespace is trimmed; Unicode inside a response is preserved. Transfer feedback appears after submission. This is practice, not a secure examination: repository owners can read the pack.

## Run and persistence

Run python3 run_rehearsal.py --port 0 from the root. Open the printed loopback address. The default port is 8876. Data defaults to .data/rehearsal.sqlite3; --data-dir selects a separate test or pilot directory.

Snapshots, events and idempotency records are stored transactionally. Sessions retain pack version and SHA-256. After the pack changes, old sessions remain readable/exportable; advancement and replay return pack_changed. No automatic migration is provided. Listing returns the latest 100 sessions; known older URLs remain accessible.

## HTTP contract

| Method | Route | Behavior |
| --- | --- | --- |
| GET | /api/status | Authored mode, no model calls, pack version and pending review |
| GET | /api/catalog | Public summaries and sources, without responses/keys |
| GET | /api/sessions | Latest summaries in items |
| POST | /api/sessions | case_id, optional title and request_id; returns session |
| GET | /api/sessions/{id} | Saved session, prompt and observed transcript |
| POST | /api/sessions/{id}/events | revision, type, choice, optional text and request_id |
| GET | /api/sessions/{id}/events | Ordered committed events in items |
| GET | /api/sessions/{id}/replay | Rebuild from events and compare saved state |
| GET | /api/sessions/{id}/export?format=md | Markdown attachment; format=json exports the snapshot |

request_id is a canonical UUID. Identical retries do not duplicate transitions. ID reuse with different content, stale revisions and out-of-order transitions return 409. Invalid input returns 400; bodies are limited to 32 KiB. Duplicate JSON keys and non-finite values are rejected.

The service binds loopback, checks Host/Origin and serves only declared UI assets. There is no general file-serving endpoint or remote account system. Server tests alone do not verify browser storage policies or complete accessibility.

## Evidence boundaries

Pack sources identify general worked-example and retrieval-practice research. Their abstract locators do not validate the authored cases, coaching or transfer items. Keep technical tests, AI-assisted appraisal, named expert review and observed user outcomes separate.
