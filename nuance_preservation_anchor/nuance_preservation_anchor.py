import json
import os

class NuancePreservationAnchor:
    def __init__(self, storage_path="/root/nuance_anchors.json"):
        self.storage_path = storage_path
        self.anchors = self._load_anchors()

    def _load_anchors(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {}

    def anchor_exception(self, context_id, nuance_data, associated_axiom=None):
        self.anchors[context_id] = {
            "nuance": nuance_data,
            "axiom_override": associated_axiom,
            "timestamp": os.popen('date -u +"%Y-%m-%dT%H:%M:%SZ"').read().strip()
        }
        self._save()

    def query_nuance(self, context_id):
        return self.anchors.get(context_id, None)

    def _save(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.anchors, f, indent=4)

if __name__ == "__main__":
    npa = NuancePreservationAnchor()
    print("Nuance-Preservation Anchor (NPA) deployed successfully.")
