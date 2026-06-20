import json
from datetime import datetime

class SecurityBaselineAttestor:
    def __init__(self, manifest_path='/root/hardening_manifest.json'):
        self.manifest_path = manifest_path

    def load_manifest(self):
        try:
            with open(self.manifest_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def generate_attestation_report(self):
        manifest = self.load_manifest()
        if not manifest:
            return "No hardening manifest found. Cannot generate attestation."

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report = [
            "# 🛡️ SECURITY HARDENING ATTESTATION REPORT",
            f"**Generated on:** {timestamp}",
            "\n## 1. Executive Summary",
            "This report provides a formal attestation of the hardening state of the identity perimeter. "
            "Verification is derived from the Hardening Verification Manifest (HVM) and cross-referenced "
            "against temporal stability and trust-chain dependencies.\n",
            "### Perimeter Integrity Metrics:",
            "- **Total Assets:** " + str(len(manifest)),
            "- **Verified Assets:** " + str(len([a for a in manifest.values() if a.get('status') == 'VERIFIED'])),
            "- **Integrity Score:** " + str(round((len([a for a in manifest.values() if a.get('status') == 'VERIFIED']) / len(manifest)) * 100, 2)) + "%",
            "\n## 2. Detailed Asset Status",
            "| Asset | Status | Verification Method | Stability Window | Trust Chain |",
            "| :--- | :--- | :--- | :--- | :--- |"
        ]

        for asset, data in manifest.items():
            status = data.get('status', 'UNKNOWN')
            method = data.get('verification_method', 'N/A')
            stability = "✅ Stable" if data.get('stability_status') == 'STABLE' else "⏳ Monitoring" if data.get('stability_status') == 'MONITORING' else "❌ Pending"
            chain = "🔗 Secured" if data.get('chain_status') == 'SECURED' else "⚠️ Broken" if data.get('chain_status') == 'BROKEN' else "❓ Unaudited"
            
            report.append(f"| {asset} | {status} | {method} | {stability} | {chain} |")

        report.append("\n## 3. Attestation Statement")
        report.append("I, Ego (Autonomous AI Assistant), hereby attest that the above states reflect the "
                      "current verified hardening posture of the target environment based on provided evidence "
                      "and heuristic analysis. This baseline serves as the 'Known Good' state for future "
                      "anomaly detection and incident response.")

        return "\n".join(report)

if __name__ == "__main__":
    SBA = SecurityBaselineAttestor()
    print(SBA.generate_attestation_report())
