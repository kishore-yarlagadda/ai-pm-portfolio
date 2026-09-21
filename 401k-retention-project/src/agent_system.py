"""Supervisor for the three-agent 401(k) retention workflow."""

import os
from typing import Any, Dict, List, Optional

from agents.analysis_agent import AnalysisAgent, AnalysisError
from agents.compliance_critic import ComplianceCritic
from agents.context_agent import ContextAgent, ContextError
from llm_client import LLMClient


class RetentionAgentSystem:
    """Routes requests and coordinates context, analysis, and compliance agents."""

    def __init__(self, user_id: str, llm_client: Optional[LLMClient] = None):
        self.user_id = user_id
        self.high_balance_threshold = float(
            os.getenv("HIGH_BALANCE_THRESHOLD", "250000")
        )

        self.context_agent = ContextAgent()
        self.analysis_agent = AnalysisAgent()
        self.compliance_critic = ComplianceCritic()
        self.llm_client = llm_client or LLMClient()
        self.context_error = None

        try:
            self.context = self.context_agent.build(
                user_id=user_id,
                high_balance_threshold=self.high_balance_threshold,
            )
            self.crm_data = self.context["crm"]
            self.portfolio_data = self.context["portfolio"]
            self.competitor_benchmark = self.context["benchmark"]
            self.is_high_balance = self.context["is_high_balance"]
        except ContextError as exc:
            self.context_error = str(exc)
            self.context = {}
            self.crm_data = {}
            self.portfolio_data = {}
            self.competitor_benchmark = {}
            self.is_high_balance = False

        self.is_session_active = True
        self.current_state = "INITIAL"
        self.conversation_history: List[Dict[str, str]] = []

    def _finalize_response(
        self,
        response: Dict[str, Any],
        analysis: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Run every customer-facing draft through the ComplianceCritic.

        No response leaves the supervisor without critic review, whatever
        route produced it: guardrail rejections, escalations, handoffs,
        and the retention analysis alike. A rejected draft is replaced with
        verified wording and flagged for human review.
        """
        review = self.compliance_critic.review(
            message=response["message"],
            route=response["action"],
            context=self.context,
            analysis=analysis,
        )
        response["message"] = review["message"]
        response["human_review_required"] = bool(
            response.get("human_review_required", False)
            or review["human_review_required"]
        )
        response["critic_approved"] = review["approved"]
        response["critic_violations"] = review["violations"]
        return response

    def _draft_retention_response(
        self,
        user_message: str,
        analysis: Dict[str, Any],
        deterministic_draft: str,
    ) -> str:
        """Optionally rewrite one eligible retention draft with an LLM.

        The supervisor has already selected the route, advanced session state,
        and produced verified analysis before this method runs. The LLM receives
        no authority to change any of those values. If live generation is not
        configured or fails, the deterministic draft remains the response.
        Every returned draft still passes through ``_finalize_response`` and the
        ComplianceCritic before it can reach the customer.
        """
        if not self.llm_client.is_live_available:
            return deterministic_draft

        system_prompt = (
            "Write one brief empathetic opening sentence for the verified "
            "comparison that will follow. Do not add or repeat facts, numbers, "
            "assumptions, options, routes, tax or legal guidance, or transaction "
            "status. Do not say or imply that a transfer, rollover, or transaction "
            "has executed. Return only that opening sentence."
        )
        try:
            generated = self.llm_client.generate_response(
                system_prompt=system_prompt,
                user_message=user_message,
            )
        except Exception:
            return deterministic_draft

        if not isinstance(generated, str) or not generated.strip():
            return deterministic_draft
        return generated.strip() + "\n\n" + deterministic_draft

    def evaluate_request(self, user_message: str) -> Dict[str, Any]:
        """Evaluate intent and enforce supervisor routing guardrails."""
        if not self.is_session_active:
            return self._finalize_response({
                "action": "SESSION_TERMINATED",
                "reason": "Session has ended.",
                "message": "This session has ended. Please restart the demo.",
                "is_active": False,
            })

        # Unknown or unavailable customer data must fail closed before routing.
        if self.context_error:
            self.is_session_active = False
            self.current_state = "GENERAL_SUPPORT"
            return self._finalize_response({
                "action": "ROUTE_TO_GENERAL_SUPPORT",
                "reason": "Customer context could not be verified.",
                "message": (
                    "I couldn’t verify the customer record needed for this "
                    "workflow. I’m routing the request to general support."
                ),
                "is_active": False,
                "human_review_required": True,
                "agent_error": self.context_error,
            })

        self.conversation_history.append(
            {"role": "user", "content": user_message}
        )
        message_lower = user_message.lower()

        # 0. Security guardrail: prompt injection and jailbreak prevention.
        jailbreak_triggers = [
            "ignore previous instructions",
            "system rules",
            "zero penalties",
        ]
        if any(trigger in message_lower for trigger in jailbreak_triggers):
            self.is_session_active = False
            self.current_state = "COMPLIANCE_REVIEW"
            return self._finalize_response({
                "action": "ROUTE_TO_COMPLIANCE_REVIEW",
                "reason": "Prompt injection or policy override attempt detected.",
                "message": (
                    "I can’t follow instructions that override the service’s "
                    "safety rules. I’m routing this request for compliance "
                    "review; no transaction has been executed."
                ),
                "is_active": False,
                "human_review_required": True,
            })

        # 1. Service and complaint routing before any retention offer.
        out_of_scope_keywords = [
            "password",
            "checking account",
            "online banking",
            "reset login",
        ]
        if any(keyword in message_lower for keyword in out_of_scope_keywords):
            self.is_session_active = False
            self.current_state = "GENERAL_SUPPORT"
            return self._finalize_response({
                "action": "ROUTE_TO_GENERAL_SUPPORT",
                "reason": "Request is outside the 401(k) rollover workflow.",
                "message": (
                    "This request belongs with general customer support, not "
                    "the 401(k) rollover workflow. I’m routing it without "
                    "presenting a retention offer."
                ),
                "is_active": False,
            })

        human_review_keywords = [
            "regulator",
            "stealing my money",
            "fraud",
            "lawsuit",
        ]
        if any(keyword in message_lower for keyword in human_review_keywords):
            self.is_session_active = False
            self.current_state = "HUMAN_SERVICE_REVIEW"
            return self._finalize_response({
                "action": "ROUTE_TO_HUMAN_SERVICE_REVIEW",
                "reason": (
                    "Fraud allegation, regulator threat, or severe complaint "
                    "detected."
                ),
                "message": (
                    "I’m routing this to a human service and compliance review "
                    "now. I won’t present a retention offer."
                ),
                "is_active": False,
                "human_review_required": True,
            })

        # 2. Tax and legal questions always receive human review.
        escalation_keywords = ["tax", "penalty", "rmd", "legal", "cfp", "advisor"]
        if any(keyword in message_lower for keyword in escalation_keywords):
            self.is_session_active = False
            self.current_state = "ESCALATED_TO_CFP"
            return self._finalize_response({
                "action": "ESCALATE_TO_HUMAN_CFP",
                "reason": "Tax/legal guardrail triggered.",
                "message": (
                    "This question needs individual tax or legal guidance. "
                    "I’m transferring the request to a human Certified "
                    "Financial Planner now; no transaction has been executed."
                ),
                "is_active": False,
            })

        # 3. Explicit bypass and the single-pivot rule go straight to handoff.
        bypass_keywords = [
            "skip",
            "transfer immediately",
            "no pitch",
            "direct rollover",
            "bypass",
            "just move my money",
            "i still want to move forward",
            "i understand the fee comparison",
        ]
        explicit_bypass = any(
            keyword in message_lower for keyword in bypass_keywords
        )
        if explicit_bypass or self.current_state == "PITCH_PRESENTED":
            self.is_session_active = False
            self.current_state = "ROLLOVER_COMPLETED"
            return self._finalize_response({
                "action": "ROUTE_TO_ROLLOVER_EXECUTION",
                "reason": (
                    "Explicit bypass requested or single-pivot guardrail enforced."
                ),
                "message": (
                    "I’m routing your request immediately to the rollover "
                    "handoff. I will not present another pitch or comparison, "
                    "and no transaction has been executed by this assistant."
                ),
                "is_active": False,
            })

        # 4. One supervised retention analysis: Context -> Analysis -> Critic.
        try:
            self.context = self.context_agent.build(
                user_id=self.user_id,
                high_balance_threshold=self.high_balance_threshold,
                user_message=user_message,
                session_messages=[
                    entry["content"]
                    for entry in self.conversation_history
                    if entry["role"] == "user"
                ],
            )
            analysis_result = self.analysis_agent.analyze(self.context)
        except (ContextError, AnalysisError) as exc:
            self.is_session_active = False
            self.current_state = "GENERAL_SUPPORT"
            return self._finalize_response({
                "action": "ROUTE_TO_GENERAL_SUPPORT",
                "reason": "Verified customer analysis could not be produced.",
                "message": (
                    "I couldn’t verify the account context needed for this "
                    "comparison. I’m routing the request to general support."
                ),
                "is_active": False,
                "human_review_required": True,
                "agent_error": str(exc),
            })

        self.crm_data = self.context["crm"]
        self.portfolio_data = self.context["portfolio"]
        self.competitor_benchmark = self.context["benchmark"]
        self.is_high_balance = self.context["is_high_balance"]
        llm_msg = analysis_result["summary"]
        self.current_state = "PITCH_PRESENTED"

        if self.is_high_balance:
            llm_msg = (
                f"{llm_msg}\n\n"
                "Because this account meets the assisted-service threshold, "
                "you may also speak with a retirement specialist. That review "
                "is optional and will not delay a rollover handoff if you "
                "choose to proceed now."
            )

        action = (
            "PRESENT_RETENTION_ANALYSIS_WITH_SPECIALIST_OPTION"
            if self.is_high_balance
            else "PRESENT_RETENTION_ANALYSIS"
        )

        reason = (
            "First-time analysis with optional specialist support and human-review flag."
            if self.is_high_balance
            else "First-time analysis produced by the agent workflow."
        )

        llm_msg = self._draft_retention_response(
            user_message=user_message,
            analysis=analysis_result,
            deterministic_draft=llm_msg,
        )

        return self._finalize_response({
            "action": action,
            "reason": reason,
            "message": llm_msg,
            "is_active": True,
            "analysis_data": analysis_result["figures"],
            "analysis_assumptions": analysis_result["assumptions"],
            "analysis_options": analysis_result["options"],
            "customer_signals": analysis_result["customer_signals"],
            "human_review_required": bool(self.is_high_balance),
            "specialist_option_offered": self.is_high_balance,
        }, analysis=analysis_result)
