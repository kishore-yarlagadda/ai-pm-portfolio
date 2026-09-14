# System Architecture Design Specification
**Feature Request:** {feature_request}
**Framework Applied:** RTF (Requirements, Topology, Flow)

## 1. Component Topology
- `eval_runner.py`: Orchestrates the execution lifecycle and manages state progression.
- `adversarial_prober.py`: Generates and dispatches edge-case adversarial prompts.
- `cost_tracker.py`: Measures token usage, latency, and computes Pareto metrics.

## 2. Data Flow Architecture
1. **Initialization:** User invokes orchestrator script with custom feature request string.
2. **State Transition:** Orchestrator reads configuration, updates state machine, and persists artifacts into structured subdirectories (`documents`, `prds`, `architecture`, `code`, `tests`, `data`).
3. **Execution Gate:** HITL validation halts progression until developer/PM approval is verified.
