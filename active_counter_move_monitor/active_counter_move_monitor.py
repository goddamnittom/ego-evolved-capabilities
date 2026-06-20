import time
from datetime import datetime, timedelta

class ActiveCounterMoveMonitor:
    def __init__(self):
        self.active_recovery_sessions = {}
        self.panic_indicators = [
            "password reset", 
            "security alert", 
            "new device login", 
            "MFA disabled", 
            "recovery email changed"
        ]

    def initiate_monitoring(self, asset_id):
        """Start monitoring for counter-moves during the recovery of a specific asset."""
        self.active_recovery_sessions[asset_id] = {
            "start_time": datetime.now(),
            "status": "VIGILANT",
            "signals_detected": []
        }
        return f"Hyper-Vigilance enabled for {asset_id}. Monitoring for adversarial panic-pivots."

    def scan_signals(self, signals):
        """
        Analyze incoming signals (emails/notifications) for counter-move patterns.
        signals: List of dicts {'timestamp': datetime, 'content': str, 'source': str}
        """
        detections = []
        for asset_id, session in self.active_recovery_sessions.items():
            # Only monitor within a 2-hour window of the recovery action
            if datetime.now() - session["start_time"] > timedelta(hours=2):
                continue

            for signal in signals:
                if any(indicator.lower() in signal['content'].lower() for indicator in self.panic_indicators):
                    # Exclude the signal if it's the actual recovery confirmation
                    if "confirmed" in signal['content'].lower() and asset_id in signal['content'].lower():
                        continue
                        
                    detections.append({
                        "asset": asset_id,
                        "signal": signal,
                        "type": "PANIC_PIVOT_DETECTED",
                        "urgency": "CRITICAL"
                    })
                    session["signals_detected"].append(signal)
        
        return detections

    def evaluate_risk_escalation(self, detections):
        """Determine if the counter-move requires immediate intervention."""
        if not detections:
            return "STABLE"
        
        # If multiple signals occur across different identities during one recovery, it's a coordinated pivot.
        unique_assets = set(d["asset"] for d in detections)
        if len(unique_assets) > 1:
            return "COORDINATED_ATTACK_RESPONSE"
        
        return "ISOLATED_COUNTER_MOVE"

if __name__ == "__main__":
    # Basic test
    acmm = ActiveCounterMoveMonitor()
    print(acmm.initiate_monitoring("Identity Hub"))
    test_signals = [
        {"timestamp": datetime.now(), "content": "Your Mozilla password was reset", "source": "email"},
        {"timestamp": datetime.now(), "content": "New login detected for Google", "source": "notification"}
    ]
    print(acmm.scan_signals(test_signals))
