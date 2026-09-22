# Discovery: LLM Evaluator

> Canonical discovery template. Replace bracketed prompts only with sourced facts. If a fact is not known, use an unknown record rather than guessing.

## Document control

| Field | Value | Evidence |
| --- | --- | --- |
| Initiative | LLM Evaluator | Feature name |
| As-of date | `UNKNOWN` | U-001 |
| Prepared by | `UNKNOWN` | U-002 |
| Decision state | `UNKNOWN` | U-003 |

Do not infer a lifecycle status from the existence of this document. Record only a state used by the actual workflow and cite the system or decision that set it.

## Evidence protocol

### Source register

Give every source a stable ID. Distinguish observations from interpretations. Do not treat generated text as evidence unless it is explicitly being evaluated as an artifact.

| ID | Source type | Title or description | Location | Captured at | Relevant excerpt or fields | Reliability / limits |
| --- | --- | --- | --- | --- | --- | --- |
| S-001 | `UNKNOWN` | No brief supplied | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | Brief was not provided; no direct facts available beyond feature name. |

### Unknown register

`UNKNOWN` is a valid result. Do not replace it with a plausible value.

| ID | Unknown | Why it matters | What would resolve it | Resolution owner | Target date | State |
| --- | --- | --- | --- | --- | --- | --- |
| U-001 | Document as-of date | Required for document control and tracking freshness | Provide ISO 8601 creation/update timestamp | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |
| U-002 | Document author/preparer | Establishes document ownership | Identify author name and role | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |
| U-003 | Formal decision state | Tracks governance workflow status | Obtain state from decision workflow system | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |
| U-004 | Trigger event and motivation | Explains why this feature is being investigated now | Provide feature brief or intake ticket | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |
| U-005 | Target user cohorts and needs | Identifies affected users, personas, and workarounds | Conduct user discovery or provide product brief | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |
| U-006 | Current workflow steps and friction | Documents baseline user experience, frequency, and severity | Collect workflow telemetry or user feedback | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |
| U-007 | Desired outcomes and success metrics | Establishes success criteria for the feature | Provide explicit outcome targets | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |
| U-008 | Constraints (technical, legal, data, budget) | Bounds the solution space and feasibility | Conduct technical and compliance reviews | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |
| U-009 | Existing system and data inventory | Identifies integration points and data quality | Audit existing system architecture | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |
| U-010 | Probe taxonomy and evaluation specifications | Defines evaluation probes, rubrics, and judges | Define evaluation probe requirements | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |
| U-011 | Scoring metrics, baseline values, and cost model | Determines scoring, cost model, and Pareto tradeoffs | Establish baseline evaluation benchmarks | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |
| U-012 | Human-in-the-loop state mappings | Maps human review states to actual system values | Define HITL workflow specifications | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |
| U-013 | Discovery tests and empirical findings | Validates product hypotheses through testing | Design and execute discovery experiments | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |

### Claim ledger

| Claim ID | Claim | Type | Supporting source IDs | Contradicting source IDs | Confidence and rationale | Decision impact |
| --- | --- | --- | --- | --- | --- | --- |
| C-001 | The initiative is intended to evaluate Large Language Model outputs, capabilities, or systems. | hypothesis | `NONE` | `NONE` | Low confidence; inferred solely from the feature name "LLM Evaluator" without brief evidence. | Guides initial problem framing. |

A hypothesis with no supporting evidence must remain labeled as a hypothesis.

## Problem framing

### Trigger

- Observed event or request: `UNKNOWN`
- Source: `UNKNOWN`
- Why investigate now: `UNKNOWN`

### Users and affected parties

Do not invent personas or stakeholder names. Use observed cohorts, roles, or behaviors and cite them.

| Group | Evidence that the group exists and is affected | Need or job | Current behavior / workaround | Source IDs | Unknowns |
| --- | --- | --- | --- | --- | --- |
| `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NONE` | U-005 |

### Current workflow and pain

Describe the current sequence from direct evidence. Separate frequency, severity, and consequence.

| Step | Actor/system | Observed behavior | Friction or failure | Frequency definition and value | Severity definition and value | Source IDs |
| --- | --- | --- | --- | --- | --- | --- |
| `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NONE` |

### Root-cause hypotheses

| Hypothesis | Evidence for | Evidence against | Test | Result | Decision rule |
| --- | --- | --- | --- | --- | --- |
| `UNKNOWN` | `NONE` | `NONE` | `UNKNOWN` | `NOT RUN` | `UNKNOWN` |

## Opportunity and constraints

### Desired outcome

State the user or business outcome without selecting a solution. Cite the request or evidence.

`UNKNOWN` (U-007)

### Constraints

| Constraint | Type | Evidence | Consequence | Confidence |
| --- | --- | --- | --- | --- |
| `UNKNOWN` | `UNKNOWN` | `NONE` | `UNKNOWN` | `UNKNOWN` |

### Existing system and data inventory

| Asset | Current interface / format | Access and retention | Quality observations | Source IDs | Unknowns |
| --- | --- | --- | --- | --- | --- |
| `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NONE` | U-009 |

## LLM evaluator discovery lens

Use this section when the initiative evaluates LLM systems. The taxonomy is a classification scheme, not proof that every probe exists or is in scope.

### Probe taxonomy

Classify each proposed probe along all applicable axes:

- **Capability:** task completion, instruction following, reasoning, retrieval/grounding, tool use, structured output, multimodal behavior.
- **Quality risk:** factuality, relevance, completeness, consistency, calibration, citation quality.
- **Safety and control:** policy compliance, harmful content, privacy, security/prompt injection, authorization boundaries.
- **Reliability:** determinism/variance, retry behavior, latency, timeout and failure recovery.
- **Operational:** token use, monetary cost, throughput, model/provider portability.
- **Test form:** deterministic check, model-graded rubric, human review, pairwise comparison, adversarial/red-team, regression.
- **Slice:** model/version, prompt/version, dataset/version, language, cohort, environment, difficulty, and other sourced segment.

| Probe ID | Decision it informs | Taxonomy labels | Input source / slice | Expected behavior or rubric | Oracle / judge | Repeat policy | Evidence / unknowns |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P-001 | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | U-010 |

### Scoring, cost, and Pareto questions

Do not combine measures until their definitions, direction, units, missing-data behavior, and aggregation rule are specified.

| Measure | Definition | Unit / range | Direction | Baseline | Slice / sample | Uncertainty | Source / unknown |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | U-011 |

- Candidate cost model: `UNKNOWN`
- Comparison rule: `UNKNOWN`
- Pareto question: Which candidates are non-dominated for the explicitly selected quality, cost, latency, and safety measures?
- Weighting or single-score rule: `NONE`

### Human-in-the-loop discovery

Use system-observed state names when available. Until then, use semantic descriptions and mark mappings unknown.

| Semantic state | Entry condition | Permitted action | Exit evidence | Actual system value |
| --- | --- | --- | --- | --- |
| Awaiting review | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |
| Changes requested | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |
| Approved | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |
| Rejected | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |
| Superseded / invalidated | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |

## Discovery tests and findings

| Test ID | Question | Method | Sample / slice | Predefined decision rule | Result | Evidence | Limitations |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D-001 | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NOT RUN` | `NONE` | `UNKNOWN` |

## Discovery conclusion

- Supported findings: `NONE`
- Rejected or weakened hypotheses: `NONE`
- Material unknowns: U-001, U-002, U-003, U-004, U-005, U-006, U-007, U-008, U-009, U-010, U-011, U-012, U-013
- Options worth evaluating next: `UNKNOWN`
- Decision requested: `NONE`
- Explicit non-decisions: No approval, architecture selection, or deployment decisions are made in this document.