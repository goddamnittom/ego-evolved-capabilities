import json
import os
from datetime import datetime

class HardeningAuditIntelligence:
    """
    HAI: Hardening Audit Intelligence
    Moves security verification from 'Trust-Based' to 'Evidence-Based'.
    """
    def __init__(self, manifest_path="/root/hardening_manifest.json"):
        self.manifest_path = manifest_path

    def load_manifest(self):
        if not os.path.exists(self.manifest_path):
            return {}
        with open(self.manifest_path, 'r') as f:
            return json.load(f)

    def save_manifest(self, manifest):
        with open(self.manifest_path, 'w') as f:
            json.dump(manifest, f, indent=4)

    def define_evidence_heuristics(self):
        """
        Defines what constitutes 'evidence' for verification.
        In a real scenario, this would be mapped to email patterns, log entries, etc.
        """
        return {
            "Financials": ["Password changed", "2FA enabled", "Security alert: New device"],
            "Identities": ["Password reset", "Recovery email updated", "Login notification"],
            "Dev Tools": ["API key rotated", "SSH key added", "2FA activated"]
        }

    def audit_evidence(self, asset_id, evidence_text):
        """
        Analyzes provided text (e.g., email body) against heuristics to 
        suggest a verification status change.
        """
        heuristics = self.define_evidence_heuristics()
        asset_type = "Financials" # Default or derived from asset_id
        
        # Simple heuristic match
        for keyword in heuristics.get(asset_type, []):
            if keyword.lower() in evidence_text.lower():
                return True, f"Found evidence: {keyword}"
        
        return False, "No conclusive evidence found."

    def suggest_verification(self, asset_id, evidence_text):
        manifest = self.load_manifest()
        success, reason = self.audit_evidence(asset_id, evidence_text)
        
        if success:
            # Note: We don't auto-verify without user confirmation, but we 'suggest' it.
            return {"status": "SUGGEST_VERIFIED", "reason": reason, "asset": asset_id}
        return {"status": "STILL_PENDING", "reason": reason, "asset": asset_id}

if __name__ == "__main__":
    hai = HardeningAuditIntelligence()
    print("HAI Module Initialized. Ready to audit security evidence.")
