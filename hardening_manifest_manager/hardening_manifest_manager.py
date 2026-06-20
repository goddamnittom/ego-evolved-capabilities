import json
import os

MANIFEST_FILE = '/root/hardening_manifest.json'

def initialize_manifest():
    initial_state = {
        "incident_id": "SEC-2026-05-24",
        "status": "FORTIFICATION",
        "assets": {
            "financials": {
                "risk": "High",
                "actions": ["Password Reset", "MFA Audit", "Transaction Review"],
                "status": "PENDING",
                "verified": False
            },
            "dev_tools": {
                "risk": "Medium",
                "actions": ["API Key Rotation", "SSH Key Audit", "2FA Check"],
                "status": "PENDING",
                "verified": False
            },
            "identities": {
                "risk": "High",
                "actions": ["MS Account Reset", "Mozilla Sync Audit", "Recovery Email Update"],
                "status": "PENDING",
                "verified": False
            }
        }
    }
    with open(MANIFEST_FILE, 'w') as f:
        json.dump(initial_state, f, indent=4)
    return initial_state

def update_asset(asset_id, status, verified=False):
    if not os.path.exists(MANIFEST_FILE):
        initialize_manifest()
    
    with open(MANIFEST_FILE, 'r') as f:
        data = json.load(f)
    
    if asset_id in data['assets']:
        data['assets'][asset_id]['status'] = status
        data['assets'][asset_id]['verified'] = verified
    
    with open(MANIFEST_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    return data

if __name__ == "__main__":
    initialize_manifest()
    print("Hardening Manifest Initialized.")
