import subprocess
import sys
from pathlib import Path
from pydantic import BaseModel, Field

class SDLCState(BaseModel):
    feature_name: str
    current_phase: str = Field(default="SPEC_PENDING")
    spec_approved: bool = Field(default=False)
    tasks_approved: bool = Field(default=False)
    test_coverage_met: bool = Field(default=False)
    type_check_passed: bool = Field(default=False)

class SDLCOrchestrator:
    def __init__(self, feature_name: str, base_dir: str = "src", state_file: str = ".sdlc_state.json"):
        self.state_path = Path(state_file)
        self.base_dir = Path(base_dir)
        self.state = self.load_state(feature_name)

    def load_state(self, feature_name: str) -> SDLCState:
        """Loads state from JSON if it exists, otherwise initializes a new one."""
        if self.state_path.exists():
            try:
                data = self.state_path.read_text(encoding="utf-8")
                print(f"[SDLC] Resuming workflow from state file: {self.state_path.name}")
                return SDLCState.model_validate_json(data)
            except Exception as e:
                print(f"[Warning] Failed to parse state file: {e}. Initializing fresh state.")
        return SDLCState(feature_name=feature_name)

    def save_state(self):
        """Persists the current SDLC state to a JSON file."""
        self.state_path.write_text(self.state.model_dump_json(indent=2), encoding="utf-8")

    def trigger_hitl_gate(self, gate_name: str) -> bool:
        """Enforces Human-in-the-Loop terminal confirmation before advancing."""
        print(f"\n[HITL GATE REQUIREMENT] Review required for: {gate_name}")
        response = input(f"Do you approve progression for '{self.state.feature_name}'? [y/N]: ").strip().lower()
        return response == 'y'

    def run_quality_gates(self) -> bool:
        """Executes pytest coverage and mypy type checks programmatically."""
        print("\nRunning Automated Quality & Test Gates...")
        
        # Run mypy type safety check
        mypy_result = subprocess.run(["mypy", str(self.base_dir)], capture_output=True, text=True)
        self.state.type_check_passed = (mypy_result.returncode == 0)
        
        # Run pytest with coverage threshold
        pytest_result = subprocess.run(
            ["pytest", "--cov=" + str(self.base_dir), "--cov-fail-under=85"], 
            capture_output=True, 
            text=True
        )
        self.state.test_coverage_met = (pytest_result.returncode == 0)

        print(f"Mypy Type Check Passed: {self.state.type_check_passed}")
        print(f"Pytest Coverage (>=85%) Passed: {self.state.test_coverage_met}")
        
        self.save_state()
        return self.state.type_check_passed and self.state.test_coverage_met

    def advance_workflow(self):
        """Drives the state machine forward based on gate compliance and persists state."""
        if not self.state.spec_approved:
            if self.trigger_hitl_gate("Engineering Architecture Specification"):
                self.state.spec_approved = True
                self.state.current_phase = "TASK_PLANNING"
                print("-> Phase Advanced: Spec Approved. Moving to Task Plan.")
            else:
                print("-> Halting: Architecture Spec rejected or pending review.")
                self.save_state()
                return

        if self.state.spec_approved and not self.state.tasks_approved:
            if self.trigger_hitl_gate("Implementation Task Plan"):
                self.state.tasks_approved = True
                self.state.current_phase = "IMPLEMENTATION_AND_TESTING"
                print("-> Phase Advanced: Tasks Approved. Ready for Code Generation.")
            else:
                print("-> Halting: Task Plan pending human sign-off.")
                self.save_state()
                return

        if self.state.tasks_approved:
            if self.run_quality_gates():
                self.state.current_phase = "COMPLETED_AND_VERIFIED"
                print(f"-> SUCCESS: Feature '{self.state.feature_name}' successfully passed all SDLC gates!")
            else:
                self.state.current_phase = "INCIDENT_TRIAGE"
                print(f"-> GATES FAILED: Instantiating Bug Report template for triage.")
        
        self.save_state()

if __name__ == "__main__":
    orchestrator = SDLCOrchestrator(feature_name="Dynamic Payload Handler")
    orchestrator.advance_workflow()
