import json
from datetime import datetime

class BehavioralAnomalyDetector:
    """
    Analyzes email metadata and content patterns to identify signs of Account Takeover (ATO)
    and subsequent exploitation (e.g., password spraying, financial fraud, spamming).
    """
    def __init__(self):
        self.threat_indicators = {
            "credential_harvesting": ["password reset", "verify your account", "security code", "unauthorized login"],
            "financial_fraud": ["payment confirmed", "order placed", "invoice", "subscription updated", "wire transfer"],
            "spam_campaign": ["get rich", "urgent offer", "winner", "crypto"],
            "exfiltration": ["forwarding rule", "filter created", "bcc"]
        }

    def analyze_batch(self, emails):
        findings = {category: [] for category in self.threat_indicators}
        findings["general_anomalies"] = []
        
        for email in emails:
            subject = email.get("subject", "").lower()
            sender = email.get("from", "").lower()
            
            for category, keywords in self.threat_indicators.items():
                if any(kw in subject for kw in keywords):
                    findings[category].append(email)
        
        return self.synthesize_report(findings)

    def synthesize_report(self, findings):
        summary = []
        for category, matches in findings.items():
            if matches:
                summary.append(f"🚨 {category.replace('_', ' ').upper()}: {len(matches)} potential indicators found.")
        
        return {
            "risk_level": "CRITICAL" if any(len(v) > 0 for k, v in findings.items() if k != "general_anomalies") else "LOW",
            "summary": summary,
            "recommendation": "Immediate account lockdown required if risk_level is CRITICAL."
        }

if __name__ == "__main__":
    # Prototype test
    detector = BehavioralAnomalyDetector()
    test_emails = [
        {"subject": "Your Amazon order has been shipped", "from": "amazon@email.com"},
        {"subject": "Password reset for your Bank of America account", "from": "boa@email.com"},
        {"subject": "Get rich quick with this crypto bot", "from": "scam@email.com"}
    ]
    print(json.dumps(detector.analyze_batch(test_emails), indent=2))
