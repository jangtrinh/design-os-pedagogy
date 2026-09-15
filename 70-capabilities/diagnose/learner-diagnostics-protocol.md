---
id: capability-learner-diagnostics
title: "Learner Diagnostics Protocol: Clinical Signal Detection & Misconception Deconstruction"
type: capability
stage: ["S2-primary", "S3-secondary", "S4-tertiary"]
axes: ["AX-01: Learning Sciences", "AX-05: Assessment"]
evidence_level: "A"
prerequisites: ["concept-cognitive-load-theory", "practice-formative-hinge-questions"]
leads_to: ["case-eric-mazur-harvard-peer-instruction", "case-grade-7-algebra-worked-examples"]
sources: ["Heritage (2010) Formative Assessment in Practice", "Chi (2013) Refuting Misconceptions", "Wiliam (2011)"]
---

# Learner Diagnostics Protocol: Clinical Signal Detection & Misconception Deconstruction

![Learner Diagnostics Scanner](../../assets/learner_diagnostics_scanner_1789443596318.jpg)

---

## 0. Capability Definition

```
INPUT                               CLINICAL REASONING                           OUTPUT
[ Student Error / Impasse ] ──► [ Classify: Slip vs. Bug vs. Schema ] ──► [ Targeted Refutation / Scaffolding ]
```

An operational, auditable protocol for diagnosing the exact cognitive root cause of learner error and deploying the precise pedagogical remedy without defaulting to blunt, repetitive reteaching.

---

## 1. Trigger Conditions & Contraindications

### When to Activate This Protocol (Triggers)
* A learner selects an incorrect distractor on a diagnostic hinge question.
* A learner exhibits sudden hesitation or latency $> 45$ seconds during a previously fluent problem set.
* A learner's explanation uses colloquial language that contradicts scientific principles (e.g., *"The cold seeped into the room"*).
* A learner makes identical errors across three isomorphic problems.

### When NOT to Activate (Contraindications)
* **Isolated Slips**: A single clerical typo or minor arithmetic oversight made by a fluent student ($\rightarrow$ Prompt: *"Check line 3"* is sufficient).
* **Novel Uninstructed Topics**: When a student has never encountered the concept ($\rightarrow$ Requires initial Direct Instruction, not clinical diagnosis).

---

## 2. The 3-Tier Error Classification Matrix

Never treat all errors as equal. An educator or AI tutor must classify an error into one of three clinical tiers:

```
                                 LEARNER ERROR
                                       │
         ┌─────────────────────────────┼─────────────────────────────┐
         ▼                             ▼                             ▼
   TIER 1: SLIPS                 TIER 2: BUGS             TIER 3: MISCONCEPTIONS
   (Working Memory Lapse)        (Procedural Algorithm)   (Faulty Mental Model)
   ──────────────────────        ──────────────────────   ──────────────────────
   - Careless oversight          - Omitted sub-step       - Coherent, naive theory
   - Student self-corrects       - Flawed rule execution  - Resists blunt correction
   - Quick check suffices        - Requires guided model  - Requires cognitive conflict
```

| Dimension | Tier 1: Careless Slip | Tier 2: Procedural Bug | Tier 3: Deep Epistemic Misconception |
| :--- | :--- | :--- | :--- |
| **Cognitive Cause** | Working memory overload, fatigue, or transient inattention. | Knowledge gap in a specific intermediate algorithmic step. | An intuitively appealing, coherent, but scientifically flawed mental schema. |
| **Example** | Student knows $7 \times 8 = 56$, but writes $54$ while rushing through a 10-step calculus problem. | Student knows fractions, but forgets to invert the second fraction when dividing ($\frac{a}{b} \div \frac{c}{d}$). | Student asserts that $\frac{1}{8} > \frac{1}{3}$ because $8 > 3$ (**Whole Number Bias**). |
| **Learner Reaction When Pointed Out** | *"Oops! I meant 56!"* (Instant self-repair). | *"Wait, how do I divide fractions again?"* (Procedural gap). | *"Of course 1/8 is bigger! Eight is much bigger than three!"* (Fierce defense of false model). |
| **Prescribed Intervention** | Simple prompt: *"Check your arithmetic in step 2."* | Provide a worked example of the missing sub-goal; model the step explicitly. | **Clinical Refutational Protocol**: Cognitive Conflict + Concrete Disconfirming Anomaly + Replacement Schema. |

---

## 3. The 4-Step Clinical Diagnostic Protocol

```
[ Step 1: SIGNAL DETECTION ]
  Administer 100%-sampling diagnostic hinge question. Do not rely on impressions.

[ Step 2: CLINICAL INTERVIEW (Think-Aloud Elicitation) ]
  Prompt: "Walk me through how you arrived at that answer. What was your brain doing?"
  Rule: Active listening without judgment. Do NOT interrupt or correct yet.

[ Step 3: COGNITIVE CONFLICT (Disconfirming Anomaly) ]
  Present a concrete physical case where the learner's flawed rule leads to an absurd result.

[ Step 4: REPLACEMENT SCHEMA & ISOMORPHIC TRANSFER ]
  Introduce the canonical model through a dual-coded representation.
  Require immediate transfer on a novel problem.
```

---

## 4. Worked Clinical Trace: Overcoming Whole Number Bias

### Student Context: Liam (Grade 5)
* **Problem**: Liam calculates $\frac{1}{2} + \frac{1}{3} = \frac{2}{5}$.

#### Step 1: Signal Detection & Classification
* *Observation*: Liam added the numerators ($1 + 1 = 2$) and added the denominators ($2 + 3 = 5$).
* *Clinical Diagnosis*: This is **NOT a Tier 1 slip**. It is a classic **Tier 3 Epistemic Misconception** (*Whole Number Bias*): Liam treats fractions not as single unified numerical magnitudes, but as two independent integer numbers separated by a line.

#### Step 2: Clinical Elicitation
* **Teacher**: *"Liam, walk me through your thinking on this calculation."*
* **Liam**: *"Easy. One plus one is two, and two plus three is five. So it’s two-fifths."*
* **Teacher Think-Aloud**: *"He is completely confident. Direct telling ('No, you need a common denominator') will only produce mechanical compliance without schema change. He needs cognitive conflict."*

#### Step 3: Generating Cognitive Conflict (The Concrete Anomaly)
* **Teacher**: *"Liam, let’s look at just the first fraction: $\frac{1}{2}$. That’s half a pizza, right?"*
* **Liam**: *"Yes."*
* **Teacher**: *"Now, what is your answer: $\frac{2}{5}$? Is two-fifths of a pizza more than half a pizza, or less than half a pizza?"*
* **Liam (Hesitating)**: *"Well... two and a half fifths would be half... so two-fifths is less than half."*
* **Teacher**: *"Look at your equation: you started with half a pizza, added one-third of another pizza to it, and ended up with LESS pizza than you started with. How is that possible?"*
* **Liam (Cognitive Dissonance / Eyes widening)**: *"Wait... that makes no sense! If I add pizza, I should have more than half!"*

#### Step 4: Replacement Model & Transfer
* **Teacher**: *"Exactly. Your rule broke because denominators aren't numbers to add—they tell us the SIZE of the slices. We can't add slices until they are the same size. Let’s bring out our fraction bars and find a slice size that fits both halves and thirds."*
* *(Liam discovers sixths: $\frac{3}{6} + \frac{2}{6} = \frac{5}{6}$. Five-sixths is clearly greater than one-half. Liam’s schema is restructured).*

---

## 5. Non-Example Trace: The "Procedural Band-Aid" Fallacy

**The Anti-Pattern**:
* **Student**: *"I got $\frac{1}{2} + \frac{1}{3} = \frac{2}{5}$."*
* **Teacher**: *"No, Liam, remember: you can't add denominators. You have to find the least common multiple of 2 and 3, which is 6, convert them to $\frac{3}{6}$ and $\frac{2}{6}$, and then add to get $\frac{5}{6}$. Write that down."*

*Why this fails*:
* Liam writes down $\frac{5}{6}$ mechanically to appease the teacher.
* The underlying whole-number misconception was never exposed or dismantled.
* Next Monday, when given $\frac{2}{3} + \frac{1}{4}$, Liam will write $\frac{3}{7}$ again because his mental schema remains unchanged.

---

## 6. AI Tutor Diagnostic State Machine (YAML Protocol)

```yaml
ai_tutor_diagnostic_engine:
  state: DETECT_ERROR
  on_error_detected:
    action: classify_error_tier
    heuristics:
      - condition: "error is a simple arithmetic miscalculation on an otherwise correct method"
        tier: TIER_1_SLIP
        response: "Point out the location: 'Check your calculation on line 2.'"
      - condition: "error skips a known algorithmic sub-goal (e.g. sign change)"
        tier: TIER_2_PROCEDURAL_BUG
        response: "Prompt for the missing sub-goal: 'What happens to the inequality sign when you multiply by a negative?'"
      - condition: "error matches documented domain misconception"
        tier: TIER_3_MISCONCEPTION
        action: trigger_socratic_conflict
        steps:
          1: "Elicit student reasoning: 'Walk me through how you arrived at this result.'"
          2: "Present an extreme boundary case or concrete physical analogy where the rule produces an impossible paradox."
          3: "Guide student to identify the contradiction."
          4: "Introduce canonical visual representation."
          5: "Verify with isomorphic transfer challenge."
```

---

## 7. Empirical Evidence & Meta-Analytic Parameters

| Source | Empirical Scope | Effect Size | Clinical Takeaway |
| :--- | :--- | :--- | :--- |
| **Chi (2013)** | Meta-analysis of refutational texts & conceptual change interventions | $d = 0.78$ | Directly refuting a naive misconception through cognitive conflict produces double the retention and transfer of standard expository teaching. |
| **Heritage (2010)** | Clinical observations of formative assessment in practice | $d = 0.54$ | Teachers who systematically diagnose error types before intervening achieve significantly higher student learning velocity than teachers who deliver immediate procedural corrections. |
| **VanLehn (1990)** | *Mind Bugs: The Cognitive Origins of Transfer Errors in Arithmetic* | Foundational Monograph | Proved that student calculation errors are not random mistakes, but the logical execution of flawed, systematic "buggy algorithms". |
