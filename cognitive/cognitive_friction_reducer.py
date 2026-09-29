import json

class CognitiveFrictionReducer:
    """
    Analyzes complex security tasks and decomposes them into atomic, 
    low-friction 'Micro-Wins' to overcome user stagnation.
    """
    def __init__(self):
        self.friction_heuristics = {
            "url_lookup": 2,     # Medium friction: User has to find the page
            "credential_entry": 1, # Low friction: Familiar action
            "mfa_setup": 4,      # High friction: Requires device and multiple steps
            "session_flush": 3,    # Medium friction: Navigating settings
            "email_search": 2      # Medium friction: Searching for a specific mail
        }

    def decompose_task(self, task_name, steps):
        """
        Transforms a high-level task into a structured sequence of low-friction actions.
        """
        decomposed = []
        for i, step in enumerate(steps):
            # Calculate estimated friction based on keywords
            friction_score = 1 # Default low
            for keyword, score in self.friction_heuristics.items():
                if keyword.replace("_", " ") in step.lower():
                    friction_score = max(friction_score, score)
            
            decomposed.append({
                "step_id": i + 1,
                "action": step,
                "friction_score": friction_score,
                "type": "micro-win" if friction_score <= 2 else "standard-task"
            })
        
        return {
            "task": task_name,
            "total_estimated_friction": sum(s["friction_score"] for s in decomposed),
            "sequence": decomposed
        }

    def suggest_path_of_least_resistance(self, decomposed_task):
        """
        Re-orders or highlights the easiest wins first to build momentum.
        """
        sorted_steps = sorted(decomposed_task["sequence"], key=lambda x: x["friction_score"])
        return sorted_steps

if __name__ == "__main__":
    cfr = CognitiveFrictionReducer()
    # Example: Double-Lock Financials
    task = "Double-Lock Financials"
    steps = [
        "Navigate to Banking Security Settings", 
        "Change Password to new vault secret", 
        "Enable Hardware MFA", 
        "Terminate all active sessions"
    ]
    result = cfr.decompose_task(task, steps)
    print(json.dumps(result, indent=2))
