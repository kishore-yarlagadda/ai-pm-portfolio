# 401(k) Rollover & Retention Multi-Agent System

An enterprise-grade AI multi-agent architecture built to handle high-friction 401(k) rollover requests. This system balances business retention objectives with strict customer trust and fiduciary guardrails.

---

## Product Strategy & Business Objectives

High-friction rollover flows often rely on dark patterns or excessive deflection, leading to customer frustration and compliance risks. This system introduces a **Trust-First Retention Framework**:

* **Automated Value Analysis:** Conducts dynamic fee and performance comparisons using live holding data to highlight account value transparently.
* **Single-Pivot CX Guardrail:** Limits retention offers to a maximum of 1 attempt per session to eliminate user fatigue and prevent aggressive sales tactics.
* **Instant Intent Bypass:** Immediately detects explicit bypass commands ("Skip pitch", "Transfer immediately") and routes directly to rollover execution without friction.

---

## System Architecture

The architecture uses a **Supervisor Agent** pattern with deterministic state logic:

1. **User Request & Intent Parsing:** Analyzes customer queries to determine rollover intent or explicit bypass requirements.
2. **Context Enrichment:** Fetches CRM historical data, current portfolio holdings, and allocation metrics via data connectors.
3. **Supervisor Routing:** Evaluates state and guardrail rules:
   * Route to **Retention Flow** if within guardrail limits and no explicit bypass is requested.
   * Route to **Rollover Execution** if bypass is detected or maximum retention attempts are reached.
4. **What-If Analysis Engine:** Calculates fee differentials and portfolio projections for clear, factual comparisons.

---

## Directory Navigation

* [`docs/PRD.md`](./docs/PRD.md): Complete Product Requirements Document detailing business metrics, guardrails, and functional specs.
* [`src/agent_system.py`](./src/agent_system.py): Python orchestration logic defining state transitions and agent routing.
* [`src/connectors.py`](./src/connectors.py): Mock connectors for portfolio holdings, CRM support history, and allocation diagnostics.
* [`evals/eval_cases.json`](./evals/eval_cases.json): Synthetic test cases for evaluating routing accuracy and guardrail adherence.

---

## Quick Start / Running the Demo

Run the agent orchestration locally:

```bash
python 01-401k-retention-agent/src/agent_system.py
