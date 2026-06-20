import json

class PivotPredictionEngine:
    def __init__(self):
        # Mapping of assets to their likely "pivot value" (what an attacker gains from them)
        self.pivot_graph = {
            "Financials": {"targets": ["Identities", "Dev Tools"], "weight": 0.8},
            "Identities": {"targets": ["Financials", "Dev Tools", "Socials"], "weight": 0.9},
            "Dev Tools": {"targets": ["Identities", "Infrastructure"], "weight": 0.7},
            "Socials": {"targets": ["Identities"], "weight": 0.4},
            "Infrastructure": {"targets": ["Financials", "Dev Tools"], "weight": 0.9}
        }

    def predict_next_target(self, secured_assets, known_vulnerabilities):
        predictions = []
        for asset, data in self.pivot_graph.items():
            if asset in secured_assets:
                continue
            
            # Score based on pivot weight and whether it's a known vulnerability
            score = data["weight"]
            if asset in known_vulnerabilities:
                score += 0.2
            
            predictions.append({"asset": asset, "probability_score": min(score, 1.0)})
        
        # Sort by highest probability
        return sorted(predictions, key=lambda x: x["probability_score"], reverse=True)

if __name__ == "__main__":
    ppe = PivotPredictionEngine()
    # Example: Financials are secured, but Identities are known to be vulnerable (T1555)
    result = ppe.predict_next_target(["Financials"], ["Identities"])
    print(json.dumps(result, indent=2))
