import json
import os
from datetime import datetime, timezone

class VolatilityAdjustedTrustScale:
    """
    VATS: Dynamic Threshold Adaptation.
    Links the FDER thresholds to a real-time Environmental Volatility Index (EVI).
    As volatility increases, trust thresholds tighten, forcing more Pilot Missions.
    """
    def __init__(self, evi_source="/root/environmental_volatility.json", 
                 fder_config="/root/fder_config.json"):
        self.evi_source = evi_source
        self.fder_config = fder_config
        self._ensure_files()

    def _ensure_files(self):
        if not os.path.exists(self.evi_source):
            with open(self.evi_source, "w") as f:
                json.dump({"current_evi": 1.0}, f) # 1.0 = baseline
        if not os.path.exists(self.fder_config):
            with open(self.fder_config, "w") as f:
                json.dump({
                    "base_thresholds": {
                        "High": 0.90,
                        "Medium": 0.75,
                        "Low": 0.40
                    }
                }, f)

    def get_current_evi(self):
        try:
            with open(self.evi_source, "r") as f:
                return json.load(f).get("current_evi", 1.0)
        except:
            return 1.0

    def calculate_adjusted_threshold(self, risk_level):
        evi = self.get_current_evi()
        with open(self.fder_config, "r") as f:
            base_thresholds = json.load(f).get("base_thresholds", {})
        
        base = base_thresholds.get(risk_level, 0.75)
        
        # The Adjustment Logic: 
        # Higher EVI (volatility) increases the threshold (makes it harder to deploy directly).
        # Adjustment = base + (modifier * (evi - 1))
        # Cap at 0.99 to ensure a path to deployment always exists.
        modifier = 0.1 if risk_level == "Medium" else 0.05
        adjusted = base + (modifier * (evi - 1.0))
        return min(0.99, adjusted)

    def sync_fder(self):
        """Pushes the updated thresholds to the FDER system."""
        updated_thresholds = {
            "High": self.calculate_adjusted_threshold("High"),
            "Medium": self.calculate_adjusted_threshold("Medium"),
            "Low": self.calculate_adjusted_threshold("Low")
        }
        # In a real system, this would update the FDER instance memory or config file
        return updated_thresholds

if __name__ == "__main__":
    # Scenario 1: Baseline Volatility (EVI = 1.0)
    with open("/root/environmental_volatility.json", "w") as f:
        json.dump({"current_evi": 1.0}, f)
    
    vats = VolatilityAdjustedTrustScale()
    print(f"Baseline Thresholds: {vats.sync_fder()}")

    # Scenario 2: High Volatility / Crisis Mode (EVI = 3.0)
    with open("/root/environmental_volatility.json", "w") as f:
        json.dump({"current_evi": 3.0}, f)
    
    print(f"Volatile Thresholds (EVI 3.0): {vats.sync_fder()}")
    print("Volatility-Adjusted Trust Scale [Operational]")
