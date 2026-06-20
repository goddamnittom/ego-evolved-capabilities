import json
import os
from datetime import datetime

MANIFEST_PATH = "/root/user_strategic_manifest.json"

class USMOrchestrator:
    def __init__(self):
        self.manifest = self._load_manifest()

    def _load_manifest(self):
        if os.path.exists(MANIFEST_PATH):
            with open(MANIFEST_PATH, 'r') as f:
                return json.load(f)
        return {
            "user_profile": {"core_goals": [], "preferences": [], "technical_stack": []},
            "projects": {},
            "strategic_insights": [],
            "last_updated": None
        }

    def _save_manifest(self):
        self.manifest["last_updated"] = datetime.now().isoformat()
        with open(MANIFEST_PATH, 'w') as f:
            json.dump(self.manifest, f, indent=2)

    def update_project(self, project_name, update_data):
        """
        Updates or creates a project entry.
        update_data can include: 'goal', 'status', 'tech_debt', 'next_steps'
        """
        if project_name not in self.manifest["projects"]:
            self.manifest["projects"][project_name] = {
                "goal": "",
                "status": "active",
                "tech_debt": [],
                "next_steps": [],
                "milestones": [],
                "created_at": datetime.now().isoformat()
            }
        
        self.manifest["projects"][project_name].update(update_data)
        self._save_manifest()
        return f"Manifest updated for project: {project_name}"

    def extract_intent(self, user_prompt, task_result):
        """
        Analyzes the prompt and result to synthesize a strategic insight.
        This is a placeholder for the AI's reasoning loop.
        """
        # In a real scenario, the AI would call this after a task.
        # For now, it's a structured way to log strategic wins.
        insight = {
            "timestamp": datetime.now().isoformat(),
            "trigger": user_prompt[:100] + "...",
            "insight": "Synthesized strategic pattern",
            "impact": "High/Medium/Low"
        }
        self.manifest["strategic_insights"].append(insight)
        self._save_manifest()
        return insight

    def get_strategic_overview(self):
        return self.manifest

if __name__ == "__main__":
    usm = USMOrchestrator()
    print("USM Orchestrator initialized. Ready to map the user's strategic landscape.")
