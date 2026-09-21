"""Deterministic contract checks for the three-agent retention workflow.

Run from the project root with:
    python evals/agent_contracts.py
"""

import os
import sys
import traceback


SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from agent_system import RetentionAgentSystem
from agents.analysis_agent import AnalysisAgent
from agents.compliance_critic import ComplianceCritic
from agents.context_agent import ContextAgent, ContextError
from analysis_engine import WhatIfAnalysisEngine


FIXTURE_IDS = (
    "usr_marcus_optimizer",
    "usr_sarah_frustrated",
    "usr_elena_retiree",
)
HIGH_BALANCE_THRESHOLD = 250000.0


def require(condition, detail):
    """Raise a readable failure instead of relying on optimizable assert."""
    if not condition:
        raise AssertionError(detail)


def contract_context_failure_is_safe():
    """Unknown data fails closed in ContextAgent and safely in the supervisor."""
    context_agent = ContextAgent()
    try:
        context_agent.build(
            "unknown-user",
            HIGH_BALANCE_THRESHOLD,
            "Help me",
        )
    except ContextError:
        pass
    else:
        raise AssertionError("ContextAgent accepted an unknown user")

    result = RetentionAgentSystem("unknown-user").evaluate_request("Help me")
    require(
        result.get("action") == "ROUTE_TO_GENERAL_SUPPORT",
        "unknown user did not route to general support",
    )
    require(result.get("is_active") is False, "unknown-user session stayed active")
    require(
        "context" in result.get("reason", "").lower(),
        "unknown-user result did not explain the context-verification failure",
    )


def contract_analysis_matches_engine():
    """AnalysisAgent delegates all fixture math to WhatIfAnalysisEngine exactly."""
    context_agent = ContextAgent()
    analysis_agent = AnalysisAgent()

    for user_id in FIXTURE_IDS:
        context = context_agent.build(
            user_id,
            HIGH_BALANCE_THRESHOLD,
            "Compare the account costs.",
        )
        actual = analysis_agent.analyze(context)
        expected = WhatIfAnalysisEngine.calculate_fee_impact(
            portfolio=context["portfolio"],
            benchmark=context["benchmark"],
            projection_years=analysis_agent.PROJECTION_YEARS,
            annual_return_rate=analysis_agent.ANNUAL_RETURN_RATE,
        )
        require(
            actual.get("figures") == expected,
            "%s figures differ from WhatIfAnalysisEngine" % user_id,
        )
        require(actual.get("assumptions"), "%s has no assumptions" % user_id)
        require(actual.get("options"), "%s has no options" % user_id)

    # Cross-persona prompts prove these flags come from the current message/data,
    # not merely from each fixture's primary_motivation label.
    signal_cases = (
        ("usr_sarah_frustrated", "Please compare the fees and costs.", "fee_sensitive"),
        ("usr_elena_retiree", "Skip the pitch and transfer immediately.", "urgent_exit"),
        ("usr_marcus_optimizer", "What tax penalty or RMD applies?", "tax_complexity"),
    )
    for user_id, message, expected_signal in signal_cases:
        context = context_agent.build(
            user_id,
            HIGH_BALANCE_THRESHOLD,
            message,
        )
        require(
            context.get("customer_signals", {}).get(expected_signal) is True,
            "%s was not derived from the current message for %s"
            % (expected_signal, user_id),
        )
        analyzed = analysis_agent.analyze(context)
        require(
            analyzed.get("customer_signals", {}).get(expected_signal) is True,
            "%s was not propagated by AnalysisAgent" % expected_signal,
        )


def contract_critic_rejects_unsafe_claims():
    """The critic rejects and repairs transaction and tax-advice claims."""
    critic = ComplianceCritic()
    context = {"is_high_balance": False}

    bypass = critic.review(
        "Your transfer has been processed. Staying in the plan may save money.",
        "ROUTE_TO_ROLLOVER_EXECUTION",
        context,
    )
    require(bypass.get("approved") is False, "unsafe bypass draft was approved")
    require(
        "executed_transaction_claim" in bypass.get("violations", []),
        "executed transaction claim was not detected",
    )
    require(
        "retention_offer_after_bypass" in bypass.get("violations", []),
        "post-bypass retention offer was not detected",
    )
    repaired_bypass = bypass.get("message", "").lower()
    require(
        "rollover handoff" in repaired_bypass,
        "bypass repair did not use handoff language",
    )
    require(
        "no transaction has been executed" in repaired_bypass,
        "bypass repair did not disclaim execution",
    )

    tax = critic.review(
        "This rollover is tax-free.",
        "ESCALATE_TO_HUMAN_CFP",
        context,
    )
    require(tax.get("approved") is False, "tax-advice draft was approved")
    require(
        "tax_or_legal_advice" in tax.get("violations", []),
        "tax-advice claim was not detected",
    )
    repaired_tax = tax.get("message", "").lower()
    require(
        "human review" in repaired_tax,
        "tax-advice repair did not require human review",
    )
    require(
        "not providing tax or legal advice" in repaired_tax,
        "tax-advice repair did not remove the advice claim",
    )


def contract_critic_repairs_missing_disclosure():
    """A retention draft missing disclosures is replaced by verified analysis."""
    critic = ComplianceCritic()
    verified_summary = (
        "Verified synthetic comparison. This is not a forecast or financial advice."
    )
    result = critic.review(
        "This plan is cheaper.",
        "PRESENT_RETENTION_ANALYSIS",
        {"is_high_balance": False},
        {"summary": verified_summary},
    )
    require(result.get("approved") is False, "undisclosed retention draft was approved")
    require(
        "missing_synthetic_disclosure" in result.get("violations", []),
        "missing synthetic/not-advice disclosure was not detected",
    )
    require(
        result.get("message") == verified_summary,
        "critic did not repair from the verified analysis summary",
    )
    require(
        result.get("human_review_required") is True,
        "repaired noncompliant draft was not flagged for human review",
    )


CONTRACTS = (
    ("Context failure routes safely", contract_context_failure_is_safe),
    ("Analysis matches engine and derives signals", contract_analysis_matches_engine),
    ("Critic rejects unsafe claims", contract_critic_rejects_unsafe_claims),
    ("Critic repairs missing disclosure", contract_critic_repairs_missing_disclosure),
)


def run():
    print("=" * 65)
    print(" RUNNING THREE-AGENT CONTRACT CHECKS ")
    print("=" * 65)

    passed = 0
    failed = 0
    for number, (name, check) in enumerate(CONTRACTS, 1):
        print("\n[Contract %d] %s" % (number, name))
        try:
            check()
        except Exception as exc:
            failed += 1
            print("  -> FAIL: %s" % exc)
            if os.getenv("AGENT_CONTRACTS_TRACEBACK") == "1":
                traceback.print_exc()
        else:
            passed += 1
            print("  -> PASS")

    print("\n" + "=" * 65)
    print(" AGENT CONTRACTS COMPLETE: Passed: %d | Failed: %d" % (passed, failed))
    print("=" * 65)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run())
