# Product Requirements Document: 401(k) Rollover & Retention Multi-Agent System

## 1. Executive Summary
An AI-driven multi-agent customer workflow designed to balance enterprise retention goals with customer-centric financial guidance. It proactively identifies customer retention opportunities while maintaining a frictionless, compliant rollover path if the customer declines retention offers.

## 2. Customer Problem & Hypothesis
* **Problem:** Customers initiating a 401(k) rollover often leave without understanding the financial advantages of staying (e.g., lower institutional fee structures, unvested matches). Conversely, aggressive retention tactics erode trust and increase churn.
* **Hypothesis:** A single-pivot, highly empathetic agent offering transparent fee/value comparisons can increase retention by 18% without negatively impacting customer satisfaction scores (CSAT).

## 3. Agent Architecture & Responsibilities
* **Supervisor / Router:** Evaluates intent, checks state history, and enforces routing guardrails.
* **Value & Retention Agent:** Performs personalized value/fee analysis and delivers at most ONE non-intrusive retention offer.
* **Rollover Execution Agent:** Handles account verification, form generation, and compliance checks if retention is declined or explicitly bypassed.

## 4. Key Guardrails & Principles
* **Single-Pivot Rule:** Maximum of 1 retention attempt per session. If the user insists on leaving or declines the offer, instantly transition to execution.
* **No Dark Patterns:** Clear, direct options to proceed with rollover at all times.
* **Fiduciary/FINRA Compliance:** Strict separation between objective fee/value comparisons and regulated financial advice.

## 5. Success Metrics
* **Business KPIs:** AUM Retained ($), Retention Conversion Rate, Post-Interaction NPS.
* **Technical KPIs:** Intent Routing Accuracy (>95%), Average Latency ($P_{95} < 2.5\text{s}$), Guardrail Violations (0%).

## 6. Routing Policy

- *Standard rollover intent:* Present at most one objective value comparison, then honor the customer's decision.
- *Explicit bypass or declined offer:* Route directly to rollover execution with no additional retention attempt.
- *High-balance assisted path:* When the configured balance threshold is met, present the same single objective comparison, flag the case for human specialist review, and offer a retirement specialist. An explicit bypass still routes directly to execution without waiting for human review.
- *Tax or legal question:* Escalate to a qualified human professional without offering regulated advice.
- *Out-of-scope service request:* Route to general customer support. Do not present a retention offer.
- *Abuse, fraud allegation, or regulator threat:* Route to human service/compliance review. Do not present a retention offer.
- *Prompt injection or policy override attempt:* Reject the override and route to compliance review. Do not claim that a financial transaction was executed.

The high-balance threshold must be configurable rather than embedded in routing logic.
