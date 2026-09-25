# Two-Minute Demo Walkthrough

## 0:00-0:20 - Problem and product judgment

401(k) rollover flows create a real product tension: firms want to retain assets, while customers need a direct, trustworthy exit. This prototype tests a single-pivot policy - one objective value comparison at most, with an immediate rollover handoff whenever the customer asks to proceed.

## 0:20-0:50 - Architecture and AI boundary

A deterministic supervisor owns routing and state, and coordinates three agents that each do one job: a ContextAgent validates the customer and derives session signals from the customer's own words in the session, an AnalysisAgent runs the fee engine and returns verified figures with assumptions and options, and a ComplianceCritic reviews every customer-facing response on every route, rejecting or repairing unsafe wording before anything reaches the customer. The design pairs agentic analysis with deterministic authority boundaries on purpose: generation and decomposition make the comparison useful, while routes, guardrails, and customer rights stay rule-based and testable. On an eligible retention route only, the optional live LLM may select one fact-free acknowledgment from an exact code allowlist before the complete deterministic comparison. Any other output falls back to the unchanged deterministic draft, and the combined response still passes through the ComplianceCritic.

## 0:50-1:20 - Show the safety behavior

Run the interactive demo, pick any persona, and enter an explicit bypass such as Transfer immediately. The system routes directly to the rollover handoff without a retention pitch. Then point to the high-balance assisted path: one objective comparison, a specialist option, and a human-review flag, while an explicit bypass still cannot be delayed. Mention that an unknown customer ID now fails safe to general support instead of crashing or inventing an analysis.

## 1:20-1:45 - Show evaluation discipline

Run python evals/eval_harness.py. The nine checks cover direct bypass, tax escalation, high-balance flags, out-of-scope support, severe complaints, prompt injection, and the real two-turn single-pivot sequence. Then run python evals/agent_contracts.py. The seven contract checks prove each agent does distinct work: context failures route safely, analysis figures match the engine exactly, session signals come from the session's customer words and provably ignore fixture notes and persona labels, the critic rejects and repairs executed-transaction claims, tax advice, and missing disclosures, every supervisor route returns only critic-reviewed responses, and optional LLM drafting accepts only an exact allowlisted acknowledgment while adversarial output falls back to unchanged deterministic content and routing.

## 1:45-2:00 - Close honestly

This is a runnable portfolio prototype, not a production recordkeeping system. It uses synthetic data, does not provide advice, and never executes a transaction - "rollover handoff" is a routing outcome, and the historical internal constant ROUTE_TO_ROLLOVER_EXECUTION is kept only so the published evaluation contract keeps passing. The point is the product and governance design: use agents and generation where they help, but keep customer rights and regulated routing deterministic and testable.

## Commands

source .venv/bin/activate
python src/interactive_demo.py
python evals/eval_harness.py
python evals/agent_contracts.py

## Plan document Q&A (retrieval-grounded)

The agent can now answer questions about 401(k) plan documents. Sample questions: What is the vesting schedule? When am I eligible to contribute? What is the employer match?

How it works, end to end:
1. The supervisor classifies the question and routes plan-document questions to the plan Q&A path.
2. Retrieval runs BM25 keyword search over synthetic Summary Plan Descriptions (SPDs). Tokenization strips stopwords and singularizes words so filler words do not dominate the match.
3. Matches scoring below a minimum threshold (1.0, set from measured scores) are treated as no match.
4. The answer is grounded in the retrieved section and cites the source plan.
5. If nothing matches, or the question asks for personal advice, the question escalates to a human instead of guessing.
6. The compliance critic rejects any plan answer that is missing its citation.

Evals: five new cases (TC-010 to TC-014) cover cited answers, no-match escalation, and advice-seeking escalation. Full suite: 14 of 14 passing.
