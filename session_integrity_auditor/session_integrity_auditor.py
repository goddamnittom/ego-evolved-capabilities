import json
import datetime

class SessionIntegrityAuditor:
    """
    SIA closes the loop between Pivot Prediction (PPE) and Signal Detection.
    It monitors for 'Silent Pivots'—successful unauthorized accesses that
    do not trigger MFA alerts but leave ambient footprints (e.g., 'New Login' emails).
    """
    def __init__(self, ppe_probability=0.0):
        self.ppe_probability = ppe_probability
        self.threat_level = "LOW"

    def analyze_signal(self, signal_type, details):
        # Weight the signal by the PPE probability
        # If PPE predicted an Identity Pivot (1.0), any Identity signal is Critical.
        weight = self.ppe_probability
        
        if signal_type == "NEW_LOGIN":
            score = 0.8 * weight
        elif signal_type == "PASSWORD_CHANGE":
            score = 1.0 * weight
        elif signal_type == "SESS_TOKEN_REFRESH":
            score = 0.6 * weight
        else:
            score = 0.1 * weight

        if score > 0.7:
            self.threat_level = "CRITICAL"
        elif score > 0.4:
            self.threat_level = "ELEVATED"
        else:
            self.threat_level = "LOW"
            
        return {
            "threat_level": self.threat_level,
            "confidence_score": score,
            "action": "IMMEDIATE_LOCKDOWN" if self.threat_level == "CRITICAL" else "MONITOR"
        }

if __name__ == "__main__":
    # Example: PPE says Identity Pivot is highly likely (1.0)
    sia = SessionIntegrityAuditor(ppe_probability=1.0)
    result = sia.analyze_signal("NEW_LOGIN", {"device": "Unknown Linux", "location": "Unknown"})
    print(json.dumps(result))
