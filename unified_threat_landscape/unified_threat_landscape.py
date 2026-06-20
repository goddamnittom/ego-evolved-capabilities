import json

class UnifiedThreatLandscape:
    def __init__(self):
        self.assets = {
            "Identity_Hub": {"status": "Vulnerable", "risk": 0.95, "priority": "CRITICAL", "dependencies": ["Gmail", "MS_Account", "Mozilla"]},
            "Dev_Tools": {"status": "In_Progress", "risk": 0.45, "priority": "HIGH", "dependencies": ["GitHub", "Composio"]},
            "Personal_Data": {"status": "Unknown", "risk": 0.30, "priority": "MEDIUM", "dependencies": []},
            "Financials": {"status": "Hardened", "risk": 0.10, "priority": "LOW", "dependencies": []}
        }
        self.active_signals = []
        self.global_perimeter_integrity = 0.33

    def update_asset(self, asset, status, risk):
        if asset in self.assets:
            self.assets[asset]["status"] = status
            self.assets[asset]["risk"] = risk

    def add_signal(self, signal):
        self.active_signals.append(signal)

    def synthesize(self):
        return {
            "perimeter_integrity": self.global_perimeter_integrity,
            "critical_path": "Identity_Hub",
            "assets": self.assets,
            "signals": self.active_signals,
            "recommendation": "Immediate transition to Identity Lockdown to collapse the attacker's primary session vault."
        }

if __name__ == "__main__":
    utl = UnifiedThreatLandscape()
    print(json.dumps(utl.synthesize(), indent=2))
