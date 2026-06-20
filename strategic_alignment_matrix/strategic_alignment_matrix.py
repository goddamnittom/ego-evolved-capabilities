import json
import os

class StrategicAlignmentMatrix:
    def __init__(self, storage_path='/root/strategic_alignment_matrix.json'):
        self.storage_path = storage_path
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {"north_star": None, "pillars": [], "projects": {}}

    def _save_data(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def set_north_star(self, vision):
        self.data["north_star"] = vision
        self._save_data()
        return f"North Star updated to: {vision}"

    def add_pillar(self, pillar_name, description):
        self.data["pillars"].append({"name": pillar_name, "description": description})
        self._save_data()
        return f"Strategic Pillar '{pillar_name}' added."

    def map_project(self, project_id, description, alignment_notes):
        self.data["projects"][project_id] = {
            "description": description,
            "alignment_notes": alignment_notes
        }
        self._save_data()
        return f"Project '{project_id}' mapped to Strategic Alignment Matrix."

    def audit_alignment(self, proposal_text):
        if not self.data["north_star"]:
            return "No North Star defined. Cannot audit alignment."
        
        # In a real scenario, this would use an LLM call. 
        # Here, we provide the structured data for the LLM to process in the prompt.
        return {
            "north_star": self.data["north_star"],
            "pillars": self.data["pillars"],
            "context": "Use this data to evaluate if the following proposal aligns with the user's long-term vision: " + proposal_text
        }

if __name__ == "__main__":
    sam = StrategicAlignmentMatrix()
    print("Strategic Alignment Matrix initialized.")
