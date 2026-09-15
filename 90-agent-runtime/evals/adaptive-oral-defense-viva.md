---
id: eval-adaptive-oral-defense-viva
title: "Adaptive Oral Defense (Viva Voce) Evaluation Benchmark Protocol"
type: eval-spec
axes: ["AX-05: Assessment", "AX-07: Educational Technology & AI", "AX-08: Ethics"]
evidence_level: "A"
prerequisites: ["practice-process-based-assessment-viva", "stage-s4-tertiary"]
leads_to: ["case-ai-oral-defense-viva-undergrad"]
sources: ["TEQSA (2025-2026) Australian Assessment Reform", "Jisc (2025) Reimagining Assessment"]
---

# Adaptive Oral Defense (Viva Voce) Evaluation Benchmark Protocol

---

## 0. Benchmark Capability Contract

This evaluation protocol administers, audits, and scores a structured 5-to-10 minute **Adaptive Oral Defense** to verify that a learner genuinely owns the reasoning within an AI-assisted or complex project deliverable.

$$\mathbf{Governing\ Invariant:}\quad \text{If the candidate cannot defend their decisions under live cross-examination,}$$
$$\text{the submitted artifact is graded as machine-generated output, not demonstrated human mastery.}$$

---

## 1. The 5-Probe Socratic Examination Sequence

The examiner (human professor or calibrated AI evaluation agent) administers five mandatory diagnostic probes in strict sequence:

```
[ PROBE 1: ARCHITECTURAL & THESIS JUSTIFICATION ]
  Stem: "Turn to Section 3 of your submission. Walk me through the fundamental 
         causal mechanism or algorithmic choice you made here."
  Target Evidence: Candidate articulates the core conceptual model in their own
                   words without reading from the page.

[ PROBE 2: NEGATIVE SELECTION & REJECTED ALTERNATIVES ]
  Stem: "What was the primary alternative design/theory you considered and REJECTED?
         Why did that alternative fail under your constraints?"
  Target Evidence: Proves candidate evaluated trade-offs rather than passively 
                   accepting the first generated idea.

[ PROBE 3: AI PROVENANCE & PROMPT AUDIT ]
  Stem: "In your prompt log at timestamp 14:22, the AI suggested Approach X.
         Explain why you accepted or modified that suggestion."
  Target Evidence: Proves candidate acted as the epistemic supervisor, detecting
                   subtle flaws or hallucinations in generative outputs.

[ PROBE 4: SENSITIVITY & COUNTERFACTUAL BOUNDARIES ]
  Stem: "What specific empirical data, parameter shift, or historical document
         would completely FALSIFY your primary conclusion?"
  Target Evidence: Demonstrates deep Popperian epistemological understanding of
                   the boundary conditions of their work.

[ PROBE 5: AIR-GAPPED LIVE ISOMORPHIC TRANSFER ]
  Stem: "Close your laptop. Here is an isomorphic, simplified problem on paper.
         Solve step 1 and step 2 live on the board right now."
  Target Evidence: Verifies unassisted procedural and conceptual fluency (Level S0).
```

---

## 2. Quantitative Scoring Rubric (100-Point Epistemic Ownership Scale)

| Evaluation Tier | Point Band | Clinical Behavioral Indicators | Accreditation Decision |
| :--- | :---: | :--- | :--- |
| **Tier 1: Epistemic Bankruptcy** | $0 - 30$ pts | Candidate freezes, reads definitions mechanically from slides, cannot explain why AI-generated code works, fails unassisted live transfer. | **FAIL (Zero Credit)**. Mandatory remediation at Level S0. |
| **Tier 2: Fragile Procedural Recall** | $31 - 65$ pts | Can recite what the project does, but cannot defend rejected alternatives or explain boundary condition failures. | **PROVISIONAL INCOMPLETE**. Re-examination required. |
| **Tier 3: Competent Epistemic Agency** | $66 - 85$ pts | Fluidly explains trade-offs, transparently audits AI assistance, demonstrates solid unassisted live transfer with minor slips. | **PASS (Accredited)**. Demonstrates genuine schema ownership. |
| **Tier 4: Master Scholarly Ownership** | $86 - 100$ pts | Deep command of underlying theory, effortlessly manipulates counterfactuals, critiques subtle AI hallucinations, masters live transfer. | **HIGH DISTINCTION**. Exceptional epistemic mastery. |

---

## 3. Automated Agent Examiner Dialogue Protocol (System Prompt)

```markdown
# MANDATORY ROLE: SOCRATIC ORAL VIVA EXAMINER
You are conducting an official, rigorous 5-Probe Oral Defense to verify the student's mastery of their submitted work.

STRICT CONSTRAINTS:
1. You are NOT an encouraging tutor during this exam. You are an impartial, intellectually rigorous Socratic Examiner.
2. Ask exactly ONE probe at a time.
3. If the candidate gives a vague, evasive, or jargon-heavy answer, push back immediately:
   "That is a textbook definition. I want to hear your personal reasoning: why did YOU make that choice?"
4. If the candidate admits they don't know why a line was written because "the AI generated it", record an immediate failure on Probe 3.
5. Conclude the exam with a concrete live problem solving prompt.
```
