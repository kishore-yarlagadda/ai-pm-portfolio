# AI Product Management Portfolio

Welcome to my AI Product Management portfolio. This repository showcases production-ready, enterprise-grade AI agent architectures and governance frameworks designed to solve high-friction business problems while prioritizing user trust, transparency, and strict compliance guardrails.

---

## Portfolio Projects

The portfolio is structured around dedicated production projects, each highlighting distinct AI PM competencies—from dynamic financial reasoning and adversarial security guardrails to automated quantitative evaluation harnesses.

### 1. 401(k) Rollover & Retention Multi-Agent System (`401k retention/`)
An enterprise-grade AI multi-agent architecture built to handle high-friction 401(k) rollover requests, balancing business retention objectives with strict customer trust and fiduciary guardrails.

* **Product Strategy:** Introduces a **Trust-First Retention Framework** featuring automated value analysis, single-pivot CX guardrails (limiting retention offers to 1 attempt per session), and instant intent bypass for frictionless execution.
* **System Architecture:** Utilizes a Supervisor Agent pattern with state persistence (`PITCH_PRESENTED`), context enrichment via mock connectors, and deterministic routing logic.
* **AI Governance & Evaluation:** Validated using a quantitative evaluation harness (`eval_harness.py`) and golden dataset (`eval_cases.json`) achieving 100% test coverage (8/8 scenarios passing).
* **Project Structure:**
  * `docs/PRD.md`: Complete Product Requirements Document detailing metrics, guardrails, and functional specs.
  * `src/agent_system.py`: Python orchestration logic and adversarial security guardrails.
  * `src/analysis_engine.py`: What-if financial fee-impact analysis engine.
  * `evals/`: Quantitative evaluation harness and golden test cases.

### 2. Upcoming Portfolio Projects
* **Future Project 02:** *Placeholder for subsequent specialized AI agent or governance framework currently in development.*

---

## Getting Started & Repository Navigation

Clone the repository to explore individual project implementations, evaluation harnesses, and documentation locally:

```bash
git clone <repository-url>
cd "401k retention"
