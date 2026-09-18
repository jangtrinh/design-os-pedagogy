# Course audit: bounded executable profile

The Grade 1 Vietnam exercise exposed gaps between a generic authoring template and an inspectable annual course. The new checker reads an actual course bundle, its independent requirement profile, per-period schedule and sample assessments. It does not deliver lessons, grade student responses or establish pedagogical effectiveness.

## Run

```sh
.venv/bin/python -B tools/course_audit.py courses/vi-vn-grade-1-math
.venv/bin/python -B tools/render_course.py courses/vi-vn-grade-1-math
.venv/bin/python -B tools/render_course.py courses/vi-vn-grade-1-math --write
```

The audit and renderer preview are read-only. The renderer's explicit --write updates only the two generated teacher-facing Markdown files, lessons.md and assessment.md. Edit the YAML source and regenerate rather than maintaining two inconsistent versions.

## Contract and boundaries

The general blueprint remains version 1.0.0 and is not a full executable schema. This fixture adds audit_contract=course-audit-1.0, a profile ID, an independent set of requirements, session file references, explicit tasks and assessment events. Additional fields in the general template are optional authoring guidance.

Supported profile: vn-grade1-math-2018-checked-20260917. Unknown profiles fail rather than inheriting a claim of national conformity. Other subjects require their own checked targets and domain rules. The 24 R identifiers are an authored decomposition, not Ministry identifiers.

Checks include the 105-period sequence, 35-minute totals, weeks, unit membership, acyclic prerequisites, practice before assessment, outcome references, source IDs/locators, nonreader response arrangements, hidden homework, integer sample-test scores and structured mathematical answer keys. Whole-number scope, two-operation order, no carrying/borrowing in the relevant written-calculation range, groups of at most four ordered numbers, whole hours, cm and date/weekday consistency are explicit.

Facts within ten and calculations on whole tens are included. Therefore 6+4, 10-6, 90+10 and 100-40 are allowed. A naive digit-carry rule would reject legitimate tasks. Unsupported operators and malformed keys fail closed.

The existing strict YAML reader and bounded regular-file reader are reused. Inputs are read locally; the audit makes no network request, installs nothing and does not change a corpus, review label or learner database. Duplicate YAML keys, unsafe paths and linked input files are rejected by those readers.

## What a pass does not mean

The checker verifies declared quantities, not the number of objects actually placed on a desk. Standard tags do not prove semantic coverage. Observation rubrics are checked for presence, not automatically graded. Long prose, the quality of explanation, textbook page alignment, printed figure accuracy, actual accessibility and classroom timing need separate review. The report always retains not_run/not_assessed for teacher review, pilot and effectiveness in this authored fixture.

An actual review found a learner prompt in period 85 used cm before its introduction at period 87. The prompt was revised to ask for a direct length comparison; the teacher's preparation measurements remain. The structure/key checks did not discover that vocabulary dependency. This is a concrete limit, not a reason to label the whole course untested.

## Tests and review record

Twenty added unittest methods exercise the actual fixture and deliberately corrupted variants: missing standards, broken alignment, cycles, wrong answers, out-of-scope operations, time conflicts, calendar mismatch, unsupported reading dependence, malformed data and fabricated effectiveness labels. Negative test inputs are constructed faults, not observed mistakes by children or a claimed baseline-model failure rate.

See [the course evaluation](../courses/vi-vn-grade-1-math/workflow-evaluation.md) and the evidence under plans/20260917-vietnam-grade1-course-test. The full existing suite must also pass after implementation. A future general course schema should formalize optional versus required fields and profile extensibility only after additional course cases expose requirements.
