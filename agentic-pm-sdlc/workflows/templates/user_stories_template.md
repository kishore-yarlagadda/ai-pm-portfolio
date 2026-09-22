# User stories: [initiative name]

> Canonical user-story template. Stories derive only from the PRD's requirements and the discovery artifact's observed user groups. No invented personas. Unknowns stay visible. Inputs: [prd](../prds/product_requirement_doc.md) and [discovery](discovery_report.md).

## Document control

| Field | Value | Evidence |
| --- | --- | --- |
| Initiative | [name or `UNKNOWN`] | [source ID] |
| As-of date | [ISO 8601 date or `UNKNOWN`] | [source ID or reason unknown] |
| Prepared by | [name/role or `UNKNOWN`] | [source ID] |
| PRD version | [commit, version, or `UNKNOWN`] | [durable path/link] |
| Discovery version | [commit, version, or `UNKNOWN`] | [durable path/link] |

## Derivation rules

- Every story traces to at least one requirement ID from the PRD.
- Every user group comes from the discovery artifact's observed groups - cite its source ID. Do not invent personas.
- Acceptance criteria are observable and testable; the test stage turns them into executable tests.
- Do not invent priorities or statuses. Record the source that set them, or mark `UNKNOWN`.

## Story register

| Story ID | User group (observed) | Story | Requirement IDs | Acceptance criteria (observable) | Priority | Status | Evidence / unknowns |
| --- | --- | --- | --- | --- | --- | --- | --- |
| US-001 | [group + discovery source ID] | As a [group], I want [capability] so that [outcome] | [requirement IDs] | [given/when/then, or a checklist that can be executed] | [approved priority or `UNKNOWN`] | [observed state or `UNKNOWN`] | [S-/U-IDs] |

## Open questions

| ID | Question | Why it matters | What would resolve it | State |
| --- | --- | --- | --- | --- |
| Q-001 | [question] | [story or criterion affected] | [specific evidence needed] | [observed state or `UNKNOWN`] |
