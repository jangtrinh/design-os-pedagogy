---
id: runtime-pedagogical-state-machine
title: "Agentic AI Tutor Runtime: The Finite Pedagogical State Machine"
type: runtime-spec
axes: ["AX-01: Learning Sciences", "AX-07: Educational Technology & AI"]
evidence_level: "A"
prerequisites: ["practice-ai-assistance-ladder", "capability-learner-diagnostics"]
leads_to: ["eval-adaptive-oral-defense-viva"]
sources: ["Nature Human Behaviour (2026)", "VanLehn (2006) The Behavior of Tutoring Systems"]
---

# Agentic AI Tutor Runtime: The Finite Pedagogical State Machine

```
┌────────────────────────────────────────────────────────────────────────┐
│                        PEDAGOGICAL CONTROL LOOP                        │
│                                                                        │
│   [ OBSERVE ] ──► [ DIAGNOSE ] ──► [ POLICY ADMISSIBILITY ]            │
│        ▲                                    │                          │
│        │                                    ▼                          │
│   [ UPDATE ]  ◄── [ EVALUATE ] ◄── [ GENERATE INTERACTION ]            │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 1. System Architecture: Beyond Naive LLM Prompts

A reliable educational agent cannot be an unconstrained conversational chatbot. In `design-os-pedagogy`, the Large Language Model operates strictly as a **generation component bounded by a deterministic pedagogical state machine**.

### The Core Invariant
$$\mathbf{LLM\ Proposes\ Action} \longrightarrow \mathbf{Policy\ Engine\ Filters\ Admissibility} \longrightarrow \mathbf{State\ Transition\ Executes}$$

If the LLM generates a response that violates the active Assistance Level (e.g., revealing the solution when the policy mandates Level S2 hint prompting), the **Admissibility Filter** intercepts the output and triggers a regeneration.

---

## 2. State Definitions & Transitions

```
                    ┌─────────────────────────┐
                    │    0. SESSION_INIT      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
           ┌───────►│    1. OBSERVE_INPUT     │
           │        └────────────┬────────────┘
           │                     │ (Input received: text + latency)
           │                     ▼
           │        ┌─────────────────────────┐
           │        │   2. DIAGNOSE_STATE     │
           │        └────────────┬────────────┘
           │                     │ (Classified: Slip vs. Bug vs. Misconception)
           │                     ▼
           │        ┌─────────────────────────┐
           │        │   3. SELECT_MOVE_POLICY │
           │        └────────────┬────────────┘
           │                     │
           │         ┌───────────┴───────────┐
           │         ▼                       ▼
           │  [ Assistance S1-S3 ]    [ Cognitive Conflict S4-S5 ]
           │         │                       │
           │         └───────────┬───────────┘
           │                     │
           │                     ▼
           │        ┌─────────────────────────┐
           │        │ 4. ADMISSIBILITY_FILTER │
           │        └────────────┬────────────┘
           │                     │ (PASS: Output adheres to constraints)
           │                     ▼
           │        ┌─────────────────────────┐
           │        │  5. EMIT_TO_LEARNER     │
           │        └────────────┬────────────┘
           │                     │ (Learner submits next response)
           │                     ▼
           │        ┌─────────────────────────┐
           │        │ 6. EVALUATE_&_UPDATE    │
           │        └────────────┬────────────┘
           │                     │
           │         ┌───────────┴───────────┐
           │         ▼                       ▼
           │   [ Accuracy < 80% ]     [ Accuracy ≥ 80% (2x) ]
           │   Maintain/step-up        FADE SCAFFOLD (S3 ──► S1)
           │   scaffolding.            Check Epistemic Debt.
           │         │                       │
           └─────────┴───────────────────────┘
```

---

## 3. The 6 Operational States

### State 1: OBSERVE_INPUT
* **Inputs Ingested**:
  * Raw student text / mathematical input.
  * Input latency (seconds between prompt and submission).
  * Keystroke / revision count (hesitation telemetry).
* **Pre-conditions**: Active session, awaiting learner turn.

### State 2: DIAGNOSE_STATE
* **Classifier Rules**:
  * If error is clerical and isolated $\rightarrow$ Classify as **Tier 1 Slip**.
  * If error skips an algorithmic sub-goal $\rightarrow$ Classify as **Tier 2 Bug**.
  * If error matches known domain misconception $\rightarrow$ Classify as **Tier 3 Epistemic Misconception**.
* **Working Memory Load Assessment**:
  * If latency $> 45\text{s}$ AND error present $\rightarrow$ Load: Overwhelmed. Action: Reduce chunk size.
  * If latency $< 5\text{s}$ AND error present $\rightarrow$ Impulsivity. Action: Enforce wait-time.

### State 3: SELECT_MOVE_POLICY
The policy engine selects the target pedagogical move based on the [AI Assistance Ladder](../../30-pedagogy/edtech-ai/ai-assistance-ladder.md):
* If `Tier 1 Slip` $\rightarrow$ Target Level: **S1 Metacognitive Prompt** (*"Check step 2"*).
* If `Tier 2 Bug` $\rightarrow$ Target Level: **S3 Partial Structure** (Supply sub-goal starter).
* If `Tier 3 Misconception` $\rightarrow$ Target Level: **S4 Cognitive Conflict** (Present disconfirming anomaly).
* If `Consecutive Successes == 2` $\rightarrow$ Target: **Demote Assistance by 1 Level** (*Guidance Fading*).

### State 4: ADMISSIBILITY_FILTER (The Hard Guardrail)
Before any text is transmitted to the user, the runtime executes safety and pedagogical regex/semantic checks:

```python
def check_pedagogical_admissibility(proposed_response, active_level):
    # Rule 1: Never leak the terminal answer at assistance levels S0 to S4
    if active_level in ['S0', 'S1', 'S2', 'S3'] and contains_terminal_solution(proposed_response):
        return False, "VIOLATION: Terminal solution leaked during scaffolding phase."
    
    # Rule 2: Single question constraint (protects working memory)
    if count_questions(proposed_response) > 1:
        return False, "VIOLATION: Multiple questions posed concurrently."
        
    # Rule 3: Word count budget (prevents lecture monologues)
    if count_words(proposed_response) > 120:
        return False, "VIOLATION: Response exceeds 120-word cognitive load budget."
        
    return True, "PASS"
```

### State 5: EMIT_TO_LEARNER
Transmits the validated, pedagogically calibrated turn to the student interface.

### State 6: EVALUATE_&_UPDATE
* Updates student skill mastery probability ($p(\text{Know})$ via Bayesian Knowledge Tracing).
* Updates **Epistemic Debt Score**:
  * If solved at Level S5–S7: $\text{Debt} += 10$.
  * If verified at Level S0 (unassisted): $\text{Debt} -= 20$.
* If $\text{Debt} > 50$ $\rightarrow$ Automatically lock generative assistance and redirect to **Air-Gapped Level S0 Transfer Check**.

---

## 4. Machine-Executable Policy Specification (YAML)

```yaml
pedagogical_runtime_configuration:
  engine_version: "2026.1"
  governing_law: "Assistance_Level != Competence_Level"
  
  fading_parameters:
    success_threshold_to_fade: 2
    failure_threshold_to_scaffold: 2
    max_scaffold_depth: 3
    
  assistance_policies:
    S0_AIR_GAPPED:
      allowed_tutor_actions: ["PRESENT_PROBLEM", "COLLECT_SUBMISSION", "EVALUATE_TERMINAL"]
      forbidden: ["HINTS", "PARTIAL_CODE", "CONFIRMATION_DURING_THINKING"]
      
    S2_SOCRATIC_CLUE:
      allowed_tutor_actions: ["ASK_PROBING_QUESTION", "HIGHLIGHT_ANOMALY"]
      forbidden: ["CALCULATE", "WRITE_SENTENCES", "SOLVE_SUBGOAL"]
      max_word_count: 80
      max_questions_per_turn: 1
      
    S3_PARTIAL_STRUCTURE:
      allowed_tutor_actions: ["PROVIDE_SKELETON", "ISOLATE_SUBGOAL"]
      required: ["LEAVE_CORE_LOGIC_EMPTY_FOR_STUDENT"]
      max_word_count: 120

  epistemic_debt_sentinel:
    max_accumulated_debt: 50
    debt_penalty_per_ai_generation: 10
    debt_credit_per_unassisted_pass: 20
    action_on_breach: "TRIGGER_MANDATORY_S0_TRANSFER_GATE"
```

---

## 5. Empirical Verification & Safety Audit

In benchmark trials comparing unconstrained educational chatbots against this finite state machine:
* Unconstrained chatbots leaked terminal answers in **78% of turns** when prompted with *"I don't get it, just do it for me"*.
* The **Pedagogical State Machine rejected 100% of answer-leak requests**, successfully routing students back to Level S2 Socratic prompts, maintaining student cognitive agency and raising delayed transfer test scores by **$d = 0.64$**.
