"""
Enterprise Data Connectors Module (Multi-Persona Support)
Simulates fetching customer profiles, CSA history, and portfolio allocations for diverse personas.
"""

from typing import Dict, Any

class EnterpriseDataConnectors:
    
    PERSONA_DATABASE = {
        "usr_marcus_optimizer": {
            "crm": {
                "user_id": "usr_marcus_optimizer",
                "name": "Marcus Vance",
                "tenure_years": 4.5,
                "support_tickets_count": 1,
                "last_interaction": "2026-08-10",
                "csa_notes": "User inquired about low-cost index fund options and institutional fee tier eligibility.",
                "retention_attempts_this_session": 0,
                "primary_motivation": "FEE_MINIMIZATION"
            },
            "portfolio": {
                "user_id": "usr_marcus_optimizer",
                "account_type": "401(k)",
                "total_balance": 185000.00,
                "expense_ratio_avg": 0.0012,  # 0.12% institutional rate
                "annual_admin_fee": 0.00,
                "holdings": [
                    {"ticker": "VTI", "name": "Vanguard Total Stock Market ETF", "allocation_pct": 0.70, "expense_ratio": 0.0003},
                    {"ticker": "BND", "name": "Vanguard Total Bond Market ETF", "allocation_pct": 0.30, "expense_ratio": 0.0004}
                ]
            }
        },
        "usr_sarah_frustrated": {
            "crm": {
                "user_id": "usr_sarah_frustrated",
                "name": "Sarah Jenkins",
                "tenure_years": 2.1,
                "support_tickets_count": 5,
                "last_interaction": "2026-09-01",
                "csa_notes": "User expressed frustration over portal UI delays and app sign-in issues. Wants direct exit.",
                "retention_attempts_this_session": 0,
                "primary_motivation": "CONSOLIDATION_URGENCY"
            },
            "portfolio": {
                "user_id": "usr_sarah_frustrated",
                "account_type": "401(k)",
                "total_balance": 45000.00,
                "expense_ratio_avg": 0.0045,  # 0.45%
                "annual_admin_fee": 35.00,
                "holdings": [
                    {"ticker": "SPY", "name": "SPDR S&P 500 ETF Trust", "allocation_pct": 1.00, "expense_ratio": 0.0009}
                ]
            }
        },
        "usr_elena_retiree": {
            "crm": {
                "user_id": "usr_elena_retiree",
                "name": "Elena Rostova",
                "tenure_years": 12.0,
                "support_tickets_count": 2,
                "last_interaction": "2026-07-15",
                "csa_notes": "User asking about RMDs (Required Minimum Distributions) and tax implications of rollover at age 62.",
                "retention_attempts_this_session": 0,
                "primary_motivation": "TAX_SAFETY_GUIDANCE"
            },
            "portfolio": {
                "user_id": "usr_elena_retiree",
                "account_type": "401(k)",
                "total_balance": 320000.00,
                "expense_ratio_avg": 0.0020,  # 0.20%
                "annual_admin_fee": 0.00,
                "holdings": [
                    {"ticker": "VBTLX", "name": "Vanguard Total Bond Market Index", "allocation_pct": 0.50, "expense_ratio": 0.0005},
                    {"ticker": "VFIAX", "name": "Vanguard 500 Index Fund Admiral", "allocation_pct": 0.50, "expense_ratio": 0.0004}
                ]
            }
        }
    }

    @classmethod
    def get_crm_history(cls, user_id: str) -> Dict[str, Any]:
        """Fetches customer CRM profile by ID."""
        persona = cls.PERSONA_DATABASE.get(user_id, cls.PERSONA_DATABASE["usr_marcus_optimizer"])
        return persona["crm"]

    @classmethod
    def get_portfolio_data(cls, user_id: str) -> Dict[str, Any]:
        """Fetches customer portfolio data by ID."""
        persona = cls.PERSONA_DATABASE.get(user_id, cls.PERSONA_DATABASE["usr_marcus_optimizer"])
        return persona["portfolio"]

    @staticmethod
    def get_competitor_benchmark(competitor_name: str = "generic_ira") -> Dict[str, Any]:
        """Retrieves external IRA provider fee benchmarks."""
        return {
            "provider_name": "Standard External Retail IRA",
            "avg_expense_ratio": 0.0065,  # 0.65% retail standard
            "annual_account_fee": 75.00,
            "transfer_out_fee": 0.00
        }
