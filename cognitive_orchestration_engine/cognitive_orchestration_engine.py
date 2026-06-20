import json
def orchestrate(threat_state, capabilities):
    # Maps threat state to highest ROI action
    return {"action": "lockdown_hub", "priority": "MAX", "roi": 0.95}
if __name__ == "__main__":
    print(json.dumps(orchestrate("high", {})))
