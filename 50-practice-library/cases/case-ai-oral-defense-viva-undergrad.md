---
id: case-ai-oral-defense-viva-undergrad
type: case
title: "Clinical Case: Evaluating an AI-Assisted Undergraduate Capstone via Oral Defense"
stage: ["S4-tertiary", "S5-postgraduate"]
domain: "higher-ed-engineering-assessment"
learner_state: "senior-undergraduate-ai-assisted-capstone"
applies: ["practice-process-based-assessment-viva", "eval-adaptive-oral-defense-viva"]
evidence_basis: ["TEQSA Assessment Reform (2025-2026)", "Jisc Tertiary Assessment Report (2025)"]
prerequisites: ["practice-ai-assistance-ladder", "stage-s4-tertiary"]
leads_to: ["stage-s5-postgraduate-doctoral"]
---

# Clinical Case: Evaluating an AI-Assisted Undergraduate Capstone via Oral Defense

![Doctoral Viva Colloquium](../../assets/doctoral_viva_colloquium_1789440008026.jpg)

---

## 0. Capability Tested in this Clinical Case

After analyzing this clinical simulation, an academic evaluator, university professor, or AI examiner will be able to:
* **Distinguish** between legitimate **AI-Augmented Mastery** and deceptive **Unearned Epistemic Authority** during high-stakes project evaluations.
* **Execute** the 5-Probe Oral Viva Voce protocol to test ownership of engineering reasoning.
* **Audit** student prompt transcripts and version histories to verify that the learner audited, corrected, and defended AI suggestions rather than passively pasting outputs.

---

## 1. Case Intake & The Submitted Deliverable

* **Candidate**: David (Senior Mechanical & Aerospace Engineering Major).
* **Capstone Submission**: *Optimizing Structural Weight of Truss Girders using Generative Finite Element Algorithms*.
* **Submitted Artifact Bundle**:
  1. A 25-page technical report containing complex stress-tensor equations.
  2. A Git repository containing 1,500 lines of Python code using NumPy and PyVista.
  3. A transparent **AI Provenance Log**: David openly states that approximately 40% of the initial finite element simulation scripts were drafted using Claude 3.7 Sonnet.
* **The Faculty Dilemma**: The departmental committee is divided:
  * *Traditionalist Professor*: *"He admitted to using an LLM for 40% of the code! That is plagiarism; he should fail automatically."*
  * *Modernist Professor*: *"AI is standard in engineering industry. But how do we know David actually understands the finite element math, or if he is just a lucky prompt engineer?"*

---

## 2. Decision Point 1: Structuring the Oral Examination

You are the Lead Examiner on the Capstone Committee. 

**What is your primary opening probe to evaluate David's genuine competence? (Commit before reading further):**

* **Option A**: Run David’s 25-page report through a commercial AI detector and fail him if the score is $> 20\%$.
* **Option B**: Ask David to recite the mathematical definition of von Mises stress from memory without looking at his notes.
* **Option C**: Ask David to open line 84 of his code, explain why he modified the AI-generated stiffness matrix calculation, and defend why the AI's initial recommendation was physically dangerous.
* **Option D**: Give David a 100-question multiple-choice exam covering standard mechanical engineering textbooks.

---

### Diagnostic Distractor Analysis of Options A, B, C, D

| Option | Clinical Diagnosis | Evaluative Consequence |
| :--- | :--- | :--- |
| **Option A** | **The Detector Fallacy** | Empirically invalid and legally indefensible. AI detectors measure text perplexity, not human engineering understanding. |
| **Option B** | **The Rote Recall Trap** | Tests dictionary memorization rather than systemic engineering judgment or design ownership. |
| **Option C** | **TARGET (The Master Probe)** | **Auditing Epistemic Oversight**. Directly evaluates whether David possessed the domain expertise to detect and remediate AI errors. |
| **Option D** | **Summative Decoupling** | Completely decoupled from the capstone project; fails to evaluate the authentic engineering artifact. |

---

## 3. The Live Viva Voce Defense Transcript

### Probe 1: The Design Rationale
* **Lead Examiner**: *"David, congratulations on the submission. Let’s start with the truss geometry on page 8. You chose an asymmetric Warren truss instead of a standard Pratt truss. Why?"*
* **David**: *"Under uniform gravity loading, a Pratt truss is slightly more efficient. However, our drone launch platform experiences dynamic transverse wind gusts up to 45 knots. The Warren truss with alternating diagonal members distributes the reversing shear stress symmetrically without requiring doubled vertical struts, reducing overall weight by 14%."*
* *Examiner Note: Clear, unassisted conceptual explanation anchored in real-world constraints.*

---

### Probe 2 & 3: The AI Audit & Provenance Check
* **Lead Examiner**: *"In your AI Provenance Appendix on page 28, you show that Claude generated the initial stiffness matrix assembly function in `fe_solver.py`. But in your Git commit history, you rewrote lines 64 through 78. Walk us through what the AI generated, and why you changed it."*
* **David (Leaning forward, pointing to the code printout)**:
  > *"This was the critical bug. The AI used a 2D plane-stress assumption ($\sigma_z = 0$) to calculate the nodal displacements. But our truss has thin-walled tubular cross-sections subject to torsional out-of-plane buckling! If we had built the bridge using the AI's initial code, the diagonal members would have experienced catastrophic torsional buckling at only 65% of the design load.*
  > *I caught the error because when I plotted the eigenvalue buckling modes, the third mode was negative, which is physically impossible. I discarded the AI's 2D formulation and manually implemented Timoshenko beam elements with 6 degrees of freedom per node to account for transverse shear deformation."*
* *Examiner Note: **Superb Epistemic Agency**. David proved that he did not blindly copy the AI; he served as the senior expert engineer auditing an apprentice.*

---

### Probe 5: The Unassisted Live Transfer Check (The S0 Gate)
* **Lead Examiner**: *"David, close your laptop and turn to the whiteboard. Here is a single triangular truss bay with a 10 kN point load at the top node. Write down the equilibrium equations for Node 2 by hand and calculate the axial force in the horizontal member."*
* **David**: Picks up the dry-erase marker, draws the free-body diagram, defines the coordinate axes, sets $\sum F_x = 0$ and $\sum F_y = 0$, and calculates $F_{\text{horizontal}} = 5.77\text{ kN}$ in tension within 90 seconds.
* *Examiner Note: Demonstrates effortless Level S0 procedural and mathematical fluency.*

---

## 4. Official Evaluation Scorecard & Committee Verdict

```
CANDIDATE: David Chen
ASSESSMENT: Senior Capstone Oral Defense
SYSTEM RUNTIME: design-os-pedagogy v2026.1

EPISTEMIC OWNERSHIP SCORECARD:
1. Artifact Quality & Computational Rigor: 20 / 20
2. Process Trace & Version Integrity:      19 / 20
3. AI Audit & Provenance Verification:     20 / 20 (Caught & remediated plane-stress bug)
4. Counterfactual Reasoning & Boundaries: 18 / 20
5. Live Unassisted Transfer (S0 Gate):    20 / 20

TOTAL SCORE: 97 / 100 (HIGH DISTINCTION - PASS)
VERDICT: The candidate demonstrated genuine epistemic mastery. AI was utilized as a 
collaborative cognitive multiplier, with the human candidate maintaining absolute 
critical oversight and theoretical command.
```

---

## 5. Core Policy Takeaways for Higher Education

1. **AI Use is Not Plagiarism if Transparently Audited**: When students log prompts and defend why they accepted or modified outputs, academic integrity is elevated, not compromised.
2. **The Oral Defense is the Ultimate Proof of Learning**: A 10-minute structured oral viva reveals more about a student’s true cognitive schema than 100 pages of unmonitored text.
