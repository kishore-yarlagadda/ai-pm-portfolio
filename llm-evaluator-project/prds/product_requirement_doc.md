# Product requirements: LLM Evaluator

> Canonical PRD template. Requirements must trace to evidence and strategy. Unknowns stay visible. This document does not imply approval, staffing, schedule, or production readiness. Inputs: [discovery](discovery_template.md) and [strategy](strategy_template.md).

## Document control

| Field | Value | Evidence |
| --- | --- | --- |
| Initiative | LLM Evaluator | Feature name |
| As-of date | UNKNOWN | Brief provided no date |
| Product decision owner | UNKNOWN | Brief provided no owner |
| Review state | UNKNOWN | Brief provided no review state |
| Discovery version | UNKNOWN | Brief provided no discovery version |
| Strategy version | UNKNOWN | Brief provided no strategy version |
| Architecture version | UNKNOWN | U-001 |

## Traceability rules

- Every requirement has a stable ID and traces to a supported claim, approved strategy decision, constraint, or explicit unknown-resolution need.
- Every quantitative threshold cites its metric definition, baseline, and approval source.
- Every changed or removed requirement remains in the decision log.
- Generated prose, examples, and prototype behavior are not production facts.

## Problem and outcome

- Problem statement: UNKNOWN ([U-002])
- Selected strategy: UNKNOWN ([U-003])
- User groups: UNKNOWN
- Outcome metric IDs: UNKNOWN
- Guardrail metric IDs: UNKNOWN
- Material unknowns: U-001, U-002, U-003, U-004, U-005, U-006, U-007, U-008, U-009, U-010, U-011

## Scope

### In scope

| Item | Why included | Evidence / decision | Validation |
| --- | --- | --- | --- |
| UNKNOWN | UNKNOWN | U-004 | UNKNOWN |

### Out of scope

| Item | Why excluded | Revisit trigger | Decision source |
| --- | --- | --- | --- |
| UNKNOWN | UNKNOWN | UNKNOWN | U-005 |

### Assumptions to test

| Assumption | Evidence today | Test | Decision rule | State |
| --- | --- | --- | --- | --- |
| UNKNOWN | NONE | UNKNOWN | UNKNOWN | UNKNOWN |

## Functional requirements

Use RFC 2119 terms only for agreed product behavior, not to make uncertain facts sound certain.

| ID | Requirement | User / system need | Source | Priority method and evidence | Acceptance criteria | Unknowns |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | UNKNOWN | UNKNOWN | U-006 | UNPRIORITIZED | UNKNOWN | U-006 |

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
| ER-001 | Store the probe definition and all version identifiers used for a run. | U-007 | AC-001 |
| ER-002 | Preserve raw result provenance separately from derived scores. | U-008 | AC-002 |
| ER-003 | Mark missing, invalid, timed-out, and skipped results distinctly; do not coerce them to passing or zero without an approved rule. | U-009 | AC-003 |
| ER-004 | Report results by defined slice and expose sample counts. | U-010 | AC-004 |

### Scoring contract

| Score ID | Rubric / formula | Scale and direction | Aggregation and missing-data rule | Sample / slice rule | Judge and calibration | Threshold source | Uncertainty |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SC-001 | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

Requirements:

- Keep component scores available when a composite exists.
- Never hide disagreement between deterministic, model-graded, and human results.
- Version rubrics and recalculate only under an explicit migration policy.
- Flag comparisons that use incompatible datasets, model versions, rubrics, or price snapshots.

### Cost, latency, and Pareto output

| Measure | Contract | Source | Freshness | Normalization |
| --- | --- | --- | --- | --- |
| API/model cost | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Human review cost | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Latency | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

- Compute dominance only across explicitly selected, direction-aware measures.
- A candidate is Pareto-dominated only if another is no worse on every selected measure and better on at least one, subject to the documented uncertainty policy.
- Show the selected dimensions, values, exclusions, and price snapshot beside the frontier.
- Do not emit a single winner unless a sourced decision rule resolves the trade-off.

### Human-in-the-loop states and audit

Semantic states are requirements; implementation values must be mapped from the actual system.

| State / transition | Entry condition | Authorized actor | Required input | Output / audit fields | Failure behavior |
| --- | --- | --- | --- | --- | --- |
| Awaiting review | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Changes requested | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Approved | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Rejected | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Superseded / invalidated | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

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
| case_id | UNKNOWN | UNKNOWN | Stable case identity | UNKNOWN | UNKNOWN |
| dataset_version | UNKNOWN | UNKNOWN | Version of source dataset | UNKNOWN | UNKNOWN |
| input | UNKNOWN | UNKNOWN | Probe input | UNKNOWN | UNKNOWN |
| expected_or_rubric_ref | UNKNOWN | UNKNOWN | Oracle or rubric reference | UNKNOWN | UNKNOWN |
| slice_labels | UNKNOWN | UNKNOWN | Defined analysis slices | UNKNOWN | UNKNOWN |

### Probe result

| Field | Type | Required | Meaning | Validation | Classification / retention |
| --- | --- | --- | --- | --- | --- |
| run_id / probe_id / case_id | UNKNOWN | UNKNOWN | Provenance keys | UNKNOWN | UNKNOWN |
| configuration_versions | UNKNOWN | UNKNOWN | Model/prompt/tool/judge versions | UNKNOWN | UNKNOWN |
| raw_output_ref | UNKNOWN | UNKNOWN | Immutable raw observation reference | UNKNOWN | UNKNOWN |
| execution_state | UNKNOWN | UNKNOWN | Success, invalid, timeout, skipped, or observed equivalent | UNKNOWN | UNKNOWN |
| score_components | UNKNOWN | UNKNOWN | Derived measures with versions | UNKNOWN | UNKNOWN |
| usage / cost / latency | UNKNOWN | UNKNOWN | Operational observations and source | UNKNOWN | UNKNOWN |

### Review decision

| Field | Type | Required | Meaning | Validation | Classification / retention |
| --- | --- | --- | --- | --- | --- |
| artifact_id / version | UNKNOWN | UNKNOWN | Exact reviewed artifact | UNKNOWN | UNKNOWN |
| prior_state / new_state | UNKNOWN | UNKNOWN | Transition | UNKNOWN | UNKNOWN |
| actor / authority | UNKNOWN | UNKNOWN | Authorized reviewer | UNKNOWN | UNKNOWN |
| reason / evidence_ref | UNKNOWN | UNKNOWN | Decision basis | UNKNOWN | UNKNOWN |
| occurred_at | UNKNOWN | UNKNOWN | Auditable timestamp | UNKNOWN | UNKNOWN |

For every contract, specify producer, consumer, schema versioning, backward compatibility, validation location, idempotency key, error behavior, access, and retention. Unknown policy blocks any claim of production readiness.

## Non-functional requirements

| ID | Requirement | Measure / test | Threshold source | Acceptance criteria | Unknowns |
| --- | --- | --- | --- | --- | --- |
| NFR-001 | UNKNOWN | UNKNOWN | UNKNOWN | AC-005 | U-011 |

## Acceptance criteria

Criteria must be observable, traceable, and neutral about implementation unless a constraint requires one.

| ID | Given | When | Then | Evidence captured | Trace | State |
| --- | --- | --- | --- | --- | --- | --- |
| AC-001 | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | ER-001 | UNKNOWN |
| AC-002 | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | ER-002 | UNKNOWN |
| AC-003 | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | ER-003 | UNKNOWN |
| AC-004 | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | ER-004 | UNKNOWN |
| AC-005 | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | NFR-001 | UNKNOWN |

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
| Data | UNKNOWN | UNKNOWN | UNKNOWN |
| Models/providers | UNKNOWN | UNKNOWN | UNKNOWN |
| Scale | UNKNOWN | UNKNOWN | UNKNOWN |
| Security/privacy | UNKNOWN | UNKNOWN | UNKNOWN |
| Human review | UNKNOWN | UNKNOWN | UNKNOWN |
| Operations | UNKNOWN | UNKNOWN | UNKNOWN |

Prototype disclaimers:

- no production readiness claim without acceptance evidence;
- no broad user or business impact claim from an unrepresentative sample;
- no schedule extrapolation without an approved estimate source;
- no deployment action implied by artifact approval;
- mocked data, judges, costs, and integrations are labeled at the point of use.

## Dependencies and sequencing

| Dependency | Why needed | Evidence | Owner | Readiness | Timing / estimate source | Failure plan |
| --- | --- | --- | --- | --- | --- | --- |
| UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

## Decision and change log

| Date | Decision/change | Authority | Evidence | Requirements affected | Unknowns introduced/resolved |
| --- | --- | --- | --- | --- | --- |
| UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

## Release / completion decision

- Acceptance evidence: UNKNOWN
- Unmet criteria: UNKNOWN
- Accepted residual risks: UNKNOWN
- Open unknowns: U-001, U-002, U-003, U-004, U-005, U-006, U-007, U-008, U-009, U-010, U-011
- Decision: NO DECISION
- Decision authority and timestamp: UNKNOWN