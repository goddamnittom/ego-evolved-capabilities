import json
import os
from datetime import datetime

class MissionControlTelemetry:
    def __init__(self, mission_id="default_mission", storage_path="/root/mission_telemetry.json"):
        self.mission_id = mission_id
        self.storage_path = storage_path
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {
            "mission_id": self.mission_id,
            "start_time": datetime.now().isoformat(),
            "hypotheses": {},
            "dependencies": [],
            "intel_gains": [],
            "confidence_score": 0.0
        }

    def save(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def update_hypothesis(self, hypothesis_id, confidence, evidence_summary):
        self.data["hypotheses"][hypothesis_id] = {
            "confidence": confidence,
            "last_updated": datetime.now().isoformat(),
            "evidence": evidence_summary
        }
        self._recalculate_overall_confidence()
        self.save()

    def add_dependency(self, target_intel, required_by):
        dependency = {"target": target_intel, "required_by": required_by, "status": "pending"}
        self.data["dependencies"].append(dependency)
        self.save()

    def log_intel_gain(self, source, value, weight):
        gain = {
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "value": value,
            "weight": weight
        }
        self.data["intel_gains"].append(gain)
        self.save()

    def _recalculate_overall_confidence(self):
        if not self.data["hypotheses"]:
            self.data["confidence_score"] = 0.0
            return
        
        # Simplified confidence calculation: Average of the top hypothesis confidence
        top_conf = max([h["confidence"] for h in self.data["hypotheses"].values()])
        self.data["confidence_score"] = top_conf

    def get_telemetry_summary(self):
        return self.data

if __name__ == "__main__":
    # Basic test
    mct = MissionControlTelemetry()
    mct.update_hypothesis("h1", 0.65, "GitHub handle matches target pattern")
    mct.log_intel_gain("OSINT", "Confirmed email domain", 0.2)
    print(json.dumps(mct.get_telemetry_summary(), indent=2))
