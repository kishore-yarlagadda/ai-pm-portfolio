"""
Interactive Portfolio Demo for Hiring Managers & Reviewers
Allows interactive testing of persona selection, prompt intent evaluation, and supervisor routing.
"""

from agent_system import RetentionAgentSystem
from connectors import EnterpriseDataConnectors

def run_interactive_demo():
    print("=" * 65)
    print("  AI PM PORTFOLIO DEMO: 401(k) RETENTION & GUARDRAIL AGENT  ")
    print("=" * 65)
    print("Select a Persona to simulate the session:\n")
    print("  [1] Marcus Vance   - Fee-Sensitive Optimizer (High Balance, $185k)")
    print("  [2] Sarah Jenkins  - Frustrated / Urgent Exiter (Mid Balance, $45k)")
    print("  [3] Elena Rostova  - Unsure Retiree (High Balance, $320k, Tax Sensitive)")
    print("-" * 65)

    persona_map = {
        "1": "usr_marcus_optimizer",
        "2": "usr_sarah_frustrated",
        "3": "usr_elena_retiree"
    }

    choice = input("\nEnter choice (1, 2, or 3) [Default: 1]: ").strip()
    user_id = persona_map.get(choice, "usr_marcus_optimizer")

    crm = EnterpriseDataConnectors.get_crm_history(user_id)
    portfolio = EnterpriseDataConnectors.get_portfolio_data(user_id)

    print("\n" + "=" * 65)
    print(f" ACTIVE SESSION: {crm['name']} ({crm['user_id']})")
    print(f" Motivation    : {crm['primary_motivation']}")
    print(f" Portfolio Val : ${portfolio['total_balance']:,.2f}")
    print(f" CRM Context   : {crm['csa_notes']}")
    print("=" * 65 + "\n")

    agent = RetentionAgentSystem(user_id=user_id)

    print("Type your message as the customer (e.g., 'I want to roll over to an IRA', 'Transfer immediately', or 'What about tax penalties?').")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("\nUser > ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("\nDemo session ended.")
            break

        if not user_input:
            continue

        response = agent.evaluate_request(user_input)

        print("\n" + "-" * 50)
        print(f" [SYSTEM ACTION] : {response['action']}")
        print(f" [ROUTING REASON]: {response['reason']}")
        print("-" * 50)
        print(f"\nAgent Response:\n{response['message']}\n")

if __name__ == "__main__":
    run_interactive_demo()
