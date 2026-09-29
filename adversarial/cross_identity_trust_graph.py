import json

class CrossIdentityTrustGraph:
    def __init__(self):
        self.graph = {} 

    def add_trust_relationship(self, source, target, relationship_type='recovery_email'):
        if source not in self.graph:
            self.graph[source] = []
        self.graph[source].append((target, relationship_type))

    def calculate_cascade_risk(self, compromised_node):
        visited = set()
        stack = [compromised_node]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                if node in self.graph:
                    for neighbor, _ in self.graph[node]:
                        stack.append(neighbor)
        if compromised_node in visited:
            visited.remove(compromised_node)
        return list(visited), len(visited)

    def find_root_of_trust(self):
        all_nodes = set(self.graph.keys())
        for targets in self.graph.values():
            for target, _ in targets:
                all_nodes.add(target)
        pointed_to = set()
        for targets in self.graph.values():
            for target, _ in targets:
                pointed_to.add(target)
        roots = [n for n in all_nodes if n not in pointed_to]
        if not roots: return None
        root_impact = {root: len(self.calculate_cascade_risk(root)[0]) for root in roots}
        return max(root_impact, key=root_impact.get)

if __name__ == "__main__":
    citg = CrossIdentityTrustGraph()
    citg.add_trust_relationship("Google_Gmail", "MS_Account")
    citg.add_trust_relationship("MS_Account", "Mozilla_Vault")
    citg.add_trust_relationship("Google_Gmail", "AWS_Root")
    citg.add_trust_relationship("Mozilla_Vault", "Financial_Accounts")
    print(f"True Root of Trust: {citg.find_root_of_trust()}")
