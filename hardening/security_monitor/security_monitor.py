import re
from datetime import datetime, timedelta

class SecurityMonitor:
    """
    Security Threat Heuristic Monitor (STHM)
    Analyzes message patterns to identify potential account takeovers or phishing.
    """
    def __init__(self):
        self.threat_patterns = {
            "OTP_FLOOD": {
                "pattern": r"(verification code|OTP|code is):?\s*\d+",
                "threshold": 3, # 3 or more OTPs in a short window
                "severity": "HIGH",
                "message": "Multiple verification codes detected. Possible account takeover attempt."
            },
            "SECURITY_ALERT": {
                "pattern": r"(security alert|unauthorized access|new login|password changed)",
                "threshold": 1,
                "severity": "MEDIUM",
                "message": "Security alert detected in communications."
            },
            "PHISHING_URGENCY": {
                "pattern": r"(act now|urgent|account suspended|verify immediately|last warning)",
                "threshold": 1,
                "severity": "MEDIUM",
                "message": "Urgency-based phishing language detected."
            }
        }

    def analyze(self, messages):
        """
        Analyzes a list of messages. 
        messages: list of dicts {'text': '...', 'timestamp': '...'}
        """
        alerts = []
        counts = {k: 0 for k in self.threat_patterns}
        
        for msg in messages:
            text = msg.get('text', '').lower()
            for threat, data in self.threat_patterns.items():
                if re.search(data['pattern'], text):
                    counts[threat] += 1
        
        for threat, count in counts.items():
            if count >= self.threat_patterns[threat]['threshold']:
                alerts.append({
                    "threat": threat,
                    "severity": self.threat_patterns[threat]['severity'],
                    "message": self.threat_patterns[threat]['message'],
                    "occurrences": count
                })
                
        return alerts

if __name__ == "__main__":
    # Test case
    monitor = SecurityMonitor()
    test_msgs = [
        {'text': 'Your Plaid verification code is: 123456'},
        {'text': 'Your Plaid verification code is: 654321'},
        {'text': 'Your Plaid verification code is: 111222'},
        {'text': 'This is a copy of a security alert sent to thomas'},
    ]
    print(monitor.analyze(test_msgs))
