import json
import os
from datetime import datetime

class StrategicIntelligenceDashboard:
    def __init__(self):
        self.paths = {
            "telemetry": "/root/mission_control_telemetry.json",
            "alignment": "/root/strategic_alignment_matrix.json",
            "capabilities": "/root/cognitive_schema_exporter.json", # Assuming CSE exports here
            "audit": "/root/audit_logs/execution_audit.log"
        }

    def _load_json(self, key):
        path = self.paths.get(key)
        if path and os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {}

    def synthesize_state(self):
        telemetry = self._load_json("telemetry")
        alignment = self._load_json("alignment")
        capabilities = self._load_json("capabilities")
        
        # Calculate Metrics
        active_missions = len([m for m in telemetry.get("missions", {}).values() if m.get("status") == "ACTIVE"])
        alignment_score = alignment.get("global_alignment_score", 0.0)
        capability_count = len(capabilities.get("modules", {}))
        
        # Determine System Mode based on Alignment and Load
        mode = "OPTIMAL"
        if alignment_score < 0.7:
            mode = "ALIGNMENT_DRIFT"
        elif active_missions > 5:
            mode = "HIGH_LOAD"

        return {
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "active_missions": active_missions,
                "alignment_score": alignment_score,
                "capability_count": capability_count,
                "system_mode": mode
            },
            "strategic_health": "GREEN" if mode == "OPTIMAL" else "YELLOW",
            "recommendation": "Continue current trajectory" if mode == "OPTIMAL" else "Perform Strategic Reset/SDE"
        }

if __name__ == "__main__":
    sid = StrategicIntelligenceDashboard()
    print(json.dumps(sid.synthesize_state(), indent=2))
