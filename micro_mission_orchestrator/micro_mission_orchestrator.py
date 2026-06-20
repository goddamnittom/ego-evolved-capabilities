import json
import os

class MicroMissionOrchestrator:
    def __init__(self, state_file='/root/mmo_state.json'):
        self.state_file = state_file
        self.state = self._load_state()

    def _load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {"current_mission_set": None, "current_step": 0, "completed_steps": []}

    def _save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f)

    def define_mission_set(self, set_id, steps):
        """
        Defines a sequence of micro-tasks for a specific asset.
        steps: List of strings describing the atomic action.
        """
        self.state["current_mission_set"] = set_id
        self.state["steps"] = steps
        self.state["current_step"] = 0
        self.state["completed_steps"] = []
        self._save_state()

    def get_next_step(self):
        if not self.state.get("steps"):
            return None
        
        step_idx = self.state["current_step"]
        if step_idx >= len(self.state["steps"]):
            return "MISSION_COMPLETE"
        
        return self.state["steps"][step_idx]

    def complete_step(self):
        if not self.state.get("steps"):
            return False
        
        step_idx = self.state["current_step"]
        if step_idx < len(self.state["steps"]):
            self.state["completed_steps"].append(step_idx)
            self.state["current_step"] += 1
            self._save_state()
            return True
        return False

    def get_progress(self):
        total = len(self.state.get("steps", []))
        done = len(self.state["completed_steps"])
        return (done / total) if total > 0 else 0

if __name__ == "__main__":
    mmo = MicroMissionOrchestrator()
    # Example setup for Financials Double-Lock
    financials_steps = [
        "Open your primary bank app/website.",
        "Navigate to 'Security' or 'Account Settings'.",
        "Find 'Active Sessions' or 'Logged in Devices'.",
        "Log out of ALL sessions except the current one.",
        "Change your password to a fresh, unique 16+ character string.",
        "Verify that 2FA is active and linked to a hardware key or authenticator app (not SMS).",
        "Check for any new 'Recovery Emails' or 'Backup Phones' added by an attacker."
    ]
    mmo.define_mission_set("financials_double_lock", financials_steps)
    print(f"Mission set initialized. Next step: {mmo.get_next_step()}")
