# Universal Pedagogical Authoring Specification & Blueprint

This document defines the **mandatory authoring contract** for all instructional and knowledge files within `design-os-pedagogy`. 

> [!IMPORTANT]
> **The Pedagogical Imperative**:
> An educational repository about pedagogy that is written non-pedagogically is a fundamental failure. If a reader (human educator or autonomous AI tutor) only reads passive declarative definitions, no meaningful schema acquisition or conceptual change occurs.
> 
> **The Canonical Content Unit**:
> $$\text{Knowledge} + \text{Experience} + \text{Diagnosis} + \text{Practice} + \text{Feedback} + \text{Transfer} + \text{Protocol}$$
> 
> A file containing only $\text{Knowledge}$ is **incomplete by specification**.

---

## 1. The Minimum Pedagogical Anatomy

Every substantive document in this system must incorporate the following components:

| Component | Mandatory Purpose |
| :--- | :--- |
| **0. Learning Contract** | Explicit, observable capabilities using behavioral verbs (*diagnose, select, design, adapt, critique*). Avoid vague verbs like "understand". |
| **1. The Intuitive Puzzle** | An authentic classroom/tutoring dilemma that exposes the limits of naive intuition. |
| **2. Active Commitment** | Forcing the reader to make a prediction or select a hypothesis *before* the theoretical explanation. |
| **3. Core Mental Model** | The underlying causal cognitive mechanism, supported by dual coding (visual asset + verbal structure). |
| **4. Worked Example** | Step-by-step canonical execution with **expert think-aloud** revealing hidden clinical decisions. |
| **5. Non-Example / Anti-Pattern** | Contrasting case demonstrating common pseudopedagogical failure or superficial implementation. |
| **6. Misconception Diagnostic** | Catalog of specific naive mental models, diagnostic cues, disconfirming experiences, and replacement models. |
| **7. Hinge Question & Distractor Map**| A diagnostic checkpoint where **every distractor diagnoses a specific misconception**, paired with remediation routing. |
| **8. Guided & Independent Practice** | Partial scaffolding fading into full independent problem solving and near/far transfer. |
| **9. Turn-Key Implementation Protocol** | Concrete, reproducible protocol (teacher moves, dialogue scripts, or AI tutor state machine). |
| **10. Evidence & Boundary Conditions**| Explicit empirical ratings (Meta-analysis, Cohen's $d$, Hedges' $g$), target population, and where the principle breaks (e.g. Expertise Reversal). |

---

## 2. Document Archetypes

### Archetype A: Foundational Learning Sciences (`10-foundations/`)
* **Core Purpose**: Restructure the reader's causal mental model of human cognitive architecture and learning processes.
* **Key Focus**: Biological and psychological mechanisms (Working Memory, Executive Functions, Self-Determination, Consolidation, Retrieval).
* **Required Sections**:
  1. Learning Contract (Prerequisites, Observable Competencies, Diagnostic Prediction)
  2. The Instructional Dilemma (Why intuitive teaching fails)
  3. Prediction Challenge (Commitment before reveal)
  4. The Underlying Cognitive Mechanism (Step-by-step architecture)
  5. Worked Clinical Example with Expert Think-Aloud
  6. Non-Example / Pathological Case (Superficial execution)
  7. Common Misconceptions & Refutational Sequence
  8. Formative Hinge Question with 4-Distractor Diagnostic Map
  9. Guided Rehearsal & Transfer Scenario
  10. Actionable Classroom & AI Tutor Execution Protocol
  11. Empirical Evidence, Effect Sizes & Boundary Conditions

### Archetype B: Life-Stage Pedagogical Guides (`20-stages/` S0–S7)
* **Core Purpose**: Answer: *Who is this learner developmentally, what cognitive constraints operate now, and how must instructional moves adapt?*
* **Required Sections**:
  1. Stage Capability Contract
  2. Learner Profile & Vignette (Authentic classroom/home scenario)
  3. Developmental Neuro-Cognitive Profile (EF, working memory, language, metacognition)
  4. Ranked Pedagogical Priorities (Top 3–5 with "What Good Practice Looks Like" vs. "Toxic Anti-Patterns")
  5. Misread-the-Learner Matrix (Surface behavior $\rightarrow$ Naive punitive view $\rightarrow$ Developmental root cause)
  6. Fully Worked Lesson Scenario (Objective $\rightarrow$ Teacher Move $\rightarrow$ Learner Signal $\rightarrow$ In-flight Adaptation)
  7. Annotated Dialogue Scripts (Master Scaffolding vs. Failed Scaffolding)
  8. Hinge Observations & Diagnostic Rubric
  9. AI Tutoring State Machine & Fading Policies
  10. Implementation Protocol (Before, During, and After Session)

### Archetype C: Instructional Methods & Frameworks (`30-pedagogy/`)
* **Core Purpose**: Equip the educator or AI agent to execute an evidence-based method with procedural and clinical fidelity.
* **Required Sections**:
  1. Capability Contract
  2. The Instructional Problem Solved (What unguided learning fails to do)
  3. Preconditions & Contraindications (When to use vs. when NOT to use)
  4. Method Anatomy & Expert Think-Aloud ($I\ Do \rightarrow We\ Do \rightarrow You\ Do$)
  5. Fully Worked Classroom Execution Transcript
  6. Superficial / Pathological Implementation
  7. Diagnostic Hinge Question for Instructional Decision-Making
  8. Adaptation Matrix (Novice vs. Advanced vs. Group vs. AI Tutor)
  9. Fidelity Checklist & Failure Mode Recovery
  10. Empirical Evidence & Meta-Analytic Effect Sizes

### Archetype D: Disciplinary Pedagogies (`40-disciplines/`)
* **Core Purpose**: Codify how domain-specific epistemologies, representations, and threshold concepts alter instructional delivery.
* **Key Focus**: STEM (CER, modeling, bar models), Humanities (historical sourcing, corroboration), etc.

### Archetype E: Clinical Case Simulations (`50-practice-library/cases/`)
* **Core Purpose**: Simulate authentic clinical judgment under uncertainty.
* **Interactive Flow**:
  $$\text{Case Intake} \rightarrow \mathbf{Decision\ Point\ 1\ (Commit)} \rightarrow \text{Evidence Reveal} \rightarrow \mathbf{Decision\ Point\ 2} \rightarrow \text{Intervention} \rightarrow \text{Debrief \& Counterfactuals}$$

### Archetype F: Operational Capability Protocols (`70-capabilities/`)
* **Core Purpose**: Algorithmic, machine-auditable state-machine protocols for real-time pedagogical diagnosis, scaffolding, and fading.

---

## 3. Hinge Question Diagnostic Standard

A hinge question is an instructional diagnostic instrument, not an arbitrary quiz.
* **Every question must have exactly 1 target answer and 3–4 functional distractors.**
* **Each distractor must state plausible explanations and a follow-up probe that distinguishes them.**
* **A selected answer alone does not establish a unique mental model. Elicit reasoning when evidence is ambiguous, retain an insufficient-evidence state, and verify the interpretation before choosing an intervention.**

Example Schema:
```yaml
hinge_question:
  stem: "Scenario prompt requiring conceptual application"
  options:
    A: "Plausible answer reflecting Misconception 1"
    B: "Plausible answer reflecting Misconception 2"
    C: "Target canonical answer"
    D: "Plausible answer reflecting Overgeneralization"
  distractor_analysis:
    A: "Reveals belief that ...; remediate via ..."
    B: "Reveals confusion between ... and ...; remediate via ..."
    C: "Demonstrates correct integration of ..."
    D: "Applies rule beyond its valid boundary; remediate via ..."
  remediation_routing:
    A: "Redirect to Section 4 with worked counter-example"
    B: "Prompt self-explanation comparing Case X and Case Y"
    C: "Proceed to independent transfer challenge"
    D: "Present boundary condition test case"
```

---

## 4. Definition of Done (DoD) Gate

Before committing any document in `design-os-pedagogy`, verify:
1. **Zero Pure Declarative Exposition**: Does the document contain active learning tasks?
2. **Commitment Required**: Is the reader forced to predict or choose before the answer is revealed?
3. **Misconceptions Explicitly Mapped**: Are plausible errors diagnosed and refuted?
4. **Worked Examples Annotated**: Does the worked example expose the invisible clinical reasoning?
5. **Operational Protocol Provided**: Can a teacher or AI execute this tomorrow morning?
6. **Zero Broken Links / 404s**: Are all visual asset paths verified and relative?
