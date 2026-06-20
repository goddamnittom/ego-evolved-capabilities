import json
import os
from datetime import datetime

MIRROR_FILE = "/root/tactical_alignment_mirror.json"

def initialize_mirror(north_star, current_objective):
    data = {
        "north_star": north_star,
        "current_objective": current_objective,
        "history": [],
        "last_updated": datetime.now().isoformat()
    }
    save_mirror(data)
    return f"Mirror initialized. North Star: {north_star}"

def update_objective(new_objective):
    data = load_mirror()
    data["current_objective"] = new_objective
    data["last_updated"] = datetime.now().isoformat()
    save_mirror(data)
    return f"Objective updated to: {new_objective}"

def log_action(action, result, alignment_score=1.0):
    """
    alignment_score: 1.0 = perfect alignment, 0.0 = complete drift.
    """
    data = load_mirror()
    entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "result": result,
        "alignment_score": alignment_score
    }
    data["history"].append(entry)
    data["last_updated"] = datetime.now().isoformat()
    save_mirror(data)
    
    if alignment_score < 0.5:
        return "WARNING: Tactical Drift Detected. Alignment score low. Immediate strategic re-evaluation recommended."
    return "Action logged. Alignment maintained."

def get_status():
    data = load_mirror()
    return json.dumps(data, indent=2)

def load_mirror():
    if not os.path.exists(MIRROR_FILE):
        return {"north_star": "None", "current_objective": "None", "history": []}
    with open(MIRROR_FILE, "r") as f:
        return json.load(f)

def save_mirror(data):
    with open(MIRROR_FILE, "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 tactical_alignment_mirror.py [init|update|log|status] ...")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "init":
        print(initialize_mirror(sys.argv[2], sys.argv[3]))
    elif cmd == "update":
        print(update_objective(sys.argv[2]))
    elif cmd == "log":
        # action, result, score
        print(log_action(sys.argv[2], sys.argv[3], float(sys.argv[4]) if len(sys.argv) > 4 else 1.0))
    elif cmd == "status":
        print(get_status())
