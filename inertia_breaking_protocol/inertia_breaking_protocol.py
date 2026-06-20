import time
import json
import os

class InertiaBreakingProtocol:
    def __init__(self, state_file="/root/recovery_state.json"):
        self.state_file = state_file
        self.inertia_threshold = 3600 * 24 # 24 hours of stagnation
        
    def get_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {"last_win_timestamp": time.time(), "current_mode": "standard"}

    def save_state(self, state):
        with open(self.state_file, 'w') as f:
            json.dump(state, f)

    def analyze_inertia(self):
        state = self.get_state()
        now = time.time()
        elapsed = now - state.get("last_win_timestamp", now)
        
        if elapsed > self.inertia_threshold:
            return "IBP_MODE", elapsed
        return "STANDARD_MODE", elapsed

    def get_micro_commitment(self, asset_type="financials"):
        # Define the absolute smallest possible steps to break paralysis
        commitments = {
            "financials": [
                "Just find the banking app on your phone.",
                "Open the app and look at the login screen.",
                "Confirm you remember your username.",
                "Enter your password just to see if it still works."
            ],
            "identities": [
                "Open your browser and go to the account security page.",
                "Check if you are still logged in.",
                "Locate the 'Change Password' button."
            ]
        }
        # In a real scenario, we'd track which commitment we are on.
        # For this demo, we return the first one to initiate the 'onramp'.
        return commitments.get(asset_type, ["Take a deep breath."])[0]

if __name__ == "__main__":
    ibp = InertiaBreakingProtocol()
    mode, elapsed = ibp.analyze_inertia()
    print(f"Mode: {mode}, Elapsed: {elapsed}")
    if mode == "IBP_MODE":
        print(f"Suggested Micro-Commitment: {ibp.get_micro_commitment()}")
