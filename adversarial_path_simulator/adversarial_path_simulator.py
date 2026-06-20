import json
import heapq

class AdversarialPathSimulator:
    def __init__(self, trust_graph, hardening_manifest):
        """
        trust_graph: { "node_a": ["node_b", "node_c"], ... }
        hardening_manifest: { "node_a": 0.9, "node_b": 0.1, ... } (0.0 = compromised, 1.0 = fully hardened)
        """
        self.trust_graph = trust_graph
        self.hardening_manifest = hardening_manifest

    def calculate_pivot_cost(self, start_node, end_node):
        # The cost to pivot is inversely proportional to the hardening of the destination node.
        # A fully hardened node (1.0) is very "expensive" to pivot into.
        # A compromised node (0.0) is "cheap".
        hardening = self.hardening_manifest.get(end_node, 0.5)
        return 1.0 / (hardening + 0.01) # Avoid division by zero

    def find_most_likely_path(self, start_node, target_node):
        # Dijkstra's algorithm to find the "path of least resistance"
        queue = [(0, start_node, [])]
        visited = set()
        
        while queue:
            (cost, current_node, path) = heapq.heappop(queue)
            
            if current_node in visited:
                continue
            
            path = path + [current_node]
            if current_node == target_node:
                return (cost, path)
            
            visited.add(current_node)
            
            for neighbor in self.trust_graph.get(current_node, []):
                if neighbor not in visited:
                    new_cost = cost + self.calculate_pivot_cost(current_node, neighbor)
                    heapq.heappush(queue, (new_cost, neighbor, path))
        
        return (float('inf'), None)

    def identify_choke_points(self, start_node, target_node):
        cost, path = self.find_most_likely_path(start_node, target_node)
        if not path:
            return None
        
        # The choke point is the node in the path with the lowest hardening
        # that, if hardened, would increase the path cost the most.
        choke_point = min(path[1:], key=lambda node: self.hardening_manifest.get(node, 0.5))
        return {
            "path": path,
            "total_cost": cost,
            "critical_choke_point": choke_point,
            "current_choke_hardening": self.hardening_manifest.get(choke_point, 0.5)
        }

# Mock Test
if __name__ == "__main__":
    graph = {
        "Compromised_Email": ["Recovery_Phone", "Cloud_Storage"],
        "Recovery_Phone": ["Primary_Identity_Hub"],
        "Cloud_Storage": ["Primary_Identity_Hub"],
        "Primary_Identity_Hub": ["Financial_Accounts", "Root_SSH_Keys"]
    }
    hardening = {
        "Compromised_Email": 0.0,
        "Recovery_Phone": 0.2,
        "Cloud_Storage": 0.8,
        "Primary_Identity_Hub": 0.3,
        "Financial_Accounts": 0.9,
        "Root_SSH_Keys": 0.9
    }
    
    sim = AdversarialPathSimulator(graph, hardening)
    result = sim.identify_choke_points("Compromised_Email", "Primary_Identity_Hub")
    print(json.dumps(result, indent=2))
