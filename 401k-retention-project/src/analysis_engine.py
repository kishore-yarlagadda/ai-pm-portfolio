"""
What-If Analysis & Competitor Comparison Engine
Calculates cost differentials, compound growth impacts, and side-by-side comparisons.
"""

from typing import Dict, Any

class WhatIfAnalysisEngine:
    @staticmethod
    def calculate_fee_impact(portfolio: Dict[str, Any], benchmark: Dict[str, Any], projection_years: int = 10, annual_return_rate: float = 0.07) -> Dict[str, Any]:
        """Calculates projected growth and fee drag over a multi-year horizon."""
        balance = portfolio["total_balance"]
        
        # Current 401(k) fees
        current_expense_ratio = portfolio["expense_ratio_avg"]
        current_admin_fee = portfolio["annual_admin_fee"]
        
        # Competitor IRA fees
        competitor_expense_ratio = benchmark["avg_expense_ratio"]
        competitor_admin_fee = benchmark["annual_account_fee"]
        
        # Projected growth calculations
        net_return_current = annual_return_rate - current_expense_ratio
        net_return_competitor = annual_return_rate - competitor_expense_ratio
        
        balance_current = balance
        balance_competitor = balance
        
        for _ in range(projection_years):
            balance_current = (balance_current * (1 + net_return_current)) - current_admin_fee
            balance_competitor = (balance_competitor * (1 + net_return_competitor)) - competitor_admin_fee
            
        fee_differential_loss = balance_current - balance_competitor
        annual_fee_savings = (balance * (competitor_expense_ratio - current_expense_ratio)) + (competitor_admin_fee - current_admin_fee)
        
        return {
            "initial_balance": balance,
            "projection_years": projection_years,
            "projected_balance_401k": round(balance_current, 2),
            "projected_balance_competitor": round(balance_competitor, 2),
            "total_estimated_fee_drag_savings": round(fee_differential_loss, 2),
            "year_one_fee_savings": round(annual_fee_savings, 2)
        }

    @staticmethod
    def generate_comparison_summary(portfolio: Dict[str, Any], benchmark: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """Generates a clear, fiduciary-compliant comparison pitch for retention."""
        return (
            f"Based on your current balance of ${portfolio['total_balance']:,.2f}:\n"
            f"- Current 401(k) Avg Fee: {portfolio['expense_ratio_avg']*100:.2f}%\n"
            f"- External IRA Avg Fee: {benchmark['avg_expense_ratio']*100:.2f}%\n"
            f"- Projected 1-Year Fee Savings by staying: ${analysis['year_one_fee_savings']:,.2f}\n"
            f"- Projected {analysis['projection_years']}-Year Savings (including compounding): ${analysis['total_estimated_fee_drag_savings']:,.2f}\n\n"
            f"Staying in the plan keeps your access to institutional index fund rates and zero administrative account fees."
        )
