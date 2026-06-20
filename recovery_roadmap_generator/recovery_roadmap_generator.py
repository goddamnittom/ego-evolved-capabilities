import json
import datetime

class RecoveryRoadmapGenerator:
    def __init__(self):
        self.phases = {
            "Phase 1: Immediate Eradication (Hour 0-2)": [
                "Execute Kill-Switch: Master Password change, App Password deletion, Device sign-out.",
                "Secure Recovery Methods: Update recovery phone and email; enable Hardware 2FA if possible.",
                "Identify the Entry Point: Audit last 10 sign-in events for anomalous IPs/locations."
            ],
            "Phase 2: Triage & Stabilization (Hour 2-24)": [
                "Run Priority Filter: Identify critical financial or security alerts buried in noise.",
                "Audit Forwarding Rules: Delete any unknown filters or forwarding addresses.",
                "Contact Critical Institutions: Notify banks or high-value accounts of the breach."
            ],
            "Phase 3: Reputation Management (Day 1-3)": [
                "Run Collateral Damage Estimator: Determine which contacts were targeted.",
                "Send 'Compromised Account' warning to affected contacts.",
                "Review Sent folder for malicious links sent in user's name."
            ],
            "Phase 4: Long-term Hardening (Day 3-7)": [
                "Perform full device malware scan (since password was leaked).",
                "Rotate passwords for all accounts using the same/similar credentials.",
                "Set up continuous monitoring alerts for account access."
            ]
        }

    def generate_plan(self, breach_severity="CATASTROPHIC"):
        # Adjusts plan based on severity
        plan = {
            "generated_at": str(datetime.datetime.utcnow()),
            "severity": breach_severity,
            "roadmap": self.phases
        }
        return plan

# Initializing for the current disaster
roadmap_gen = RecoveryRoadmapGenerator()
print(json.dumps(roadmap_gen.generate_plan(), indent=4))
