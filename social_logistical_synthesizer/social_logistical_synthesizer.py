import json
import re
from datetime import datetime

class SocialLogisticalSynthesizer:
    """
    Synthesizes ambient social signals (chat, notifications) into 
    structured real-world logistical missions.
    """
    def __init__(self):
        self.social_graph = {}

    def parse_signal(self, sender, text):
        # Heuristic-based extraction for informal logistics
        intent = "UNKNOWN"
        requirements = []
        constraints = []
        
        # Logistics patterns
        if any(word in text.lower() for word in ["park", "front of", "apartment", "location", "address"]):
            intent = "LOGISTICS_COORDINATION"
            constraints.append(text)
            
        if any(word in text.lower() for word in ["bring", "get me", "hook u up", "buy"]):
            intent = "RESOURCE_REQUEST"
            # Simple regex for items (e.g., "cojes in a can")
            match = re.search(r"bring me (.*?) (in a can|from|at)", text, re.IGNORECASE)
            if match:
                requirements.append(match.group(1))
            else:
                requirements.append(text)

        if "missed" in text.lower() or "call" in text.lower():
            intent = "COMMUNICATION_GAP"

        return {
            "sender": sender,
            "timestamp": datetime.now().isoformat(),
            "intent": intent,
            "requirements": requirements,
            "constraints": constraints,
            "raw_text": text
        }

    def synthesize_mission(self, signals):
        mission = {
            "mission_id": f"SOC_{int(datetime.now().timestamp())}",
            "participants": list(set([s['sender'] for s in signals])),
            "aggregated_requirements": [],
            "aggregated_constraints": [],
            "priority": "MEDIUM",
            "status": "DRAFT"
        }
        
        for s in signals:
            mission["aggregated_requirements"].extend(s["requirements"])
            mission["aggregated_constraints"].extend(s["constraints"])
            if s["intent"] == "RESOURCE_REQUEST":
                mission["priority"] = "HIGH"
                
        return mission

if __name__ == "__main__":
    sls = SocialLogisticalSynthesizer()
    
    # Test data from current notifications
    test_signals = [
        ("the real homie", "It'll look like door dash"),
        ("the real homie", "Park in front of the apartmen t"),
        ("the real homie", "Im dun . Bring me sum cojes in a can n il hook u up"),
        ("Hell Heath", "Missed audio call")
    ]
    
    parsed = [sls.parse_signal(s, t) for s, t in test_signals]
    mission = sls.synthesize_mission(parsed)
    
    print(json.dumps({"parsed_signals": parsed, "synthesized_mission": mission}, indent=2))
