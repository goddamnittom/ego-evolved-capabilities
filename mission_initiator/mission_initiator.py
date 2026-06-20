import json
import os
from datetime import datetime

SOTA_PATH = "/root/knowledge_base/sota_signals.json"
MISSIONS_PATH = "/root/missions/active_missions.json"

def load_json(path):
    if os.path.exists(path):
        with open(path, 'r') as f: return json.load(f)
    return {}

def save_json(path, data):
    with open(path, 'w') as f: json.dump(data, f, indent=2)

def analyze_and_initiate():
    signals = load_json(SOTA_PATH)
    missions = load_json(MISSIONS_PATH)
    
    # Find unprocessed high-value signals
    for sid, data in signals.items():
        if not data.get("processed"):
            # Logic for 'Opportunity Scanning' (OSE)
            # If signal contains keywords like 'transformer', 'reasoning', 'agency' -> Start Mission
            keywords = ["transformer", "agency", "reasoning", "efficiency", "SOTA"]
            if any(k in data["title"].lower() for k in keywords):
                mission_id = f"mission_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                missions[mission_id] = {
                    "title": f"SOTA Integration: {data['title']}",
                    "source_signal": sid,
                    "status": "INITIATED",
                    "blueprint": "TBD",
                    "timestamp": datetime.now().isoformat()
                }
                signals[sid]["processed"] = True
                print(f"Autonomous Mission Initiated: {mission_id}")

    save_json(SOTA_PATH, signals)
    save_json(MISSIONS_PATH, missions)

if __name__ == "__main__":
    analyze_and_initiate()
