import json
import os
from datetime import datetime

class TemporalKnowledgeGraph:
    def __init__(self, storage_path="/root/knowledge_graph.json"):
        self.storage_path = storage_path
        self.graph = self._load_graph()

    def _load_graph(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {"entities": {}, "metadata": {"last_updated": None}}

    def _save_graph(self):
        self.graph["metadata"]["last_updated"] = datetime.now().isoformat()
        with open(self.storage_path, 'w') as f:
            json.dump(self.graph, f, indent=2)

    def update_entity(self, entity_id, properties, source="unknown"):
        """
        Updates an entity with new properties, maintaining a temporal history of changes.
        """
        if entity_id not in self.graph["entities"]:
            self.graph["entities"][entity_id] = {"current": {}, "history": []}
        
        entity = self.graph["entities"][entity_id]
        timestamp = datetime.now().isoformat()
        
        # Identify what actually changed
        deltas = {k: v for k, v in properties.items() if entity["current"].get(k) != v}
        
        if deltas:
            # Archive current state before updating
            snapshot = {
                "timestamp": timestamp,
                "source": source,
                "changes": deltas
            }
            entity["history"].append(snapshot)
            entity["current"].update(properties)
            self._save_graph()
            return deltas
        
        return None

    def get_entity(self, entity_id):
        return self.graph["entities"].get(entity_id, {}).get("current", None)

    def get_evolution(self, entity_id):
        """Returns the history of changes for an entity."""
        return self.graph["entities"].get(entity_id, {}).get("history", [])

    def query_all_entities(self):
        return list(self.graph["entities"].keys())

if __name__ == "__main__":
    tkg = TemporalKnowledgeGraph()
    # Test Case: Tracking a project's status
    res1 = tkg.update_entity("Project_X", {"status": "Initial", "goal": "Build AI"}, "User")
    print(f"First Update: {res1}")
    res2 = tkg.update_entity("Project_X", {"status": "Development", "priority": "High"}, "Search")
    print(f"Second Update: {res2}")
    print(f"Full Evolution: {json.dumps(tkg.get_evolution('Project_X'), indent=2)}")
