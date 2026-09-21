from typing import Any, Dict

from analysis_engine import WhatIfAnalysisEngine


class AnalysisError(Exception):
    """Raised when verified analysis cannot be produced."""


class AnalysisAgent:
    ANNUAL_RETURN_RATE = 0.07
    PROJECTION_YEARS = 10

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        try:
            portfolio = context["portfolio"]
            benchmark = context["benchmark"]
            figures = WhatIfAnalysisEngine.calculate_fee_impact(
                portfolio=portfolio,
                benchmark=benchmark,
                projection_years=self.PROJECTION_YEARS,
                annual_return_rate=self.ANNUAL_RETURN_RATE,
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise AnalysisError(str(exc)) from exc
        summary = WhatIfAnalysisEngine.generate_comparison_summary(
            portfolio=portfolio,
            benchmark=benchmark,
            analysis=figures,
            annual_return_rate=self.ANNUAL_RETURN_RATE,
        )

        options = [
            "Proceed to rollover handoff now",
            "Review the synthetic cost comparison first",
        ]
        if context["is_high_balance"]:
            options.append(
                "Speak with a retirement specialist without delaying handoff"
            )

        return {
            "figures": figures,
            "assumptions": [
                "Same starting balance in both fixtures",
                "No contributions or withdrawals",
                "7.0% annual return before fees",
                "10-year projection horizon",
                "Synthetic plan and IRA fee inputs",
            ],
            "options": options,
            "summary": summary,
            "customer_signals": context.get("customer_signals", {}),
        }
