import json
import os
from datetime import datetime

class CognitiveTemplateSynthesizer:
    def __init__(self, storage_path="/root/cognitive_templates.json"):
        self.storage_path = storage_path
        self.templates = self._load_templates()

    def _load_templates(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                return json.load(f)
        return {}

    def _save_templates(self):
        with open(self.storage_path, "w") as f:
            json.dump(self.templates, f, indent=2)

    def synthesize_template(self, template_id, domain, structure, success_criteria, examples):
        """
        Extracts a structural pattern from a success and codifies it as a template.
        """
        template = {
            "domain": domain,
            "structure": structure,
            "success_criteria": success_criteria,
            "examples": examples,
            "created_at": datetime.utcnow().isoformat(),
            "version": 1.0
        }
        self.templates[template_id] = template
        self._save_templates()
        return f"Template '{template_id}' synthesized successfully."

    def suggest_templates(self, current_task_description):
        """
        Scans existing templates for structural similarity to the current task.
        (Simulated semantic match)
        """
        suggestions = []
        for tid, tdata in self.templates.items():
            # Simple keyword match for simulation; in reality, this would use embeddings
            if any(word in current_task_description.lower() for word in tdata["domain"].lower().split()):
                suggestions.append({"id": tid, "domain": tdata["domain"], "structure": tdata["structure"]})
        return suggestions

# Example Usage
if __name__ == "__main__":
    cts = CognitiveTemplateSynthesizer()
    # Synthesizing a 'Cascading Recovery' pattern based on security wins
    print(cts.synthesize_template(
        "cascading_recovery", 
        "Security / Asset Recovery", 
        "Root Identity -> Session Neutralization -> Downstream Asset Verification -> Integrity Audit", 
        "Zero re-entry points, verified state parity", 
        ["Google Account Recovery", "AWS Root Access Restoration"]
    ))
    print("Suggestions for 'recover a hacked social media account':", cts.suggest_templates("recover a hacked social media account"))
