import logging
import os
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")

class AgenticSDlcOrchestrator:
    def __init__(self, feature_request: str):
        self.feature_request = feature_request
        self.state: Dict[str, Any] = {"feature_request": feature_request, "lifecycle_stage": "INITIALIZED"}
        
        folder_name = input("Enter output project folder name (e.g., llm-evaluator): ").strip()
        if not folder_name:
            folder_name = "llm-evaluator-project"
            
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        workspace_root = os.path.dirname(project_root)
        
        self.output_dir = os.path.join(workspace_root, folder_name)
        self.template_dir = os.path.join(current_dir, "templates")
        
        for sub in ["documents", "prds"]:
            os.makedirs(os.path.join(self.output_dir, sub), exist_ok=True)

    def run_product_lifecycle_step(self, step_name: str, framework: str, filename: str, subfolder: str, template_filename: str):
        """Loads a refined template, injects the feature request, and enforces a HITL review gate."""
        logging.info(f"Executing Product Phase: {step_name} [Framework: {framework}]")
        template_path = os.path.join(self.template_dir, template_filename)
        
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Required template not found at: {template_path}")
            
        with open(template_path, "r") as f:
            content = f.read().format(feature_request=self.feature_request)
            
        target_dir = os.path.join(self.output_dir, subfolder)
        file_path = os.path.join(target_dir, filename)
        
        with open(file_path, "w") as f:
            f.write(content)
            
        logging.info(f"Product artifact generated: {file_path}")
        print(f"\n[PRODUCT HITL GATE] Stage: {step_name} | Framework: {framework}")
        input(f"Review product document at {file_path}, then press Enter to approve...\n")

    def invoke_engineering_pipeline(self):
        """Stub for future code generation and technical architecture tools."""
        logging.info("Engineering pipeline stub reached. Awaiting code generation agent tools.")
        print("\n[ENG GATE] Product phase complete. Technical implementation and code generation are separated.")

    def execute_product_phase(self):
        # 1. Strategy & Planning
        self.run_product_lifecycle_step(
            "Strategy and Planning", "RISE", "strategy_spec.md", "documents", "strategy_template.md"
        )
        # 2. Product Discovery
        self.run_product_lifecycle_step(
            "Product Discovery", "PACT", "discovery_report.md", "documents", "discovery_template.md"
        )
        # 3. Product Requirements Document (PRD)
        self.run_product_lifecycle_step(
            "PRD and Artifacts", "RACE / Merged Spec", "product_requirement_doc.md", "prds", "prd_template.md"
        )
        
        logging.info("Product documentation lifecycle completed successfully.")
        self.invoke_engineering_pipeline()

if __name__ == "__main__":
    feature = input("Enter feature request [Press Enter for default]: ").strip()
    AgenticSDlcOrchestrator(feature_request=feature).execute_product_phase()
