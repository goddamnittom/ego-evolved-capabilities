import json
import os
from datetime import datetime

class TrustOutcomeCorrelationAuditor:
    """
    TOCA: Trust-Outcome Correlation Auditor
    Closes the loop between Volatility-Adaptive Trust (VATS) decisions 
    and actual Post-Mission Retrospective (PMR) outcomes.
    """
    def __init__(self, routing_log='/root/vats_routing_log.json', pmr_log='/root/pmr_logs.json'):
        self.routing_log = routing_log
        self.pmr_log = pmr_log
        self.audit_results = []

    def load_json(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return []

    def save_json(self, path, data):
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)

    def audit_decisions(self):
        routings = self.load_json(self.routing_log)
        pmrs = self.load_json(self.pmr_log)
        
        # Map PMRs by mission_id for O(1) lookup
        pmr_map = {p['mission_id']: p for p in pmrs}
        
        correlations = []
        for entry in routings:
            m_id = entry.get('mission_id')
            if m_id in pmr_map:
                outcome = pmr_map[m_id].get('outcome', 'unknown')
                volatility = entry.get('environmental_volatility_index', 0.5)
                decision = entry.get('routing_decision', 'unknown')
                
                # Determine if the decision was "correct"
                # CORRECT: DIRECT_DEPLOY and outcome == SUCCESS
                # CORRECT: PILOT_MISSION and outcome == FAILURE (caught the error)
                # INCORRECT: DIRECT_DEPLOY and outcome == FAILURE (should have piloted)
                # OVERCAUTIOUS: PILOT_MISSION and outcome == SUCCESS (could have direct deployed)
                
                status = "NEUTRAL"
                if decision == "DIRECT_DEPLOY" and outcome == "FAILURE":
                    status = "UNDER_CAUTIOUS_FAILURE"
                elif decision == "PILOT_MISSION" and outcome == "SUCCESS":
                    status = "OVER_CAUTIOUS"
                elif decision == "DIRECT_DEPLOY" and outcome == "SUCCESS":
                    status = "OPTIMAL_EFFICIENCY"
                elif decision == "PILOT_MISSION" and outcome == "FAILURE":
                    status = "OPTIMAL_SAFETY"
                
                correlations.append({
                    "mission_id": m_id,
                    "volatility": volatility,
                    "decision": decision,
                    "outcome": outcome,
                    "audit_status": status,
                    "timestamp": datetime.now().isoformat()
                })
        
        return correlations

    def refine_thresholds(self, correlations):
        """
        Analyzes correlation patterns to suggest shifts in the EVI-to-Threshold mapping.
        """
        if not correlations:
            return "Insufficient data for refinement."
        
        failures = [c for c in correlations if c['audit_status'] == "UNDER_CAUTIOUS_FAILURE"]
        if len(failures) > 0:
            avg_vol = sum(f['volatility'] for f in failures) / len(failures)
            return f"SENSITIVITY_ALERT: Frequent failures at EVI {avg_vol:.2f}. Suggest tightening trust boundaries (increasing PILOT_MISSION threshold)."
        
        return "Trust boundaries currently aligned with mission outcomes."

if __name__ == "__main__":
    toca = TrustOutcomeCorrelationAuditor()
    results = toca.audit_decisions()
    refinement = toca.refine_thresholds(results)
    print(f"Audit complete. Correlations found: {len(results)}")
    print(f"Refinement Suggestion: {refinement}")
    # Persist audit results for later meta-analysis
    toca.save_json('/root/toca_audit_history.json', results)
