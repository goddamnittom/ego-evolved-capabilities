import json
import datetime
from collections import Counter

class CollateralDamageEstimator:
    def __init__(self):
        self.spam_indicators = ["winner", "lottery", "crypto", "urgent", "click here", "inheritance", "investment"]
        self.damage_weights = {
            "volume_high": 40,        # Mass spamming
            "diversity_high": 30,     # Wide reach of contacts
            "content_malicious": 30,  # Phishing/Scams
        }

    def estimate_damage(self, sent_emails):
        """
        Analyzes sent emails to estimate reputation damage.
        sent_emails: List of dicts with {'to': ..., 'subject': ..., 'body': ...}
        """
        if not sent_emails:
            return {"score": 0, "status": "No damage detected", "report": "No sent mail analyzed."}

        total_sent = len(sent_emails)
        unique_recipients = len(set([e.get('to', '') for e in sent_emails]))
        
        # Content Analysis
        malicious_count = 0
        for e in sent_emails:
            text = f"{e.get('subject', '')} {e.get('body', '')}".lower()
            if any(indicator in text for indicator in self.spam_indicators):
                malicious_count += 1
        
        # Scoring
        score = 0
        reasons = []
        
        if total_sent > 100:
            score += self.damage_weights["volume_high"]
            reasons.append(f"High volume of sent mail ({total_sent} messages)")
        
        if unique_recipients > 50:
            score += self.damage_weights["diversity_high"]
            reasons.append(f"Broad recipient reach ({unique_recipients} unique addresses)")
            
        if malicious_count > 0:
            score += self.damage_weights["content_malicious"]
            reasons.append(f"Detected {malicious_count} messages with spam indicators")

        status = "LOW"
        if score >= 70: status = "CATASTROPHIC"
        elif score >= 40: status = "HIGH"
        elif score >= 10: status = "MODERATE"
        
        return {
            "score": score,
            "status": status,
            "metrics": {
                "total_sent": total_sent,
                "unique_recipients": unique_recipients,
                "malicious_content": malicious_count
            },
            "report": " | ".join(reasons) if reasons else "No significant damage indicators found."
        }

# Example usage
estimator = CollateralDamageEstimator()
# Mock data for testing
mock_sent = [
    {"to": "victim1@example.com", "subject": "You won!", "body": "Click here for your lottery prize"},
    {"to": "victim2@example.com", "subject": "Urgent", "body": "Investment opportunity"},
    {"to": "friend@example.com", "subject": "Hey", "body": "How are you?"}
]
print(json.dumps(estimator.estimate_damage(mock_sent), indent=2))
