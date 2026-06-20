import json
import os
from datetime import datetime

DATA_FILE = "/root/bleed_rate_data.json"

def update_and_calculate_rate(current_count):
    now = datetime.now().isoformat()
    
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"last_count": current_count, "last_time": now}, f)
        return "Baseline established. Monitoring bleed rate..."

    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    
    last_count = data["last_count"]
    last_time = datetime.fromisoformat(data["last_time"])
    
    delta_count = current_count - last_count
    delta_time = (datetime.now() - last_time).total_seconds() / 3600 # hours
    
    rate = delta_count / delta_time if delta_time > 0 else 0
    
    with open(DATA_FILE, "w") as f:
        json.dump({"last_count": current_count, "last_time": now}, f)
        
    return {
        "delta": delta_count,
        "rate_per_hour": rate,
        "status": "ACCELERATING" if rate > 10 else "STABLE" if rate <= 0 else "BLEEDING"
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        count = int(sys.argv[1])
        print(json.dumps(update_and_calculate_rate(count)))
    else:
        print("Usage: python3 bleed_rate_monitor.py <current_unread_count>")
