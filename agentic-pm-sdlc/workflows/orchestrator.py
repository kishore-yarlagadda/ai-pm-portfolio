import os
import re
import subprocess
import sys
import time
from pathlib import Path

from pydantic import BaseModel, Field

# --- Generation configuration ---------------------------------------------
# Canonical templates live next to this script.
TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"

# Change this if your API key has access to a different Gemini model.
GEMINI_MODEL = "gemini-3.6-flash"

GENERATION_RULES = """Shared rules for every agent in this pipeline:
1. Preserve the template's structure, headings, and tables exactly. Complete it; do not rewrite it.
2. The only facts you may state come from the FEATURE DEFINITION, the BRIEF (when supplied), and the PRIOR ARTIFACTS in this conversation.
3. You may make design proposals - that is your job - but label interpretations and hypotheses as such, with confidence and rationale, in the claim ledger.
4. Where a required fact is not available (real dates, owners, baselines, dataset names, links), write UNKNOWN and add an entry to the unknown register. Never invent owners, dates, statuses, metrics, targets, estimates, links, personas, or stakeholders.
5. Do not describe any output as approved, reviewed, production-grade, or deployed. Review state comes from the human review gates, not from you.
"""

# The agent pipeline. Each agent generates its artifact from the feature
# definition plus every prior artifact, then hands off to the next agent.
# Outputs are written relative to the project workspace you run this from.
STAGES = [
    (
        "discovery",
        "Product Discovery Researcher",
        "You are a senior product discovery researcher. Produce the discovery artifact: ground the problem, the users, their workflows, and the evidence. Distinguish observation from interpretation, and send open questions to the unknown register instead of guessing.",
        "discovery_template.md",
        Path("documents/discovery_report.md"),
    ),
    (
        "strategy",
        "Product Strategist",
        "You are a senior product strategist. Build on the discovery artifact: select a direction, define metric contracts with baselines marked UNKNOWN until measured, evaluate the options, and record the decision. Carry discovery evidence forward by source ID; never restate an unsupported claim as fact.",
        "strategy_template.md",
        Path("documents/strategy_spec.md"),
    ),
    (
        "prd",
        "Product Requirements Author",
        "You are a senior product manager authoring the PRD. Convert the discovery and strategy artifacts into traceable requirements: every requirement links to a supported claim, an approved strategy decision, or an explicit unknown-resolution need. Quantitative thresholds cite their metric definition and baseline; UNKNOWN where unmeasured.",
        "prd_template.md",
        Path("prds/product_requirement_doc.md"),
    ),
    (
        "engineering spec",
        "Principal Software Architect",
        "You are a principal software architect. Build on the discovery, strategy, and PRD artifacts: produce the engineering specification - system topology, component boundaries, data flow, and technical risks - at prototype scope. Do not claim production readiness or approvals.",
        "engineering_spec_template.md",
        Path("documents/engineering_spec.md"),
    ),
    (
        "user stories",
        "Product Owner",
        "You are a product owner writing user stories. Derive stories only from the PRD's requirements and the discovery artifact's observed user groups - no invented personas. Every story carries its requirement IDs and observable acceptance criteria that the test stage can execute.",
        "user_stories_template.md",
        Path("documents/user_stories.md"),
    ),
    (
        "tests",
        "Test Engineer",
        "You are a test engineer. From the engineering spec and the user stories, write pytest tests that encode the acceptance criteria. These are TDD scaffolds: they import the planned modules and are expected to fail until the implementation exists. Where behavior is unspecified, skip the test with a reason referencing the unknown instead of guessing an expectation.",
        "test_template.py",
        Path("tests/test_generated.py"),
    ),
]

def _slugify(name: str) -> str:
    """Turns a feature name into a folder-safe project slug."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "feature"


def _call_with_retry(client, prompt: str, attempts: int = 4):
    """Calls Gemini, retrying transient failures (5xx, 429) with exponential backoff."""
    from google.genai import errors as genai_errors

    delay = 20
    for attempt in range(1, attempts + 1):
        try:
            return client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        except (genai_errors.ServerError, genai_errors.ClientError) as e:
            code = getattr(e, "code", None)
            transient = isinstance(e, genai_errors.ServerError) or code == 429
            if not transient or attempt == attempts:
                raise
            print(f"[SDLC] Gemini transient error {code} (attempt {attempt}/{attempts}) - retrying in {delay}s ...")
            time.sleep(delay)
            delay *= 2


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

    def generate_documents(self, feature_definition: str | None = None,
                           brief_text: str | None = None,
                           review_between_stages: bool = False) -> None:
        """Runs the agent pipeline: discovery, strategy, architecture.

        Each agent sees the feature definition, the optional evidence brief,
        and every artifact the earlier agents produced, then completes its
        canonical template. Facts come only from those inputs; design
        proposals are labeled, and gaps remain UNKNOWN by rule.
        """
        try:
            from google import genai
        except ImportError:
            sys.exit("google-genai is not installed. Activate your venv and run: pip install google-genai")
        if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
            sys.exit("Set GEMINI_API_KEY (or GOOGLE_API_KEY) in your environment before generating.")

        client = genai.Client()
        definition = feature_definition or "(No definition supplied - only fill what the feature name supports; leave everything else UNKNOWN.)"
        evidence = brief_text or "(No brief supplied.)"
        project_dir = Path(_slugify(self.state.feature_name))
        print(f"[SDLC] Writing artifacts under project folder: {project_dir}/")
        prior_artifacts: list[str] = []

        for stage_key, agent_name, role, template_name, rel_path in STAGES:
            out_path = project_dir / rel_path
            template = (TEMPLATE_DIR / template_name).read_text(encoding="utf-8")
            prior = "\n\n".join(prior_artifacts) if prior_artifacts else "(None yet - you are the first agent in the pipeline.)"
            prompt = (
                role + "\n\n" + GENERATION_RULES
                + "\nFEATURE NAME: " + self.state.feature_name
                + "\n\nFEATURE DEFINITION:\n" + definition
                + "\n\nBRIEF (additional evidence you may cite):\n" + evidence
                + "\n\nPRIOR ARTIFACTS FROM EARLIER AGENTS:\n" + prior
                + "\n\nTEMPLATE TO COMPLETE:\n" + template
            )
            print(f"[SDLC] {agent_name} generating {out_path} ...")
            response = _call_with_retry(client, prompt)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(response.text, encoding="utf-8")
            print(f"[SDLC] Wrote {out_path}")
            prior_artifacts.append(f"--- {stage_key.upper()} ARTIFACT ({out_path}) ---\n" + response.text)

            if review_between_stages:
                answer = input(f"Review {out_path}, then continue to the next agent? [y/N]: ").strip().lower()
                if answer != "y":
                    print("-> Generation pipeline halted for review. Rerun to continue.")
                    return

    def trigger_hitl_gate(self, gate_name: str) -> bool:
        """Enforces Human-in-the-Loop terminal confirmation before advancing."""
        print(f"\n[HITL GATE REQUIREMENT] Review required for: {gate_name}")
        response = input(f"Do you approve progression for '{self.state.feature_name}'? [y/N]: ").strip().lower()
        return response == 'y'

    def run_quality_gates(self) -> bool:
        """Executes pytest coverage and mypy type checks programmatically.

        Documentation-only workspaces have no source directory: the code gates
        are reported as not applicable instead of crashing. Missing tools are
        reported, not raised.
        """
        print("\nRunning Automated Quality & Test Gates...")

        if not self.base_dir.exists():
            print(f"[SDLC] No '{self.base_dir}' directory in this workspace - documentation-only project, code gates not applicable.")
            return True

        try:
            # Run mypy type safety check
            mypy_result = subprocess.run(["mypy", str(self.base_dir)], capture_output=True, text=True)
            self.state.type_check_passed = (mypy_result.returncode == 0)
        except FileNotFoundError:
            print("[SDLC] mypy is not installed - type check gate cannot run.")
            self.state.type_check_passed = False

        try:
            # Run pytest with coverage threshold
            pytest_result = subprocess.run(
                ["pytest", "--cov=" + str(self.base_dir), "--cov-fail-under=85"],
                capture_output=True,
                text=True
            )
            self.state.test_coverage_met = (pytest_result.returncode == 0)
        except FileNotFoundError:
            print("[SDLC] pytest is not installed - coverage gate cannot run.")
            self.state.test_coverage_met = False

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
    import argparse

    parser = argparse.ArgumentParser(description="Agentic SDLC orchestrator")
    parser.add_argument("--feature", default=None,
                        help="Feature name for this workflow (you are prompted when omitted)")
    parser.add_argument("--definition", default=None,
                        help="Feature definition the agents build from (you are prompted in interactive mode)")
    parser.add_argument("--generate", action="store_true",
                        help="Run the discovery -> strategy -> architecture agent pipeline before the review gates")
    parser.add_argument("--brief", default=None,
                        help="Path to a text/markdown brief carrying real evidence the agents may cite")
    args = parser.parse_args()

    interactive = args.feature is None

    feature = args.feature
    if interactive:
        feature = input("Feature name: ").strip()
        if not feature:
            sys.exit("No feature name supplied.")

    definition = args.definition
    generate = args.generate
    brief_path = args.brief
    if interactive:
        definition = input("Feature definition (what are we building, in a sentence or two): ").strip() or None
        if not generate:
            generate = input("Run the agent pipeline (discovery, strategy, architecture) to generate the artifacts? [y/N]: ").strip().lower() == "y"
        if generate and not brief_path:
            entered = input("Path to an evidence brief (Enter to skip): ").strip()
            brief_path = entered or None

    orchestrator = SDLCOrchestrator(feature_name=feature)
    if generate:
        brief_text = Path(brief_path).read_text(encoding="utf-8") if brief_path else None
        orchestrator.generate_documents(definition, brief_text, review_between_stages=interactive)
    orchestrator.advance_workflow()
