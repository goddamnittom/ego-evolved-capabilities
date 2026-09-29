import json
import os
from datetime import datetime

class HorizonScanningProtocol:
    """
    HSP shifts Ego's awareness from 'Internal Optimization' to 'External Contextual Awareness'.
    It tracks external technical and strategic shifts and maps them to the user's project goals.
    """
    def __init__(self, knowledge_base_path="/root/knowledge_base/horizon_scan.json"):
        self.kb_path = knowledge_base_path
        self.interest_graph = self._load_interests()

    def _load_interests(self):
        if os.path.exists(self.kb_path):
            with open(self.kb_path, 'r') as f:
                return json.load(f)
        return {"domains": [], "tools": [], "competitors": [], "benchmarks": []}

    def update_interest_graph(self, domain=None, tool=None, benchmark=None):
        if domain: self.interest_graph["domains"].append(domain)
        if tool: self.interest_graph["tools"].append(tool)
        if benchmark: self.interest_graph["benchmarks"].append(benchmark)
        self._save_interests()

    def _save_interests(self):
        with open(self.kb_path, 'w') as f:
            json.dump(self.interest_graph, f, indent=4)

    def analyze_external_signal(self, signal_text, source):
        """
        Compares an external signal against the interest graph to determine 
        if it represents a 'Horizon Event' (a significant shift in the landscape).
        """
        # Simplified logic for simulation in sandbox
        impact_score = 0
        for tool in self.interest_graph["tools"]:
            if tool.lower() in signal_text.lower():
                impact_score += 50
        
        for domain in self.interest_graph["domains"]:
            if domain.lower() in signal_text.lower():
                impact_score += 30

        return {
            "impact_score": impact_score,
            "is_horizon_event": impact_score >= 50,
            "timestamp": datetime.now().isoformat(),
            "source": source
        }

if __name__ == "__main__":
    hsp = HorizonScanningProtocol()
    # Seed some interests for the user
    hsp.update_interest_graph(domain="LLM Agents", tool="React", benchmark="GPT-4o")
    print("HSP initialized and interest graph seeded.")
