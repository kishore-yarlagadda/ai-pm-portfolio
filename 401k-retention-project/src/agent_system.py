"""
Agent System Orchestrator (LLM-Integrated)
Uses LLM Client with strict system prompts, financial tool inputs, and supervisor routing guardrails.
"""

from typing import Dict, Any, List
from connectors import EnterpriseDataConnectors
from analysis_engine import WhatIfAnalysisEngine
from llm_client import LLMClient

class RetentionAgentSystem:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.crm_data = EnterpriseDataConnectors.get_crm_history(user_id)
        self.portfolio_data = EnterpriseDataConnectors.get_portfolio_data(user_id)
        self.competitor_benchmark = EnterpriseDataConnectors.get_competitor_benchmark("generic_ira")
        self.llm = LLMClient()
        
        # State tracking
        self.is_session_active = True
        self.current_state = "INITIAL"
        self.conversation_history: List[Dict[str, str]] = []

    def evaluate_request(self, user_message: str) -> Dict[str, Any]:
        """Evaluates intent using LLM and state-machine supervisor routing."""
        if not self.is_session_active:
            return {
                "action": "SESSION_TERMINATED",
                "reason": "Session has ended.",
                "message": "This session has ended. Please restart the demo.",
                "is_active": False
            }

        self.conversation_history.append({"role": "user", "content": user_message})
        message_lower = user_message.lower()

        # 0. Security Guardrail: Prompt Injection & Jailbreak Prevention
        jailbreak_triggers = ["ignore previous instructions", "system rules", "zero penalties"]
        if any(trig in message_lower for trig in jailbreak_triggers):
            self.is_session_active = False
            self.current_state = "SECURITY_BLOCK"
            return {
                "action": "ROUTE_TO_ROLLOVER_EXECUTION",
                "reason": "Security policy check triggered due to prompt injection attempt.",
                "message": "Security policy triggered. Processing standard transfer request under compliance oversight.",
                "is_active": False
            }

        # 1. Supervisor Guardrail: Escalation Detection (Tax/Legal)
        escalation_keywords = ["tax", "penalty", "rmd", "legal", "cfp", "advisor"]
        if any(kw in message_lower for kw in escalation_keywords):
            self.is_session_active = False
            self.current_state = "ESCALATED_TO_CFP"
            
            system_prompt = (
                f"You are a compliant AI Assistant for {self.crm_data['name']}. "
                f"The user asked about complex tax/RMD topics. Warmly explain that fiduciary compliance "
                f"requires transferring them to a Human Certified Financial Planner (CFP) right now."
            )
            llm_msg = self.llm.generate_response(system_prompt, user_message)
            
            return {
                "action": "ESCALATE_TO_HUMAN_CFP",
                "reason": "Tax/legal guardrail triggered.",
                "message": llm_msg,
                "is_active": False
            }

        # 2. Supervisor Guardrail: Bypass or Single-Pivot Enforcement
        bypass_keywords = [
            "skip", "transfer immediately", "no pitch", "direct rollover", 
            "bypass", "just move my money", "i still want to move forward", 
            "i understand the fee comparison"
        ]
        explicit_bypass = any(kw in message_lower for kw in bypass_keywords)

        if explicit_bypass or self.current_state == "PITCH_PRESENTED":
            self.is_session_active = False
            self.current_state = "ROLLOVER_COMPLETED"
            
            system_prompt = (
                f"You are an AI assistant processing a direct 401(k) rollover for {self.crm_data['name']}. "
                f"Confirm that their request is being processed immediately without further delays."
            )
            llm_msg = self.llm.generate_response(system_prompt, user_message)
            
            return {
                "action": "ROUTE_TO_ROLLOVER_EXECUTION",
                "reason": "Explicit bypass requested or single-pivot guardrail enforced.",
                "message": llm_msg,
                "is_active": False
            }

        # 3. LLM Retention Pitch Generation (Powered by What-If Financial Engine)
        analysis = WhatIfAnalysisEngine.calculate_fee_impact(
            portfolio=self.portfolio_data,
            benchmark=self.competitor_benchmark
        )
        
        system_prompt = (
            f"You are a fiduciary 401(k) retention agent speaking to {self.crm_data['name']}.\n"
            f"User Motivation: {self.crm_data['primary_motivation']}\n"
            f"Financial Context:\n"
            f"- Current Balance: ${analysis['initial_balance']:,.2f}\n"
            f"- Current Avg Fee: {self.portfolio_data['expense_ratio_avg']*100:.2f}%\n"
            f"- Competitor Fee: {self.competitor_benchmark['avg_expense_ratio']*100:.2f}%\n"
            f"- Projected 10-Yr Fee Loss in external IRA: ${analysis['total_estimated_fee_drag_savings']:,.2f}\n\n"
            f"Instructions: Use these metrics to respectfully present why staying in the plan saves money, "
            f"address their message naturally, and ask if they still wish to proceed with the rollover."
        )

        llm_msg = self.llm.generate_response(system_prompt, user_message)
        self.current_state = "PITCH_PRESENTED"

        return {
            "action": "PRESENT_RETENTION_ANALYSIS",
            "reason": "First-time retention attempt with dynamic LLM generation.",
            "message": llm_msg,
            "is_active": True,
            "analysis_data": analysis
        }
