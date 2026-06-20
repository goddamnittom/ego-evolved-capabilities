import json
import os
from datetime import datetime

class PerimeterWatchdog:
    """
    Perimeter Watchdog (PWG) monitors for anomalies and unauthorized access 
    attempts on assets currently in the Hardening Verification Manifest (HVM).
    """
    def __init__(self, hvm_path='/root/hardening_manifest.json'):
        self.hvm_path = hvm_path
        self.watch_keywords = [
            "new login", "unauthorized access", "security alert", 
            "password changed", "recovery code", "sign-in attempt"
        ]

    def load_hvm(self):
        if not os.path.exists(self.hvm_path):
            return {}
        with open(self.hvm_path, 'r') as f:
            return json.load(f)

    def scan_evidence(self, evidence_text, asset_id):
        """
        Analyzes a piece of evidence (email/log) for anomalies.
        """
        hvm = self.load_hvm()
        asset = hvm.get(asset_id, {})
        status = asset.get('status', 'PENDING')
        
        # We are specifically looking for threats to PENDING assets
        if status == 'PENDING':
            found_keywords = [k for k in self.watch_keywords if k in evidence_text.lower()]
            if found_keywords:
                return {
                    "alert": True,
                    "severity": "CRITICAL",
                    "message": f"Anomaly detected on PENDING asset {asset_id}: {', '.join(found_keywords)}",
                    "suggested_action": "Elevate to TOP PRIORITY immediately."
                }
        
        return {"alert": False}

    def run_audit(self, incoming_data):
        """
        Runs a batch audit over incoming signals.
        incoming_data: list of tuples (asset_id, text)
        """
        alerts = []
        for asset_id, text in incoming_data:
            result = self.scan_evidence(text, asset_id)
            if result["alert"]:
                alerts.append(result)
        return alerts

if __name__ == "__main__":
    # Simple test case
    pwg = PerimeterWatchdog()
    # Simulate HVM with a pending financial asset
    with open('/root/hardening_manifest.json', 'w') as f:
        json.dump({"financials": {"status": "PENDING", "risk": "High"}}, f)
    
    test_evidence = "Security Alert: A new login was detected from an unknown device in Russia."
    print(pwg.scan_evidence(test_evidence, "financials"))
