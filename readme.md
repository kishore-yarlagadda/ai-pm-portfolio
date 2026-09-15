# AI Product Management Portfolio: SDLC Orchestrator & Case Studies

Welcome to my AI Product Management Portfolio repository. This workspace demonstrates an outcome-driven product management framework designed for AI systems, financial tech, and enterprise automation. It decouples value-focused product strategy artifacts from technical engineering code generation, ensuring alignment from initial product discovery to requirements engineering.

---

## **Portfolio Architecture & Modules**

```text
ai-pm-portfolio/
├── agentic-pm-sdlc/            # Modular PM SDLC Orchestrator & Workflows
│   ├── workflows/              # Python automation scripts & PM templates
│   │   ├── orchestrator.py     # Interactive pipeline controller with HITL gates
│   │   └── templates/          # RISE, PACT, and Merged PRD templates
│   └── README.md               # Detailed orchestrator workflow guide
├── llm-evaluator-project/      # Featured AI Case Study: LLM Adversarial Probing
│   ├── documents/              # Strategy specs and PACT discovery reports
│   └── prds/                   # Production-grade requirements documents
└── 401k-retention-project/     # Featured Fintech Case Study: Asset Leakage & Retention
    ├── documents/              # Strategy specs and PACT discovery reports
    └── prds/                   # Production-grade requirements documents

```

---

## **Core Product Management Methodologies Applied**

Every project in this portfolio utilizes standardized, professional-grade frameworks to eliminate ambiguity and enforce quality governance:

1. **Strategy & Planning (RISE Framework):** Evaluates features based on *Relevance, Impact, Strategic Fit, and Effort*, supplemented by structured pre-mortem risk mitigation analysis.
2. **Product Discovery (PACT Framework):** Maps *People, Activities, Context, and Technologies* to establish explicit user Jobs-to-be-Done (JTBD).
3. **Requirements & Traceability (Merged PostHog / Atlassian Model):** Combines narrative problem framing with structured user story matrices, priority definitions (`P0`, `P1`), and failure-mode analysis.

---

## **Featured Case Studies**

### **1. LLM Evaluator Module (`llm-evaluator-project/`)**

* **The Problem:** Deploying generative AI features to staging without automated guardrails exposes enterprises to prompt-injection vulnerabilities, unpredictable quality drift, and unmonitored token expenses.
* **The Solution:** An automated evaluation module featuring **adversarial prompt generation**, **runtime cost-vs-accuracy Pareto frontier tracking**, and strict **Human-in-the-Loop (HITL)** validation gates.

### **2. 401(k) Retention Module (`401k-retention-project/`)**

* **The Problem:** Significant asset leakage occurs when plan participants change jobs or initiate external rollovers due to a lack of proactive engagement loops and behavioral triggers.
* **The Solution:** A retention framework combining **automated rollover risk detection**, **retention campaign efficiency Pareto tracking**, and **compliance-driven HITL oversight gates** to protect long-term Assets Under Management (AUM).

---

## **Running the Orchestrator Pipeline**

To experience how these standardized requirements and strategies are dynamically compiled through automated Python workflows:

1. **Set up your environment:**
```bash
python -m venv venv
source venv/bin/activate

```


2. **Execute the orchestrator script:**
```bash
python agentic-pm-sdlc/workflows/orchestrator.py

```


3. **Interact with the Lifecycle Gates:**
* Enter your target feature request or output module name.
* Review and approve generated product assets sequentially at each **Product HITL Gate** before downstream progression.



```

```
