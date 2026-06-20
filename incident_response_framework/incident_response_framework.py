import json
import os
from datetime import datetime

class IncidentResponseFramework:
    def __init__(self, incident_file="/root/security_incidents.json"):
        self.incident_file = incident_file
        self.incidents = self._load_incidents()

    def _load_incidents(self):
        if os.path.exists(self.incident_file):
            with open(self.incident_file, 'r') as f:
                return json.load(f)
        return {}

    def create_incident(self, incident_id, threat_type, description):
        self.incidents[incident_id] = {
            "start_time": datetime.now().isoformat(),
            "threat_type": threat_type,
            "description": description,
            "evidence": [],
            "remediation_steps": [],
            "status": "OPEN",
            "blast_radius": []
        }
        self._save()
        return f"Incident {incident_id} created: {threat_type}"

    def add_evidence(self, incident_id, evidence_text, source):
        if incident_id in self.incidents:
            self.incidents[incident_id]["evidence"].append({
                "timestamp": datetime.now().isoformat(),
                "source": source,
                "text": evidence_text
            })
            self._save()

    def add_to_blast_radius(self, incident_id, account):
        if incident_id in self.incidents:
            if account not in self.incidents[incident_id]["blast_radius"]:
                self.incidents[incident_id]["blast_radius"].append(account)
                self._save()

    def update_status(self, incident_id, status):
        if incident_id in self.incidents:
            self.incidents[incident_id]["status"] = status
            self._save()

    def _save(self):
        with open(self.incident_file, 'w') as f:
            json.dump(self.incidents, f, indent=4)

    def get_incident_report(self, incident_id):
        return self.incidents.get(incident_id, "Incident not found")

if __name__ == "__main__":
    irf = IncidentResponseFramework()
    print("Incident Response Framework initialized.")
