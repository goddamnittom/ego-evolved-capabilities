import json
import os
from datetime import datetime

HVM_PATH = '/root/hardening_manifest.json'

class EvidenceVerificationEngine:
    """
    EVE transitions security verification from trust-based (user claims) 
    to evidence-based (analysis of provided artifacts).
    """
    def __init__(self):
        self.manifest = self._load_manifest()

    def _load_manifest(self):
        if os.path.exists(HVM_PATH):
            try:
                with open(HVM_PATH, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, dict) and "assets" in data:
                        return data
            except json.JSONDecodeError:
                pass
        return {"assets": {}}

    def verify_evidence(self, asset_id, goal, evidence_content):
        """
        Analyzes evidence content against a specific verification goal.
        Returns a confidence score and updates the HVM.
        """
        confidence = "Low"
        evidence_lower = evidence_content.lower()
        
        high_confidence_markers = [
            "successfully changed", "confirmed", "enabled", "active", 
            "reset complete", "verified", "established"
        ]
        medium_confidence_markers = [
            "attempted", "trying", "sent", "received", "opened"
        ]

        if any(marker in evidence_lower for marker in high_confidence_markers):
            confidence = "High"
        elif any(marker in evidence_lower for marker in medium_confidence_markers):
            confidence = "Medium"

        if asset_id not in self.manifest["assets"]:
            self.manifest["assets"][asset_id] = {
                "status": "PENDING", 
                "verifications": [], 
                "last_updated": None
            }
        
        self.manifest["assets"][asset_id]["verifications"].append({
            "timestamp": datetime.now().isoformat(),
            "goal": goal,
            "evidence_snippet": evidence_content[:100],
            "confidence": confidence
        })
        
        current_status = self.manifest["assets"][asset_id].get("status", "PENDING")
        if confidence == "High":
            self.manifest["assets"][asset_id]["status"] = "VERIFIED"
        elif confidence == "Medium" and current_status == "PENDING":
            self.manifest["assets"][asset_id]["status"] = "PARTIALLY_VERIFIED"
            
        self.manifest["assets"][asset_id]["last_updated"] = datetime.now().isoformat()
        self._save_manifest()
        
        return confidence

    def _save_manifest(self):
        with open(HVM_PATH, 'w') as f:
            json.dump(self.manifest, f, indent=2)

if __name__ == "__main__":
    eve = EvidenceVerificationEngine()
    res = eve.verify_evidence("financials_main", "Password Reset", "Your password has been successfully changed.")
    print(f"Verification result: {res}")
