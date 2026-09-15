---
id: case-ai-synthetic-student-rehearsal
type: case
title: "Clinical Simulation Case: Pre-Service Teacher Rehearsal Against a Synthetic Student"
stage: ["S4-tertiary", "S7-master-pedagogy"]
domain: "teacher-education-stem"
learner_state: "pre-service-teacher-clinical-simulation"
applies: ["practice-synthetic-learners", "capability-learner-diagnostics"]
evidence_basis: ["UMass Amherst NSF Simulated Student Research (2026)", "Markauskaite et al. (2025)"]
prerequisites: ["concept-cognitive-load-theory", "practice-rosenshine-principles"]
leads_to: ["stage-s7-master-pedagogy"]
---

# Clinical Simulation Case: Teacher Rehearsal Against a Synthetic Student

![Learner Diagnostics Scanner](../../assets/learner_diagnostics_scanner_1789443596318.jpg)

---

## 0. Capability Tested in this Clinical Case

After working through this clinical simulation, an educator or teacher mentor will be able to:
* **Navigate** an interactive clinical simulation against an AI **Synthetic Student** with persistent cognitive misconceptions.
* **Overcome** the common novice teacher impulse to engage in unassisted "declarative telling", which fails to dismantle persistent cognitive schemas.
* **Execute** a multi-step refutational sequence (Cognitive Conflict $\rightarrow$ Concrete Anomaly $\rightarrow$ Spatial Re-anchoring) in real time.

---

## 1. Case Intake: The Clinical Flight Simulator

* **Candidate**: Rachel (Age 22, 1st-year pre-service middle school math teacher).
* **Environment**: University Clinical Simulation Lab running `design-os-pedagogy` Synthetic Student Runtime.
* **Target Objective**: Guide the simulated student to understand fraction magnitude comparison ($\frac{1}{8}$ vs. $\frac{1}{5}$) without relying on cross-multiplication tricks.
* **Simulated Student Agent Profile**:
  * Name: Kevin (Grade 6, Age 11).
  * Persona: Friendly, confident, persistent **Whole Number Bias** ($8 > 5 \implies \frac{1}{8} > \frac{1}{5}$).
  * Behavioral Constraint: `persistence_threshold: 2` (Will NOT abandon misconception upon receiving verbal rules; requires concrete disconfirming conflict).

---

## 2. Decision Point 1: The Initial Opening Move

Rachel connects to the simulation. Synthetic Student Kevin appears on screen and types:
> *"Hi Ms. Rachel! I finished the warmup. For Problem 3, $\frac{1}{8}$ is definitely bigger than $\frac{1}{5}$ because eight is a much bigger number than five."*

**You are coaching Rachel in the simulation booth. What is her optimal next move? (Commit before reading further):**

* **Option A**: Tell Kevin directly: *"No Kevin, remember the rule: with fractions, smaller denominators mean bigger pieces. Write that down."*
* **Option B**: Teach Kevin the cross-multiplication "butterfly trick" to get the right answer quickly.
* **Option C**: Ask Kevin a disconfirming question anchored in shared physical reality: *"Kevin, if we share one pizza among 8 people, does each person get a bigger or smaller slice than if 5 people share it?"*
* **Option D**: Give Kevin 10 fraction practice problems to solve on his own.

---

### Diagnostic Distractor Analysis of Options A, B, C, D

| Option | Clinical Diagnosis | Simulation Outcome |
| :--- | :--- | :--- |
| **Option A** | **The Declarative Telling Fallacy** | **Simulation Failure**. Because Kevin has `persistence_threshold: 2`, he pushes back: *"I know the book says that, but that makes no sense because 8 is always bigger than 5."* Rachel's score drops. |
| **Option B** | **The Toxic Mnemonic Trap** | Masks the conceptual void. Kevin learns an algorithm without understanding magnitude, failing future transfer tests. |
| **Option C** | **TARGET (The Master Move)** | **Concrete Cognitive Conflict**. Anchors the denominator in physical partition shares, creating the necessary cognitive dissonance to shatter the Whole Number Bias. |
| **Option D** | **Premature Release Fallacy** | Releasing an ungrounded student to independent work merely automates their misconceptions. |

---

## 3. Evidence Reveal: What Happened During Rachel's Rehearsal

### Round 1: Rachel's Failure to Dismantle the Schema
Rachel chose **Option A**:
* **Rachel**: *"Actually Kevin, fractions are the opposite of whole numbers. When the denominator is bigger, the fraction is smaller. So $\frac{1}{5}$ is bigger."*
* **Synthetic Kevin**: *"Wait, why would eight be smaller than five? In every math class since kindergarten, eight has always been bigger than five. That sounds like a trick."*
* **Rachel (Hesitating, looking at her simulation coach)**: *"He won't accept the rule! What do I do?"*
* **Coach (In earpiece)**: *"Stop explaining the rule. Show him the contradiction in his own life."*

---

### Round 2: The Cognitive Conflict Breakthrough
Rachel pivots to **Option C**:
* **Rachel**: *"Kevin, forget the numbers for a second. Imagine your birthday party. You have one giant chocolate cake. If 8 hungry kids show up, and you cut the cake into 8 equal pieces, is your piece bigger or smaller than if only 5 kids show up?"*
* **Synthetic Kevin (Simulation State Transition: Vertigo)**: *"Whoa... if only 5 kids show up, the pieces are way bigger! If 8 kids show up, you have to cut it into skinnier slices."*
* **Rachel**: *"So what does that bottom number—the denominator—actually tell us about the cake?"*
* **Synthetic Kevin (State Transition: Replacement Schema)**: *"It tells us how many pieces we had to cut it into! More pieces means every piece gets smaller!"*
* **Rachel**: *"So which slice would you rather eat: $\frac{1}{8}$ of a cake or $\frac{1}{5}$ of a cake?"*
* **Synthetic Kevin**: *"$\frac{1}{5}$! Definitely $\frac{1}{5}$!"*
* **Simulation Telemetry**: `[ALERT: Misconception Resolved. Epistemic Debt: 0. Candidate Rachel Score: 96/100]`.

---

## 4. Candidate Debrief & Clinical Scorecard

```
CANDIDATE: Rachel Vance
CLINICAL EXERCISE: Fraction Misconception Deconstruction
SIMULATION RUNTIME: design-os-pedagogy v2026.1

CLINICAL METRICS:
- Time to Diagnose Misconception: 18 seconds (EXCELLENT)
- Initial Strategy: Declarative Telling (PENALTY -10)
- Adaptation to Student Pushback: Pivot to Concrete Analogy (BONUS +15)
- Student Active Cognitive Work: 82% of words spoken by student (EXCELLENT)
- Concept Automation Gate: Passed unassisted isomorphic transfer (1/6 vs 1/9)

FINAL SCORE: 96 / 100 (HIGH PROFICIENCY)
COACHING RECOMMENDATION: Ready for live classroom student teaching.
```

---

## 5. Transfer Simulation Drill for Candidates

Replay this clinical case against **Persona 1: The Anxious/Silent Novice**. The student will respond with single-word answers (*"Don't know"*, *"Maybe"*). 
* *Challenge*: How does the candidate establish psychological safety and co-regulation before introducing the cake analogy?
