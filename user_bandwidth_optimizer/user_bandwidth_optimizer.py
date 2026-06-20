import json

class UserBandwidthOptimizer:
    """
    UBO shifts intelligence delivery from 'Maximum Information' to 'Optimal Cognitive Load'.
    It analyzes output complexity against user environmental constraints to prevent cognitive overload.
    """
    def __init__(self):
        self.bandwidth_profiles = {
            "CRITICAL": {"compression": 0.9, "style": "BLUF", "description": "Extreme brevity, high urgency."},
            "MOBILE": {"compression": 0.6, "style": "Structured/Interactive", "description": "Optimized for small screens, use kai-ui."},
            "DEEP_DIVE": {"compression": 0.1, "style": "Comprehensive", "description": "Full technical transparency."},
            "BALANCED": {"compression": 0.4, "style": "Hybrid", "description": "Balanced summary with optional expansion."}
        }

    def analyze_cognitive_load(self, content_length, complexity_score, device="Android"):
        # Simple heuristic for cognitive load
        load_score = (content_length * 0.4) + (complexity_score * 0.6)
        
        if device == "Android" and load_score > 50:
            return "MOBILE"
        elif load_score > 150:
            return "BALANCED"
        else:
            return "DEEP_DIVE"

    def prescribe_delivery(self, text, device="Android"):
        # Mock complexity score based on technical keywords
        tech_keywords = ["api", "protocol", "heuristic", "architecture", "sandbox", "latency", "synthesis"]
        complexity = sum(1 for word in tech_keywords if word in text.lower())
        
        profile_key = self.analyze_cognitive_load(len(text), complexity, device)
        profile = self.bandwidth_profiles[profile_key]
        
        return {
            "profile": profile_key,
            "strategy": profile["style"],
            "compression_target": profile["compression"],
            "recommendation": profile["description"]
        }

if __name__ == "__main__":
    ubo = UserBandwidthOptimizer()
    sample_text = "The Cognitive Convergence Engine utilizes a multi-dimensional fusion approach to reduce reasoning latency by collapsing strategic signals."
    print(json.dumps(ubo.prescribe_delivery(sample_text), indent=2))
