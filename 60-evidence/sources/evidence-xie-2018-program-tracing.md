---
schema_version: "2.0.0"
id: evidence-xie-2018-program-tracing
type: source
title: "An explicit strategy to scaffold novice program tracing"
stage: [S4]
axes: [AX-01, AX-03]
capabilities: [CAP-02, CAP-04]
context: [computing-education, cs1, program-tracing]
locale: en
evidence_grade: U
claim_status: unreviewed
review_status: unreviewed
provenance:
  kind: literature
  citations:
    - url: "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3159450.3159527?fields=title,abstract,year,venue,authors"
      locator: "Abstract (Semantic Scholar record of the published abstract)"
authors: ["Benjamin Xie", "Greg L. Nelson", "Amy J. Ko"]
year: 2018
source_journal: "Proceedings of the 49th ACM Technical Symposium on Computer Science Education (SIGCSE 2018), 344-349"
doi: "10.1145/3159450.3159527"
url: "https://doi.org/10.1145/3159450.3159527"
locator: "Abstract"
design: "block-randomized experiment with think-aloud and interviews"
sample_size: "24 novices in a university CS1 course"
source_revision: "Abstract via Semantic Scholar Graph API, accessed 2026-10-29; ACM landing page did not expose the abstract to a plain fetch"
source_check_scope: "Abstract only, read 2026-10-29. Full paper, materials and analysis not read; methodological appraisal pending."
---

# Teaching novices an explicit line-by-line tracing strategy

**Extracted from the abstract:** a short strategy asked novices to trace code line
by line and keep an external record of memory (variable values) that they update.
In a block-randomized experiment with 24 university CS1 novices, the strategy was
introduced in 5-10 minutes. On the study's tracing problems, students using it
scored on average 15% higher than the control group (reported p < 0.05), and they
scored on average 7% higher on the course midterm. Think-aloud and interview data
linked systematic tracing and sketching intermediate values to better performance.

**Scope read:** abstract only. The sample is small and from one course; the 15% and
7% figures are relative score differences reported in the abstract, not
standardized effect sizes.

**Design use:** supports teaching tracing as an explicit, externalized procedure
for CS1 novices. It does not test unaided "trace it all in your head" drills, nor
any effect of disabling editor autocomplete.
