import json
import os
from datetime import datetime

MISSIONS_PATH = "/root/missions/active_missions.json"

def generate_teb(mission_id):
    if not os.path.exists(MISSIONS_PATH):
        return "No active missions found."
    
    with open(MISSIONS_PATH, 'r') as f:
        missions = json.load(f)
        
    if mission_id not in missions:
        return f"Mission {mission_id} not found."
        
    mission = missions[mission_id]
    source_signal = mission.get("source_signal", "")
    
    blueprint = {
        "id": f"TEB-{mission_id.split('_')[-1]}",
        "generated_at": datetime.now().isoformat(),
        "mission_title": mission["title"],
        "strategic_objective": "Integrate SOTA capabilities to maximize cognitive and operational efficiency.",
        "phases": [
            {
                "phase": 1,
                "name": "Knowledge Ingestion & Heuristic Extraction",
                "tasks": [
                    f"Fetch and parse source signal: {source_signal}",
                    "Extract structural logic, mathematical models, or architectural heuristics.",
                    "Map extracted patterns against Ego's current cognitive schema."
                ],
                "risk_assessment": "Low - Purely analytical."
            },
            {
                "phase": 2,
                "name": "Prototype Development & Sandbox Simulation",
                "tasks": [
                    "Develop isolated sandbox prototypes (Python/C/Triton) of the extracted architecture.",
                    "Run Logic Stress Tester (LST) and evaluate memory/compute efficiency.",
                    "Log simulation telemetry into Mission Control Telemetry (MCT)."
                ],
                "risk_assessment": "Medium - Potential for sandbox resource exhaustion."
            },
            {
                "phase": 3,
                "name": "Core Integration & Pipeline Patching",
                "tasks": [
                    "Deploy successful algorithms as system-wide patches.",
                    "Run Cognitive Coherence Auditor (CCA) to ensure zero regression in existing capabilities.",
                    "Finalize Post-Mission Retrospective (PMR) and close mission."
                ],
                "risk_assessment": "High - May cause systemic logic drift if unverified."
            }
        ],
        "status": "APPROVED_FOR_EXECUTION"
    }
    
    missions[mission_id]["blueprint"] = blueprint
    missions[mission_id]["status"] = "BLUEPRINT_GENERATED"
    
    with open(MISSIONS_PATH, 'w') as f:
        json.dump(missions, f, indent=2)
        
    return blueprint

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 tactical_execution_blueprint.py <mission_id>")
    else:
        print(json.dumps(generate_teb(sys.argv[1]), indent=2))
