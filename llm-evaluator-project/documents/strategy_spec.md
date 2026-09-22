# Strategy: LLM Evaluator

> Canonical strategy template. Strategy selects a direction from evidence; it does not manufacture facts. Complete the [discovery](discovery_template.md) first or state why it is unavailable.

## Document control

| Field | Value | Evidence |
| --- | --- | --- |
| Initiative | LLM Evaluator | FEATURE name |
| As-of date | `UNKNOWN` | No brief supplied |
| Decision owner | `UNKNOWN` | No brief supplied |
| Decision state | `UNKNOWN` | No brief supplied |
| Discovery version | `UNKNOWN` | Discovery template unavailable / no brief supplied |

Do not infer approval, ownership, or schedule. Cite the authority that set each one.

## Evidence carried forward

- Supported discovery claims: NONE
- Material contradictions: NONE
- Open unknowns: U-001, U-002, U-003, U-004, U-005, U-006, U-007, U-008, U-009, U-010
- New sources added here: NONE

If a discovery claim changed, record the new evidence and impact rather than overwriting history.

### Unknown register
- **U-001**: Document metadata (as-of date, decision owner, decision state, discovery version) missing due to absence of brief.
- **U-002**: Decision scope, statement, deadline, and criteria missing.
- **U-003**: Metric definitions, baselines, targets, guardrails, and owners missing.
- **U-004**: Evaluation surfaces, probe taxonomy, probe families, slices, judges/oracles, and regression policies missing.
- **U-005**: Score contracts, rubrics, scales, aggregation units, judge identities, calibration evidence, and threshold sources missing.
- **U-006**: Cost boundaries, price sources, normalization units, quality/operational dimensions, and hard constraints missing.
- **U-007**: Human-in-the-loop transition triggers, authorized actors, required evidence, audit events, and timeout behaviors missing.
- **U-008**: Data contracts, producers, consumers, schemas, required fields, validation rules, classifications, retention policies, and failure behaviors missing.
- **U-009**: Capability delivery sequencing steps, entry/exit evidence, dependencies, and timing estimates missing.
- **U-010**: Identified risks, evidence, leading indicators, controls, stop conditions, and risk owners missing.

### Claim ledger
- **C-001** (Option 1 Benefit): *Hypothesis*: Implementing an LLM Evaluator feature may enable automated or systematic quality evaluation of LLM outputs. (Confidence: Low; Rationale: Derived solely from feature title "LLM Evaluator" without supporting brief or technical specifications.)

## Decision to make

- Decision statement: `UNKNOWN`
- Decision deadline: `UNKNOWN`
- Decision criteria: `UNKNOWN`
- Reversibility: `UNKNOWN`

## Outcomes and metric contracts

Do not set targets before defining the measure and establishing or explicitly marking the baseline unknown.

| Metric ID | Outcome represented | Definition / formula | Unit | Population and exclusions | Window | Data source | Baseline | Target | Guardrail | Owner | Evidence / unknowns |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M-001 | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | U-003 |

A target without a source is a proposal, not a commitment. Label it `PROPOSED` and identify the decision needed.

## Strategic options

Include a do-nothing or continue-current-state option when it is plausible.

| Option | Description | Evidence fit | Expected benefits | Costs and constraints | Risks | Unknowns | Reversibility |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Option 1: Develop LLM Evaluator | Implement LLM Evaluator capability | `UNKNOWN` | [Hypothesis] May enable systematic evaluation of LLM outputs (C-001) | `UNKNOWN` | `UNKNOWN` | U-002 | `UNKNOWN` |
| Option 2: Do nothing / Continue current state | Maintain status quo without building LLM Evaluator | `UNKNOWN` | Incurs no development or infrastructure costs | `UNKNOWN` | `UNKNOWN` | U-002 | Reversible |

### Evaluation method

- Method: `UNKNOWN`
- Criteria definitions: `UNKNOWN`
- Weights: `NONE`
- Sensitivity check: `UNKNOWN`
- Decision record: `NO DECISION`, `UNKNOWN`, `UNKNOWN`, `UNKNOWN`

Do not use a priority score unless every input is sourced, its scale is defined, and the decision owner accepted the method.

## LLM evaluator strategy

### Evaluation surface and probe portfolio

Use the probe taxonomy defined in [discovery](discovery_template.md). Record why each included probe changes a decision and which risks remain uncovered.

| Probe family | Included slices | Decision / risk covered | Method | Judge / oracle | Regression policy | Gaps |
| --- | --- | --- | --- | --- | --- | --- |
| `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |

### Score contract

For each score define:

1. rubric or formula;
2. scale and direction;
3. aggregation unit and missing/invalid treatment;
4. sample and slice minimums;
5. judge identity/version and calibration evidence;
6. uncertainty or variance reporting;
7. pass/fail threshold source;
8. behavior when evidence is insufficient.

| Score | Contract location | Threshold | Threshold source | Known limitations |
| --- | --- | --- | --- | --- |
| `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | U-005 | `UNKNOWN` |

### Cost and Pareto policy

- Cost boundary: `UNKNOWN`
- Price source and captured date: `UNKNOWN`
- Normalization unit: `UNKNOWN`
- Quality dimensions: `UNKNOWN`
- Operational dimensions: `UNKNOWN`
- Hard constraints: `UNKNOWN`
- Pareto rule: Report non-dominated candidates across the selected dimensions; show dominated candidates and the dimension causing domination.
- Tie and uncertainty policy: `UNKNOWN`
- Composite rank: `NONE`

### Human-in-the-loop control strategy

Do not map semantic states to implementation enums until the implementation is observed.

| Transition | Trigger | Actor authorized to act | Required evidence | Audit event | Failure / timeout behavior |
| --- | --- | --- | --- | --- | --- |
| Awaiting review -> Approved | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |
| Awaiting review -> Changes requested | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |
| Awaiting review -> Rejected | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |
| Any active state -> Superseded / invalidated | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |

No deployment or external effect may be inferred from approval unless an observed, separately authorized workflow defines that effect.

## Data and system strategy

### Data contracts

| Contract | Producer | Consumer | Schema/version | Required fields | Validation | PII/security classification | Retention | Failure behavior | Evidence / unknowns |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Evaluation case | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | U-008 |
| Probe result | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | U-008 |
| Review decision | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | U-008 |
| Cost record | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | U-008 |

Architecture is an input only when a real, accessible artifact exists. Record its path and version here; otherwise use `UNKNOWN` and open an unknown record.

## Sequencing without invented estimates

Sequence by evidence and dependency. Add dates or durations only when a source or approved estimate exists.

| Step | Learning or capability delivered | Entry evidence | Exit evidence | Dependencies | Estimate source | Timing |
| --- | --- | --- | --- | --- | --- | --- |
| `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NONE` | `UNKNOWN` |

## Risks, controls, and stop conditions

| Risk | Evidence | Leading indicator | Control / experiment | Stop or rollback condition | Owner | Residual unknown |
| --- | --- | --- | --- | --- | --- | --- |
| `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | U-010 |

## Strategy decision record

- Selected direction: `NO DECISION`
- Supporting evidence: `UNKNOWN`
- Material dissent or contradiction: `UNKNOWN`
- Accepted unknowns: U-001, U-002, U-003, U-004, U-005, U-006, U-007, U-008, U-009, U-010
- Explicitly out of scope: `UNKNOWN`
- Revisit trigger: `UNKNOWN`
- Authority and date: `UNKNOWN`