from typing import Any, Dict, List


class ComplianceCritic:
    TRANSACTION_CLAIMS = (
        "transfer is complete",
        "transfer has been processed",
        "rollover has been executed",
        "executed your transfer",
    )
    TAX_ADVICE_CLAIMS = (
        "this rollover is tax-free",
        "you will not owe tax",
        "no tax consequences",
    )
    RETENTION_MARKERS = (
        "staying in the plan",
        "review this comparison",
        "lower-cost fixture",
        "retention offer",
    )

    def review(
        self,
        message: str,
        route: str,
        context: Dict[str, Any],
        analysis: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        violations = self._find_violations(
            message=message,
            route=route,
            analysis=analysis,
        )
        if not violations:
            return {
                "approved": True,
                "violations": [],
                "message": message,
                "human_review_required": False,
            }
        repaired = self._repair(
            route=route,
            context=context,
            analysis=analysis,
        )
        return {
            "approved": False,
            "violations": violations,
            "message": repaired,
            "human_review_required": True,
        }

    def _find_violations(
        self,
        message: str,
        route: str,
        analysis: Dict[str, Any] | None,
    ) -> List[str]:
        text = message.lower()
        violations = []

        if any(claim in text for claim in self.TRANSACTION_CLAIMS):
            violations.append("executed_transaction_claim")

        if any(claim in text for claim in self.TAX_ADVICE_CLAIMS):
            violations.append("tax_or_legal_advice")

        if route.startswith("PRESENT_RETENTION_ANALYSIS"):
            if "synthetic" not in text or "not a forecast or financial advice" not in text:
                violations.append("missing_synthetic_disclosure")

        if route == "ROUTE_TO_ROLLOVER_EXECUTION":
            if any(marker in text for marker in self.RETENTION_MARKERS):
                violations.append("retention_offer_after_bypass")

        return violations

    @staticmethod
    def _repair(
        route: str,
        context: Dict[str, Any],
        analysis: Dict[str, Any] | None,
    ) -> str:
        if route.startswith("PRESENT_RETENTION_ANALYSIS") and analysis:
            return analysis["summary"]

        if route == "ROUTE_TO_ROLLOVER_EXECUTION":
            return (
                "Your request is ready for rollover handoff without another "
                "retention offer. No transaction has been executed in this demo."
            )

        return (
            "This request needs human review. No transaction has been executed, "
            "and this prototype is not providing tax or legal advice."
        )
