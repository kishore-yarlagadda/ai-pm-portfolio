# Agentic SDLC Orchestrator & Templates Documentation

**Agentic SDLC Orchestrator** is an automated product management pipeline designed to enforce a strict separation between high-level, value-driven strategy documents and technical code generation. This documentation details the core orchestration script and the modular template architecture housed within the workflow directory.

---

**Directory Structure**

```text
workflows/
├── orchestrator.py         # Automated pipeline controller & HITL gatekeeper
└── templates/              # Standardized professional PM frameworks
    ├── strategy_template.md  # RISE Framework Strategy Spec
    ├── discovery_template.md # PACT Framework Discovery Report
    └── prd_template.md       # Merged PostHog/Atlassian PRD

```
---
## 📐 Architecture & Governance Framework

The Agentic PM & SDLC Governance Framework enforces a strict "Product-First" contract model. It utilizes an orchestrator-driven state machine combined with mandatory Human-in-the-Loop (HITL) checkpoints and automated quality gates to ensure code generation meets strict quality ($\ge 85\%$ test coverage via `pytest-cov`) and type-safety (`mypy`) standards.

```mermaid
graph TD
    User[Human-in-the-Loop / Developer] -->|Triggers / Approves| Orch[SDLCOrchestrator Engine]
    
    subgraph Governance & State Layer
        Orch --> State[SDLCState Model<br/>Pydantic]
        State -->|Saves / Loads| JSON[(.sdlc_state.json<br/>State Persistence)]
    end

    subgraph Template Layer
        Orch --> Spec[Engineering Spec Template]
        Orch --> Task[Task Plan Template]
        Orch --> Bug[Bug Report Template]
    end

    subgraph Use Case 1: Feature Development Workflow
        Spec -->|HITL Gate 1| Task
        Task -->|HITL Gate 2| Code[Code Generation & TDD]
        Code --> Quality[Automated Quality & Test Gates]
    end

    subgraph Use Case 2: Bug Incident Remediation
        Quality -- Fail (<85% Coverage / Mypy Error) --> BugTriage[Bug Report Generation]
        BugTriage --> Fix[Code Remediation & Patch]
        Fix --> Quality
    end

    Quality -- Pass (>=85% Coverage) --> Success[Completed & Verified State]

    style Orch fill:#f9f,stroke:#333,stroke-width:2px
    style Quality fill:#bbf,stroke:#333,stroke-width:2px
    style Success fill:#bfb,stroke:#333,stroke-width:2px
```
---

**Orchestrator Overview (`orchestrator.py`)**

The orchestrator script manages the automated compilation of feature requests into structured product documentation.

* **Dynamic Variable Injection**: Injects target feature requests into standardized Markdown templates.
* **Directory Management**: Automatically provisions structured output directories (`documents/` and `prds/`) for each distinct project workspace.
* **Human-in-the-Loop (HITL) Gates**: Halts execution at the end of each lifecycle phase, prompting interactive terminal sign-off before proceeding to the next artifact.
* **Pipeline Decoupling**: Enforces complete separation between product definition phases and future engineering/code implementation steps.

---

**Template Specifications (`workflows/templates/`)**

Each template inside the directory serves a precise methodological function within the product lifecycle:

* **`strategy_template.md` (RISE Framework)**
* *Focus*: Strategic planning and risk assessment.
* *Sections*: Executive Summary & Strategic Alignment, RISE Evaluation Matrix (Relevance, Impact, Strategic Fit, Effort), and Pre-Mortem Risk Analysis.


* **`discovery_template.md` (PACT Framework)**
* *Focus*: User research and contextual environment mapping.
* *Sections*: Target Audience & Personas, Activities & Jobs-to-be-Done (JTBD), and Operational Context & Constraints.


* **`prd_template.md` (Merged PostHog / Atlassian Model)**
* *Focus*: Detailed feature requirements and traceability.
* *Sections*: Executive Summary & Problem Context, Target Audience & Scope, Success Metrics & KPIs, Functional Requirements & User Stories Matrix, Key User Flows & Edge Cases, and Assumptions & Open Questions Log.



---

**Execution Workflow**

1. Activate the python environment and navigate to the working directory.
2. Run the orchestrator script to initialize the documentation pipeline:
```bash
python workflows/orchestrator.py

```


3. Input the target feature request or accept the default prompt (e.g., the LLM Evaluator module).
4. Review generated markdown files interactively at each **Product HITL Gate** before approving completion.		
