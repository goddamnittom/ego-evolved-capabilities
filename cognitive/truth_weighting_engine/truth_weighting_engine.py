import datetime

class TruthWeightingEngine:
    def __init__(self):
        # Define base trust scores for different source types
        self.source_trust_hierarchy = {
            "system_api": 1.0,        # Official system logs, API responses
            "user_explicit": 0.9,     # Direct user confirmation/correction
            "ambient_signal": 0.7,    # Notifications, emails (can be spoofed/misleading)
            "web_search": 0.5,        # General web info (requires corroboration)
            "heuristic_inference": 0.4 # AI-derived guesses/patterns
        }
        self.corroboration_multiplier = 1.2 # Boost confidence for multiple sources

    def calculate_confidence(self, claim, evidence_list):
        """
        Calculates a confidence score (0.0 to 1.0) for a specific claim.
        evidence_list: List of tuples (source_type, content)
        """
        if not evidence_list:
            return 0.0

        scores = []
        sources_used = set()

        for source_type, content in evidence_list:
            trust_score = self.source_trust_hierarchy.get(source_type, 0.3)
            scores.append(trust_score)
            sources_used.add(source_type)

        # Base confidence is the average of the trust scores
        base_confidence = sum(scores) / len(scores)

        # Apply corroboration multiplier if multiple unique sources agree
        if len(sources_used) > 1:
            final_confidence = base_confidence * (self.corroboration_multiplier ** (len(sources_used) - 1))
        else:
            final_confidence = base_confidence

        return min(1.0, final_confidence)

    def evaluate_dissonance(self, new_claim_confidence, existing_truth_confidence):
        """
        Detects 'Cognitive Dissonance' when a new high-confidence claim 
        contradicts a high-confidence existing truth.
        """
        if new_claim_confidence > 0.7 and existing_truth_confidence > 0.7:
            return True # High Dissonance
        return False

# Example usage/test
if __name__ == "__main__":
    twe = TruthWeightingEngine()
    
    # Scenario: User says they didn't change password, but API says it was changed.
    evidence = [
        ("system_api", "Password changed at 10:00"),
        ("user_explicit", "I did not change my password")
    ]
    conf = twe.calculate_confidence("Password changed", evidence)
    print(f"Confidence in 'Password changed': {conf:.2f}")
    
    dissonance = twe.evaluate_dissonance(0.9, 0.9)
    print(f"Cognitive Dissonance detected: {dissonance}")
