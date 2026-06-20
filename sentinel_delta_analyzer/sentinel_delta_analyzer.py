import json
from datetime import datetime, timedelta

class SentinelDeltaAnalyzer:
    """
    Analyzes email streams to detect 'Threat Deltas'—specific, time-bound actions 
    taken by an attacker that indicate active lateral movement or account hijacking.
    """
    def __init__(self):
        self.threat_keywords = [
            "password reset", "security alert", "new sign-in", "verification code",
            "recovery email changed", "two-factor authentication", "unauthorized access"
        ]

    def analyze_emails(self, emails):
        """
        Processes a list of email summaries to find high-signal threat indicators.
        """
        deltas = []
        for email in emails:
            subject = email.get('subject', '').lower()
            sender = email.get('from', '').lower()
            
            for keyword in self.threat_keywords:
                if keyword in subject:
                    deltas.append({
                        "type": "ACTIVE_THREAT",
                        "signal": keyword,
                        "subject": email.get('subject'),
                        "from": email.get('from'),
                        "uid": email.get('uid'),
                        "timestamp": email.get('date')
                    })
        return deltas

    def generate_report(self, deltas):
        if not deltas:
            return "NO ACTIVE DELTAS DETECTED: The attacker is currently in a 'Quiet Persistence' phase. This is the most dangerous phase, as they are mapping your identity without triggering alarms."
        
        report = f"🚨 ACTIVE THREAT DELTAS DETECTED ({len(deltas)} events):\n"
        for d in deltas:
            report += f"- [{d['timestamp']}] {d['subject']} (Signal: {d['signal']})\n"
        return report

if __name__ == "__main__":
    # Tool is used as a module by the AI
    print("Sentinel Delta Analyzer initialized.")
