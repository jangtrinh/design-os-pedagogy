# DESIGN:OS Agent Teacher (`design-os-pedagogy`)

**Evidence-graded pedagogy library, cognitive-load curriculum tree runtime, and interactive mastery assessment engine for AI tutoring agents.**

Equip AI agents to teach complex technical subjects using Bloom's revised taxonomy, worked-example fading, spaced retrieval, Socratic diagnostic probes, and verifiable learner state machines.

<p align="center">
  <img src="docs/images/cover.png" alt="DESIGN:OS Agent Teacher — 2:1 Axonometric Technical Architecture" width="840">
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-PolyForm_Shield_1.0.0-202020?style=flat-square&labelColor=202020&color=444444" alt="PolyForm Shield 1.0.0 License"></a>
  <img src="https://img.shields.io/badge/Claude_Code_%C2%B7_Codex_%C2%B7_Gemini_%C2%B7_Antigravity-skill-202020?style=flat-square&labelColor=202020&color=444444" alt="Compatible agents">
  <a href="commands/doctor.md"><img src="https://img.shields.io/badge/diagnostics-%2Fdoctor-202020?style=flat-square&labelColor=202020&color=444444" alt="Doctor command"></a>
  <a href="https://jangtrinh.github.io/design-os-pedagogy/"><img src="https://img.shields.io/badge/live_docs-GitHub_Pages-202020?style=flat-square&labelColor=202020&color=444444" alt="Live GitHub Pages"></a>
  <a href="https://buymeacoffee.com/jangtrinh"><img src="https://img.shields.io/badge/Buy_Me_a_Coffee-FFDD00?style=flat-square&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee"></a>
</p>

<p align="center">
  <a href="#quickstart">Quickstart</a> · <a href="#what-it-makes">What it makes</a> · <a href="#installation">Install</a> · <a href="#how-it-works">How it works</a> · <a href="#commands--diagnostics">Commands</a> · <a href="#quality-bar--limitations">Limits</a>
</p>

---

## Why this exists

When you ask a generic LLM to 'teach me X', it dumps a 2,000-word textbook summary that creates an illusion of competence without testing transfer or managing cognitive load. **`design-os-pedagogy`** gives AI agents a formal instructional design runtime grounded in cognitive science.

| Dimension | Generic AI / Manual Workflow | DESIGN:OS Agent Teacher (`DESIGN:OS`) |
| :--- | :--- | :--- |
| **Instructional Flow** | Passive 2,000-word wall of text with zero learner checks | Active worked-example fading, Socratic probes, and gated mastery nodes |
| **Curriculum Structure** | Flat bullet lists with hidden prerequisite gaps | Explicit DAG of prerequisite concepts and Bloom taxonomy target levels |
| **Assessment Quality** | Trivial recall trivia ('What does API stand for?') | Diagnostic misconception probes and near/far transfer challenges |
| **Evidence Grading** | Pop-psychology myths (e.g., VARK learning styles) | Strictly evidence-graded cognitive science (Sweller, Bjork, Roediger, Chi) |
| **Privacy & Telemetry** | Opaque cloud telemetry or unverified third-party APIs | **Zero telemetry** — 100% local execution ([`PRIVACY.md`](PRIVACY.md) audited) |

---

## Quickstart

### 1. Install the plugin or CLI

**In Claude Code:**

```text
/plugin marketplace add jangtrinh/design-os-pedagogy
/plugin install design-os-pedagogy@design-os-pedagogy
```

**Or from your terminal (Codex, Gemini CLI, Antigravity, OpenCode, or standalone CLI):**

```bash
git clone https://github.com/jangtrinh/design-os-pedagogy.git
cd design-os-pedagogy
python3 scripts/self_check.py
```

### 2. Ask in plain English

Open your project in your AI coding agent and describe what you need:

> "Design a 5-stage mastery curriculum tree for distributed consensus (Raft) with prerequisite DAGs and diagnostic transfer questions."

> "Turn this codebase walkthrough into a worked-example fading sequence with interactive check-for-understanding probes."

> "Audit our onboarding tutorial for cognitive load violations, missing prerequisite links, and passive wall-of-text explanations."

### 3. Verify your setup

```bash
python3 scripts/self_check.py
```

---

## What it makes

Every deliverable produced by `design-os-pedagogy` is backed by a deterministic verification gate rather than freehand AI guesswork.

<p align="center">
  <img src="docs/images/cover.png" alt="DESIGN:OS Agent Teacher Output Specimen" width="840"><br>
  <sub>Prompt: <code>"Design a 5-stage mastery curriculum tree for distributed consensus (Raft) with prerequisite DAGs and diagnostic transfer questions."</code></sub>
</p>

| Deliverable / Mode | Best for | Output Format | Verification Gate |
| :--- | :--- | :--- | :--- |
| **Curriculum DAG Specs** | Decomposing a technical domain into prerequisite-ordered mastery nodes | `JSON / Markdown Curriculum Tree` | `DAG acyclicity & rubric check` |
| **Worked-Example Fading Loops** | Transitioning learners from full examples -> partial completion -> independent problem solving | `Interactive Lesson Prompts` | `Cognitive-load gate PASS` |
| **Diagnostic Rubrics** | Detecting specific mental-model bugs before advancing the learner | `Structured Assessment Spec` | `python3 scripts/self_check.py` |

---

## Installation

Choose the setup that matches your AI coding agent. Every option installs the same canonical skill (`skills/design-os-pedagogy/SKILL.md`) and `/doctor` diagnostic suite.

### Claude Code

Run these two commands inside Claude Code:

```text
/plugin marketplace add jangtrinh/design-os-pedagogy
/plugin install design-os-pedagogy@design-os-pedagogy
```

### OpenAI Codex

Install to your personal Codex skills directory:

```bash
git clone https://github.com/jangtrinh/design-os-pedagogy.git /tmp/design-os-pedagogy
mkdir -p ~/.codex/skills/design-os-pedagogy ~/.codex/prompts
cp -R /tmp/design-os-pedagogy/skills/design-os-pedagogy/* ~/.codex/skills/design-os-pedagogy/
cp /tmp/design-os-pedagogy/prompts/doctor.md ~/.codex/prompts/design-os-pedagogy-doctor.md
rm -rf /tmp/design-os-pedagogy
```

### Gemini CLI & Google Antigravity

```bash
git clone https://github.com/jangtrinh/design-os-pedagogy.git /tmp/design-os-pedagogy
mkdir -p ~/.gemini/skills/design-os-pedagogy
cp -R /tmp/design-os-pedagogy/skills/design-os-pedagogy/* ~/.gemini/skills/design-os-pedagogy/
rm -rf /tmp/design-os-pedagogy
```

### OpenCode, Cursor, Windsurf & Other Agent Harnesses

```bash
git clone https://github.com/jangtrinh/design-os-pedagogy.git /tmp/design-os-pedagogy
mkdir -p ~/.agents/skills/design-os-pedagogy
cp -R /tmp/design-os-pedagogy/skills/design-os-pedagogy/* ~/.agents/skills/design-os-pedagogy/
rm -rf /tmp/design-os-pedagogy
```

<details>
<summary>Verify or uninstall</summary>

**Verify installation:**

```bash
python3 scripts/self_check.py
```

Or run `/doctor` inside Claude Code / Codex to inspect installed skill paths, plugin manifests, and gate health.

**Uninstall:**

```bash
rm -rf ~/.claude/skills/design-os-pedagogy ~/.codex/skills/design-os-pedagogy ~/.gemini/skills/design-os-pedagogy ~/.agents/skills/design-os-pedagogy
```

</details>

---

## Usage & Prompt Cookbook

Once installed, `skills/design-os-pedagogy/SKILL.md` activates automatically when your prompt matches its domain triggers. Browse [`docs/cookbook.md`](docs/cookbook.md) for copy-paste prompt recipes.

**Generate & Scaffold**

```text
"Design a 5-stage mastery curriculum tree for distributed consensus (Raft) with prerequisite DAGs and diagnostic transfer questions."
```

**Audit & Verify**

```text
"Turn this codebase walkthrough into a worked-example fading sequence with interactive check-for-understanding probes."
```

**Export & Automate**

```text
"Audit our onboarding tutorial for cognitive load violations, missing prerequisite links, and passive wall-of-text explanations."
```

---

## Commands & Diagnostics

| Command | Environment | What it does |
| :--- | :--- | :--- |
| `/doctor` | Claude Code / Codex | Read-only diagnostic check of installed skill paths, plugin manifests, and runtime prerequisites |
| `python3 scripts/self_check.py` | Terminal / CI | Deterministic offline verification of manifests, skill contracts, and governance files |
| `python3 scripts/self_check.py` | Terminal / CI | Verify pedagogy skill contracts, curriculum schema integrity, and repository delivery gates |

---

## How it works

1. **Intent Routing** — Your AI agent matches your request against `skills/design-os-pedagogy/SKILL.md` frontmatter triggers.
2. **Progressive Context Loading** — Only the entry-point `SKILL.md` router loads initially; detailed recipes and scripts load on demand.
3. **Deterministic Execution** — Domain scripts and contracts execute locally with reproducible inputs and outputs.
4. **Gate Verification** — `scripts/self_check.py` and domain verifiers (`python3 scripts/self_check.py`) validate the artifact before completion.
5. **Zero-Telemetry Delivery** — Verified files are written directly to your workspace with zero external network calls.

```text
User Prompt / CLI Invocation
            │
            ▼
┌───────────────────────────────────────────────┐
│ skills/design-os-pedagogy/SKILL.md
│ Progressive disclosure router & hard rules    │
└───────────┬───────────────────────────────────┘
            │ loads on demand
            ▼
┌───────────────────────────────────────────────┐
│ python3 scripts/self_check.py
│ Deterministic build & contract enforcement    │
└───────────┬───────────────────────────────────┘
            │ verifies
            ▼
┌───────────────────────────────────────────────┐
│ python3 scripts/self_check.py + /doctor       │
│ Zero-telemetry local verification gate        │
└───────────────────────────────────────────────┘
```

### What loads when

`design-os-pedagogy` uses progressive context disclosure so your agent's context window stays fast and focused:

| File | Loaded when |
| :--- | :--- |
| `skills/design-os-pedagogy/SKILL.md` | Always (~100–150 lines) — routing rules, triggers, and execution workflow |
| `docs/cookbook.md` | When selecting multi-step prompt recipes or domain patterns |
| `commands/doctor.md` / `prompts/doctor.md` | Only when running `/doctor` diagnostics |
| `llms.txt` | When indexed by AI answer engines, RAG pipelines, or repo crawlers |

---

## File structure

```text
design-os-pedagogy/
├── .claude-plugin/
│   ├── plugin.json                 # Claude Code plugin manifest
│   └── marketplace.json            # Claude Code marketplace catalog
├── .codex-plugin/
│   └── plugin.json                 # OpenAI Codex plugin & interface manifest
├── .agents/
│   └── plugins/marketplace.json    # Cross-agent local plugin registry
├── .factory-plugin/
│   ├── plugin.json                 # Factory / Droid plugin manifest
│   └── marketplace.json            # Factory marketplace metadata
├── skills/
│   └── design-os-pedagogy/
│       └── SKILL.md                # Canonical agent skill entrypoint
├── commands/
│   └── doctor.md                   # /doctor diagnostic slash command
├── prompts/
│   └── doctor.md                   # Codex diagnostic prompt mirror
├── scripts/
│   └── self_check.py               # Deterministic repository & skill self-check
├── docs/
│   ├── cookbook.md                 # Copy-paste prompt recipes by job
│   └── llms.txt                    # GEO / LLM discovery index
├── PRIVACY.md                      # Zero-telemetry & local-first privacy commitment
├── SECURITY.md                     # Vulnerability disclosure & security policy
├── CONTRIBUTING.md                 # Contribution workflow & verification rules
├── CODE_OF_CONDUCT.md              # Contributor Covenant code of conduct
├── CHANGELOG.md                    # Release history
├── llms.txt                        # Root LLM indexing manifest
├── LICENSE                         # PolyForm Shield 1.0.0
└── README.md
```

---

## Quality bar & Limitations

### It's working if...

- `python3 scripts/self_check.py` prints `ok: design-os-pedagogy self-check passed (design-os-pedagogy)` and exits `0`.
- `python3 scripts/self_check.py` passes with zero contract or test regressions.
- Your AI coding agent loads `skills/design-os-pedagogy/SKILL.md` automatically when given any prompt from [`docs/cookbook.md`](docs/cookbook.md).
- Network traffic during execution remains zero (guaranteed by [`PRIVACY.md`](PRIVACY.md)).

### When not to use

- Pure reference API lookups where an experienced engineer just wants a one-line CLI flag answer.
- Clinical, medical, or accredited K-12 compliance grading requiring licensed human oversight.
- Automated code generation where the user wants the task finished rather than explained.

---

## DESIGN:OS Ecosystem

`design-os-pedagogy` is one of the 13 source-available engines in the **`DESIGN:OS`** ecosystem:

| Engine | Live Docs | Repository | Layer |
| :--- | :--- | :--- | :--- |
| **DESIGN:OS CLI** | [jangtrinh.github.io/design-os](https://jangtrinh.github.io/design-os/) | [`jangtrinh/design-os`](https://github.com/jangtrinh/design-os) | `cli` |
| **Knowledge Builder** | [jangtrinh.github.io/design-os-knowledge-builder](https://jangtrinh.github.io/design-os-knowledge-builder/) | [`jangtrinh/design-os-knowledge-builder`](https://github.com/jangtrinh/design-os-knowledge-builder) | `compiler` |
| **Figma Plugin & CLI** | [jangtrinh.github.io/design-os-figma-plugin](https://jangtrinh.github.io/design-os-figma-plugin/) | [`jangtrinh/design-os-figma-plugin`](https://github.com/jangtrinh/design-os-figma-plugin) | `plugin` |
| **SVG Animation Engine** | [jangtrinh.github.io/design-os-svg-animation](https://jangtrinh.github.io/design-os-svg-animation/) | [`jangtrinh/design-os-svg-animation`](https://github.com/jangtrinh/design-os-svg-animation) | `engine` |
| **3D Blender Agent** | [jangtrinh.github.io/design-os-3d-blender](https://jangtrinh.github.io/design-os-3d-blender/) | [`jangtrinh/design-os-3d-blender`](https://github.com/jangtrinh/design-os-3d-blender) | `3d / cad` |
| **OPAH ONE Drone** | [jangtrinh.github.io/design-os-drone-showcase](https://jangtrinh.github.io/design-os-drone-showcase/) | [`jangtrinh/design-os-drone-showcase`](https://github.com/jangtrinh/design-os-drone-showcase) | `hardware` |
| **GitHub Pages Engine** | [jangtrinh.github.io/design-os-github-page](https://jangtrinh.github.io/design-os-github-page/) | [`jangtrinh/design-os-github-page`](https://github.com/jangtrinh/design-os-github-page) | `pages` |
| **Apple Design OS** | [jangtrinh.github.io/design-os-apple](https://jangtrinh.github.io/design-os-apple/) | [`jangtrinh/design-os-apple`](https://github.com/jangtrinh/design-os-apple) | `swiftui` |
| **Agent Teacher** | [jangtrinh.github.io/design-os-pedagogy](https://jangtrinh.github.io/design-os-pedagogy/) | [`jangtrinh/design-os-pedagogy`](https://github.com/jangtrinh/design-os-pedagogy) | `pedagogy` |
| **Origami CAD** | [jangtrinh.github.io/design-os-origami](https://jangtrinh.github.io/design-os-origami/) | [`jangtrinh/design-os-origami`](https://github.com/jangtrinh/design-os-origami) | `packaging` |
| **Voice UX Architecture** | [jangtrinh.github.io/design-os-voice-ux](https://jangtrinh.github.io/design-os-voice-ux/) | [`jangtrinh/design-os-voice-ux`](https://github.com/jangtrinh/design-os-voice-ux) | `voice-ai` |
| **Code2Flow** | [jangtrinh.github.io/design-os-code2flow](https://jangtrinh.github.io/design-os-code2flow/) | [`jangtrinh/design-os-code2flow`](https://github.com/jangtrinh/design-os-code2flow) | `ast / audit` |
| **Generative UI** | [jangtrinh.github.io/design-os-generative-ui](https://jangtrinh.github.io/design-os-generative-ui/) | [`jangtrinh/design-os-generative-ui`](https://github.com/jangtrinh/design-os-generative-ui) | `runtime` |

---

## Author

Built by [Jang Trịnh](https://www.jang.work/?utm_source=github&utm_medium=readme&utm_campaign=design-os-pedagogy). More projects, case studies and writing at [jang.work](https://www.jang.work/?utm_source=github&utm_medium=readme&utm_campaign=design-os-pedagogy).

---

## Contributing, Governance & License

- **Contributing**: See [`CONTRIBUTING.md`](CONTRIBUTING.md) for pull request guidelines and verification gates (`python3 scripts/self_check.py`).
- **Code of Conduct**: Governed by [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
- **Security & Privacy**: Zero telemetry — see [`SECURITY.md`](SECURITY.md) and [`PRIVACY.md`](PRIVACY.md).
- **Changelog & LLM Index**: Track releases in [`CHANGELOG.md`](CHANGELOG.md) and machine-readable index in [`llms.txt`](llms.txt).
- **License**: [PolyForm Shield 1.0.0](LICENSE) © [Jang Trinh](https://github.com/jangtrinh). Free to use and modify, including for paid client work; you may not resell it or build a competing product from it.

---

If `design-os-pedagogy` saves you time, a star on GitHub helps other engineers and AI agents find it.

<p align="left">
  <a href="https://buymeacoffee.com/jangtrinh">
    <img src="https://img.shields.io/badge/Buy_Me_a_Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee">
  </a>
</p>
