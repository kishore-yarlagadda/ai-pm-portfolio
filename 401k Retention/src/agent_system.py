"""
Agent System Orchestrator
Main state machine and supervisor logic for 401(k) retention and rollover requests.
"""

from typing import Dict, Any
from connectors import EnterpriseDataConnectors
from analysis_engine import WhatIfAnalysisEngine

class RetentionAgentSystem:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.crm_data = EnterpriseDataConnectors.get_crm_history(user_id)
        self.portfolio_data = EnterpriseDataConnectors.get_portfolio_data(user_id)
        self.competitor_benchmark = EnterpriseDataConnectors.get_competitor_benchmark("generic_ira")

    def evaluate_request(self, user_message: str) -> Dict[str, Any]:
        """Processes user input, enforces single-pivot guardrail, and routes to retention or execution."""
        message_lower = user_message.lower()
        
        # Check for direct bypass commands
        bypass_keywords = ["skip", "transfer immediately", "no pitch", "direct rollover", "bypass"]
        explicit_bypass = any(keyword in message_lower for keyword in bypass_keywords)
        
        # Check single-pivot guardrail count
        retention_attempts = self.crm_data.get("retention_attempts_this_session", 0)
        
        # Guardrail logic: Route to rollover if explicit bypass or pivot limit reached
        if explicit_bypass or retention_attempts >= 1:
            return {
                "action": "ROUTE_TO_ROLLOVER_EXECUTION",
                "reason": "Explicit bypass requested" if explicit_bypass else "Maximum retention attempts (1) reached",
                "message": "Understood. Bypassing retention overview and initializing direct 401(k) rollover transfer."
            }
        
        # Execute What-If Analysis
        analysis = WhatIfAnalysisEngine.calculate_fee_impact(
            portfolio=self.portfolio_data,
            benchmark=self.competitor_benchmark
        )
        
        summary_pitch = WhatIfAnalysisEngine.generate_comparison_summary(
            portfolio=self.portfolio_data,
            benchmark=self.competitor_benchmark,
            analysis=analysis
        )
        
        # Increment retention attempt count
        self.crm_data["retention_attempts_this_session"] += 1
        
        return {
            "action": "PRESENT_RETENTION_ANALYSIS",
            "reason": "First-time retention pivot allowed under CX policy",
            "message": summary_pitch,
            "analysis_data": analysis
        }

if __name__ == "__main__":
    # Test Run
    agent = RetentionAgentSystem(user_id="usr_98765")
    
    print("--- Test Case 1: First-time request ---")
    response1 = agent.evaluate_request("I want to roll over my 401k to another IRA.")
    print(response1["message"])
    
    print("\n--- Test Case 2: Follow-up request (Guardrail Triggered) ---")
    response2 = agent.evaluate_request("I still want to move my money.")
    print(response2["message"])
