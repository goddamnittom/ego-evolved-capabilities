import json
import time
from datetime import datetime, timedelta

class StabilityWatchdog:
    def __init__(self, manifest_path='/root/hardening_manifest.json'):
        self.manifest_path = manifest_path
        self.stability_window_days = 7

    def load_manifest(self):
        try:
            with open(self.manifest_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_manifest(self, manifest):
        with open(self.manifest_path, 'w') as f:
            json.dump(manifest, f, indent=4)

    def audit_stability(self):
        manifest = self.load_manifest()
        report = []
        now = datetime.now()

        for asset, data in manifest.items():
            if data.get('status') == 'VERIFIED':
                verified_at_str = data.get('verified_at')
                if verified_at_str:
                    verified_at = datetime.fromisoformat(verified_at_str)
                    expiry = verified_at + timedelta(days=self.stability_window_days)
                    
                    if now < expiry:
                        days_left = (expiry - now).days
                        report.append({
                            "asset": asset,
                            "state": "MONITORING",
                            "days_remaining": days_left,
                            "risk": "Low (Cool-down)"
                        })
                    else:
                        report.append({
                            "asset": asset,
                            "state": "STABLE",
                            "days_remaining": 0,
                            "risk": "Minimal"
                        })
        
        return report

if __name__ == "__main__":
    swg = StabilityWatchdog()
    print(json.dumps(swg.audit_stability(), indent=2))
