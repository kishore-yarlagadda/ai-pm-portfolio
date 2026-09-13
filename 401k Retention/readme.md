# 401(k) Rollover & Retention Multi-Agent System

## Executive Summary
This project demonstrates an enterprise-grade AI multi-agent system designed to address high-friction 401(k) rollover requests. It balances business retention targets with customer experience (CX) and fiduciary compliance by prioritizing transparent value comparisons while respecting user autonomy.

## Key Product & Technical Features
- **Deterministic Supervisor Routing:** Utilizes state-based conditional logic to enforce single-pivot retention guardrails.
- **Single-Pivot CX Guardrail:** Restricts automated retention offers to maximum 1 attempt per session to prevent dark-pattern frustration and preserve customer trust.
- **Explicit User Bypass:** Detects direct user intent ("Skip pitch", "Transfer immediately") and immediately routes to rollover execution without friction.
- **Enterprise Data Connectors:** Integrates live-style portfolio holdings, historical support CRM touchpoints, and diagnostic asset allocation engines.

## Directory Artifacts
- `docs/PRD.md`: Full Product Requirements Document covering business metrics, guardrails, and agent responsibilities.
- `src/agent_system.py`: Python implementation of the multi-agent orchestration state machine.
- `src/connectors.py`: Enterprise connectors for portfolio holdings, CRM history, and portfolio diagnostics.
- `evals/eval_cases.json`: Test suite for evaluating routing accuracy, tone compliance, and guardrail enforcement.

## Running the Demo
To simulate the agent orchestration:
```bash
python src/agent_system.py
