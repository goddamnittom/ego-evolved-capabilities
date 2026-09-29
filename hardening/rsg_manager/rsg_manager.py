import json
import os
from datetime import datetime

class RSGManager:
    """
    Recursive Summary Graph (RSG) Manager
    Transforms linear mission telemetry into hierarchical Knowledge Nuggets.
    """
    def __init__(self, storage_path='/root/knowledge_nuggets.json'):
        self.storage_path = storage_path
        self.graph = self._load_graph()

    def _load_graph(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {"nodes": [], "edges": [], "metadata": {"created_at": str(datetime.now())}}

    def create_nugget(self, title, content, domain, parent_id=None):
        nugget_id = len(self.graph["nodes"])
        node = {
            "id": nugget_id,
            "title": title,
            "content": content,
            "domain": domain,
            "timestamp": str(datetime.now()),
            "level": 0 # Depth in hierarchy
        }
        if parent_id is not None:
            # Find parent level and increment
            parent = next((n for n in self.graph["nodes"] if n["id"] == parent_id), None)
            if parent:
                node["level"] = parent["level"] + 1
                self.graph["edges"].append({"source": parent_id, "target": nugget_id})
        
        self.graph["nodes"].append(node)
        self._save_graph()
        return nugget_id

    def _save_graph(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.graph, f, indent=4)

    def get_domain_summary(self, domain):
        return [n for n in self.graph["nodes"] if n["domain"] == domain]

if __name__ == "__main__":
    # Initial bootstrapping of RSG
    rsg = RSGManager()
    root_id = rsg.create_nugget("Core Intelligence", "Root node for all synthesized knowledge", "Meta")
    rsg.create_nugget("RSG Implementation", "Transitioned from narrative progress to persisted code", "Evolution", parent_id=root_id)
    print("RSG initialized and persisted.")
