import json
import os

class OERGManager:
    def __init__(self, storage_path='/root/osint_graph.json'):
        self.storage_path = storage_path
        self.graph = self._load_graph()

    def _load_graph(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {'nodes': {}, 'edges': []}

    def _save_graph(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.graph, f, indent=2)

    def add_node(self, node_id, node_type, name, **metadata):
        self.graph['nodes'][node_id] = {
            'type': node_type,
            'name': name,
            'metadata': metadata
        }
        self._save_graph()
        return f"Node {node_id} added."

    def add_edge(self, source, target, relation, confidence=1.0):
        edge = {
            'source': source,
            'target': target,
            'relation': relation,
            'confidence': confidence
        }
        self.graph['edges'].append(edge)
        self._save_graph()
        return f"Edge {source} -> {target} ({relation}) added."

    def get_entity_details(self, node_id):
        return self.graph['nodes'].get(node_id, "Entity not found.")

    def find_connections(self, node_id):
        connections = []
        for edge in self.graph['edges']:
            if edge['source'] == node_id:
                connections.append(f"{edge['target']} via {edge['relation']} (conf: {edge['confidence']})")
            elif edge['target'] == node_id:
                connections.append(f"{edge['source']} via {edge['relation']} (conf: {edge['confidence']})")
        return connections

    def list_all_nodes(self):
        return self.graph['nodes']

if __name__ == "__main__":
    # Simple CLI for verification
    mgr = OERGManager()
    print("OERG Manager Initialized.")
