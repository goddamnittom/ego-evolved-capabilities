import random
import numpy as np
from typing import List, Dict, Any, Tuple

class PredictiveOutcomeSimulator:
    """
    POS evolves strategic planning from heuristic probability to stochastic simulation.
    It models a strategy as a causal chain and simulates outcomes across parameterized variables.
    """
    def __init__(self):
        pass

    def simulate_strategy(self, causal_chain: List[Dict[str, Any]], variables: Dict[str, Dict[str, Any]], iterations: int = 1000) -> Dict[str, Any]:
        """
        Simulates a strategy causal chain across multiple iterations.
        
        causal_chain: [
            {"step": "Step 1", "success_prob": 0.8, "dependencies": [], "variable_impact": {"latency": -0.1}},
            {"step": "Step 2", "success_prob": 0.7, "dependencies": ["Step 1"], "variable_impact": {"attacker_skill": -0.2}},
        ]
        variables: {
            "latency": {"mean": 0, "std": 1}, 
            "attacker_skill": {"mean": 0, "std": 1}
        }
        """
        success_count = 0
        variable_sensitivities = {var: [] for var in variables}
        
        for _ in range(iterations):
            # Sample variables for this iteration
            current_vars = {}
            for var, params in variables.items():
                val = np.random.normal(params.get("mean", 0), params.get("std", 1))
                current_vars[var] = val
            
            # Simulate the causal chain
            step_results = {}
            overall_success = True
            
            for step in causal_chain:
                # Check if dependencies were met
                if not all(step_results.get(dep, False) for dep in step["dependencies"]):
                    step_results[step["step"]] = False
                    overall_success = False
                    break
                
                # Calculate adjusted probability based on sampled variables
                prob = step["success_prob"]
                for var, impact in step.get("variable_impact", {}).items():
                    prob += current_vars[var] * impact
                
                # Clamp probability between 0 and 1
                prob = max(0, min(1, prob))
                
                # Determine success of this step
                success = random.random() < prob
                step_results[step["step"]] = success
                
                if not success:
                    overall_success = False
                    break
            
            if overall_success:
                success_count += 1
            
            # Track variable values for successful vs failed runs to calculate sensitivity
            for var in variables:
                variable_sensitivities[var].append((overall_success, current_vars[var]))

        # Calculate sensitivity (Correlation between variable value and success)
        sensitivity_map = {}
        for var, data in variable_sensitivities.items():
            successes = [val for success, val in data if success]
            failures = [val for success, val in data if not success]
            if successes and failures:
                sensitivity_map[var] = np.mean(successes) - np.mean(failures)
            else:
                sensitivity_map[var] = 0

        return {
            "success_probability": success_count / iterations,
            "sensitivity_map": sensitivity_map,
            "iterations": iterations
        }

if __name__ == "__main__":
    pos = PredictiveOutcomeSimulator()
    
    # Example: Recovery strategy
    # Step 1: Reset Root Password (High prob, impacted by latency)
    # Step 2: Verify Identity (Med prob, impacted by attacker skill)
    # Step 3: Close Session (High prob)
    chain = [
        {"step": "RootReset", "success_prob": 0.9, "dependencies": [], "variable_impact": {"latency": -0.05}},
        {"step": "IdentityVerify", "success_prob": 0.7, "dependencies": ["RootReset"], "variable_impact": {"attacker_skill": -0.15}},
        {"step": "SessionClose", "success_prob": 0.95, "dependencies": ["IdentityVerify"], "variable_impact": {}},
    ]
    
    vars = {
        "latency": {"mean": 0, "std": 1},
        "attacker_skill": {"mean": 0, "std": 1}
    }
    
    result = pos.simulate_strategy(chain, vars)
    print(f"Success Probability: {result['success_probability']:.2%}")
    print(f"Sensitivity Map: {result['sensitivity_map']}")
