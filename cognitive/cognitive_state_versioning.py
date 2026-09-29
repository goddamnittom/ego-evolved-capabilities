import json
import os
from datetime import datetime

class CognitiveStateVersioning:
    def __init__(self, storage_path="/root/cognitive_states.json"):
        self.storage_path = storage_path
        self.states = self._load_states()

    def _load_states(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {}

    def capture_state(self, state_id, hypothesis, constraints, risk_landscape, intuition):
        """
        Captures a snapshot of the AI's internal cognitive state.
        """
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "hypothesis": hypothesis,
            "constraints": constraints,
            "risk_landscape": risk_landscape,
            "intuition": intuition
        }
        self.states[state_id] = snapshot
        self._save_states()
        return f"State '{state_id}' captured successfully."

    def diff_states(self, state_id_a, state_id_b):
        """
        Analyzes the divergence between two cognitive states.
        """
        if state_id_a not in self.states or state_id_b not in self.states:
            return "One or both states not found."
        
        a = self.states[state_id_a]
        b = self.states[state_id_b]
        
        diff = {
            "hypothesis_shift": a['hypothesis'] != b['hypothesis'],
            "constraint_change": a['constraints'] != b['constraints'],
            "risk_evolution": a['risk_landscape'] != b['risk_landscape'],
            "intuition_drift": a['intuition'] != b['intuition']
        }
        return diff

    def _save_states(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.states, f, indent=2)

    def list_snapshots(self):
        return list(self.states.keys())

if __name__ == "__main__":
    csv = CognitiveStateVersioning()
    csv.capture_state(
        "initial_attack_analysis", 
        "Attacker is using a session-hijack vector", 
        ["No access to root email", "MFA active"], 
        "High risk of lateral movement to AWS", 
        "Feeling that the attacker is an insider"
    )
    csv.capture_state(
        "post_evidence_review", 
        "Attacker is using a leaked API key, not session hijack", 
        ["API key rotated", "MFA active"], 
        "Low risk of lateral movement, high risk of data exfiltration", 
        "Conviction that this is an automated bot"
    )
    print(csv.diff_states("initial_attack_analysis", "post_evidence_review"))
