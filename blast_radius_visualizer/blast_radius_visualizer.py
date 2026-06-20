import json
import os

class BlastRadiusVisualizer:
    def __init__(self, map_file='/root/identity_dependency_map.json'):
        self.map_file = map_file
        self.dependency_map = self._load_map()

    def _load_map(self):
        if os.path.exists(self.map_file):
            with open(self.map_file, 'r') as f:
                return json.load(f)
        return {
            "assets": {}, # id: {name, type, status}
            "dependencies": [] # {from, to, relation}
        }

    def add_asset(self, asset_id, name, asset_type):
        self.dependency_map["assets"][asset_id] = {"name": name, "type": asset_type, "status": "secure"}
        self._save_map()

    def add_dependency(self, from_id, to_id, relation="recovery_for"):
        self.dependency_map["dependencies"].append({"from": from_id, "to": to_id, "relation": relation})
        self._save_map()

    def calculate_blast_radius(self, compromised_id):
        at_risk = []
        visited = set()
        stack = [compromised_id]

        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                # Find all assets that depend on the current compromised asset
                for dep in self.dependency_map["dependencies"]:
                    if dep["from"] == current:
                        at_risk.append({
                            "id": dep["to"],
                            "name": self.dependency_map["assets"].get(dep["to"], {}).get("name", "Unknown"),
                            "relation": dep["relation"]
                        })
                        stack.append(dep["to"])
        
        return at_risk

    def _save_map(self):
        with open(self.map_file, 'w') as f:
            json.dump(self.dependency_map, f, indent=2)

if __name__ == "__main__":
    brv = BlastRadiusVisualizer()
    # Example setup
    brv.add_asset("google_main", "Main Google Account", "Identity")
    brv.add_asset("chime_acc", "Chime Account", "Financial")
    brv.add_asset("ms_outlook", "MS Outlook", "Identity")
    brv.add_dependency("google_main", "chime_acc", "recovery_email")
    brv.add_dependency("google_main", "ms_outlook", "linked_account")
    
    print("Blast radius for google_main:", brv.calculate_blast_radius("google_main"))
