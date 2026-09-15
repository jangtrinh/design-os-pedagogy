---
id: EVI-02
title: "Pedagogical Evidence Map: 2D Stage-Intervention Matrix"
stage_applicability: ["S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7"]
prerequisites: ["EVI-01"]
leads_to: ["RUB-01", "CAP-02", "CAP-04"]
evidence_basis:
  hattie_d: 0.79
  meta_citations:
    - "Hattie, J. (2023). Visible Learning: The Sequel. Routledge."
    - "EEF. (2021). Teaching and Learning Toolkit: Evidence Summaries."
    - "Kapur, M. (2016). Examining productive failure, cognitive load, and transfer. Educational Psychologist, 51(2), 289-299."
---

# Pedagogical Evidence Map: 2D Stage-Intervention Matrix

## 1. Learning Contract
By studying this evidence map, instructional designers and agent developers will be able to:
1. Cross-reference any of the 20 primary pedagogical interventions across developmental stages S0 (Prenatal/Infant) through S7 (Elite/Doctoral) to identify optimal effect sizes and developmental contraindications.
2. Select instructional interventions that maximize learning gains (\(d \ge 0.50\)) while avoiding expertise reversal and cognitive overload risks.
3. Diagnose and resolve stage-mismatched instructional choices (e.g., pure discovery in S2, or rigid direct instruction in S6/S7) using verified empirical transition rules.

---

## 2. Causal Cognitive Mechanism & Developmental Fit
Pedagogical effect sizes are not developmental constants. The efficacy of any instructional intervention depends on the learner's existing cognitive architecture:
1. **Novice Stages (S1–S3)**: Working memory is constrained by minimal domain-specific long-term memory schemas. Interventions providing external cognitive architecture (Direct Instruction, Worked Examples, Phonics) yield high effect sizes (\(d = 0.59\) to \(d = 0.84\)), whereas unguided inquiry produces negative to negligible gains due to extraneous load.
2. **Intermediate Stages (S4–S5)**: Schemas begin automating. The *Expertise Reversal Effect* emerges: heavy explicit guidance becomes extraneous load. Dual-phase models (Productive Failure, Socratic dialogue, Peer Instruction) jump in effectiveness (\(d = 0.55\) to \(d = 0.88\)).
3. **Advanced / Expert Stages (S6–S7)**: Learners possess deep, automated schemata and metacognitive executive control. Prescriptive instruction degrades performance (\(d < 0.20\)). Clinical reasoning, deliberate practice with bio-feedback, studio critique, and viva voce cross-examination become the only methods driving frontier mastery (\(d \ge 0.70\)).

```
Developmental Trajectory:
[S0-S1: Sensorimotor / Play] ──> [S2-S3: Schema Building] ──> [S4-S5: Schema Automation] ──> [S6-S7: Frontier Mastery]
External Architecture Required:      MAXIMAL (DI / Scaffolds)          BALANCED (Productive Failure)        MINIMAL / ADVERSARIAL (Deliberate Practice)
```

---

## 3. The 2D Stage-by-Intervention Evidence Matrix

Legend:
- **Optimal (High Gain)**: \(d \ge 0.60\) (Primary recommended intervention)
- **Effective (Moderate Gain)**: \(0.40 \le d < 0.60\) (Above average hinge-point)
- **Emerging / Contextual**: \(0.20 \le d < 0.40\) (Requires specific scaffolding)
- **Contraindicated / Harmful**: \(d < 0.20\) or Negative (Expertise reversal or cognitive collapse risk)

| Intervention | S0: Prenatal/Infancy (0-2y) | S1: Early Childhood (2-5y) | S2: Primary Foundational (6-9y) | S3: Upper Primary (9-12y) | S4: Lower Secondary (12-15y) | S5: Upper Sec / Pre-U (15-18y) | S6: Undergraduate / Prof (18-22y) | S7: Doctoral / Master (>22y) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Direct Instruction (Engelmann)** | Contraindicated (N/A) | Emerging (\(d=0.35\)) | **Optimal (\(d=0.74\))** | **Optimal (\(d=0.68\))** | Effective (\(d=0.52\)) | Emerging (\(d=0.38\)) | Contraindicated (\(d=0.18\)) | Contraindicated (\(d=-0.12\)) |
| **Worked Example Fading** | Contraindicated (N/A) | Contraindicated (\(d=0.15\)) | Effective (\(d=0.55\)) | **Optimal (\(d=0.72\))** | **Optimal (\(d=0.65\))** | Effective (\(d=0.50\)) | Emerging (\(d=0.30\)) | Contraindicated (\(d=-0.22\)) |
| **Spaced Retrieval Practice** | Contraindicated (N/A) | Emerging (\(d=0.28\)) | Effective (\(d=0.58\)) | **Optimal (\(d=0.74\))** | **Optimal (\(d=0.76\))** | **Optimal (\(d=0.78\))** | **Optimal (\(d=0.72\))** | Effective (\(d=0.54\)) |
| **Interleaving Practice** | Contraindicated (N/A) | Contraindicated (\(d=0.10\)) | Emerging (\(d=0.34\)) | Effective (\(d=0.48\)) | **Optimal (\(d=0.65\))** | **Optimal (\(d=0.68\))** | **Optimal (\(d=0.64\))** | Effective (\(d=0.52\)) |
| **Productive Failure (Kapur)** | Contraindicated (N/A) | Contraindicated (\(d=-0.15\)) | Contraindicated (\(d=-0.05\)) | Emerging (\(d=0.32\)) | **Optimal (\(d=0.62\))** | **Optimal (\(d=0.66\))** | **Optimal (\(d=0.60\))** | Effective (\(d=0.48\)) |
| **Peer Instruction / Mazur** | Contraindicated (N/A) | Contraindicated (\(d=0.08\)) | Emerging (\(d=0.25\)) | Effective (\(d=0.46\)) | **Optimal (\(d=0.64\))** | **Optimal (\(d=0.70\))** | **Optimal (\(d=0.68\))** | Effective (\(d=0.50\)) |
| **Systematic Synthetic Phonics** | Contraindicated (N/A) | Effective (\(d=0.52\)) | **Optimal (\(d=0.70\))** | Effective (\(d=0.45\)) | Contraindicated (N/A) | Contraindicated (N/A) | Contraindicated (N/A) | Contraindicated (N/A) |
| **CPA Bar Modeling (Bruner)** | Contraindicated (N/A) | Emerging (\(d=0.30\)) | **Optimal (\(d=0.65\))** | **Optimal (\(d=0.62\))** | Effective (\(d=0.48\)) | Emerging (\(d=0.25\)) | Contraindicated (N/A) | Contraindicated (N/A) |
| **Clinical Deliberate Practice** | Contraindicated (N/A) | Contraindicated (N/A) | Contraindicated (N/A) | Contraindicated (N/A) | Emerging (\(d=0.35\)) | Effective (\(d=0.52\)) | **Optimal (\(d=0.75\))** | **Optimal (\(d=0.88\))** |
| **Socratic Dialogue / Paul-Elder**| Contraindicated (N/A) | Contraindicated (\(d=0.05\)) | Emerging (\(d=0.22\)) | Effective (\(d=0.42\)) | **Optimal (\(d=0.60\))** | **Optimal (\(d=0.68\))** | **Optimal (\(d=0.72\))** | **Optimal (\(d=0.75\))** |
| **Rowe Twin Wait-Time (3s+)** | Contraindicated (N/A) | Emerging (\(d=0.30\)) | **Optimal (\(d=0.68\))** | **Optimal (\(d=0.74\))** | **Optimal (\(d=0.72\))** | **Optimal (\(d=0.70\))** | Effective (\(d=0.55\)) | Effective (\(d=0.50\)) |
| **Diagnostic Hinge Questions** | Contraindicated (N/A) | Contraindicated (\(d=0.12\)) | Effective (\(d=0.54\)) | **Optimal (\(d=0.72\))** | **Optimal (\(d=0.75\))** | **Optimal (\(d=0.78\))** | **Optimal (\(d=0.74\))** | Effective (\(d=0.56\)) |
| **Guided Play / Joint Attention** | **Optimal (\(d=0.80\))** | **Optimal (\(d=0.76\))** | Emerging (\(d=0.32\)) | Contraindicated (N/A) | Contraindicated (N/A) | Contraindicated (N/A) | Contraindicated (N/A) | Contraindicated (N/A) |
| **Executive Function Training** | Effective (\(d=0.45\)) | **Optimal (\(d=0.65\))** | **Optimal (\(d=0.60\))** | Effective (\(d=0.50\)) | Emerging (\(d=0.32\)) | Emerging (\(d=0.28\)) | Contraindicated (\(d=0.10\)) | Contraindicated (N/A) |

---

## 4. Worked Example with Think-Aloud

### Task:
Design a physics unit on Newton's Second Law for two cohorts:
- Cohort A: Grade 7 novice students (Stage S3/S4 boundary, no prior mechanics coursework).
- Cohort B: Second-year undergraduate engineering students (Stage S6, fluent in vector calculus).

### Expert Designer Think-Aloud:
> *"Let's inspect the evidence matrix for S3/S4 vs S6. For Cohort A, their long-term memory lacks schemas for reconciling gravitational acceleration with net force. If I assign an open-ended lab immediately, cognitive load theory predicts failure (\(d < 0.15\)). 
> Looking at the matrix: S3/S4 demands **Worked Example Fading (\(d=0.65\))** followed by **Productive Failure (\(d=0.62\))** with heavy teacher-led consolidation. I will start with an explicit model of \(F_{\text{net}} = ma\) with concrete numbers, fade the final calculation step, then give a structured non-routine problem with a hinge diagnostic question.
> Now for Cohort B: They already possess automated schemas for 1D force balance. Direct instruction on basic force equations will trigger the expertise reversal effect (\(d=0.18\)), causing disengagement and shallow processing. For Cohort B, the evidence matrix indicates **Peer Instruction (\(d=0.68\))** and **Deliberate Clinical Practice (\(d=0.75\))**. I will throw them into a multi-body coupled differential simulation, challenge their intuitive misconceptions about non-inertial reference frames via Mazur peer voting, and mandate critique of real failure telemetry."*

---

## 5. Non-Example / Anti-Pattern

### The Failure: Universal Pedagogical Dogmatism
An EdTech curriculum company deploys an AI tutoring agent that applies identical Socratic questioning and unguided exploratory prompts across all grade levels:
```
AI Tutor (to 7-year-old child in Grade 2 struggling with double-digit subtraction with regrouping):
"What do you think happens when the number on top is smaller than the number on the bottom? Where could you discover a group of ten?"
Child: "I don't know, take the small from the big?"
AI Tutor: "How does that make you feel about the balance of numbers? What experiment could you try?"
```

### Forensic Defect Analysis:
1. **Stage Violation**: In Stage S2, learners do not possess the conceptual schema to discover positional base-10 regrouping through philosophical reflection.
2. **Cognitive Collapse**: The unguided Socratic prompt floods working memory with extraneous search load. The student resorts to the common buggy algorithm ($72 - 38 = 46$ by taking $8 - 2 = 6$).
3. **Evidence Matrix Verdict**: In S2, Socratic dialogue has an effect size of \(d = 0.22\) (sub-threshold), whereas **Direct Instruction (\(d=0.74\))** and **CPA Bar Modeling (\(d=0.65\))** provide the required cognitive scaffold. The AI tutor committed pedagogical malpractice by ignoring stage boundary conditions.

---

## 6. Misconception Diagnostics

| Student Misconception | Diagnostic Symptom | Underlying Epistemic Flaw | Corrective Stage-Matched Intervention |
| :--- | :--- | :--- | :--- |
| **"Constructivism is always superior to Direct Instruction"** | Teacher refuses to model algorithms; expects students to 'invent' matrix multiplication or phonics rules. | Conflating the *goal* of instruction (autonomous constructivist understanding) with the *means* (explicit scaffolding). | Switch to Engelmann Direct Instruction for initial schema acquisition in S2–S3 (\(d=0.74\)). |
| **"Lecture is bad; active learning means physical movement"** | Replacing structured problem solving with superficial group poster-making and unguided gallery walks. | Conflating behavioral activity with cognitive activity. Physical activity without cognitive challenge yields \(d < 0.20\). | Implement Mazur Peer Instruction or Kapur Productive Failure: high cognitive friction, low extraneous behavioral noise. |
| **"Drill and kill is the only way to ensure basic skills"** | Assigning 100 identical massed subtraction worksheets in a single evening. | Confusing massed practice (immediate performance illusion) with spaced retrieval and interleaving (durable retention). | Convert to spaced retrieval waves (\(d=0.74\)) and interleaving (\(d=0.65\)). |

---

## 7. Hinge Question: Diagnostic Decision Check

**Question for Instructional Designers & AI Agents:**
> You are tasked with teaching "Quantum Eigenstates and Hilbert Space Operators" to an advanced Master's physics seminar (Stage S7). Which of the following pedagogical strategies is supported by the highest effect size and lowest expertise-reversal risk?

- [ ] A) High-density Direct Instruction script with scripted choral responses and step-by-step worked example demonstrations of standard matrix diagonalization.
- [ ] B) Completely unguided pure discovery where students are handed Dirac's 1930 textbook with zero scaffolding or diagnostic feedback.
- [x] C) Deliberate Practice with bio-telemetry/expert critique: analyzing anomalous quantum decoherence datasets, identifying mathematical non-unitary violations, and defending solutions in oral defense viva. *(Correct)*
- [ ] D) Concrete-Pictorial-Abstract (CPA) manipulative modeling using physical colored blocks to represent infinite-dimensional Hilbert state vectors.

### Distractor Analysis:
- **Distractor A**: Triggers severe *Expertise Reversal Effect* (\(d = -0.12\)). Master's students already have automated linear algebra; scripted choral response induces cognitive frustration and suppresses authentic schema restructuring.
- **Distractor B**: Pure discovery remains ineffective even for experts (\(d = 0.15\)) due to unconstrained search space without expert corrective feedback loops.
- **Distractor C is Correct**: S7 learners thrive on Deliberate Practice (\(d = 0.88\)) targeting edge-case failures, boundary conditions, and oral viva defense, maximizing productive cognitive friction.
- **Distractor D**: CPA is designed for early foundational operations (S1–S3, \(d = 0.65\)). Physical manipulatives for infinite-dimensional Hilbert spaces introduce catastrophic pedagogical analogies that fail to generalize.

---

## 8. Turn-Key Operational Protocol: Selecting Interventions

```
Step 1: Identify Learner Stage (S0 - S7) via prior schema diagnostic test.
Step 2: Check Cognitive Architecture Constraint:
         - If Novice (S1-S3): Filter for interventions with External Guidance d >= 0.60.
         - If Intermediate (S4-S5): Filter for Dual-Phase Interventions (Productive Failure, Mazur PI).
         - If Advanced (S6-S7): Filter for Deliberate Practice and Socratic Critique.
Step 3: Verify Contraindication Gate:
         - Reject any intervention marked < 0.20 in target stage cell.
Step 4: Execute 3-Part Lesson Loop:
         - Part A: Spaced Retrieval warm-up (5 min).
         - Part B: Core Stage-Matched Intervention (20-30 min).
         - Part C: Formative Hinge Diagnostic Check (5 min).
Step 5: Stopping / Transition Rule:
         - If student score on Hinge Diagnostic >= 85%: Fade guidance up to next stage profile.
         - If student score < 60%: Trigger step-down corrective loop (re-introduce worked examples).
```

---

## 9. Empirical Evidence & Boundary Conditions

| Metric | Empirical Parameter |
| :--- | :--- |
| **Meta-Analytic Dataset** | Hattie (2023) Sequel ($k > 2,100$ meta-analyses, $N > 300\text{M}$ students); EEF Toolkit (2021). |
| **Zone of Desired Effects** | $d \ge 0.40$ (Interventions achieving greater than a year's growth for a year's input). |
| **Expertise Reversal Point** | When working memory capacity spent processing redundant guidance exceeds intrinsic task load ($p < 0.001$, Kalyuga et al., 2003). |
| **Key Limitation** | Effect sizes represent population averages. Domain familiarity within an individual can create intra-subject stage variance (e.g., S6 in History but S2 in Coding). Always assess domain-specific schema, not age alone. |
