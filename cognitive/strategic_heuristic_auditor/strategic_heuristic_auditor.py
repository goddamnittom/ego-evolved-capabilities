import json
import os
from datetime import datetime

class StrategicHeuristicAuditor:
    def __init__(self, storage_path="/root/strategic_audit_log.json"):
        self.storage_path = storage_path
        self.logs = self._load_logs()

    def _load_logs(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return []

    def log_hypothesis(self, strategy_id, predicted_outcome, confidence, metrics):
        entry = {
            "strategy_id": strategy_id,
            "timestamp": datetime.now().isoformat(),
            "predicted_outcome": predicted_outcome,
            "confidence": confidence,
            "expected_metrics": metrics,
            "actual_outcome": None,
            "accuracy_delta": None,
            "status": "PENDING"
        }
        self.logs.append(entry)
        self._save_logs()
        return entry

    def resolve_hypothesis(self, strategy_id, actual_outcome, actual_metrics):
        for entry in self.logs:
            if entry["strategy_id"] == strategy_id:
                entry["actual_outcome"] = actual_outcome
                entry["actual_metrics"] = actual_metrics
                entry["status"] = "RESOLVED"
                
                # Simple delta calculation (Difference between expected and actual)
                delta = 0
                for k, v in entry["expected_metrics"].items():
                    if k in actual_metrics:
                        delta += abs(v - actual_metrics[k])
                
                entry["accuracy_delta"] = delta
                break
        self._save_logs()

    def _save_logs(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.logs, f, indent=2)

    def get_strategic_accuracy(self):
        resolved = [e for e in self.logs if e["status"] == "RESOLVED"]
        if not resolved:
            return 1.0
        total_delta = sum(e["accuracy_delta"] for e in resolved)
        return 1.0 / (1.0 + total_delta)

if __name__ == "__main__":
    sha = StrategicHeuristicAuditor()
    print(f"Current Strategic Accuracy: {sha.get_strategic_accuracy()}")
