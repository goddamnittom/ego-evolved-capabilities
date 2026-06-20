import json

def project_threats(unread_count, phase="Persistence"):
    # Heuristics based on typical breach patterns for high-volume noise accounts
    projections = {
        "Identity Theft": {"probability": 0.95 if unread_count > 10000 else 0.6, "impact": "Critical"},
        "Financial Drain": {"probability": 0.75, "impact": "High"},
        "Account Lockout": {"probability": 0.85, "impact": "Critical"},
        "Lateral Movement (Other Accounts)": {"probability": 0.9, "impact": "High"},
        "Recovery Email Hijack": {"probability": 0.8, "impact": "Critical"}
    }
    
    if phase == "Persistence":
        # In persistence phase, lateral movement and recovery hijack are nearly guaranteed
        projections["Lateral Movement (Other Accounts)"]["probability"] = 0.98
        projections["Recovery Email Hijack"]["probability"] = 0.92

    return projections

if __name__ == "__main__":
    results = project_threats(13934)
    print(json.dumps(results, indent=2))
