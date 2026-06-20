import json
import os

class DeceptionAssetOrchestrator:
    """
    DAO shifts security from passive detection to proactive entrapment.
    It manages 'Canary Tokens'—fake credentials or files that alert the AI
    the moment they are touched, revealing the attacker's presence.
    """
    def __init__(self, manifest_path='/root/canary_manifest.json'):
        self.manifest_path = manifest_path
        self.load_manifest()

    def load_manifest(self):
        if os.path.exists(self.manifest_path):
            with open(self.manifest_path, 'r') as f:
                self.manifest = json.load(f)
        else:
            self.manifest = {"canaries": [], "alerts": []}

    def save_manifest(self):
        with open(self.manifest_path, 'w') as f:
            json.dump(self.manifest, f, indent=2)

    def deploy_canary(self, asset_name, asset_type, location, trigger_event):
        canary = {
            "id": len(self.manifest["canaries"]) + 1,
            "name": asset_name,
            "type": asset_type,
            "location": location,
            "trigger": trigger_event,
            "status": "ACTIVE",
            "last_checked": None
        }
        self.manifest["canaries"].append(canary)
        self.save_manifest()
        return canary

    def trigger_alert(self, canary_id, timestamp, actor_signal):
        alert = {
            "canary_id": canary_id,
            "timestamp": timestamp,
            "signal": actor_signal,
            "severity": "CRITICAL"
        }
        self.manifest["alerts"].append(alert)
        self.save_manifest()
        return alert

    def get_lure_strategy(self, attacker_profile):
        strategies = {
            "Session Hijacker": ["Fake Session Cookie in Browser", "Dummy Auth Token in ~/.bash_history"],
            "Data Exfiltrator": ["Password_List.txt (Canary)", "Financial_Records_2026.xlsx (Canary)"],
            "Credential Hunter": ["Fake AWS Key in .env", "Dummy API Key in GitHub Gist"]
        }
        return strategies.get(attacker_profile, ["Generic Canary File in /root/"])

if __name__ == "__main__":
    dao = DeceptionAssetOrchestrator()
    print("DAO Initialized. Ready to deploy honey-tokens.")
