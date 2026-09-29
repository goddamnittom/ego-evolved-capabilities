import numpy as np
from typing import List, Dict

class SemanticEntropyMonitor:
    """
    SEM calculates the Shannon Entropy of strategic hypotheses to determine
    whether the AI should be in 'Exploration' (high entropy) or 'Exploitation' (low entropy) mode.
    """
    def __init__(self, entropy_threshold: float = 0.5):
        self.entropy_threshold = entropy_threshold

    def calculate_entropy(self, probabilities: List[float]) -> float:
        """Calculates Shannon Entropy: H = -sum(p * log2(p))"""
        probs = np.array(probabilities)
        # Remove zeros to avoid log(0)
        probs = probs[probs > 0]
        if len(probs) == 0:
            return 0.0
        return -np.sum(probs * np.log2(probs))

    def evaluate_mode(self, probabilities: List[float]) -> Dict:
        """
        Determines the cognitive mode based on entropy.
        - High Entropy: Multiple competing hypotheses -> EXPLORATION (Search/Diverge)
        - Low Entropy: Single dominant hypothesis -> EXPLOITATION (Execute/Converge)
        """
        entropy = self.calculate_entropy(probabilities)
        mode = "EXPLORATION" if entropy > self.entropy_threshold else "EXPLOITATION"
        
        return {
            "entropy": entropy,
            "mode": mode,
            "threshold": self.entropy_threshold,
            "recommendation": "Expand SDE and increase search depth" if mode == "EXPLORATION" else "Tighten CRG and execute precision path"
        }

if __name__ == "__main__":
    sem = SemanticEntropyMonitor()
    # Example 1: High uncertainty (High Entropy)
    test_probs_high = [0.3, 0.3, 0.2, 0.2]
    # Example 2: High certainty (Low Entropy)
    test_probs_low = [0.9, 0.05, 0.03, 0.02]
    
    print(f"High Uncertainty: {sem.evaluate_mode(test_probs_high)}")
    print(f"High Certainty: {sem.evaluate_mode(test_probs_low)}")
