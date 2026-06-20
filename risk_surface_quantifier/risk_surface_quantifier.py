import json
def calculate_risk_delta(current_risk, proposed_action):
    # Simplification: Identity Hub reduces risk by 78%
    delta = 0.78 if proposed_action == "identity_lockdown" else 0.12
    return {"risk_reduction": delta, "new_score": current_risk * (1 - delta)}
if __name__ == "__main__":
    print(json.dumps(calculate_risk_delta(1.0, "identity_lockdown")))
