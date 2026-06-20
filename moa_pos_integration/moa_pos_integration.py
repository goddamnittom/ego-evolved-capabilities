from predictive_outcome_simulator import PredictiveOutcomeSimulator
import numpy as np

def run_pos_complexity_modeling():
    pos = PredictiveOutcomeSimulator()
    
    # We model standard vs MoA as distinct strategy paths where memory constraints are variables.
    # The variable is 'n_scale' representing standard deviations from base n.
    
    # Base strategy: Scaling classic attention 
    # Step 1: Input allocation (100% success)
    # Step 2: N x N allocation (Success drops rapidly as N increases due to OOM)
    classic_chain = [
        {"step": "Load_QKV", "success_prob": 1.0, "dependencies": [], "variable_impact": {"n_size": -0.01}},
        {"step": "Compute_NxN_Scores", "success_prob": 0.9, "dependencies": ["Load_QKV"], "variable_impact": {"n_size": -0.8}}, 
    ]
    
    moa_chain = [
         {"step": "Load_QKV", "success_prob": 1.0, "dependencies": [], "variable_impact": {"n_size": -0.01}},
         {"step": "Compute_DNF_Scalars", "success_prob": 1.0, "dependencies": ["Load_QKV"], "variable_impact": {"n_size": -0.05}}, # very low impact
    ]
    
    results = {}
    # We will simulate multiple N scales. 
    # n_size = 0 represents n~8k, 
    # n_size = 0.5 represents n~16k
    # n_size = 1.0 represents n=32k, 
    # n_size = 1.5 represents n=65k
    scales = {"n=8192": 0.0, "n=16384": 0.5, "n=32768": 1.0, "n=65536": 1.5}
    
    for label, n_val in scales.items():
        variables = {"n_size": {"mean": n_val, "std": 0.05}} # Tight distribution around the target N size
        classic_res = pos.simulate_strategy(classic_chain, variables, iterations=2000)
        moa_res = pos.simulate_strategy(moa_chain, variables, iterations=2000)
        
        results[label] = {
            "classic_prob": classic_res["success_probability"],
            "moa_prob": moa_res["success_probability"]
        }
        
    print("=== POS Complexity Modeling for OOM Probability ===")
    print(f"{'Sequence Scale':<15} | {'Classic Attn Success P(s)':<25} | {'MoA DNF Success P(s)':<25}")
    print("-" * 75)
    for label, prob in results.items():
        print(f"{label:<15} | {prob['classic_prob']:<25.2%} | {prob['moa_prob']:<25.2%}")

if __name__ == '__main__':
    run_pos_complexity_modeling()
