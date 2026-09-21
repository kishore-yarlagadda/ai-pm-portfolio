from typing import Any, Dict, Optional, Sequence

from connectors import EnterpriseDataConnectors


class ContextError(Exception):
    """Raised when customer context is missing or invalid."""


class ContextAgent:
    REQUIRED_CRM_FIELDS = {"user_id", "name", "primary_motivation"}
    REQUIRED_PORTFOLIO_FIELDS = {
        "user_id",
        "total_balance",
        "expense_ratio_avg",
        "annual_admin_fee",
        "holdings",
    }

    def build(
            self,
            user_id: str,
            high_balance_threshold: float,
            user_message: str = "",
            session_messages: Optional[Sequence[str]] = None,
    ) -> Dict[str, Any]:
        try:
            crm = EnterpriseDataConnectors.get_crm_history(user_id)
            portfolio = EnterpriseDataConnectors.get_portfolio_data(user_id)
            benchmark = EnterpriseDataConnectors.get_competitor_benchmark(
                "generic_ira"
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ContextError(str(exc)) from exc

        self._validate_required(crm, self.REQUIRED_CRM_FIELDS, "crm")
        self._validate_required(
            portfolio, self.REQUIRED_PORTFOLIO_FIELDS, "portfolio"
        )
        self._validate_numeric(portfolio)
        customer_signals = self._derive_signals(
            portfolio=portfolio,
            session_text=self._session_text(user_message, session_messages),
            high_balance_threshold=high_balance_threshold,
        )
        return {
            "crm": crm,
            "portfolio": portfolio,
            "benchmark": benchmark,
            "is_high_balance": (
                portfolio["total_balance"] >= high_balance_threshold
            ),
            "high_balance_threshold": high_balance_threshold,
            "customer_signals": customer_signals,

        }
    @staticmethod
    def _validate_required(
        record: Dict[str, Any], required: set, label: str
    ) -> None:
        missing = sorted(required - set(record))
        if missing:
            raise ContextError(
                f"Missing {label} fields: {', '.join(missing)}"
            )

    @staticmethod
    def _validate_numeric(portfolio: Dict[str, Any]) -> None:
        for field in (
            "total_balance",
            "expense_ratio_avg",
            "annual_admin_fee",
        ):
            value = portfolio[field]
            if not isinstance(value, (int, float)) or value < 0:
                raise ContextError(
                    f"Invalid portfolio field {field}: {value!r}"
                )

        for holding in portfolio["holdings"]:
            allocation = holding.get("allocation_pct")
            if not isinstance(allocation, (int, float)) or not 0 < allocation <= 1:
                raise ContextError(
                    f"Invalid holding allocation: {allocation!r}"
                )

    @staticmethod
    def _session_text(
        user_message: str,
        session_messages: Optional[Sequence[str]],
    ) -> str:
        """Return the customer's own words for signal derivation.

        When the supervisor supplies the session's customer messages, they
        are the signal source; otherwise the single current message is.
        """
        if session_messages is not None:
            return " ".join(session_messages)
        return user_message

    @staticmethod
    def _derive_signals(
        portfolio: Dict[str, Any],
        session_text: str,
        high_balance_threshold: float,
    ) -> Dict[str, bool]:
        """Derive transparent, multi-label signals from this session only.

        Signals come from the customer's own words in the current session
        plus verified account data. CRM case notes and persona fixture
        labels are deliberately excluded: they are stable per fixture, so
        deriving signals from them would misrepresent a fixed persona
        property as observed session behavior.
        """
        text = session_text.lower()
        return {
            "high_balance": (
                portfolio["total_balance"] >= high_balance_threshold
            ),
            "fee_sensitive": any(
                term in text
                for term in ("fee", "cost", "expense", "low-cost")
            ),
            "urgent_exit": any(
                term in text
                for term in (
                    "immediately",
                    "skip",
                    "direct exit",
                    "frustration",
                    "urgent",
                )
            ),
            "tax_complexity": any(
                term in text
                for term in ("tax", "penalty", "rmd")
            ),
        }
