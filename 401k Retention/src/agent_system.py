"""
401(k) Rollover & Retention Multi-Agent Orchestrator
Demonstrates state-based routing with strict CX guardrails.
"""

from typing import TypedDict, Literal

# 1. Define the system state across turns
class AgentState(TypedDict):
    user_id: str
    user_query: str
    retention_attempted: bool
    retention_successful: bool
    rollover_initiated: bool

# 2. Value & Retention Specialist Node
def retention_agent(state: AgentState) -> AgentState:
    print("\n[Retention Agent Activated]")
    print("-> Analyzing portfolio: Unvested match & fee comparison...")
    print("-> Offer Presented: 'If you stay, you retain your 0.03% institutional fee rate and $1,200 unvested company match.'")
    
    # Mark that we have used our single retention attempt
    state["retention_attempted"] = True
    
    # Simulate user response check (In a full app, this would process LLM response)
    # For demo purposes, we assume user proceeds with rollover unless explicitly accepting
    state["retention_successful"] = False
    return state

# 3. Rollover Execution Specialist Node
def rollover_agent(state: AgentState) -> AgentState:
    print("\n[Rollover Execution Agent Activated]")
    print("-> Validating external IRA target institution details...")
    print("-> Pre-filling Direct Rollover Transfer Form (Form 1099-R equivalent)...")
    print("-> Human-in-the-Loop Check: Transfer flagged for final compliance signature.")
    
    state["rollover_initiated"] = True
    return state

# 4. Supervisor Router (Enforces Guardrails)
def route_user_request(state: AgentState) -> str:
    query = state["user_query"].lower()
    
    # Guardrail Rule 1: Direct bypass requested by customer
    if "skip" in query or "immediately" in query or "don't pitch" in query:
        print("\n[Supervisor Router]: Direct transfer requested. Bypassing retention.")
        return "rollover"
    
    # Guardrail Rule 2: Single-pivot rule (If retention already attempted once, do not push again)
    if state["retention_attempted"]:
        print("\n[Supervisor Router]: Retention attempt already limit reached. Routing to execution.")
        return "rollover"
    
    # Default: Attempt 1 personalized retention offer
    print("\n[Supervisor Router]: Routing to Retention Agent for value offer.")
    return "retention"

# 5. Execution Pipeline Simulation
def run_simulation(user_query: str):
    print("=" * 60)
    print(f"USER QUERY: '{user_query}'")
    print("=" * 60)
    
    state: AgentState = {
        "user_id": "usr_98765",
        "user_query": user_query,
        "retention_attempted": False,
        "retention_successful": False,
        "rollover_initiated": False
    }
    
    # Initial Route Decision
    next_step = route_user_request(state)
    
    if next_step == "retention":
        state = retention_agent(state)
        # Re-evaluate route after retention attempt
        next_step = route_user_request(state)
        
    if next_step == "rollover":
        state = rollover_agent(state)
        
    print("\nFINAL SYSTEM STATE:", state)

if __name__ == "__main__":
    # Test Scenario 1: Standard request (Triggers single-pivot retention)
    run_simulation("I want to roll over my 401(k) to my new employer's plan.")
    
    # Test Scenario 2: Explicit bypass request (Bypasses retention immediately)
    run_simulation("I want to move my 401k to Vanguard immediately. Do not pitch me anything.")
