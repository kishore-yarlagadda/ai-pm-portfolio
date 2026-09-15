# Bug & Exception Incident Report: {issue_title}
**Status:** Open / Pending Triage
**Reported By:** AI SDLC Governance Agent
**Related Component:** [`src/core/`, `src/services/`, or `src/utils/`]

## 1. Incident Overview & Context
* **Symptom / Failure Description:** Brief summary of the unexpected behavior, test failure, or unhandled exception caught during execution.
* **Trigger Condition:** Specific inputs, payloads, or environmental states that caused the fault to manifest.

## 2. Diagnostics & Stack Trace Analysis
* **Captured Exception / Error Log:**
  ```python
  # Paste the relevant stack trace, error code, or Pydantic validation failure logs here
  ```
* **Boundary Validation Impact:** Did this failure bypass boundary interceptors or get safely caught by error handling strategies?

## 3. Resolution Plan & Remediation Gate
* **Proposed Fix:** Technical description of the code adjustment required (e.g., updating Pydantic validators, adding retry decorators, or adjusting timeout bounds).
* **Regression Verification:** Mandatory rerun of `pytest` and `mypy` to ensure the fix resolves the incident without breaking existing test coverage ($\ge 85\%$).


