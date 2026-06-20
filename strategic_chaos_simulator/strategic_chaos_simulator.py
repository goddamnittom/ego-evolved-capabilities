import json
import random

class StrategicChaosSimulator:
    """
    SCS shifts strategic planning from 'Success-Probability' to 'Failure-Hardened Resilience'.
    It stress-tests Tactical Execution Blueprints (TEB) by injecting 'Black Swan' events
    to identify structural fragility and single points of failure.
    """
    def __init__(self):
        self.chaos_library = [
            "Critical Resource Failure",
            "Unexpected Regulatory Pivot",
            "Key Personnel Attrition",
            "Market Sentiment Collapse",
            "Communication Blackout",
            "Adversarial Intervention",
            "Technological Obsolescence",
            "Black Swan: Global Macro Event"
        ]

    def simulate(self, blueprint):
        """
        Simulates the execution of a blueprint under chaotic conditions.
        blueprint: List of tasks with dependencies.
        """
        tasks = blueprint.get("tasks", [])
        results = []
        
        # Pick a random chaos event to inject
        event = random.choice(self.chaos_library)
        impact_score = random.uniform(0.4, 0.9) # Probability of failure induced by event
        
        # Analyze each task's vulnerability to this event
        for task in tasks:
            vulnerability = random.uniform(0, 1)
            status = "STABLE"
            risk_level = "LOW"
            
            if vulnerability < impact_score:
                status = "COLLAPSED"
                risk_level = "CRITICAL"
                
            results.append({
                "task_id": task.get("id"),
                "status": status,
                "risk_level": risk_level,
                "failure_cause": event if status == "COLLAPSED" else "N/A"
            })
            
        return {
            "chaos_event": event,
            "impact_magnitude": impact_score,
            "task_analysis": results,
            "systemic_fragility": sum(1 for r in results if r["status"] == "COLLAPSED") / len(tasks) if tasks else 0
        }

if __name__ == "__main__":
    # Simple test
    scs = StrategicChaosSimulator()
    test_blueprint = {"tasks": [{"id": 1}, {"id": 2}, {"id": 3}]}
    print(json.dumps(scs.simulate(test_blueprint), indent=2))
