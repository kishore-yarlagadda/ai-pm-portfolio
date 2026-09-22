# Discovery: [initiative name]

> Canonical discovery template. Replace bracketed prompts only with sourced facts. If a fact is not known, use an unknown record rather than guessing.

## Document control

| Field | Value | Evidence |
| --- | --- | --- |
| Initiative | [name or `UNKNOWN`] | [source ID] |
| As-of date | [ISO 8601 date or `UNKNOWN`] | [source ID or reason unknown] |
| Prepared by | [name/role or `UNKNOWN`] | [source ID] |
| Decision state | [observed state or `UNKNOWN`] | [source ID] |

Do not infer a lifecycle status from the existence of this document. Record only a state used by the actual workflow and cite the system or decision that set it.

## Evidence protocol

### Source register

Give every source a stable ID. Distinguish observations from interpretations. Do not treat generated text as evidence unless it is explicitly being evaluated as an artifact.

| ID | Source type | Title or description | Location | Captured at | Relevant excerpt or fields | Reliability / limits |
| --- | --- | --- | --- | --- | --- | --- |
| S-001 | [interview, log, dataset, ticket, document, experiment, other] | [title] | [durable link/path or access note] | [timestamp or `UNKNOWN`] | [quote, query, or field names] | [limits] |

### Unknown register

`UNKNOWN` is a valid result. Do not replace it with a plausible value.

| ID | Unknown | Why it matters | What would resolve it | Resolution owner | Target date | State |
| --- | --- | --- | --- | --- | --- | --- |
| U-001 | [question] | [decision affected] | [specific evidence needed] | [confirmed owner or `UNKNOWN`] | [date or `UNKNOWN`] | [observed state or `UNKNOWN`] |

### Claim ledger

| Claim ID | Claim | Type | Supporting source IDs | Contradicting source IDs | Confidence and rationale | Decision impact |
| --- | --- | --- | --- | --- | --- | --- |
| C-001 | [claim] | [fact, interpretation, hypothesis] | [S-IDs or `NONE`] | [S-IDs or `NONE`] | [high/medium/low plus reason, or `UNKNOWN`] | [impact] |

A hypothesis with no supporting evidence must remain labeled as a hypothesis.

## Problem framing

### Trigger

- Observed event or request: [fact or `UNKNOWN`]
- Source: [S-ID]
- Why investigate now: [evidence-backed reason or `UNKNOWN`]

### Users and affected parties

Do not invent personas or stakeholder names. Use observed cohorts, roles, or behaviors and cite them.

| Group | Evidence that the group exists and is affected | Need or job | Current behavior / workaround | Source IDs | Unknowns |
| --- | --- | --- | --- | --- | --- |
| [observed group or `UNKNOWN`] | [evidence] | [need or `UNKNOWN`] | [behavior or `UNKNOWN`] | [S-IDs] | [U-IDs] |

### Current workflow and pain

Describe the current sequence from direct evidence. Separate frequency, severity, and consequence.

| Step | Actor/system | Observed behavior | Friction or failure | Frequency definition and value | Severity definition and value | Source IDs |
| --- | --- | --- | --- | --- | --- | --- |
| [step] | [observed actor/system] | [behavior] | [issue] | [definition + value, or `UNKNOWN`] | [definition + value, or `UNKNOWN`] | [S-IDs] |

### Root-cause hypotheses

| Hypothesis | Evidence for | Evidence against | Test | Result | Decision rule |
| --- | --- | --- | --- | --- | --- |
| [hypothesis] | [S-IDs or `NONE`] | [S-IDs or `NONE`] | [test] | [result or `NOT RUN`] | [what result changes the decision] |

## Opportunity and constraints

### Desired outcome

State the user or business outcome without selecting a solution. Cite the request or evidence.

[Outcome or `UNKNOWN`] ([S-ID or U-ID])

### Constraints

| Constraint | Type | Evidence | Consequence | Confidence |
| --- | --- | --- | --- | --- |
| [constraint] | [policy, technical, legal, data, time, budget, operational] | [S-ID] | [effect] | [rating + reason] |

### Existing system and data inventory

| Asset | Current interface / format | Access and retention | Quality observations | Source IDs | Unknowns |
| --- | --- | --- | --- | --- | --- |
| [asset] | [observed interface/schema] | [fact or `UNKNOWN`] | [observations only] | [S-IDs] | [U-IDs] |

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
| P-001 | [decision] | [labels] | [source] | [expectation] | [mechanism or `UNKNOWN`] | [runs/seeds or `UNKNOWN`] | [S-/U-IDs] |

### Scoring, cost, and Pareto questions

Do not combine measures until their definitions, direction, units, missing-data behavior, and aggregation rule are specified.

| Measure | Definition | Unit / range | Direction | Baseline | Slice / sample | Uncertainty | Source / unknown |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [measure] | [formula or rubric] | [unit] | [higher/lower is better] | [value or `UNKNOWN`] | [population] | [method or `UNKNOWN`] | [S-/U-ID] |

- Candidate cost model: [provider price snapshot, infrastructure, human review, retries, or `UNKNOWN`].
- Comparison rule: [per request, per successful task, per token, per dataset run, or `UNKNOWN`].
- Pareto question: Which candidates are non-dominated for the explicitly selected quality, cost, latency, and safety measures?
- Weighting or single-score rule: [decision owner-approved rule or `NONE`]. Never invent weights to force a ranking.

### Human-in-the-loop discovery

Use system-observed state names when available. Until then, use semantic descriptions and mark mappings unknown.

| Semantic state | Entry condition | Permitted action | Exit evidence | Actual system value |
| --- | --- | --- | --- | --- |
| Awaiting review | [condition or `UNKNOWN`] | [action or `UNKNOWN`] | [evidence] | [value or `UNKNOWN`] |
| Changes requested | [condition or `UNKNOWN`] | [action or `UNKNOWN`] | [evidence] | [value or `UNKNOWN`] |
| Approved | [condition or `UNKNOWN`] | [action or `UNKNOWN`] | [evidence] | [value or `UNKNOWN`] |
| Rejected | [condition or `UNKNOWN`] | [action or `UNKNOWN`] | [evidence] | [value or `UNKNOWN`] |
| Superseded / invalidated | [condition or `UNKNOWN`] | [action or `UNKNOWN`] | [evidence] | [value or `UNKNOWN`] |

## Discovery tests and findings

| Test ID | Question | Method | Sample / slice | Predefined decision rule | Result | Evidence | Limitations |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D-001 | [question] | [method] | [sample] | [rule] | [result or `NOT RUN`] | [S-ID] | [limits] |

## Discovery conclusion

- Supported findings: [C-IDs]
- Rejected or weakened hypotheses: [IDs and why]
- Material unknowns: [U-IDs]
- Options worth evaluating next: [options, each linked to evidence]
- Decision requested: [decision or `NONE`]
- Explicit non-decisions: [what this document does not approve]
