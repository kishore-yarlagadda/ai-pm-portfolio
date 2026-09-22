# Product requirements: [initiative name]

> Canonical PRD template. Requirements must trace to evidence and strategy. Unknowns stay visible. This document does not imply approval, staffing, schedule, or production readiness. Inputs: [discovery](discovery_template.md) and [strategy](strategy_template.md).

## Document control

| Field | Value | Evidence |
| --- | --- | --- |
| Initiative | [name or `UNKNOWN`] | [source ID] |
| As-of date | [ISO 8601 date or `UNKNOWN`] | [source ID or reason unknown] |
| Product decision owner | [confirmed person/role or `UNKNOWN`] | [source ID] |
| Review state | [observed state or `UNKNOWN`] | [source ID] |
| Discovery version | [commit/version or `UNKNOWN`] | [path/link] |
| Strategy version | [commit/version or `UNKNOWN`] | [path/link] |
| Architecture version | [real artifact path/version or `UNKNOWN`] | [source or U-ID] |

## Traceability rules

- Every requirement has a stable ID and traces to a supported claim, approved strategy decision, constraint, or explicit unknown-resolution need.
- Every quantitative threshold cites its metric definition, baseline, and approval source.
- Every changed or removed requirement remains in the decision log.
- Generated prose, examples, and prototype behavior are not production facts.

## Problem and outcome

- Problem statement: [supported statement] ([claim/source IDs])
- Selected strategy: [decision] ([decision source])
- User groups: [observed groups and sources; no invented personas]
- Outcome metric IDs: [M-IDs]
- Guardrail metric IDs: [M-IDs]
- Material unknowns: [U-IDs]

## Scope

### In scope

| Item | Why included | Evidence / decision | Validation |
| --- | --- | --- | --- |
| [item] | [reason] | [ID] | [how verified] |

### Out of scope

| Item | Why excluded | Revisit trigger | Decision source |
| --- | --- | --- | --- |
| [item] | [reason] | [trigger] | [ID] |

### Assumptions to test

| Assumption | Evidence today | Test | Decision rule | State |
| --- | --- | --- | --- | --- |
| [assumption] | [S-IDs or `NONE`] | [test] | [rule] | [untested/tested result] |

## Functional requirements

Use RFC 2119 terms only for agreed product behavior, not to make uncertain facts sound certain.

| ID | Requirement | User / system need | Source | Priority method and evidence | Acceptance criteria | Unknowns |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | The system [behavior]. | [need] | [claim/decision/constraint ID] | [method + inputs, or `UNPRIORITIZED`] | [AC-IDs] | [U-IDs or `NONE`] |

## LLM evaluator requirements

### Probe definition and execution

Each probe must carry:

- stable probe ID and taxonomy labels from [discovery](discovery_template.md);
- dataset and slice version;
- input, context, and expected-output/rubric contract;
- model, prompt, tool, and judge versions;
- repeat/seed policy where variance matters;
- timeout, retry, invalid-result, and partial-run behavior;
- raw observation retention and provenance;
- decision the result informs.

| ID | Requirement | Trace | Acceptance criteria |
| --- | --- | --- | --- |
| ER-001 | Store the probe definition and all version identifiers used for a run. | [decision/claim ID] | [AC-IDs] |
| ER-002 | Preserve raw result provenance separately from derived scores. | [decision/constraint ID] | [AC-IDs] |
| ER-003 | Mark missing, invalid, timed-out, and skipped results distinctly; do not coerce them to passing or zero without an approved rule. | [score contract] | [AC-IDs] |
| ER-004 | Report results by defined slice and expose sample counts. | [metric/strategy ID] | [AC-IDs] |

### Scoring contract

| Score ID | Rubric / formula | Scale and direction | Aggregation and missing-data rule | Sample / slice rule | Judge and calibration | Threshold source | Uncertainty |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [SC-001] | [definition] | [range; direction] | [rule] | [rule] | [identity/version/evidence] | [source or `UNKNOWN`] | [method or `UNKNOWN`] |

Requirements:

- Keep component scores available when a composite exists.
- Never hide disagreement between deterministic, model-graded, and human results.
- Version rubrics and recalculate only under an explicit migration policy.
- Flag comparisons that use incompatible datasets, model versions, rubrics, or price snapshots.

### Cost, latency, and Pareto output

| Measure | Contract | Source | Freshness | Normalization |
| --- | --- | --- | --- | --- |
| API/model cost | [included fields/formula] | [provider/billing source or `UNKNOWN`] | [captured date] | [unit] |
| Human review cost | [time/rate treatment or `UNKNOWN`] | [source] | [captured date] | [unit] |
| Latency | [clock boundaries and percentile] | [telemetry] | [window] | [unit] |

- Compute dominance only across explicitly selected, direction-aware measures.
- A candidate is Pareto-dominated only if another is no worse on every selected measure and better on at least one, subject to the documented uncertainty policy.
- Show the selected dimensions, values, exclusions, and price snapshot beside the frontier.
- Do not emit a single winner unless a sourced decision rule resolves the trade-off.

### Human-in-the-loop states and audit

Semantic states are requirements; implementation values must be mapped from the actual system.

| State / transition | Entry condition | Authorized actor | Required input | Output / audit fields | Failure behavior |
| --- | --- | --- | --- | --- | --- |
| Awaiting review | [condition] | [role or `UNKNOWN`] | [versioned artifact] | [actor, timestamp, artifact version, prior state] | [behavior] |
| Changes requested | [condition] | [role or `UNKNOWN`] | [reason/notes] | [audit fields] | [behavior] |
| Approved | [condition] | [role or `UNKNOWN`] | [review evidence] | [audit fields] | [behavior] |
| Rejected | [condition] | [role or `UNKNOWN`] | [reason] | [audit fields] | [behavior] |
| Superseded / invalidated | [condition] | [role or `UNKNOWN`] | [new version/reason] | [audit fields] | [behavior] |

Required controls:

- stale reviews cannot approve a newer artifact version;
- transitions are authorized and auditable;
- retrying a transition is idempotent or safely rejected;
- approval alone triggers no deployment or external side effect unless a separately specified and authorized workflow says so;
- unresolved mappings to real enums remain `UNKNOWN` and block implementation acceptance.

## Data contracts

Define schemas in the repository's actual schema format when known. The tables below are the minimum contract checklist, not invented implementation.

### Evaluation case

| Field | Type | Required | Meaning | Validation | Classification / retention |
| --- | --- | --- | --- | --- | --- |
| case_id | [type or `UNKNOWN`] | [yes/no or `UNKNOWN`] | Stable case identity | [rule] | [policy or `UNKNOWN`] |
| dataset_version | [type or `UNKNOWN`] | [value] | Version of source dataset | [rule] | [policy or `UNKNOWN`] |
| input | [type or `UNKNOWN`] | [value] | Probe input | [rule] | [policy or `UNKNOWN`] |
| expected_or_rubric_ref | [type or `UNKNOWN`] | [value] | Oracle or rubric reference | [rule] | [policy or `UNKNOWN`] |
| slice_labels | [type or `UNKNOWN`] | [value] | Defined analysis slices | [rule] | [policy or `UNKNOWN`] |

### Probe result

| Field | Type | Required | Meaning | Validation | Classification / retention |
| --- | --- | --- | --- | --- | --- |
| run_id / probe_id / case_id | [types or `UNKNOWN`] | [values] | Provenance keys | [rules] | [policy or `UNKNOWN`] |
| configuration_versions | [type or `UNKNOWN`] | [value] | Model/prompt/tool/judge versions | [rule] | [policy or `UNKNOWN`] |
| raw_output_ref | [type or `UNKNOWN`] | [value] | Immutable raw observation reference | [rule] | [policy or `UNKNOWN`] |
| execution_state | [type or `UNKNOWN`] | [value] | Success, invalid, timeout, skipped, or observed equivalent | [rule] | [policy or `UNKNOWN`] |
| score_components | [type or `UNKNOWN`] | [value] | Derived measures with versions | [rule] | [policy or `UNKNOWN`] |
| usage / cost / latency | [types or `UNKNOWN`] | [value] | Operational observations and source | [rule] | [policy or `UNKNOWN`] |

### Review decision

| Field | Type | Required | Meaning | Validation | Classification / retention |
| --- | --- | --- | --- | --- | --- |
| artifact_id / version | [types or `UNKNOWN`] | [values] | Exact reviewed artifact | [rules] | [policy or `UNKNOWN`] |
| prior_state / new_state | [types or `UNKNOWN`] | [values] | Transition | [rules] | [policy or `UNKNOWN`] |
| actor / authority | [types or `UNKNOWN`] | [values] | Authorized reviewer | [rules] | [policy or `UNKNOWN`] |
| reason / evidence_ref | [types or `UNKNOWN`] | [values] | Decision basis | [rules] | [policy or `UNKNOWN`] |
| occurred_at | [type or `UNKNOWN`] | [value] | Auditable timestamp | [rule] | [policy or `UNKNOWN`] |

For every contract, specify producer, consumer, schema versioning, backward compatibility, validation location, idempotency key, error behavior, access, and retention. Unknown policy blocks any claim of production readiness.

## Non-functional requirements

| ID | Requirement | Measure / test | Threshold source | Acceptance criteria | Unknowns |
| --- | --- | --- | --- | --- | --- |
| NFR-001 | [reliability/security/privacy/performance/observability requirement] | [defined measure] | [source or `UNKNOWN`] | [AC-IDs] | [U-IDs] |

## Acceptance criteria

Criteria must be observable, traceable, and neutral about implementation unless a constraint requires one.

| ID | Given | When | Then | Evidence captured | Trace | State |
| --- | --- | --- | --- | --- | --- | --- |
| AC-001 | [precondition] | [action/event] | [observable result, including error behavior] | [log/artifact/result] | [FR/ER/NFR ID] | [not run/pass/fail/blocked, with source] |

Minimum acceptance coverage:

- valid, invalid, missing, timeout, retry, and partial-run paths;
- version/provenance preservation;
- slice counts and score reproducibility within the declared repeat policy;
- cost and latency boundaries;
- Pareto calculation with dominance, ties, exclusions, and uncertainty;
- HITL authorization, stale-version rejection, idempotency, and audit history;
- contract validation and incompatible-version behavior;
- privacy/security controls supported by actual policy.

## Prototype limits

A prototype is evidence-gathering, not production proof.

| Dimension | Prototype includes | Prototype excludes / simulates | Evidence needed to expand |
| --- | --- | --- | --- |
| Data | [sourced subset] | [omitted data] | [validation/privacy/representativeness evidence] |
| Models/providers | [tested versions] | [untested options] | [compatibility/performance evidence] |
| Scale | [observed volume] | [untested scale] | [load/cost/reliability evidence] |
| Security/privacy | [implemented controls] | [missing controls] | [policy/threat review] |
| Human review | [tested flow] | [manual/simulated steps] | [authority/usability/audit evidence] |
| Operations | [observability/recovery present] | [missing production operations] | [runbook/SLO/recovery evidence] |

Prototype disclaimers:

- no production readiness claim without acceptance evidence;
- no broad user or business impact claim from an unrepresentative sample;
- no schedule extrapolation without an approved estimate source;
- no deployment action implied by artifact approval;
- mocked data, judges, costs, and integrations are labeled at the point of use.

## Dependencies and sequencing

| Dependency | Why needed | Evidence | Owner | Readiness | Timing / estimate source | Failure plan |
| --- | --- | --- | --- | --- | --- | --- |
| [dependency] | [reason] | [source] | [confirmed owner or `UNKNOWN`] | [observed state or `UNKNOWN`] | [source or `UNKNOWN`] | [plan] |

## Decision and change log

| Date | Decision/change | Authority | Evidence | Requirements affected | Unknowns introduced/resolved |
| --- | --- | --- | --- | --- | --- |
| [ISO date or `UNKNOWN`] | [change] | [confirmed authority or `UNKNOWN`] | [source] | [IDs] | [U-IDs] |

## Release / completion decision

- Acceptance evidence: [AC results]
- Unmet criteria: [IDs]
- Accepted residual risks: [risk IDs + authority/source]
- Open unknowns: [U-IDs]
- Decision: [observed decision or `NO DECISION`]
- Decision authority and timestamp: [source or `UNKNOWN`]
