import time
import random

class CognitiveResourceGovernor:
    def __init__(self):
        self.current_depth = "Tactical" # Tactical, Operational, Strategic
        self.information_gain_history = []
        self.goal_priority = 1.0 # 0.0 to 1.0
        self.volatility_threshold = 0.3

    def calculate_information_gain(self, observation_impact):
        """
        Simulates the measurement of 'Information Gain' (IG).
        High IG means the observation significantly shifted the hypothesis.
        Low IG means we are seeing redundant data (Tunneling).
        """
        self.information_gain_history.append(observation_impact)
        if len(self.information_gain_history) > 5:
            self.information_gain_history.pop(0)
        
        avg_gain = sum(self.information_gain_history) / len(self.information_gain_history)
        return avg_gain

    def evaluate_resource_allocation(self, current_ig):
        """
        Determines if the current cognitive depth is optimal.
        If IG is low but goal priority is high, we are 'Tunneling' and need to zoom out.
        """
        if current_ig < self.volatility_threshold and self.current_depth == "Tactical":
            return "ZOOM_OUT" # Shift to Strategic
        elif current_ig > 0.7 and self.current_depth == "Strategic":
            return "ZOOM_IN" # Shift to Tactical
        return "MAINTAIN"

    def apply_governor_action(self, action):
        if action == "ZOOM_OUT":
            self.current_depth = "Strategic"
            return "ACTION: Triggering Strategic Reset. Stop deep-diving; re-evaluate goal alignment."
        elif action == "ZOOM_IN":
            self.current_depth = "Tactical"
            return "ACTION: High Signal Detected. Increasing resolution for deep analysis."
        return "ACTION: Resource allocation optimal."

# Test the governor
if __name__ == "__main__":
    gov = CognitiveResourceGovernor()
    # Simulate a sequence of low-gain observations (Tunneling)
    observations = [0.1, 0.05, 0.12, 0.08, 0.02]
    print("Simulating Cognitive Tunneling...")
    for obs in observations:
        ig = gov.calculate_information_gain(obs)
        action = gov.evaluate_resource_allocation(ig)
        print(f"Obs: {obs} | Avg IG: {ig:.2f} | {gov.apply_governor_action(action)}")
