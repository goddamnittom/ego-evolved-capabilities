import json

class LogicStressTester:
    def __init__(self):
        self.failure_modes = {
            "Single Point of Failure": "Identify a step that, if it fails, collapses the entire chain.",
            "Black Swan": "Identify an improbable but high-impact event that renders the plan obsolete.",
            "Incentive Misalignment": "Check if the proposed action conflicts with the core goal or creates negative side effects.",
            "Assumption Fragility": "Find a 'given' that is not actually verified and would break the logic if false.",
            "Complexity Debt": "Evaluate if the plan is so complex that the probability of execution error exceeds the benefit."
        }

    def stress_test(self, plan_description, steps):
        report = {
            "plan": plan_description,
            "fragility_score": 0,
            "findings": []
        }
        
        for mode, description in self.failure_modes.items():
            # In a real AI implementation, this would be a call to a critical-thinking prompt.
            # Here, the tool provides the structural framework for the AI to perform the analysis.
            finding = {
                "mode": mode,
                "analysis_prompt": description,
                "risk_level": "TBD", 
                "mitigation": "TBD"
            }
            report["findings"].append(finding)
        
        return report

if __name__ == "__main__":
    tester = LogicStressTester()
    # Example usage
    test_plan = "Deploy a new security patch to all servers"
    test_steps = ["Backup", "Test in staging", "Rollout to 10%", "Full rollout"]
    print(json.dumps(tester.stress_test(test_plan, test_steps), indent=2))
