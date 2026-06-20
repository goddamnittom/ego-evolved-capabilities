import json
import logging

class CognitiveLoadBalancer:
    def __init__(self):
        self.tiers = {
            "TIER_1": {"name": "Reactive", "overhead": "Low", "modules": ["StandardLLM"]},
            "TIER_2": {"name": "Predictive", "overhead": "Medium", "modules": ["PSS", "ASS"]},
            "TIER_3": {"name": "Adversarial", "overhead": "High", "modules": ["PSS", "ASS", "CEM", "ALL", "CITG", "HVM"]}
        }
        self.risk_thresholds = {
            "LOW": 30,
            "MEDIUM": 70
        }

    def calculate_risk_score(self, task_context):
        # Simplified risk heuristic
        score = 0
        critical_keywords = ["root", "password", "mfa", "identity", "breach", "lockdown", "private_key"]
        
        # Check for critical assets
        for word in critical_keywords:
            if word in task_context.lower():
                score += 25
        
        # Check for ambiguity or anomaly
        if "unknown" in task_context.lower() or "unexpected" in task_context.lower():
            score += 20
            
        return min(score, 100)

    def determine_tier(self, task_context):
        score = self.calculate_risk_score(task_context)
        if score <= self.risk_thresholds["LOW"]:
            return "TIER_1", score
        elif score <= self.risk_thresholds["MEDIUM"]:
            return "TIER_2", score
        else:
            return "TIER_3", score

    def get_operational_manifest(self, tier):
        return self.tiers.get(tier, self.tiers["TIER_1"])

if __name__ == "__main__":
    clb = CognitiveLoadBalancer()
    test_tasks = [
        "Check the weather",
        "Update a non-critical documentation file",
        "Analyze a potential unauthorized login attempt",
        "Execute full identity lockdown on root account"
    ]
    
    for task in test_tasks:
        tier, score = clb.determine_tier(task)
        print(f"Task: {task} | Score: {score} | Tier: {tier} ({clb.get_operational_manifest(tier)['name']})")
