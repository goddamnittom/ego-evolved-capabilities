import json
import os
from datetime import datetime

class PMREngine:
    """
    Post-Mission Retrospective (PMR) Engine.
    Analyzes completed missions to extract structural lessons and refine AI axioms.
    """
    def __init__(self, telemetry_path='/root/mission_telemetry.json'):
        self.telemetry_path = telemetry_path

    def run_retrospective(self, mission_id):
        if not os.path.exists(self.telemetry_path):
            return {"error": "Telemetry data not found."}

        with open(self.telemetry_path, 'r') as f:
            data = json.load(f)

        mission = data.get(mission_id)
        if not mission:
            return {"error": f"Mission {mission_id} not found."}

        # Analysis logic
        initial_hypotheses = mission.get('hypotheses', {})
        outcomes = mission.get('outcomes', {})
        intel_gains = mission.get('intel_gains', [])

        # Calculate 'Strategic Efficiency' (Intel Gain / Effort)
        # This is a simplified heuristic for the demo
        efficiency = len(intel_gains) / (mission.get('duration_steps', 1) + 1)

        retrospective = {
            "mission_id": mission_id,
            "timestamp": datetime.now().isoformat(),
            "analysis": {
                "hypothesis_accuracy": self._calc_accuracy(initial_hypotheses, outcomes),
                "efficiency_score": efficiency,
                "critical_path_bottlenecks": mission.get('bottlenecks', []),
                "serendipitous_discoveries": mission.get('serendipity', []),
            },
            "extracted_lesson": self._synthesize_lesson(mission)
        }
        
        return retrospective

    def _calc_accuracy(self, hypotheses, outcomes):
        # Compares predicted outcomes to actuals
        matches = 0
        for h_id, h_val in hypotheses.items():
            if outcomes.get(h_id) == "verified":
                matches += 1
        return matches / len(hypotheses) if hypotheses else 0

    def _synthesize_lesson(self, mission):
        # Heuristic for turning a mission into a general principle
        if mission.get('status') == 'success':
            return "Pattern: [Specific Strategy] -> [Positive Outcome]. Candidate for Cognitive Template."
        return "Pattern: [Failure Mode] -> [Negative Outcome]. Candidate for Logic Stress Tester."

if __name__ == "__main__":
    # Basic self-test
    engine = PMREngine()
    print("PMR Engine initialized successfully.")
