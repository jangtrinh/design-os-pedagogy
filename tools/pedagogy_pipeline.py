#!/usr/bin/env python3
"""
tools/pedagogy_pipeline.py - Autonomous End-to-End Pedagogical Knowledge Pipeline

Given a research topic, this tool autonomously:
1. Analyzes the topic, determines the correct Archetype, Target Path, and Map of Content (MOC).
2. Formulates an adversarial, empirically grounded debate & synthesis prompt based on 
   00-system/pedagogical-authoring-spec.md.
3. Dispatches to Codex Web (ChatGPT Web / Codex Native bridge) for deep reasoning, 
   empirical retrieval (author, year, Cohen's d), and refutational synthesis.
4. Robustly parses the output, stripping prompts and runtime banners, and writes the clean module.
5. Auto-detects matching visual assets in assets/ and embeds them into the header.
6. Updates the corresponding Map of Content (00-navigation/MOC-*.md) with bidirectional wikilinks.
7. Runs the AST link, image, and wikilink integrity auditor (tools/verify_links.py).
8. Optionally commits and pushes changes to GitHub.

Usage:
    python3 tools/pedagogy_pipeline.py "Topic description or concept name" [OPTIONS]
    ./bin/pedagogy-pipeline "Topic description or concept name" [OPTIONS]
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Optional, Tuple


# ANSI Color codes for clean terminal output
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def find_repo_root() -> Path:
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / ".git").exists() or (current / "00-system").exists():
            return current
        current = current.parent
    return Path.cwd()


def slugify(text: str) -> str:
    cleaned = re.sub(r"\(.*?\)", "", text)
    cleaned = re.sub(r"[^a-zA-Z0-9\s-]", "", cleaned).strip().lower()
    return re.sub(r"[\s_-]+", "-", cleaned)


def classify_topic(topic: str, archetype: str = "auto") -> Dict[str, str]:
    t_lower = topic.lower()

    if archetype != "auto":
        arch = archetype.lower()
        if arch in ("a", "foundations"):
            return {
                "archetype": "A",
                "dir": "10-foundations/learning-science",
                "moc": "00-navigation/MOC-Learning-Science.md",
                "section": "## 1. Core Cognitive Foundations",
                "domain": "cognitive-architecture"
            }
        elif arch in ("b", "stages"):
            return {
                "archetype": "B",
                "dir": "20-stages/s3-secondary",
                "moc": "00-navigation/MOC-Instructional-Design.md",
                "section": "## 1. By Lifecycle Stage",
                "domain": "developmental-pedagogy"
            }
        elif arch in ("e", "cases"):
            return {
                "archetype": "E",
                "dir": "50-practice-library/cases",
                "moc": "00-navigation/MOC-Classroom-Practice.md",
                "section": "## 2. Clinical Classroom Cases & Transcripts",
                "domain": "clinical-case"
            }
        elif arch in ("f", "capabilities"):
            return {
                "archetype": "F",
                "dir": "70-capabilities/diagnose",
                "moc": "00-navigation/MOC-Assessment.md",
                "section": "## 1. Classroom Assessment Instruments",
                "domain": "learner-diagnostics"
            }
        elif arch == "runtime":
            return {
                "archetype": "Runtime",
                "dir": "90-agent-runtime/evals",
                "moc": "00-navigation/MOC-Assessment.md",
                "section": "## 3. Capability Benchmarks & Assessment Runtimes",
                "domain": "agent-runtime"
            }

    # Auto-detection heuristics
    if any(k in t_lower for k in ["case", "transcript", "trial", "rct", "simulation"]):
        return {
            "archetype": "E",
            "dir": "50-practice-library/cases",
            "moc": "00-navigation/MOC-Classroom-Practice.md",
            "section": "## 2. Clinical Classroom Cases & Transcripts",
            "domain": "clinical-case"
        }
    elif any(k in t_lower for k in ["dual coding", "working memory", "load theory", "executive function", "neuro", "consolidation", "retrieval practice", "schema"]):
        return {
            "archetype": "A",
            "dir": "10-foundations/learning-science",
            "moc": "00-navigation/MOC-Learning-Science.md",
            "section": "## 1. Core Cognitive Foundations",
            "domain": "cognitive-architecture"
        }
    elif any(k in t_lower for k in ["assessment", "hinge", "viva", "eval", "diagnostic", "psychometric"]):
        return {
            "archetype": "F",
            "dir": "30-pedagogy/assessment-psychometrics",
            "moc": "00-navigation/MOC-Assessment.md",
            "section": "## 1. Classroom Assessment Instruments",
            "domain": "assessment-diagnostics"
        }
    elif any(k in t_lower for k in ["ai", "llm", "agent", "synthetic", "offloading", "assistance ladder"]):
        return {
            "archetype": "C",
            "dir": "30-pedagogy/edtech-ai",
            "moc": "00-navigation/MOC-Instructional-Design.md",
            "section": "## 3. Cutting-Edge AI-Era Pedagogy & Epistemic Scaffolding (2026 Frontiers)",
            "domain": "edtech-ai"
        }
    else:
        return {
            "archetype": "C",
            "dir": "30-pedagogy/instructional-methods",
            "moc": "00-navigation/MOC-Instructional-Design.md",
            "section": "## 2. High-Impact Pedagogical Frameworks",
            "domain": "instructional-design"
        }


def build_research_prompt(topic: str, file_slug: str, clean_title: str, domain: str, archetype: str) -> str:
    prompt = f"""You are the Lead Pedagogical Scientist of DESIGN:OS Pedagogy.
Perform comprehensive empirical research, adversarial debate, and author a master pedagogical module on:

TOPIC: "{topic}"
MODULE ID: {file_slug}
CANONICAL TITLE: {clean_title}
ARCHETYPE: Archetype {archetype}
KNOWLEDGE HORIZON: Up to September 15, 2026.

=== MANDATORY GOVERNING INVARIANTS ===
1. Universal Pedagogical Authoring Specification:
   Formula: Knowledge + Experience + Diagnosis + Practice + Feedback + Transfer + Protocol.
   Every section MUST be fully written out with substantive analysis, authentic classroom dialogues, and explicit teacher moves.
   DO NOT OUTPUT PLACEHOLDERS, BULLET OUTLINES, OR ANGLE-BRACKET TEXT.
2. Epistemic Invariant:
   AI may carry cognitive load, but must not silently inherit epistemic authority.
   Assistance Level != Competence Level | Authorship != Mastery.
3. Empirical Grounding:
   Cite authentic studies with Authors, Years, Sample Sizes (N), and Effect Sizes (Cohen's d or Hedges' g).
   Dismantle any naive neuromyths or misinterpretations.
4. Formative Hinge Question:
   Create a four-option diagnostic question where Options A, B, C, and D EACH uniquely diagnose a verified misconception.

=== REQUIRED OUTPUT STRUCTURE ===
Generate the complete Markdown document starting directly with the YAML frontmatter block below:

---
id: {file_slug}
title: "{clean_title}"
stage: ["S2-primary", "S3-secondary", "S4-tertiary"]
domain: "{domain}"
learner_state: "novice-to-intermediate"
applies: ["all-instructional-contexts"]
evidence_basis: ["<Real empirical study with effect size>"]
prerequisites: ["cognitive-load-theory"]
leads_to: ["rosenshine-10-principles"]
clinical_cases: []
aliases:
  - "{clean_title}"
---

# {clean_title}

> [!NOTE]
> (1-2 sentence core governing epistemic thesis explaining the causal cognitive mechanism).

---

## 1. Learning Contract
* **Prerequisites**: ...
* **Observable Competencies**: (diagnose, design, scaffold, critique).
* **Diagnostic Prediction**: ...

## 2. The Intuitive Dilemma (Why Naive Teaching Fails)
(Detailed authentic instructional dilemma exposing why intuitive delivery fails).

## 3. Active Prediction Challenge
(Forced-choice scenario where the educator/reader must commit to a hypothesis before reading the mechanism).

## 4. The Underlying Cognitive Mechanism
(Detailed causal architecture, working memory interactions, sensory channels, schema integration).

## 5. Fully Worked Clinical Example with Expert Think-Aloud
(Verbatim classroom/tutoring transcript with teacher moves, student responses, and in-flight clinical commentary).

## 6. Non-Example / Pathological Case (Superficial Implementation)
(Contrasting failure showing lethal mutations or cosmetic mimicry).

## 7. Common Misconceptions & Refutational Sequence
(Markdown table with columns: Naive Mental Model | Diagnostic Cue | Disconfirming Experience | Scientifically Grounded Replacement Model).

## 8. Formative Hinge Question & 4-Distractor Diagnostic Map
(A diagnostic multiple-choice question with A, B, C, D followed by the exact diagnosis for each distractor).

## 9. Guided Rehearsal & Transfer Scenarios
* **Near Transfer Scenario**: ...
* **Far Transfer Scenario**: ...

## 10. Turn-Key Operational Protocol
(Step-by-step checklist, dialogue routine, or state machine for classroom or AI tutor deployment).

## 11. Empirical Evidence, Effect Sizes & Boundary Conditions
* **Empirical Studies**: (Real papers, RCTs, meta-analyses with effect sizes).
* **Boundary Conditions & Inversion Points**: (Where the method breaks or reverses).

Write the full, complete document now from the first '---' line to the final boundary conditions.
"""
    return prompt


def run_codex_web(prompt: str, model: str = "medium", timeout: int = 360) -> Tuple[bool, str]:
    codex_bin = shutil.which("codex-web") or "/Users/jang/.gemini/antigravity/bin/codex-web"
    if not os.path.exists(codex_bin):
        return False, f"Error: 'codex-web' executable not found at {codex_bin}"

    cmd = [codex_bin, "-m", model, prompt]
    print(f"{CYAN}⚡ Dispatching to Codex Web (Model: {model}, Timeout: {timeout}s)...{RESET}")

    start_time = time.time()
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )

        spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        idx = 0

        while process.poll() is None:
            elapsed = int(time.time() - start_time)
            sym = spinner[idx % len(spinner)]
            print(f"\r{BLUE}{sym} Researching & debating in background... [{elapsed}s elapsed]{RESET}", end="", flush=True)
            time.sleep(0.5)
            idx += 1

            if elapsed > timeout:
                process.kill()
                print("\n")
                return False, f"Error: Codex Web query timed out after {timeout} seconds."

        stdout, stderr = process.communicate()
        print("\n")

        full_output = stdout + "\n" + stderr

        if process.returncode != 0 and not ("id:" in full_output and file_slug in full_output):
            return False, f"Codex Web exited with code {process.returncode}: {stderr[:300]}"

        return True, full_output

    except Exception as e:
        print("\n")
        return False, f"Subprocess execution error: {str(e)}"


def extract_clean_markdown(raw_output: str, file_slug: str, clean_title: str, repo_root: Path) -> Optional[str]:
    text = raw_output
    if "hook: Stop" in text:
        text = text.split("hook: Stop")[0]

    lines = text.splitlines()
    matches = [i for i, line in enumerate(lines) if f"id: {file_slug}" in line or f"id: \"{file_slug}\"" in line]

    if matches:
        last_idx = matches[-1]
        start_line = last_idx - 1
        while start_line >= 0 and not ("---" in lines[start_line] or "* * *" in lines[start_line]):
            start_line -= 1
        if start_line < 0:
            start_line = last_idx
        extracted = "\n".join(lines[start_line:])
    else:
        yaml_match = re.search(r"(---\s*\nid:\s*[^\n]+\n.*?---.*)", text, re.DOTALL)
        if yaml_match:
            extracted = yaml_match.group(1).strip()
        else:
            return None

    # Normalize delimiters
    extracted = re.sub(r"^\*\s*\*\s*\*$", "---", extracted, count=2, flags=re.MULTILINE)
    if not extracted.startswith("---"):
        extracted = "---\n" + extracted

    # Clean markdown escapes
    extracted = extracted.replace(r"\[", "[").replace(r"\]", "]").replace(r"\_", "_")

    # Check for matching visual asset
    asset_dir = repo_root / "assets"
    if asset_dir.exists():
        for asset_file in os.listdir(asset_dir):
            if asset_file.endswith(".jpg") or asset_file.endswith(".png"):
                keywords = file_slug.replace("-", "_").split("_")
                if sum(1 for k in keywords if k in asset_file) >= 2:
                    # Check if already embedded
                    if asset_file not in extracted:
                        img_tag = f"\n![{clean_title} Visual Architecture](../../assets/{asset_file})\n"
                        extracted = re.sub(
                            rf"(#\s+{re.escape(clean_title)}\n)",
                            rf"\1{img_tag}",
                            extracted,
                            count=1,
                        )
                    break

    # Clean any trailing codex runtime lines
    clean_lines = []
    for line in extracted.splitlines():
        if line.startswith("tokens used") or line.startswith("hook:"):
            continue
        clean_lines.append(line)

    return "\n".join(clean_lines).strip() + "\n"


def integrate_into_moc(repo_root: Path, moc_rel_path: str, moc_section: str, stem: str, title: str) -> bool:
    moc_full_path = repo_root / moc_rel_path
    if not moc_full_path.exists():
        print(f"{YELLOW}Warning: MOC file {moc_rel_path} does not exist. Skipping MOC update.{RESET}")
        return False

    with open(moc_full_path, "r", encoding="utf-8") as f:
        content = f.read()

    if f"[[{stem}" in content:
        print(f"{GREEN}✓ Entry for '{stem}' already present in {moc_rel_path}.{RESET}")
        return True

    entry_line = f"* [[{stem}|{title}]]: Master module examining cognitive mechanisms, empirical RCTs, and clinical protocols."

    lines = content.splitlines()
    new_lines = []
    inserted = False
    section_found = False

    for i, line in enumerate(lines):
        new_lines.append(line)
        if moc_section.lower() in line.lower():
            section_found = True
        elif section_found and (line.startswith("## ") or (i == len(lines) - 1 and not inserted)):
            new_lines.insert(len(new_lines) - 1, entry_line)
            inserted = True
            section_found = False

    if not inserted:
        new_lines.append(entry_line)

    with open(moc_full_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines) + "\n")

    print(f"{GREEN}✓ Updated {moc_rel_path} under '{moc_section}'.{RESET}")
    return True


def run_verification(repo_root: Path) -> bool:
    verify_script = repo_root / "tools" / "verify_links.py"
    if not verify_script.exists():
        return True

    print(f"{CYAN}🔍 Running repository link & image integrity audit...{RESET}")
    res = subprocess.run([sys.executable, str(verify_script), str(repo_root)], capture_output=True, text=True)
    print(res.stdout)
    return res.returncode == 0


def git_commit_and_push(repo_root: Path, target_file: str, title: str, push: bool = False) -> bool:
    try:
        subprocess.run(["git", "add", "."], cwd=str(repo_root), check=True)
        commit_msg = f"feat(pedagogy): add {title.lower()} master module"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=str(repo_root), check=True)
        print(f"{GREEN}✓ Git committed: '{commit_msg}'{RESET}")

        if push:
            print(f"{CYAN}🚀 Pushing changes to remote main branch...{RESET}")
            subprocess.run(["git", "push", "origin", "main"], cwd=str(repo_root), check=True)
            print(f"{GREEN}✓ Successfully pushed to origin main!{RESET}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{RED}Git operation failed: {e}{RESET}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Autonomous Pedagogical Knowledge Pipeline - Brainstorm, Auto-Research & Build"
    )
    parser.add_argument("topic", type=str, help="Research topic or pedagogical construct to synthesize")
    parser.add_argument("-m", "--model", type=str, default="medium", help="Codex Web model (medium, high, pro, astra, light)")
    parser.add_argument("-a", "--archetype", type=str, default="auto", help="Archetype (auto, foundations, stages, methods, cases, capabilities, runtime)")
    parser.add_argument("--timeout", type=int, default=360, help="Max execution timeout in seconds (default: 360)")
    parser.add_argument("--no-commit", action="store_true", help="Skip git commit after synthesis")
    parser.add_argument("-p", "--push", action="store_true", help="Push to GitHub after commit")
    parser.add_argument("--dry-run", action="store_true", help="Perform prompt synthesis without saving files")

    args = parser.parse_args()
    repo_root = find_repo_root()

    file_slug = slugify(args.topic)
    clean_title = re.sub(r"\s+", " ", args.topic).strip()
    classification = classify_topic(args.topic, archetype=args.archetype)

    target_rel_path = f"{classification['dir']}/{file_slug}.md"
    destination_file = repo_root / target_rel_path

    print(f"\n{BOLD}{GREEN}============================================================{RESET}")
    print(f"{BOLD}{GREEN} 🧠 DESIGN:OS PEDAGOGY AUTONOMOUS PIPELINE{RESET}")
    print(f"{BOLD}{GREEN}============================================================{RESET}")
    print(f"• Topic:      {BOLD}{clean_title}{RESET}")
    print(f"• ID / Slug:  {file_slug}")
    print(f"• Archetype:  {classification['archetype']}")
    print(f"• Target Path:{target_rel_path}")
    print(f"• Target MOC: {classification['moc']}")
    print(f"• Model:      {args.model}")
    print("------------------------------------------------------------\n")

    # Step 1: Prompt Construction
    print(f"{BLUE}[1/4] Formulating adversarial research prompt...{RESET}")
    prompt = build_research_prompt(
        topic=args.topic,
        file_slug=file_slug,
        clean_title=clean_title,
        domain=classification["domain"],
        archetype=classification["archetype"],
    )

    if args.dry_run:
        print(f"{YELLOW}--- DRY RUN PROMPT ---{RESET}\n{prompt[:600]}...\n{YELLOW}[Dry run complete. No files written]{RESET}")
        return

    # Step 2: Codex Web Dispatch
    print(f"{BLUE}[2/4] Querying Codex Web (adversarial debate & literature retrieval)...{RESET}")
    success, raw_output = run_codex_web(prompt, model=args.model, timeout=args.timeout)
    if not success:
        print(f"{RED}Pipeline failed during research phase:{RESET}\n{raw_output}")
        sys.exit(1)

    # Step 3: Extraction & Saving
    print(f"{BLUE}[3/4] Validating and writing module...{RESET}")
    module_text = extract_clean_markdown(raw_output, file_slug, clean_title, repo_root)

    if not module_text or len(module_text.splitlines()) < 40:
        print(f"{RED}Error: Output failed validation (too short or missing frontmatter).{RESET}")
        debug_log = repo_root / "tools" / "last_failed_run.log"
        with open(debug_log, "w", encoding="utf-8") as f:
            f.write(raw_output)
        print(f"Raw output dumped to: {debug_log}")
        sys.exit(1)

    destination_file.parent.mkdir(parents=True, exist_ok=True)
    with open(destination_file, "w", encoding="utf-8") as f:
        f.write(module_text)

    print(f"{GREEN}✓ Successfully written:{RESET} {BOLD}{target_rel_path}{RESET} ({len(module_text.splitlines())} lines)")

    # Step 4: MOC Navigation Integration
    print(f"{BLUE}[4/4] Updating Navigation MOC & Running Audit...{RESET}")
    integrate_into_moc(
        repo_root=repo_root,
        moc_rel_path=classification["moc"],
        moc_section=classification["section"],
        stem=file_slug,
        title=clean_title,
    )

    # Verification
    audit_passed = run_verification(repo_root)
    if not audit_passed:
        print(f"{YELLOW}Warning: Verification reported warnings. Please inspect above.{RESET}")

    # Git Operations
    if not args.no_commit:
        git_commit_and_push(repo_root, target_rel_path, clean_title, push=args.push)

    print(f"\n{BOLD}{GREEN}🎉 Pipeline Execution Complete!{RESET}")
    print(f"• Generated file: {destination_file}")
    print(f"• To inspect:     open \"{target_rel_path}\"\n")


if __name__ == "__main__":
    main()
