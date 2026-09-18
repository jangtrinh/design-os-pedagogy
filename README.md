# Agent Teacher

DESIGN:OS Pedagogy combines a pedagogy knowledge library, a local teacher rehearsal and an explicit draft publication pipeline.

![Agent Teacher knowledge workspace](assets/pedagogy_hero_console_1789438819020.jpg)

[Tiếng Việt](README.vi.md) · [Knowledge map](00-navigation/MOC-Master.md) · [Course design](90-agent-runtime/prompts/course-design-assistant.md) · [Knowledge roadmap](docs/knowledge-roadmap.md) · [Rehearsal contract](docs/rehearsal-contract.md) · [Publication and recovery](docs/publication.md)

For the local checkout, environment checks and evidence locations, see [Local workspace](docs/local-workspace.md).

## Implemented scope

The Vietnamese rehearsal contains three authored fraction cases: magnitude comparison, a correct answer with an insufficient explanation, and notation conflicting with the learner's explanation. Participants select teaching actions, record their words, inspect feedback tied to the transcript, attempt a transfer task and save a reflection.

Sessions and events are saved in SQLite with revision checks, duplicate-request handling, reopening, replay and Markdown/JSON export. Student replies and coaching follow authored branches. Free text is stored but not semantically graded. The application makes no external model calls and does not certify teaching competence.

The registry checks metadata, canonical IDs, explicit aliases and typed references. The publisher validates drafts before a separate apply action. Source appraisal, named expert review and a real-user pilot remain pending. Passing software tests or having a clean reference graph does not establish teaching effectiveness.

## Run the rehearsal

From the project root:

~~~sh
python3 run_rehearsal.py --port 0
~~~

Open the printed loopback address. Port 0 selects a free port; the default is 8876. Data defaults to .data/rehearsal.sqlite3. Use --data-dir with a separate directory for a test or pilot. This is a single-user local service, not a public multi-account deployment.

The workflow is probe → interpret → teach → check → review → transfer → reflect → complete. Sessions retain the pack version and fingerprint. After a pack changes, old sessions remain readable/exportable but cannot advance or replay against different content. Listing returns the latest 100 sessions; known older URLs remain accessible.

## Explore the library

Start with [the master map](00-navigation/MOC-Master.md). The authoring model connects knowledge, experience, diagnosis, practice, feedback, transfer and an implementation protocol.

| Area | Contents |
| --- | --- |
| 00-system | Ontology, schema, epistemic policy and authoring contract |
| 10-foundations and 20-stages | Foundations and education-stage guides |
| 30-pedagogy and 40-disciplines | Methods, assessment and disciplinary practice |
| 50-practice-library and 60-evidence | Cases, source notes, claims and estimates |
| 70-capabilities and 80-professor-development | Teaching capabilities and professional learning |
| 90-agent-runtime | Runtime specifications, prompts and evaluation proposals |
| rehearsal | The implemented local fraction rehearsal |
| tools and tests | Registry, publication, local link auditing and executable tests |

Education stages use S0 through S7; AI assistance uses AL0 through AL7. The versioned ontology/schema is authoritative. Stage, assistance and competence are different attributes. The broader tutor runtime in 90-agent-runtime remains a specification.

Read verification, claim status, effect metric, applicability and review status separately. Authored examples are not observed classroom outcomes. Legacy evidence grades and validated flags do not confer expert review. Brand visuals are described in [ART-DIRECTION.md](ART-DIRECTION.md); instructional visuals may use labels and accurate scales when useful.

## Design a course with an AI assistant

Use the [course-design prompt](90-agent-runtime/prompts/course-design-assistant.md), [design protocol](70-capabilities/design/instructional-system-design-protocol.md) and [blueprint template](docs/templates/course-blueprint.yaml). They guide intake, subject-source research, prerequisites, outcome-assessment-practice alignment, unit materials and review. The template is an authoring aid, not an executable course schema or a general course runtime.

The [research cycle](90-agent-runtime/workflows/knowledge-research-cycle.md) explains how to extend missing knowledge. The [acceptance scenarios](90-agent-runtime/evals/course-design-acceptance.md) define a manual design review; they are not a completed model benchmark. The [roadmap](docs/knowledge-roadmap.md) records current coverage and the next acceptance gates.

Run `.venv/bin/python -B tools/knowledge_coverage.py` for a read-only inventory. Add `--stage S6 --axis AX-04 --capability CAP-02 --json` to intersect tags and inspect record paths and source trails. Metadata counts do not establish curriculum completeness or learning effectiveness.

The first concrete full-year authoring exercise is [Vietnamese Grade 1 mathematics](courses/vi-vn-grade-1-math/README.md): 105 period plans, a requirements map, teacher guidance and sample assessments. Its [workflow evaluation](courses/vi-vn-grade-1-math/workflow-evaluation.md) records actual structural/key checks and remaining teacher/pilot work. The [bounded course auditor](docs/course-audit.md) does not validate every subject or establish learning gains.

## Prepare and apply a module

Registry and publication require the packages in requirements.txt. Use the existing .venv, or create an environment when absent and install those requirements. Publication uses POSIX filesystem locking.

~~~sh
.venv/bin/python -B tools/pedagogy_pipeline.py "Fraction teaching routine" --stage S2 --archetype methods --dry-run
~~~

Preview prints the route, ID and full authoring contract without writing a draft or calling a model. Author a matching module, then import it:

~~~sh
.venv/bin/python -B tools/pedagogy_pipeline.py "Fraction teaching routine" --stage S2 --archetype methods --input /path/to/module.md
~~~

Review module.md, moc.md and manifest.json in the returned folder. Replace DRAFT_ID below with that exact folder name:

~~~sh
.venv/bin/python -B tools/pedagogy_pipeline.py --apply .pedagogy-drafts/DRAFT_ID
~~~

Draft metadata must stay unreviewed; import is not scientific approval. Existing targets, changed drafts or changed navigation produce conflicts. Unicode filenames are supported; supply --id with a canonical ASCII identifier when necessary. An optional provider must be explicitly selected with --provider. No Git add, commit or push occurs. The former -m and -p commands are obsolete.

## Inspect interrupted publication

~~~sh
.venv/bin/python -B tools/pedagogy_pipeline.py --inspect-publication
.venv/bin/python -B tools/pedagogy_pipeline.py --recover-publication
~~~

Recovery explicitly finishes an unchanged interrupted transaction. Edited or replaced files produce a conflict. Keep the journal, draft and stages; do not remove them to force apply. [The recovery procedure](docs/publication.md) explains ownership checks and manual conflict handling. Two file changes are not one atomic transaction; process-exit tests do not cover every storage or power failure.

## Verification and remaining gates

~~~sh
.venv/bin/python -B -m unittest discover -s tests -v
.venv/bin/python -B tools/knowledge_registry.py
.venv/bin/python -B tools/verify_links.py
~~~

Tests use temporary corpora and databases. The link auditor checks local paths/anchors, not external HTTP responses or scientific support for a claim. Review diagnostics within their scope.

[Implementation status](docs/implementation-status.md) records evidence locations and boundaries. [Fraction review and pilot](docs/fraction-pilot.md) defines the remaining human work. General course execution, transcript coaching, portfolios, agent adapters and new domains remain conditional roadmap options.
