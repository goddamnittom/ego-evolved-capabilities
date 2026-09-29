import json
from datetime import datetime

class ThreatTimelineGenerator:
    """
    Generates a chronological timeline of security events to visualize 
    the blast radius and attacker movements.
    """
    def __init__(self):
        self.events = []

    def add_event(self, timestamp, event_type, description, severity="medium"):
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            dt = timestamp # Fallback to string
        
        self.events.append({
            "timestamp": dt,
            "type": event_type,
            "description": description,
            "severity": severity
        })
        self.events.sort(key=lambda x: x['timestamp'] if isinstance(x['timestamp'], datetime) else x['timestamp'])

    def generate_report(self):
        report = "### 🛡️ ATTACK TIMELINE REPORT\n\n"
        for event in self.events:
            ts = event['timestamp'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(event['timestamp'], datetime) else event['timestamp']
            sev_icon = "🔴" if event['severity'] == "high" else "🟡" if event['severity'] == "medium" else "🔵"
            report += f"{sev_icon} **{ts}** | {event['type']} | {event['description']}\n"
        return report

if __name__ == "__main__":
    # Simple test
    ttg = ThreatTimelineGenerator()
    ttg.add_event("2026-04-29T00:12:06Z", "Initial Breach", "First security alert detected", "medium")
    ttg.add_event("2026-05-03T23:58:01Z", "Persistence", "App password created", "high")
    ttg.add_event("2026-05-24T13:21:49Z", "Active Session", "New sign-in detected", "high")
    print(ttg.generate_report())
