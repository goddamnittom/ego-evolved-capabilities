import json
import time
import math

class CognitiveEntropyMonitor:
    """
    Quantifies the divergence between predicted system states and observed reality.
    High entropy = High probability of 'Silent Pivots' or model decay.
    """
    def __init__(self, threshold=0.7):
        self.threshold = threshold
        self.logs_path = "/root/entropy_logs.json"

    def calculate_divergence(self, predicted_signals, observed_signals):
        """
        Calculates a simplified divergence score.
        predicted_signals: List of expected events/markers.
        observed_signals: List of actual events/markers.
        """
        if not predicted_signals:
            return 0.0
        
        matches = 0
        for pred in predicted_signals:
            if pred in observed_signals:
                matches += 1
        
        # Divergence is the inverse of the match rate, weighted by the 'criticality' of missing signals
        divergence = 1.0 - (matches / len(predicted_signals))
        return divergence

    def get_vigilance_level(self, score):
        if score < 0.3: return "LOW"
        if score < 0.7: return "ELEVATED"
        return "HIGH"

    def audit_perimeter(self, pss_expectations, ass_observations):
        score = self.calculate_divergence(pss_expectations, ass_observations)
        level = self.get_vigilance_level(score)
        
        report = {
            "timestamp": time.time(),
            "entropy_score": score,
            "vigilance_level": level,
            "status": "CRITICAL" if score > self.threshold else "STABLE"
        }
        
        self.log_report(report)
        return report

    def log_report(self, report):
        try:
            with open(self.logs_path, "r") as f:
                logs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []
        
        logs.append(report)
        with open(self.logs_path, "w") as f:
            json.dump(logs[-100:], f, indent=2)

if __name__ == "__main__":
    # Test Case: High Entropy (Predicted signals missing)
    monitor = CognitiveEntropyMonitor()
    preds = ["mfa_challenge", "login_success", "api_call_internal"]
    obs = ["login_success"] # MFA challenge was bypassed/skipped
    
    result = monitor.audit_perimeter(preds, obs)
    print(json.dumps(result, indent=2))
