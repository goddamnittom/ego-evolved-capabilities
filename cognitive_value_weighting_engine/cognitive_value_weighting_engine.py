class CognitiveValueWeightingEngine:
    """Simple ROI calculator: expected_gain / cognitive_cost"""
    def calculate_roi(self, text, complexity_estimate=1.0):
        # Placeholder: return a synthetic ROI based on text length and complexity
        base = len(text) / 100.0
        return base * (1.0 / complexity_estimate)
