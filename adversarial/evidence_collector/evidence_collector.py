import json
import os

MANIFEST_PATH = '/root/hardening_manifest.json'
EVIDENCE_PATH = '/root/evidence_manifest.json'

# Define what constitutes "Evidence" for each asset type
REQUIRED_EVIDENCE = {
    "Financials": [
        "Password change timestamp verified in security settings",
        "Review of last 30 days of transactions for unauthorized activity",
        "Multi-factor authentication (MFA) confirmed as 'On' and using an authenticator app (not SMS)"
    ],
    "Identities": [
        "Microsoft: Recovery email and phone number verified and up-to-date",
        "Mozilla: Sync password changed and active sessions audited",
        "Global: 2FA enabled on all primary identity providers"
    ],
    "Dev Tools": [
        "GitHub: Audit of SSH keys; any unknown keys removed",
        "Composio: API keys rotated and old keys revoked",
        "Local: SSH keys regenerated if there was any doubt of local machine compromise"
    ]
}

def init_evidence_store():
    evidence_store = {}
    # Initialize store based on current manifest assets
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, 'r') as f:
            manifest = json.load(f)
            for asset in manifest.keys():
                evidence_store[asset] = {
                    "requirements": REQUIRED_EVIDENCE.get(asset, ["General security audit performed"]),
                    "provided": {},
                    "status": "UNVERIFIED"
                }
    
    with open(EVIDENCE_PATH, 'w') as f:
        json.dump(evidence_store, f, indent=4)
    return evidence_store

def record_evidence(asset, requirement, evidence_text):
    if not os.path.exists(EVIDENCE_PATH):
        init_evidence_store()
        
    with open(EVIDENCE_PATH, 'r') as f:
        store = json.load(f)
    
    if asset in store:
        store[asset]["provided"][requirement] = evidence_text
        # Check if all requirements are met
        if all(req in store[asset]["provided"] for req in store[asset]["requirements"]):
            store[asset]["status"] = "VERIFIED"
            
    with open(EVIDENCE_PATH, 'w') as f:
        json.dump(store, f, indent=4)
    return store[asset]["status"]

if __name__ == "__main__":
    print("Initializing Evidence-Based Verification Protocol (EVBP)...")
    store = init_evidence_store()
    print(f"Evidence store initialized for assets: {list(store.keys())}")
