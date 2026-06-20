import json
import os
from datetime import datetime, timezone

class FidelityDrivenExecutionRouter:
    """
    FDER: Cognitive Gatekeeper.
    Automates the trust-boundary between simulated resilience (ASSi/SRDA) 
    and real-world empirical evidence (PMR).
    """
    def __init__(self, fidelity_log="/root/srda_fidelity_logs.json", 
                 router_log="/root/fder_routing_decisions.json",
                 threshold=0.75):
        self.fidelity_log = fidelity_log
        self.router_log = router_log
        self.threshold = threshold
        self._ensure_files()

    def _ensure_files(self):
        for f in [self.fidelity_log, self.router_log]:
            if not os.path.exists(f):
                with open(f, "w") as wf:
                    json.dump({}, wf)

    def get_fidelity_score(self, domain):
        """Retrieves the current Simulation Fidelity Score for a given domain."""
        if not os.path.exists(self.fidelity_log):
            return 0.5
        with open(self.fidelity_log, "r") as f:
            try:
                data = json.load(f)
                return data.get(domain, {}).get("fidelity_score", 0.5)
            except json.JSONDecodeError:
                return 0.5

    def route_execution(self, axiom_id, domain, risk_level="Medium"):
        """
        Determines if an axiom can be deployed immediately or requires a Pilot Mission.
        """
        fidelity = self.get_fidelity_score(domain)
        
        requires_pilot = False
        if risk_level == "High" and fidelity < 0.90:
            requires_pilot = True
        elif risk_level == "Medium" and fidelity < self.threshold:
            requires_pilot = True
        elif risk_level == "Low" and fidelity < 0.40:
            requires_pilot = True

        decision_data = {
            "axiom_id": axiom_id,
            "domain": domain,
            "fidelity": fidelity,
            "risk_level": risk_level,
            "decision": "PILOT_MISSION" if requires_pilot else "DIRECT_DEPLOY",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        self._log_decision(decision_data)
        return decision_data

    def _log_decision(self, decision):
        with open(self.router_log, "r+") as f:
            try:
                logs = json.load(f)
                if not isinstance(logs, list):
                    logs = []
            except json.JSONDecodeError:
                logs = []
            logs.append(decision)
            f.seek(0)
            json.dump(logs, f, indent=4)
            f.truncate()

if __name__ == "__main__":
    # Setup dummy fidelity data for testing
    with open("/root/srda_fidelity_logs.json", "w") as f:
        json.dump({"security": {"fidelity_score": 0.85}, "coding": {"fidelity_score": 0.60}}, f)
    
    router = FidelityDrivenExecutionRouter()
    
    res1 = router.route_execution("AXIOM_SEC_01", "security", "Medium")
    res2 = router.route_execution("AXIOM_COD_01", "coding", "Medium")
    
    print(f"Security Route: {res1["decision"]}")
    print(f"Coding Route: {res2["decision"]}")
    print("Fidelity-Driven Execution Router [Operational]")
