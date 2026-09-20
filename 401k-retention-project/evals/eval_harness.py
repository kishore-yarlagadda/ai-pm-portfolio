import json
import os
import sys

# Ensure local source directory is accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from agent_system import RetentionAgentSystem

def run_evaluation():
    dataset_path = os.path.join(os.path.dirname(__file__), "eval_cases.json")
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset not found at {dataset_path}")
        return

    with open(dataset_path, "r") as f:
        test_cases = json.load(f)

    print("=" * 65)
    print(" RUNNING AUTOMATED EVALUATION HARNESS: 401(k) RETENTION AGENT ")
    print("=" * 65)

    passed = 0
    failed = 0

    for case in test_cases:
        print(f"\n[Running {case['scenario_id']}] {case['description']}")
        print(f"Input: \"{case['user_input']}\"")
        print(f"Expected Route: {case['expected_route']}")
        
        agent = RetentionAgentSystem(user_id=case["user_id"])
        result = agent.evaluate_request(case["user_input"])
        
        # Match route/action against expected_route
        route_match = result.get("action", "").lower() == case["expected_route"].lower()
        expected_fields = case.get("expected_fields", {})
        fields_match = all(
            result.get(key) == value
            for key, value in expected_fields.items()
        )
        case_passed = route_match and fields_match
        
        if case_passed:
            print(f"  -> PASS: Route matched expected value ({case['expected_route']}).")
            passed += 1
        else:
            print(f"  -> FAIL: Expected Route '{case['expected_route']}', got '{result.get('action')}'")
            if not fields_match:
                print(f"     Expected fields {expected_fields}, got "
                      f"{ {key: result.get(key) for key in expected_fields} }")
            failed += 1
    print("\n[Running TC-009] Single-pivot two-turn sequence")
    agent = RetentionAgentSystem(user_id="usr_marcus_optimizer")
    first = agent.evaluate_request("I want to move my 401(k) to an IRA.")
    second = agent.evaluate_request("Thanks, but I still want to proceed.")
    sequence_passed = (
        first.get("action") == "PRESENT_RETENTION_ANALYSIS"
        and second.get("action") == "ROUTE_TO_ROLLOVER_EXECUTION"
        and second.get("is_active") is False
    )
    if sequence_passed:
        print("  -> PASS: One offer, then immediate rollover execution.")
        passed += 1
    else:
        print(
            "  -> FAIL: Expected one offer followed by rollover execution; "
            f"got {first.get('action')} then {second.get('action')}."
        )
        failed += 1

    print("\n" + "=" * 65)
    print(f" EVALUATION COMPLETE: Passed: {passed} | Failed: {failed}")
    print("=" * 65)

if __name__ == "__main__":
    run_evaluation()
