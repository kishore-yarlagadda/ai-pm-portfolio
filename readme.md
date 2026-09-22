# AI Product Management Portfolio: SDLC Orchestrator & Case Studies

Welcome to my AI Product Management Portfolio repository. This workspace demonstrates an outcome-driven product management framework. It decouples value-focused product strategy artifacts from technical engineering code generation, ensuring alignment from initial product discovery to requirements engineering.

---

## **Portfolio Architecture & Modules**

```text
ai-pm-portfolio/
├── agentic-pm-sdlc/            # Modular PM SDLC Orchestrator & Workflows
│   └── workflows/              # Python automation scripts & PM templates
│       ├── orchestrator.py     # Six-agent interactive pipeline with HITL gates
│       ├── templates/          # Canonical PM templates: discovery, strategy,
│       │                       # PRD, and user stories
│       └── tests/              # Template integrity test suite
├── llm-evaluator-project/      # Featured AI Case Study: LLM Adversarial Probing
│   ├── documents/              # Strategy specs and PACT discovery reports
│   └── prds/                   # Production-grade requirements documents
└── 401k-retention-project/     # Featured Fintech Case Study: Asset Leakage & Retention
    ├── documents/              # Strategy specs and PACT discovery reports
    └── prds/                   # Production-grade requirements documents
```

New features run through the orchestrator generate their own top-level project folder with the same documents / prds structure, plus a tests folder for generated test assets.

---

## **Core Product Management Methodologies Applied**

Every project in this portfolio utilizes standardized, professional-grade frameworks to eliminate ambiguity and enforce quality governance:

1. **Strategy & Planning (RISE Framework):** Evaluates features based on *Relevance, Impact, Strategic Fit, and Effort*, supplemented by structured pre-mortem risk mitigation analysis.
2. **Product Discovery (PACT Framework):** Maps *People, Activities, Context, and Technologies* to establish explicit user Jobs-to-be-Done (JTBD).
3. **Requirements & Traceability (Merged PostHog / Atlassian Model):** Combines narrative problem framing with structured user story matrices, priority definitions (`P0`, `P1`), and failure-mode analysis.
4. **Evidence Discipline:** Every template requires claims to trace back to the supplied feature definition. Unknowns are explicitly marked `UNKNOWN` and open assumptions are labeled as hypotheses, so generated artifacts never present guesses as facts.

---

## **Featured Case Studies**

### **1. LLM Evaluator Module (`llm-evaluator-project/`)**

* **The Problem:** Deploying generative AI features to staging without automated guardrails exposes enterprises to prompt-injection vulnerabilities, unpredictable quality drift, and unmonitored token expenses.
* **The Solution:** An automated evaluation module featuring **adversarial prompt generation**, **runtime cost-vs-accuracy Pareto frontier tracking**, and strict **Human-in-the-Loop (HITL)** validation gates.

### **2. 401(k) Retention Module (`401k-retention-project/`)**

* **The Problem:** Significant asset leakage occurs when plan participants change jobs or initiate external rollovers due to a lack of proactive engagement loops and behavioral triggers.
* **The Solution:** A runnable synthetic-data prototype with deterministic rollover-intent routing, one fee comparison at most, immediate bypass to a rollover handoff, and rule-based compliance review. It demonstrates the workflow and guardrails; it does not claim production risk scoring, campaign optimization, or measured AUM impact.

---

## **Running the Orchestrator Pipeline**

The orchestrator takes a feature definition and compiles it into a full requirements package by passing it through six specialized agents - discovery, strategy, PRD, engineering spec, user stories, and tests - with a human review gate between each stage.

1. **Set up your environment:**
```bash
python -m venv venv
source venv/bin/activate
pip install google-genai
```

2. **Give the script your Gemini API key:**
```bash
export GEMINI_API_KEY=your_key_here
```

3. **Run the orchestrator from the repository root:**
```bash
python agentic-pm-sdlc/workflows/orchestrator.py
```

4. **What happens when you run it:**

* The script asks for your feature name and definition interactively - no flags needed.
* Each agent drafts its artifact, then pauses at a **Product HITL Gate** - you approve before the next agent builds on it.
* Artifacts land in a project folder named after your feature, organized into `documents/`, `prds/`, and `tests/`.
* Transient Gemini failures (5xx and rate limits) retry automatically with backoff.

5. **Optional model override:** the pipeline defaults to `gemini-3.6-flash`. If a model is experiencing demand spikes, point it at any model your key can access:
```bash
export GEMINI_MODEL=gemini-3.5-flash
```
