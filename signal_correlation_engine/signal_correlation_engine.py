import json
from datetime import datetime, timedelta

class SignalCorrelationEngine:
    def __init__(self):
        self.patterns = {
            "ACCOUNT_TAKEOVER_SEQUENCE": {
                "signals": ["PASSWORD_RESET", "NEW_DEVICE_LOGIN"],
                "window_minutes": 30,
                "severity": "CRITICAL"
            },
            "STEALTH_EXFILTRATION": {
                "signals": ["LOGIN_SUCCESS", "EMAIL_FORWARDING_ENABLED"],
                "window_minutes": 60,
                "severity": "HIGH"
            },
            "COORDINATED_ATTACK": {
                "signals": ["SECURITY_ALERT_A", "SECURITY_ALERT_B"],
                "window_minutes": 15,
                "severity": "HIGH"
            }
        }

    def correlate(self, events):
        """
        events: List of dicts { "type": str, "timestamp": datetime, "source": str }
        """
        findings = []
        sorted_events = sorted(events, key=lambda x: x['timestamp'])
        
        for pattern_name, details in self.patterns.items():
            required_signals = details["signals"]
            window = details["window_minutes"]
            
            for i in range(len(sorted_events)):
                for j in range(i + 1, len(sorted_events)):
                    e1 = sorted_events[i]
                    e2 = sorted_events[j]
                    
                    time_diff = (e2['timestamp'] - e1['timestamp']).total_seconds() / 60
                    if time_diff > window:
                        break
                    
                    # Check if these two events match a known malicious pattern
                    if e1['type'] == required_signals[0] and e2['type'] == required_signals[1]:
                        findings.append({
                            "pattern": pattern_name,
                            "severity": details["severity"],
                            "events": [e1, e2],
                            "confidence": "High"
                        })
        return findings

if __name__ == "__main__":
    # Test Case
    sce = SignalCorrelationEngine()
    test_events = [
        {"type": "PASSWORD_RESET", "timestamp": datetime.now() - timedelta(minutes=10), "source": "Gmail"},
        {"type": "NEW_DEVICE_LOGIN", "timestamp": datetime.now() - timedelta(minutes=2), "source": "BankX"}
    ]
    print(json.dumps(sce.correlate(test_events), indent=2, default=str))
