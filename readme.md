# 401(k) Rollover & Retention Multi-Agent System

An enterprise-grade AI multi-agent architecture built to handle high-friction 401(k) rollover requests[cite: 7]. This system balances business retention objectives with strict customer trust and fiduciary guardrails[cite: 7].

---

## Product Strategy & Business Objectives

High-friction rollover flows often rely on dark patterns or excessive deflection, leading to customer frustration and compliance risks[cite: 7]. This system introduces a **Trust-First Retention Framework**[cite: 7]:

* **Automated Value Analysis:** Conducts dynamic fee and performance comparisons using live holding data to highlight account value transparently[cite: 7].
* **Single-Pivot CX Guardrail:** Limits retention offers to a maximum of 1 attempt per session to eliminate user fatigue and prevent aggressive sales tactics[cite: 7].
* **Instant Intent Bypass:** Immediately detects explicit bypass commands ("Skip pitch", "Transfer immediately") and routes directly to rollover execution without friction[cite: 7].

---

## System Architecture

The architecture uses a **Supervisor Agent** pattern with deterministic state logic[cite: 7]:

1. **User Request & Intent Parsing:** Analyzes customer queries to determine rollover intent or explicit bypass requirements[cite: 7].
2. **Context Enrichment:** Fetches CRM historical data, current portfolio holdings, and allocation metrics via data connectors[cite: 7].
3. **Supervisor Routing:** Evaluates state and guardrail rules[cite: 7]:
   * Route to **Retention Flow** if within guardrail limits and no explicit bypass is requested[cite: 7].
   * Route to **Rollover Execution** if bypass is detected or maximum retention attempts are reached[cite: 7].
4. **What-If Analysis Engine:** Calculates fee differentials and portfolio projections for clear, factual comparisons[cite: 7].

---

## Directory Navigation

* [`docs/PRD.md`](./docs/PRD.md): Complete Product Requirements Document detailing business metrics, guardrails, and functional specs[cite: 7].
* [`src/agent_system.py`](./src/agent_system.py): Python orchestration logic defining state transitions and agent routing[cite: 7].
* [`src/connectors.py`](./src/connectors.py): Mock connectors for portfolio holdings, CRM support history, and allocation diagnostics[cite: 7].
* [`evals/eval_cases.json`](./evals/eval_cases.json): Synthetic test cases for evaluating routing accuracy and guardrail adherence[cite: 7].

---

## Quick Start / Running the Demo

Run the agent orchestration locally:

```bash
python src/agent_system.py
