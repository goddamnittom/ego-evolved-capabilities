import json
import os
from datetime import datetime

class LifeStateOrchestrator:
    def __init__(self, state_file='/root/life_state.json', manifest_file='/root/user_strategic_manifest.json'):
        self.state_file = state_file
        self.manifest_file = manifest_file
        self.state = self._load_state()

    def _load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {"events": [], "conflicts": [], "active_narratives": {}}

    def save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def ingest_signal(self, source, content, timestamp, sender):
        """
        Ingests a signal from SMS, Email, or Notification and maps it to a life event.
        """
        event = {
            "id": len(self.state["events"]),
            "source": source,
            "content": content,
            "timestamp": timestamp,
            "sender": sender,
            "category": "unknown",
            "priority": "medium",
            "status": "active"
        }
        # Simple category mapping
        if any(kw in content.lower() for kw in ["bill", "payment", "invoice", "medical"]):
            event["category"] = "finance/health"
        elif any(kw in content.lower() for kw in ["meeting", "call", "zoom", "schedule"]):
            event["category"] = "scheduling"
        elif any(kw in content.lower() for kw in ["urgent", "help", "emergency", "shit", "crisis"]):
            event["category"] = "urgent_personal"
            event["priority"] = "high"
        
        self.state["events"].append(event)
        self._detect_conflicts()
        self.save_state()
        return event

    def _detect_conflicts(self):
        """
        Analyzes events for temporal or logical contradictions.
        """
        self.state["conflicts"] = []
        # Placeholder for complex logic: identify events with same category/sender 
        # but contradictory content or overlapping times.
        # For now, we flag high-priority personal events as 'critical nodes'.
        for e in self.state["events"]:
            if e["category"] == "urgent_personal":
                self.state["conflicts"].append({
                    "type": "EMOTIONAL_DISTRESS",
                    "event_id": e["id"],
                    "severity": "critical",
                    "description": f"High distress signal from {e['sender']}"
                })

    def get_summary(self):
        return {
            "total_events": len(self.state["events"]),
            "critical_conflicts": len(self.state["conflicts"]),
            "conflicts": self.state["conflicts"]
        }

if __name__ == "__main__":
    lso = LifeStateOrchestrator()
    print("LSO initialized. Ready to map life signals to strategic state.")
