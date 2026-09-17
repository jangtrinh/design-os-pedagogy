# Agent Teacher: local technical delivery

Date: 16 September 2026.
Verified host: jangtrinhs-MacBook-Pro-2.local.
Complete checkout: `/Users/jang/Products/Agent Teacher`.

## Delivered changes

The current working tree contains the local three-case rehearsal, registry, draft validation and journaled publication recovery. Existing uncommitted work was retained. The consolidation fixes blocking imports of special files using the common bounded reader, adds FIFO and linked-input regression tests, separates operational portability notices from actual link failures, and ensures unsupported URL schemes are reported rather than suppressed by the parser.

README EN/VI, local workspace instructions, publication contract, implementation status and local delivery instructions are present in the checkout. The fraction pack was reviewed and preserved; no session database was migrated or replaced.

## Final observed verification

| Check | Result |
| --- | --- |
| Full native unittest suite | 70 tests passed in 15.166 seconds |
| Registry | 86 records, 326 edges, zero errors, zero unresolved edges |
| Review labels | 83 unreviewed records and 69 legacy warnings retained |
| Local link audit at source packaging | 100 Markdown files, zero errors, zero structural errors, three operational portability warnings |
| Python source syntax | Parsed successfully |
| JavaScript syntax | app.js and views.js passed node --check |
| Git whitespace check | Exit 0 |
| Source identity | 229 source entries unchanged across final checks |

The full command outputs and source hashes are in `consolidation-checks-r03.json`. Earlier failed or narrower runs remain available and are not represented as final acceptance.

## Archive on the MacBook

File: `Agent-Teacher-local-source-20260916.tar.gz`, in this directory.

Size: 19,159,814 bytes. Members: 248. Member contents and symlinks were compared with their native counterparts before `delivery-manifest.json` was written.

SHA-256:

```text
0f16ae2cbb76923c462cfab44acd28e24355514026c992d2f3664dd43ca3a455
```

The archive contains working source, curated content, assets, tests, documentation and available native evidence at packaging time. This completion note and the final plan status were added afterward. Git internals, virtual environments, session databases, active drafts, credentials and older compressed archives are excluded; originals remain in the checkout.

## Open the application

From the complete checkout, run:

```sh
python3 -B run_rehearsal.py --port 0
```

Open the loopback address printed by the server. Verification used temporary databases and stopped its test servers. This delivery does not claim a persistent server remains running.

## Still requiring separate acceptance

The implementation and content review here was performed by the implementing assistant. Worker dispatch was unavailable, so independent implementation review remains open. The historical browser JSON was inspected, but a new browser run and pixel review were not completed. Human mathematics/teaching review and a real-user pilot remain pending. Software tests do not establish learning gains or validate the weak transfer distractors.

The attachment download tool rejected the original conversation re-audit ZIP host before copying. That ZIP's raw bytes were not transferred. The native source archive is generated from the complete checkout and does not recreate or bypass that attachment.

No commit, push, deployment, model call or participant contact was performed.
