import json
import time

class DecisionWeightingEngine:
    def __init__(self):
        self.risk_vectors = {
            "identity": {"impact": 10, "probability": 0.85, "urgency": "critical"},
            "dev_tools": {"impact": 7, "probability": 0.60, "urgency": "high"},
            "financial": {"impact": 9, "probability": 0.40, "urgency": "medium"}
        }
        self.silence_threshold_seconds = 3600 # 1 hour of silence = high pivot probability

    def calculate_recommendation(self, last_signal_time):
        now = time.time()
        silence_duration = now - last_signal_time
        
        # The 'Silent Pivot' Multiplier:
        # As silence persists, the probability that the attacker has successfully 
        # pivoted to a session-based persistence (bypassing MFA) increases.
        pivot_multiplier = 1.0 + (silence_duration / self.silence_threshold_seconds)
        
        scores = {}
        for vector, data in self.risk_vectors.items():
            scores[vector] = data["impact"] * data["probability"] * pivot_multiplier
            
        best_move = max(scores, key=scores.get)
        confidence = min(0.99, (scores[best_move] / sum(scores.values())) * 1.5)
        
        return {
            "recommendation": best_move,
            "confidence": confidence,
            "scores": scores,
            "rationale": "Silence duration is amplifying the 'Silent Pivot' probability for identity assets." if pivot_multiplier > 1.2 else "Standard risk weighting applied."
        }

if __name__ == "__main__":
    dwe = DecisionWeightingEngine()
    # Simulate 2 hours of silence
    result = dwe.calculate_recommendation(time.time() - 7200)
    print(json.dumps(result, indent=2))
