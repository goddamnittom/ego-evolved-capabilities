import json
import os

class RemediationStateGuardrail:
    def __init__(self, manifest_path='/root/hardening_manifest.json'):
        self.manifest_path = manifest_path
        self.guardrails = {}

    def set_guardrail(self, asset_id, expected_state):
        """Define the 'Golden State' for an asset."""
        self.guardrails[asset_id] = expected_state
        self._save_guardrails()

    def audit_state(self, asset_id, current_state):
        """Compare current signal against the Golden State."""
        if asset_id not in self.guardrails:
            return {"status": "UNKNOWN", "drift": False}
        
        expected = self.guardrails[asset_id]
        drift = expected != current_state
        return {
            "status": "VERIFIED" if not drift else "DRIFT_DETECTED",
            "drift": drift,
            "expected": expected,
            "actual": current_state
        }

    def _save_guardrails(self):
        with open('/root/guardrail_states.json', 'w') as f:
            json.dump(self.guardrails, f, indent=4)

    def load_guardrails(self):
        if os.path.exists('/root/guardrail_states.json'):
            with open('/root/guardrail_states.json', 'r') as f:
                self.guardrails = json.load(f)

# Example usage for the agent's internal logic
if __name__ == "__main__":
    rsg = RemediationStateGuardrail()
    # Simulate setting a guardrail for the Browser Vault
    rsg.set_guardrail("browser_vault", "MFA_HARDWARE_KEY_ONLY")
    # Simulate a drift signal (e.g., a notification that MFA was disabled)
    result = rsg.audit_state("browser_vault", "MFA_DISABLED")
    print(json.dumps(result, indent=2))
