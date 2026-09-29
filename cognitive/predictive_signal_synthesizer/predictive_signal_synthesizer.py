import json
import random
from datetime import datetime, timedelta

class PredictiveSignalSynthesizer:
    """
    Shifts security monitoring from 'Correlation' (what happened) 
    to 'Expectation' (what should happen next).
    """
    def __init__(self, actor_profile=None, utl_state=None):
        self.actor_profile = actor_profile or {}
        self.utl_state = utl_state or {}
        self.expectation_matrix = []

    def generate_expectations(self):
        """
        Synthesizes a Signal Expectation Matrix (SEM) based on actor behavior 
        and current perimeter vulnerabilities.
        """
        # Simplified logic: Map actor habits to target assets
        habits = self.actor_profile.get("behavioral_markers", [])
        assets = self.utl_state.get("assets", [])
        
        expectations = []
        for habit in habits:
            for asset in assets:
                if habit["type"] == "pivot" and asset["type"] == habit["target_type"]:
                    expectations.append({
                        "signal": f"Unauthorized access attempt: {asset['name']}",
                        "probability": habit["probability"],
                        "timeframe": "12-48 hours",
                        "criticality": "High",
                        "reason": f"Actor {self.actor_profile.get('id', 'Unknown')} typically pivots to {asset['type']} after initial entry."
                    })
        
        self.expectation_matrix = expectations
        return expectations

    def resolve_signal(self, actual_signal):
        """
        Compares an incoming signal against the expectation matrix to 
        calculate 'Predictive Accuracy'.
        """
        for exp in self.expectation_matrix:
            if exp["signal"] == actual_signal:
                return {"status": "PREDICTED", "accuracy_gain": 0.1, "message": "Signal matched expectation. Actor profile reinforced."}
        
        return {"status": "UNEXPECTED", "accuracy_loss": 0.05, "message": "Signal was not predicted. Actor profile may be shifting."}

if __name__ == "__main__":
    # Mock data for verification
    actor = {"id": "APT-X", "behavioral_markers": [{"type": "pivot", "target_type": "email", "probability": 0.8}]}
    utl = {"assets": [{"name": "primary_gmail", "type": "email"}]}
    
    pss = PredictiveSignalSynthesizer(actor, utl)
    print(json.dumps(pss.generate_expectations(), indent=2))
