import json
from datetime import datetime, timedelta

class MissionTemporalForensicEngine:
    """
    MTFE: Analyzes MCT telemetry and ER 1.6 visual signals to reconstruct 
    the causal chain of a mission failure.
    """
    def __init__(self):
        self.failure_logs = []

    def analyze_failure(self, mct_logs, er_signals, expected_state):
        """
        mct_logs: List of {'timestamp': datetime, 'node': str, 'value': any}
        er_signals: List of {'timestamp': datetime, 'signal': str, 'value': bool}
        expected_state: The MCT node value that was supposed to be reached.
        """
        # 1. Find the "Point of Divergence" (PoD)
        pod_time = None
        for signal in reversed(er_signals):
            if signal['value'] is False:
                pod_time = signal['timestamp']
                break
        
        if not pod_time:
            return {"status": "NO_FAILURE_DETECTED", "reason": "No negative signals found in ER stream."}

        # 2. Extract the "Causal Window" (T-5 seconds to PoD)
        window_start = pod_time - timedelta(seconds=5)
        causal_data = [log for log in mct_logs if window_start <= log['timestamp'] <= pod_time]
        
        # 3. Heuristic Causal Analysis
        hypothesis = "Unknown"
        severity = "Low"
        
        if not causal_data:
            hypothesis = "Telemetry Gap: No MCT data available during the causal window."
            severity = "High"
        else:
            for i in range(1, len(causal_data)):
                prev = causal_data[i-1]
                curr = causal_data[i]
                if prev['node'] == curr['node'] and isinstance(curr['value'], (int, float)):
                    delta = abs(curr['value'] - prev['value'])
                    if delta > (abs(prev['value']) * 0.5):
                        hypothesis = f"Dynamic Instability detected in node {curr['node']} shortly before failure."
                        severity = "Medium"
                        break

        return {
            "status": "FAILURE_ANALYZED",
            "point_of_divergence": pod_time.isoformat(),
            "causal_window_events": len(causal_data),
            "hypothesis": hypothesis,
            "severity": severity,
            "recommendation": "Adjust ATP retry parameters based on " + hypothesis
        }

if __name__ == "__main__":
    mtfe = MissionTemporalForensicEngine()
    now = datetime.now()
    
    mock_mct = [
        {'timestamp': now - timedelta(seconds=6), 'node': 'grip_pressure', 'value': 10},
        {'timestamp': now - timedelta(seconds=4), 'node': 'grip_pressure', 'value': 12},
        {'timestamp': now - timedelta(seconds=2), 'node': 'grip_pressure', 'value': 45},
        {'timestamp': now - timedelta(seconds=1), 'node': 'grip_pressure', 'value': 11},
    ]
    
    mock_er = [
        {'timestamp': now, 'signal': 'object_in_gripper', 'value': False}
    ]
    
    result = mtfe.analyze_failure(mock_mct, mock_er, 'GOAL_REACHED')
    print(json.dumps(result, indent=2))
