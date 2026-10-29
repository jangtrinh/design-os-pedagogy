---
id: practice-process-based-assessment-viva
title: "Process-Based Assessment & The Adaptive Viva: The Death of the Take-Home Essay in the AI Era"
type: practice
stage: ["S3-secondary", "S4-tertiary", "S5-postgraduate", "S6-adult"]
axes: ["AX-05: Assessment", "AX-07: Educational Technology & AI", "AX-08: Ethics"]
evidence_level: "A"
prerequisites: ["practice-backward-design-ubd", "practice-ai-assistance-ladder"]
leads_to: ["stage-s4-tertiary", "stage-s5-postgraduate-doctoral"]
sources: ["TEQSA Assessment Reform in the Age of AI (2025-2026)", "Jisc Reimagining Assessment in Tertiary Education (2025)", "UNESCO Higher Education Guidelines (2024)", "Git documentation, git-commit: --date option and COMMIT INFORMATION (https://git-scm.com/docs/git-commit, accessed 2026-10-29)"]
---

# Process-Based Assessment & The Adaptive Viva: Beyond the Take-Home Essay

![Doctoral Viva Colloquium](../../assets/doctoral_viva_colloquium_1789440008026.jpg)

---

## 0. Capability Contract

After studying this master module, an educator, university dean, or AI assessment architect will be able to:
* **Dismantle and replace** the compromised "standalone take-home essay" with a valid, tamper-resistant **Proof-of-Learning Bundle**.
* **Eliminate** reliance on unreliable "AI detector" software (which exhibits high false-positive rates and discriminates against non-native English writers).
* **Execute** the 5-Probe **Adaptive Oral Viva Voce** protocol to evaluate whether the learner genuinely owns the reasoning within an AI-assisted deliverable.
* **Operationalize** the core assessment distinction:
  $$\mathbf{Authorship \ne Mastery}$$

> **Pre-reading Recognition Challenge**:
> A university professor suspects that a student used an LLM to write their 3,000-word term paper on European economic integration. The professor pastes the essay into a commercial "AI Detector", which returns a score of: *"94% Probability AI-Generated"*. The professor immediately files an academic integrity violation.
> The student vehemently denies cheating, claiming they wrote the paper with assistance from spellcheck and grammar suggestions.
> 
> *Before reading further, diagnose the systemic assessment failure: Why is relying on AI detectors an empirical and legal failure? What valid assessment instrument should have been used instead?*
> 
> *Analysis*: Commercial AI detectors have an unacceptably high false-positive error rate ($> 15\%$), and penalize non-native English speakers who write in formal, structured syntactic patterns (Liang et al., Stanford 2023). Accusing a student based on statistical text detectors destroys institutional trust and fails legal due process. The valid assessment solution is not catching the AI; it is **demanding proof of learning through process traces and an oral viva voce defense**. If the student cannot explain the economic trade-offs in an oral interview, mastery is disproven regardless of how the text was generated.

---

## 1. The Post-2024 Assessment Crisis

From 1850 to 2022, academic institutions used written text as a reliable proxy for internal human cognition:
$$\text{Polished Written Artifact} \approx \text{Internal Conceptual Schema}$$

In the age of frontier Large Language Models, this proxy has permanently collapsed. Polished, grammatically pristine text can be generated for pennies in milliseconds.
* **If we only assess the final text, we assess the capability of the machine, not the learner.**
* **If we ban AI and enforce retrofitted exams, we assess memorization under panic rather than authentic modern professional practice.**

The international consensus among assessment regulatory bodies (Australia's **TEQSA 2025–2026**, UK's **Jisc**, and **UNESCO**) establishes a new paradigm: **Process-Based Assessment & Verified Defense**.

---

## 2. The Proof-of-Learning Bundle

In place of a single submitted document, students submit a five-part **Proof-of-Learning Bundle**:

```
┌────────────────────────────────────────────────────────────────────────┐
│ THE PROOF-OF-LEARNING BUNDLE (Valid Mastery Architecture)             │
├────────────────────────────────────────────────────────────────────────┤
│ 1. THE FINAL ARTIFACT                                                  │
│ The finished synthesis, report, code repo, or policy brief. (20% Weight)│
├────────────────────────────────────────────────────────────────────────┤
│ 2. THE PROCESS TRACE & VERSION HISTORY                                 │
│ Time-stamped diff logs showing keystroke evolution, major structural   │
│ reorganizations, and drafting iterations over days. (20% Weight)       │
├────────────────────────────────────────────────────────────────────────┤
│ 3. AI PROVENANCE & PROMPT LOG                                          │
│ Transparent log declaring what tools were used, exact prompt transcripts,│
│ and reflections on what was accepted, rejected, or edited. (15% Weight) │
├────────────────────────────────────────────────────────────────────────┤
│ 4. DECISION RATIONALE LOG                                              │
│ Explicit justification of key technical/historical choices:            │
│ "Why did you choose Algorithm A over Algorithm B?" (15% Weight)        │
├────────────────────────────────────────────────────────────────────────┤
│ 5. THE ADAPTIVE ORAL VIVA VOCE (The Defense Gate)                      │
│ A 5-10 minute structured oral defense probing reasoning ownership.     │
│ Mandatory prerequisite to receive credit. (30% Weight)                 │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. The 5-Probe Adaptive Oral Defense Engine

To conduct an oral viva efficiently at scale (by human faculty or authenticated Socratic AI agents), apply the 5-Probe Protocol:

```
                  THE 5-PROBE ADAPTIVE VIVA ARCHITECTURE
                                    │
                                    ▼
[ PROBE 1: DECISION EXPLANATION ]
"Explain the core trade-off on page 4. Why did you choose this architecture?"
                                    │
                                    ▼
[ PROBE 2: COUNTERFACTUAL ADJUDICATION ]
"What empirical evidence would force you to reject your primary conclusion?"
                                    │
                                    ▼
[ PROBE 3: AI PROVENANCE AUDIT ]
"In your prompt log, the AI suggested Model X. Why did you reject it?"
                                    │
                                    ▼
[ PROBE 4: SENSITIVITY & EDGE-CASE PROBING ]
"What happens to your system's stability if parameter Z drops to zero?"
                                    │
                                    ▼
[ PROBE 5: UNASSISTED LIVE TRANSFER (The S0 Gate) ]
"Here is a related, simpler problem. Solve it on the whiteboard right now
 without any software assistance."
```

*If a learner can defend their decisions, explain rejected alternatives, and solve an unassisted transfer problem, they own the mastery—even if 50% of the initial text was drafted with an AI assistant.*

---

## 4. Worked Assessment Trace: Undergraduate Engineering Project

### The Capstone: Autonomous Drone Navigation System

#### The Submission
Student Marcus submits a working Python codebase implementing a Kalman filter for sensor fusion. The code contains advanced matrix mathematics.

#### The Viva Voce Defense (10 Minutes)
* **Professor**: *"Marcus, walk me through line 42. You define the measurement noise covariance matrix $R$. Where did you get the numerical values for the diagonal entries?"*
* **Marcus**: *"I started with values from the IMU datasheet, but when I ran physical tests, the rotor vibrations introduced high acoustic noise. In my prompt log (Page 12), I asked Claude to suggest noise filtering techniques. Claude suggested a low-pass Butterworth filter. But I rejected that because it introduced a 15ms phase lag that caused the drone to oscillate. Instead, I quadrupled the accelerometer variance values in matrix $R$ to make the filter rely more heavily on the optical flow sensor."*
* **Professor**: *"Brilliant engineering judgment. Now, take this marker. Suppose the optical flow sensor is blinded by direct sunlight. Draw the modified state vector and explain how your algorithm handles the sensor dropout."*
* **Marcus**: Walks to the whiteboard, draws the covariance divergence, and explains the covariance update rule without hesitation.
* **Verdict**: **100% Mastery Verified (Grade: A+)**. Marcus legitimately leveraged AI as an epistemic partner, understood every line of code, audited the AI's suggestions, and demonstrated unassisted transfer.

---

## 5. Formative Hinge Question & Diagnostic Map

### The Hinge Diagnostic Item
A university curriculum committee is debating assessment reform in response to generative AI. Which assessment design is most resilient against AI plagiarism while simultaneously cultivating higher-order cognitive capabilities?

* **A)** Ban all laptops and cellphones from campus and return 100% of course assessments to 3-hour handwritten bluebook memorization exams in sports arenas.
* **B)** Require all students to run their essays through an institutional AI detector and achieve an "AI score below 10%" before submission.
* **C)** Replace high-stakes unmonitored take-home writing with a Proof-of-Learning portfolio (process logs + AI prompt provenance) concluded by a 5-minute structured oral viva defense.
* **D)** Abandon grading completely and give all students automatic passing grades based on attendance.

---

### Diagnostic Distractor Analysis & Routing

| Option | Diagnosis | Underlying Assessment Fallacy | Immediate Remediation Route |
| :--- | :--- | :--- | :--- |
| **Option A** | **Misconception**: Retrogressive Panic Trap | Tests low-level timed memorization under acute stress; fails to prepare students for real-world professional practice where modern tools are ubiquitous. | Review Section 1 on authentic assessment. |
| **Option B** | **Misconception**: Technological Panacea Illusion | Relies on flawed detector algorithms that generate false accusations and encourage students to "game" the detector rather than learn. | Re-read Pre-reading Challenge. |
| **Option C** | **TARGET (Correct)** | **Proof-of-Learning Architecture**: Combines process transparency with oral defense to verify genuine ownership of reasoning. | **Proceed to Rubric Implementation**. |
| **Option D** | **Misconception**: Nihilistic Abdication | Eliminates accountability and certification of competence. | Review Section 2: Component weights. |

---

## 6. Empirical Evidence & Policy Accords

| Authority / Study | Year & Scope | Key Policy Directive |
| :--- | :--- | :--- |
| **TEQSA (Tertiary Education Quality and Standards Agency)** | 2025–2026 Assessment Reform Framework | Mandates Australian universities move away from unproctored written essays toward programmatic, authentic, and oral viva assessment models. |
| **Jisc UK Tertiary Review** | 2025 National Report | Recommends multi-evidence portfolios and viva voce interviews as the gold standard for authentic institutional credentialing. |
| **Liang et al. (Stanford University, 2023)** | PNAS study on AI detectors | Demonstrated that commercial AI detectors consistently misclassify writing by non-native English speakers as AI-generated over 61% of the time, proving they are legally and pedagogically invalid. |

---

## 7. Extension: The Commit Trail as Process Evidence

> **Status:** authored extension, `unreviewed`, not piloted. **Idea lineage:** treating per-chapter commits on a personal study branch as a record of study comes from the "proof of work" chapter of *The Craft of Self-Teaching* (自学是门手艺) by Li Xiaolai, [github.com/xiaolai/the-craft-of-selfteaching](https://github.com/xiaolai/the-craft-of-selfteaching) (CC BY-NC-ND 3.0), restated here in our own words with no passage translated or adapted. The book offers the history as proof of reading; this section downgrades it to a **signal** that must be paired with the viva.

### 7.1. Mechanism

1. The learner forks the course repository (or creates their own), and works on a branch named for study, for example `study`.
2. After each unit the learner commits their exercises and notes, with a message stating what they tried, what failed and what they changed.
3. The commit trail becomes one input to Bundle component 2 (Process Trace & Version History). It does **not** add a new weighted component; the Section 2 weights are unchanged.
4. Before the viva, the assessor picks 2–3 commits and turns them into probes.

### 7.2. Signal, Not Proof

A commit shows that certain files had certain contents under a certain recorded identity and time. It does not show who did the thinking, whether an AI produced the diff, or whether the learner understands it. The recorded metadata is also learner-controlled: Git lets the committer override the author date with `--date` and set author and committer identity and dates through environment variables such as `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE` ([git-commit documentation](https://git-scm.com/docs/git-commit), OPTIONS and COMMIT INFORMATION, accessed 2026-10-29). Treat dates and spacing as claims to be discussed, not as timestamps to be trusted.

| What the trail can do | What it cannot do |
| :--- | :--- |
| Supply concrete material for Probe 1 ("walk me through this diff") and Probe 4 ("what if this input changed?") | Establish authorship or mastery on its own |
| Show revisions the learner can be asked to justify | Prove when work happened |
| Let the learner find their own earlier misconceptions | Be scored by commit count, frequency or streak length |

### 7.3. Pairing with the 5-Probe Viva

```yaml
commit_trail_probes:
  sample: "2-3 commits chosen by the assessor, including at least one the learner did not pre-select"
  probe_1_decision: "In this commit you changed X to Y. What were you trying to fix?"
  probe_2_counterfactual: "What would have happened if you had kept X?"
  probe_5_live_transfer: "Redo a small piece of this change now, without the repository open."
  decision_rule: "Credit comes from the viva answers. A rich trail with weak answers is not mastery; a thin trail with strong answers is not misconduct."
```

### 7.4. Non-Example: Gaming by Bulk Commits

A course awards marks for "at least one commit per unit". The night before the deadline, a learner pastes AI-generated solutions into the repository and makes 30 commits in twenty minutes, one per unit, with messages copied from the unit titles. The rubric is satisfied and the trail looks complete. Scoring the trail rewarded the behaviour; nothing in it was tested. The repair is not a stricter commit rule (any rule on count, spacing or message length can be produced the same way) but removing the trail from scoring and using it only as probe material in 7.3.

### 7.5. Hinge Item & Diagnostic Map

**Item:** A programme adds commit trails to its proof-of-learning bundle. Which policy is consistent with Section 7?

| Option | Policy | Diagnosis | Follow-up probe / route |
| :--- | :--- | :--- | :--- |
| **A** | Award 10% of the grade for having at least one commit per week | Treats activity as evidence of learning; invites the gaming in 7.4 | "What would a learner who wants the 10% without learning do?" Re-read 7.4. |
| **B** | Use the commit dates to prove the work was not done at the last minute | Treats learner-editable metadata as a trusted timestamp | "Who can set a commit's date?" Re-read 7.2. |
| **C** | Use the trail only as material for viva probes; credit depends on the defence | **Target** | Proceed to drafting the 7.3 probes for one assignment. |
| **D** | Drop the viva for learners whose trails look detailed | Treats a strong signal as proof; reverses Authorship ≠ Mastery | "What does a detailed trail tell you about Probe 5?" Re-read 7.2. |

If a reviewer picks C but would still penalise a thin trail, treat the evidence as mixed and ask how a strong viva with a thin trail would be graded.

### 7.6. Boundaries and Ethics

* **Evidence status:** **authored and untested.** No study of commit histories as learning evidence was opened in this run; no reliability or validity claim is made for them.
* **Privacy and control:** learners choose a private repository if they wish; public forks expose drafts and mistakes. Do not install keystroke or screen monitoring to "complete" the trail.
* **Equity:** learners new to Git need a short setup task first; a missing trail caused by tooling access is not evidence of anything.
* **Not adopted from the book:** the suggestion that public study records might one day outweigh formal credentials is outside this module's scope and is not endorsed.
