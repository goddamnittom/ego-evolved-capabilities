import json
import os

class PersistenceAuditEngine:
    def __init__(self, blast_radius_file='/root/blast_radius.json', remediation_log_file='/root/remediation_log.json'):
        self.blast_radius_file = blast_radius_file
        self.remediation_log_file = remediation_log_file

    def load_json(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {}

    def audit_persistence(self):
        blast_radius = self.load_json(self.blast_radius_file)
        remediation = self.load_json(self.remediation_log_file)
        
        # Common persistence vectors in Gmail/Google
        critical_vectors = [
            "app_passwords",
            "active_sessions",
            "master_password",
            "third_party_apps",
            "recovery_email",
            "recovery_phone",
            "email_forwarding_filters",
            "delegated_access"
        ]
        
        findings = []
        completed_steps = remediation.get('completed_steps', [])
        
        for vector in critical_vectors:
            # Check if the vector was part of the blast radius and if it's been remediated
            is_compromised = vector in blast_radius.get('compromised_vectors', [])
            is_remediated = any(vector in step.lower() for step in completed_steps)
            
            if is_compromised and not is_remediated:
                findings.append({
                    "vector": vector,
                    "status": "UNRESOLVED",
                    "risk": "High",
                    "description": f"Persistence via {vector} was identified in blast radius but not marked as remediated."
                })
            elif not is_compromised and not is_remediated:
                # Even if not in blast radius, these are 'blind spots' that should be checked
                findings.append({
                    "vector": vector,
                    "status": "AUDIT_REQUIRED",
                    "risk": "Medium",
                    "description": f"Verify {vector} has not been modified by attacker as a stealth persistence mechanism."
                })
        
        return findings

if __name__ == "__main__":
    engine = PersistenceAuditEngine()
    results = engine.audit_persistence()
    print(json.dumps(results, indent=2))
