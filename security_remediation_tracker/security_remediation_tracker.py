import json
import os

STATE_FILE = '/root/security_remediation_state.json'

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"incidents": {}}
    return {"incidents": {}}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=4)

def create_incident(incident_id, steps):
    state = load_state()
    state["incidents"][incident_id] = {
        "status": "active",
        "steps": {step: "pending" for step in steps},
        "updated_at": None
    }
    save_state(state)
    return f"Incident {incident_id} created with {len(steps)} steps."

def update_step(incident_id, step, status="completed"):
    state = load_state()
    if incident_id in state["incidents"] and step in state["incidents"][incident_id]["steps"]:
        state["incidents"][incident_id]["steps"][step] = status
        save_state(state)
        return f"Step '{step}' updated to {status}."
    return "Incident or step not found."

def get_status(incident_id):
    state = load_state()
    return state["incidents"].get(incident_id, "Incident not found.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 security_remediation_tracker.py [create|update|status] ...")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "create":
        if len(sys.argv) < 3:
            print("Error: incident_id required")
            sys.exit(1)
        inc_id = sys.argv[2]
        steps = sys.argv[3:]
        print(create_incident(inc_id, steps))
    elif cmd == "update":
        if len(sys.argv) < 4:
            print("Error: incident_id and step required")
            sys.exit(1)
        print(update_step(sys.argv[2], sys.argv[3]))
    elif cmd == "status":
        if len(sys.argv) < 3:
            print("Error: incident_id required")
            sys.exit(1)
        print(json.dumps(get_status(sys.argv[2]), indent=2))
