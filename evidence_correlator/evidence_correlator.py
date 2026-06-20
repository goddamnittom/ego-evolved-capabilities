import json
import os
from datetime import datetime

class EvidenceCorrelator:
    def __init__(self, storage_path="/root/evidence_bundles.json"):
        self.storage_path = storage_path
        self.bundles = self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {}

    def _save(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.bundles, f, indent=2)

    def bundle_evidence(self, event_id, log_text=None, screenshot_path=None, metadata=None):
        """
        Links textual logs and visual screenshots to a single event identifier.
        """
        self.bundles[event_id] = {
            "timestamp": datetime.now().isoformat(),
            "log_text": log_text,
            "screenshot_path": screenshot_path,
            "metadata": metadata or {},
            "verified": False
        }
        self._save()
        return f"Evidence bundled for event {event_id}"

    def get_bundle(self, event_id):
        return self.bundles.get(event_id, "No bundle found for this event ID.")

    def list_bundles(self):
        return list(self.bundles.keys())

    def verify_bundle(self, event_id):
        if event_id in self.bundles:
            self.bundles[event_id]["verified"] = True
            self._save()
            return f"Event {event_id} verified."
        return "Event not found."

if __name__ == "__main__":
    # Basic CLI test
    ec = EvidenceCorrelator()
    print(ec.bundle_evidence("evt_001", "Failed login attempt from 1.2.3.4", "/root/screenshots/login_fail.jpg", {"severity": "medium"}))
    print(ec.list_bundles())
