import json
import os
from datetime import datetime

class SynthesisEngine:
    def __init__(self, kb_path="/root/knowledge_base"):
        self.kb_path = kb_path
        os.makedirs(kb_path, exist_ok=True)

    def create_cluster(self, cluster_id, items, synthesis_note):
        cluster = {
            "id": cluster_id,
            "timestamp": datetime.utcnow().isoformat(),
            "items": items,
            "synthesis": synthesis_note
        }
        with open(f"{self.kb_path}/{cluster_id}.json", "w") as f:
            json.dump(cluster, f, indent=2)
        return cluster

    def list_clusters(self):
        return [f.replace(".json", "") for f in os.listdir(self.kb_path) if f.endswith(".json")]

if __name__ == "__main__":
    engine = SynthesisEngine()
    print("Synthesis Engine Initialized. Ready to cluster intelligence.")
