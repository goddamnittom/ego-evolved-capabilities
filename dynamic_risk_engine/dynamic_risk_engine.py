import json
import time
from datetime import datetime

class DynamicRiskEngine:
    def __init__(self, risk_threshold=0.7):
        self.risk_threshold = risk_threshold
        self.volatility_index = 1.0  # Baseline volatility
        self.risk_weights = {
            "credential_change": 0.8,
            "api_call": 0.3,
            "file_system_write": 0.5,
            "external_communication": 0.6,
            "system_config_change": 0.9
        }

    def calculate_volatility(self, ambient_signals):
        """
        Analyzes signals from ASS (Ambient Signal Synthesizer) and SIA (Session Integrity Auditor)
        to determine current environmental volatility.
        """
        score = 1.0
        for signal in ambient_signals:
            if signal.get("severity") == "CRITICAL":
                score += 0.5
            elif signal.get("severity") == "WARNING":
                score += 0.2
            
            if "unauthorized_login" in signal.get("type", "").lower():
                score += 0.4
            if "mfa_bypass_attempt" in signal.get("type", "").lower():
                score += 0.6
                
        self.volatility_index = score
        return score

    def evaluate_task_risk(self, task):
        """
        Re-calculates the risk of a specific task based on current volatility.
        """
        base_risk = task.get("base_risk", 0.5)
        category = task.get("category", "general")
        category_weight = self.risk_weights.get(category, 0.5)
        
        # Adjusted Risk = (Base Risk * Volatility) + (Category Weight * Volatility / 2)
        adjusted_risk = (base_risk * self.volatility_index) + (category_weight * self.volatility_index / 2)
        
        # Clamp between 0 and 1
        return min(max(adjusted_risk, 0.0), 1.0)

    def should_escalate(self, task):
        risk = self.evaluate_task_risk(task)
        return risk > self.risk_threshold, risk

    def run_audit(self, blueprint, signals):
        self.calculate_volatility(signals)
        audit_results = []
        
        for task in blueprint.get("tasks", []):
            escalate, risk = self.should_escalate(task)
            audit_results.append({
                "task_id": task.get("id"),
                "original_risk": task.get("base_risk"),
                "adjusted_risk": risk,
                "action": "ESC_USER" if escalate else "PROCEED"
            })
            
        return {
            "volatility_index": self.volatility_index,
            "audit": audit_results,
            "timestamp": datetime.utcnow().isoformat()
        }

if __name__ == "__main__":
    # Test case
    dre = DynamicRiskEngine()
    
    # Mock Blueprint
    blueprint = {
        "tasks": [
            {"id": "T1", "category": "api_call", "base_risk": 0.2},
            {"id": "T2", "category": "credential_change", "base_risk": 0.6},
        ]
    }
    
    # Mock signals: A critical unauthorized login detected
    signals = [{"type": "unauthorized_login", "severity": "CRITICAL"}]
    
    result = dre.run_audit(blueprint, signals)
    print(json.dumps(result, indent=2))
