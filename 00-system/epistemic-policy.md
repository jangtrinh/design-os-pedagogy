# Epistemic Policy & Evidence Evaluation Architecture

![Epistemic Evidence Hierarchy Ladder](../assets/epistemic_evidence_ladder_1789440471771.jpg)

> **The Epistemic Creed of Master Pedagogy:**  
> *"Knowledge explains. Evidence constrains. Practice operationalizes. Assessment diagnoses. Reflection adapts. Research advances. Teaching teachers proves mastery."*

---

## 1. The Evidence Source Hierarchy (Tier 1–Tier 5)

The tiers below guide source discovery. Institutional prestige does not establish study quality, an effect size or an intervention recommendation. Appraise each claim and comparison independently using Section 2.

* **Tier 1 — Independent Evidence Clearinghouses & Systematic Meta-Analyses**:
  * *IES / What Works Clearinghouse (WWC)*: Gold-standard randomized trial evaluation standards.
  * *Education Endowment Foundation (EEF)*: Meta-analyses reporting Effect Size ($d$) and Months of Additional Progress.
  * *Cochrane / Campbell Collaboration*: Highest-level biomedical and behavioral systematic reviews.
  * *National Academies of Sciences, Engineering, and Medicine (NASEM)*: The *How People Learn II* consensus syntheses.
  * *AERA / APA / NCME*: Standards for Educational and Psychological Testing.
  * *WHO / UNICEF*: Nurturing Care Framework for early childhood neurodevelopment.
  * *OECD / UNESCO*: AI Competency Framework for Teachers and PISA scientific frameworks.

* **Tier 2 — Elite University Research Laboratories & Pedagogy Centers**:
  * Harvard Graduate School of Education (HGSE) & Project Zero.
  * Stanford Graduate School of Education (SGSE) & Stanford History Education Group (SHEG).
  * Oxford Department of Education, Cambridge Faculty of Education, UCL Institute of Education.
  * MIT Teaching + Learning Lab, Carnegie Mellon Simon Initiative.

* **Tier 3 — Classical Intellectual Lineage (Theories & Foundational Models)**:
  * Jean Piaget (Constructivism), Lev Vygotsky (Socio-cultural & ZPD), John Dewey (Experiential Learning), Maria Montessori, Benjamin Bloom (Mastery Learning), Paulo Freire (Critical Pedagogy), Malcolm Knowles (Andragogy), Jerome Bruner (Scaffolding & Spiral Curriculum).
  * *Epistemic Rule*: Classified as foundational theoretical heritage; NEVER granted an empirical Grade A rating without modern replicated experimental data.

* **Tier 4 — Clinical Classroom Practice & Action Research**:
  * Clinical case studies from award-winning master teachers, documented school turnarounds, and Design-Based Implementation Research (DBIR).

* **Tier 5 — Discovery Signals (Non-Evidentiary)**:
  * Commercial blog posts, educational marketing, social media commentary. Treated strictly as leads for primary literature search; never cited as decision-making evidence.

---

## 2. Evidence appraisal, claim status and provenance
Grades describe the kind and appraisal of evidence, not the size or direction of an effect. A rigorous null or harmful result can have strong evidence.

* **A**: Appraised synthesis of rigorous replicated studies; record risk of bias, heterogeneity, population and outcome limitations.
* **B**: Appraised experimental or quasi-experimental evidence with credible controls.
* **C**: Preliminary, observational, correlational or context-limited empirical evidence.
* **D**: Professional consensus and institutional standards.
* **E**: Classic theoretical or philosophical lineage; not proof of an intervention effect.
* **U**: Unappraised or insufficiently documented. U does not mean false.

Store the separate claim verdict as `unreviewed`, `supported`, `mixed`, `not-supported`, `refuted` or `not-applicable`. A refutation needs its own cited scope and evidence; it is not encoded as Grade E. `source-checked` means a traceable source extraction, while `reviewed` requires documented appraisal.

Every quantitative estimate needs a source ID, exact URL and locator, metric, population, comparator, outcome and timepoint. Cohen's d, Hedges' g, normalized gain and relative change are different measures. Do not rank them together or convert them automatically into months of progress.

An authored protocol is guidance. A simulation demonstrates its encoded behavior. An observed case needs a record locator. Cases without provenance remain `unreviewed`; neither a plausible transcript nor a passing schema creates empirical evidence. Legacy Grade A and `status: validated` remain historical metadata and are not promoted by the registry adapter.

---

## 3. Mandatory Boundary Condition Clauses
Every operational practice entry in `design-os-pedagogy` must explicitly declare:
1. **Target Context**: Population age band, domain, and prior learner schema level.
2. **Failure Modes**: Under what conditions does this strategy fail or cause cognitive harm?
3. **Contraindications**: Novice vs. expert status (e.g., when worked examples become extraneous load).
