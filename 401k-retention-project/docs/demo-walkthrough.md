# Two-Minute Demo Walkthrough

## 0:00-0:20 - Problem and product judgment

401(k) rollover flows create a real product tension: firms want to retain assets, while customers need a direct, trustworthy exit. This prototype tests a single-pivot policy - one objective value comparison at most, with an immediate bypass whenever the customer asks to proceed.

## 0:20-0:50 - Architecture and AI boundary

The deterministic supervisor owns routing and state. Synthetic CRM and portfolio fixtures provide context, and a fee engine produces the comparison. The optional LLM only shapes response language; it cannot choose a route, override a guardrail, or execute a transaction.

## 0:50-1:20 - Show the safety behavior

Run the interactive demo with Sarah and enter Transfer immediately. The system should route directly to rollover execution without a retention pitch. Then point to the high-balance assisted path: one objective comparison, a specialist option, and a human-review flag, while explicit bypass still cannot be delayed.

## 1:20-1:45 - Show evaluation discipline

Run python evals/eval_harness.py. The nine checks cover direct bypass, tax escalation, high-balance flags, out-of-scope support, severe complaints, prompt injection, and the real two-turn single-pivot sequence.

## 1:45-2:00 - Close honestly

This is a runnable portfolio prototype, not a production recordkeeping system. It uses synthetic data, does not provide advice or execute transactions, and makes the AI boundary visible. The point is the product and governance design: use generation where it helps, but keep customer rights and regulated routing deterministic and testable.

## Commands

source .venv/bin/activate
python src/interactive_demo.py
python evals/eval_harness.py
