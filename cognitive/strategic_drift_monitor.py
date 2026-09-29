import re
import json

class StrategicDriftMonitor:
    """
    Monitors the delta between expected strategic outcomes and actual execution signals
    to detect 'Strategic Drift' before catastrophic failure occurs.
    """
    def __init__(self, threshold=0.4):
        self.threshold = threshold

    def analyze_drift(self, expected_kpis, actual_output):
        """
        Calculates the drift score based on the presence of expected signals in the output.
        """
        hits = 0
        total = len(expected_kpis)
        
        if total == 0:
            return 0.0, "No KPIs defined."

        for kpi in expected_kpis:
            if re.search(kpi, actual_output, re.IGNORECASE):
                hits += 1
        
        # Confidence in the current path: hits/total
        # Drift: 1 - confidence
        confidence = hits / total
        drift_score = 1.0 - confidence
        
        status = "STABLE" if drift_score <= self.threshold else "DRIFTING"
        
        return drift_score, status

    def generate_pivot_alert(self, drift_score, status, missing_kpis):
        if status == "DRIFTING":
            return {
                "alert": "STRATEGIC_DRIFT_DETECTED",
                "score": drift_score,
                "missing": missing_kpis,
                "recommendation": "Trigger Synthetic Divergence Engine (SDE) to evaluate alternative vectors."
            }
        return {"status": "OK"}

if __name__ == "__main__":
    # Test Case
    sdm = StrategicDriftMonitor()
    expected = ["Success", "User created", "ID: [0-9]+"]
    actual = "Error: Database connection timed out. Retrying..."
    
    score, status = sdm.analyze_drift(expected, actual)
    print(f"Drift Score: {score}, Status: {status}")
