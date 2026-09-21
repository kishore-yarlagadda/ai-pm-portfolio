# Product Requirements Document: 401(k) Rollover & Retention Multi-Agent System

## 1. Executive Summary
An AI-assisted multi-agent customer workflow designed to balance retention goals with customer-centric financial guidance. A deterministic supervisor coordinates three focused agents - context, analysis, and compliance critique - to present at most one objective value comparison while keeping a frictionless, compliant rollover handoff path available whenever the customer asks to proceed.

## 2. Customer Problem & Hypothesis
* **Problem:** Customers initiating a 401(k) rollover often leave without understanding the financial trade-offs of staying (e.g., lower institutional fee structures). Conversely, aggressive retention tactics erode trust and increase churn.
* **Hypothesis (unvalidated):** A single-pivot, empathetic agent offering transparent fee/value comparisons could increase retention without harming customer satisfaction. This prototype exists to make that policy testable; it does not claim a measured retention lift.

## 3. Agent Architecture & Responsibilities
* **Supervisor / Router (`src/agent_system.py`):** Evaluates intent, checks state history, and enforces routing guardrails in a fixed order. It is the only component allowed to choose an action or change session state, and it calls the agent pipeline only on an eligible retention turn.
* **ContextAgent (`src/agents/context_agent.py`):** Builds validated customer context from the synthetic CRM and portfolio fixtures. It rejects unknown or invalid customers (`ContextError`) and derives session-level signals from the customer's own words in the current session plus verified account data; CRM case notes and persona labels never contribute: `high_balance`, `fee_sensitive`, `urgent_exit`, and `tax_complexity`.
* **AnalysisAgent (`src/agents/analysis_agent.py`):** Owns the what-if fee engine. Returns figures, explicit assumptions, customer options, and a summary, and raises `AnalysisError` when verified analysis cannot be produced. Its figures must match the engine exactly - no invented numbers.
* **ComplianceCritic (`src/agents/compliance_critic.py`):** Deterministic rule-based review of customer-facing drafts. Rejects executed-transaction claims, tax or legal advice, retention language on a bypass route, and missing synthetic/not-advice disclosures, then repairs the draft with verified text and flags human review. The supervisor passes every customer-facing draft on every route through the critic before returning it.

There is deliberately no execution agent: the bypass outcome is a rollover handoff - a deterministic routing decision, not a transaction. The internal action constant `ROUTE_TO_ROLLOVER_EXECUTION` remains stable for evaluation compatibility and does not mean a transaction executes.

## 4. Fixture Personas vs. Derived Session Signals
* **Fixture personas** (`src/connectors.py`): three synthetic customers (a fee-sensitive optimizer, a frustrated urgent exiter, and a tax-sensitive near-retiree) exist only to make the demo and evaluations reproducible. They are test fixtures, not a customer model.
* **Derived session signals:** the ContextAgent computes `high_balance`, `fee_sensitive`, `urgent_exit`, and `tax_complexity` on each turn from the customer messages in the current session and account data. CRM case notes and persona labels never set a signal; the contract tests verify that identical session wording yields identical signals for every fixture, and that fixture notes alone never turn a signal on.

## 5. Key Guardrails & Principles
* **Single-Pivot Rule:** Maximum of 1 retention attempt per session. If the user insists on leaving or declines the offer, instantly transition to the rollover handoff.
* **No Dark Patterns:** Clear, direct options to proceed with the rollover at all times.
* **Deterministic Authority:** Routing, state, and guardrails are deterministic and testable. Optional LLM generation shapes language only and cannot select a route, bypass a guardrail, or claim a transaction.
* **Advice Boundary:** Strict separation between objective fee/value comparisons on synthetic data and regulated financial advice. Tax or legal questions escalate to a qualified human professional.
* **Safe Failure:** When verified customer context or analysis cannot be produced, the system routes to general support rather than fabricating an answer.

## 6. Success Metrics
* **Prototype KPIs (measured):** Evaluation harness route/flag accuracy (currently 9/9 checks passing), per-agent contract checks (currently 6/6 passing), guardrail violations across the suite (0).
* **Business KPIs (future validation only):** AUM retained, retention conversion rate, post-interaction NPS. No business lift is claimed from this prototype.

## 7. Routing Policy

- *Standard rollover intent:* Present at most one objective value comparison, then honor the customer's decision.
- *Explicit bypass or declined offer:* Route directly to the rollover handoff with no additional retention attempt. (Internal action constant: `ROUTE_TO_ROLLOVER_EXECUTION`; no transaction executes.)
- *High-balance assisted path:* When the configured balance threshold is met, present the same single objective comparison, flag the case for human specialist review, and offer a retirement specialist. An explicit bypass still routes directly to the handoff without waiting for human review.
- *Tax or legal question:* Escalate to a qualified human professional without offering regulated advice.
- *Out-of-scope service request:* Route to general customer support. Do not present a retention offer.
- *Abuse, fraud allegation, or regulator threat:* Route to human service/compliance review. Do not present a retention offer.
- *Prompt injection or policy override attempt:* Reject the override and route to compliance review. Do not claim that a financial transaction was executed.
- *Unknown or invalid customer:* Route to general support without a traceback or a fabricated comparison.

The high-balance threshold must be configurable rather than embedded in routing logic.

## 8. Future Work (not in this prototype)
Further agent decomposition is future work, not current capability: a real handoff integration with a recordkeeper, retrieval over versioned plan documents, per-signal confidence scoring, and a richer compliance critic. The current critic is deliberately rule-based and testable; anything beyond deterministic checks is out of scope for this branch.
