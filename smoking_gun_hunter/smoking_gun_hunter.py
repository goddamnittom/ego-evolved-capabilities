import json

def hunt_for_smoking_guns(emails):
    # High-impact keywords that trigger loss aversion
    keywords = [
        "password reset", 
        "security alert", 
        "unauthorized login", 
        "recovery email changed", 
        "bank", 
        "payment", 
        "credit card", 
        "verified purchase", 
        "account recovery",
        "new device login"
    ]
    
    evidence = []
    for email in emails:
        subject = email.get('subject', '').lower()
        for kw in keywords:
            if kw in subject:
                evidence.append({
                    'keyword': kw,
                    'subject': email.get('subject'),
                    'uid': email.get('uid'),
                    'date': email.get('date')
                })
    
    # Sort by priority (roughly based on the order of keywords list)
    # In a real scenario, we'd rank by urgency.
    return evidence

if __name__ == "__main__":
    # This script expects a JSON list of emails as input from the AI agent
    import sys
    try:
        input_data = sys.stdin.read()
        emails = json.loads(input_data)
        results = hunt_for_smoking_guns(emails)
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")
