# Strategy: [initiative name]

> Canonical strategy template. Strategy selects a direction from evidence; it does not manufacture facts. Complete the [discovery](discovery_template.md) first or state why it is unavailable.

## Document control

| Field | Value | Evidence |
| --- | --- | --- |
| Initiative | [name or `UNKNOWN`] | [source ID] |
| As-of date | [ISO 8601 date or `UNKNOWN`] | [source ID or reason unknown] |
| Decision owner | [confirmed person/role or `UNKNOWN`] | [source ID] |
| Decision state | [observed state or `UNKNOWN`] | [source ID] |
| Discovery version | [commit, version, or `UNKNOWN`] | [durable path/link] |

Do not infer approval, ownership, or schedule. Cite the authority that set each one.

## Evidence carried forward

- Supported discovery claims: [claim IDs]
- Material contradictions: [claim IDs]
- Open unknowns: [unknown IDs]
- New sources added here: [source IDs with full source-register entries]

If a discovery claim changed, record the new evidence and impact rather than overwriting history.

## Decision to make

- Decision statement: [specific choice or `UNKNOWN`]
- Decision deadline: [sourced date or `UNKNOWN`]
- Decision criteria: [criteria and source]
- Reversibility: [reversible, partly reversible, hard to reverse, or `UNKNOWN`, with rationale]

## Outcomes and metric contracts

Do not set targets before defining the measure and establishing or explicitly marking the baseline unknown.

| Metric ID | Outcome represented | Definition / formula | Unit | Population and exclusions | Window | Data source | Baseline | Target | Guardrail | Owner | Evidence / unknowns |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M-001 | [outcome] | [formula] | [unit] | [population] | [window] | [system/query] | [value + date or `UNKNOWN`] | [approved value or `UNKNOWN`] | [limit or `UNKNOWN`] | [confirmed owner or `UNKNOWN`] | [S-/U-IDs] |

A target without a source is a proposal, not a commitment. Label it `PROPOSED` and identify the decision needed.

## Strategic options

Include a do-nothing or continue-current-state option when it is plausible.

| Option | Description | Evidence fit | Expected benefits | Costs and constraints | Risks | Unknowns | Reversibility |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [option] | [scope] | [claim/source IDs] | [hypotheses, not promises] | [knowns/unknowns] | [risks] | [U-IDs] | [assessment] |

### Evaluation method

- Method: [trade-off table, experiment, cost-effectiveness, other]
- Criteria definitions: [definitions]
- Weights: [approved weights and source, or `NONE`]
- Sensitivity check: [whether plausible weight/baseline changes alter the choice]
- Decision record: [selected option or `NO DECISION`, authority, date, and evidence]

Do not use a priority score unless every input is sourced, its scale is defined, and the decision owner accepted the method.

## LLM evaluator strategy

### Evaluation surface and probe portfolio

Use the probe taxonomy defined in [discovery](discovery_template.md). Record why each included probe changes a decision and which risks remain uncovered.

| Probe family | Included slices | Decision / risk covered | Method | Judge / oracle | Regression policy | Gaps |
| --- | --- | --- | --- | --- | --- | --- |
| [taxonomy label] | [slices] | [decision/risk] | [deterministic, model-graded, human, pairwise, adversarial] | [mechanism] | [when run/fail behavior or `UNKNOWN`] | [gaps] |

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
| [score] | [section/path] | [value or `UNKNOWN`] | [source or U-ID] | [limits] |

### Cost and Pareto policy

- Cost boundary: [API, infrastructure, human review, retries, storage, or other included components]
- Price source and captured date: [source or `UNKNOWN`]
- Normalization unit: [per request, successful task, token, run, or `UNKNOWN`]
- Quality dimensions: [defined metric IDs]
- Operational dimensions: [cost/latency metric IDs]
- Hard constraints: [sourced limits or `UNKNOWN`]
- Pareto rule: Report non-dominated candidates across the selected dimensions; show dominated candidates and the dimension causing domination.
- Tie and uncertainty policy: [policy or `UNKNOWN`]
- Composite rank: [approved formula/source or `NONE`]

### Human-in-the-loop control strategy

Do not map semantic states to implementation enums until the implementation is observed.

| Transition | Trigger | Actor authorized to act | Required evidence | Audit event | Failure / timeout behavior |
| --- | --- | --- | --- | --- | --- |
| Awaiting review -> Approved | [condition] | [confirmed role or `UNKNOWN`] | [artifact/version + review evidence] | [event contract] | [behavior or `UNKNOWN`] |
| Awaiting review -> Changes requested | [condition] | [confirmed role or `UNKNOWN`] | [review notes] | [event contract] | [behavior or `UNKNOWN`] |
| Awaiting review -> Rejected | [condition] | [confirmed role or `UNKNOWN`] | [reason] | [event contract] | [behavior or `UNKNOWN`] |
| Any active state -> Superseded / invalidated | [condition] | [confirmed role or `UNKNOWN`] | [new version/reason] | [event contract] | [behavior or `UNKNOWN`] |

No deployment or external effect may be inferred from approval unless an observed, separately authorized workflow defines that effect.

## Data and system strategy

### Data contracts

| Contract | Producer | Consumer | Schema/version | Required fields | Validation | PII/security classification | Retention | Failure behavior | Evidence / unknowns |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Evaluation case | [system] | [system] | [version or `UNKNOWN`] | [fields] | [rules] | [classification or `UNKNOWN`] | [policy or `UNKNOWN`] | [behavior] | [S-/U-IDs] |
| Probe result | [system] | [system] | [version or `UNKNOWN`] | [fields] | [rules] | [classification or `UNKNOWN`] | [policy or `UNKNOWN`] | [behavior] | [S-/U-IDs] |
| Review decision | [system] | [system] | [version or `UNKNOWN`] | [fields] | [rules] | [classification or `UNKNOWN`] | [policy or `UNKNOWN`] | [behavior] | [S-/U-IDs] |
| Cost record | [system] | [system] | [version or `UNKNOWN`] | [fields] | [rules] | [classification or `UNKNOWN`] | [policy or `UNKNOWN`] | [behavior] | [S-/U-IDs] |

Architecture is an input only when a real, accessible artifact exists. Record its path and version here; otherwise use `UNKNOWN` and open an unknown record.

## Sequencing without invented estimates

Sequence by evidence and dependency. Add dates or durations only when a source or approved estimate exists.

| Step | Learning or capability delivered | Entry evidence | Exit evidence | Dependencies | Estimate source | Timing |
| --- | --- | --- | --- | --- | --- | --- |
| [step] | [outcome] | [evidence] | [evidence] | [dependencies] | [source or `NONE`] | [duration/date or `UNKNOWN`] |

## Risks, controls, and stop conditions

| Risk | Evidence | Leading indicator | Control / experiment | Stop or rollback condition | Owner | Residual unknown |
| --- | --- | --- | --- | --- | --- | --- |
| [risk] | [S-ID] | [metric] | [control] | [condition] | [confirmed owner or `UNKNOWN`] | [U-ID] |

## Strategy decision record

- Selected direction: [option or `NO DECISION`]
- Supporting evidence: [claim/source IDs]
- Material dissent or contradiction: [IDs]
- Accepted unknowns: [U-IDs and accepting authority]
- Explicitly out of scope: [items]
- Revisit trigger: [new evidence or metric condition]
- Authority and date: [source or `UNKNOWN`]
