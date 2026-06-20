import os
import subprocess
import json
from datetime import datetime

class CIHM:
    def __init__(self):
        self.tool_dir = "/root"
        self.cognitive_prefix = "cognitive_"
        self.security_prefix = "security_" # Including security tools in infra check
        self.known_tools = [
            "cognitive_resource_governor.py",
            "axiomatic_synthesizer.py",
            "semantic_entropy_monitor.py",
            "threat_model_synthesizer.py",
            "signal_correlation_engine.py",
            "hardening_sequence_orchestrator.py",
            "cognitive_friction_reducer.py",
            "attack_surface_delta_mapper.py",
            "ambient_signal_synthesizer.py",
            "crisis_interface_generator.py",
            "actor_behavioral_profiling.py",
            "session_integrity_auditor.py",
            "remediation_state_guardrail.py",
            "cross_identity_trust_graph.py",
            "decision_weighting_engine.py",
            "unified_threat_landscape.py",
            "adversarial_path_simulator.py",
            "prescriptive_hardening_engine.py",
            "strategic_heuristic_auditor.py",
            "hardening_bypass_simulator.py",
            "deception_asset_orchestrator.py",
            "predictive_signal_synthesizer.py",
            "digital_footprint_mapper.py",
            "visual_signature_manager.py",
            "cross_platform_fingerprinter.py"
        ]

    def check_tool_integrity(self, tool_name):
        path = os.path.join(self.tool_dir, tool_name)
        if not os.path.exists(path):
            return {"status": "MISSING", "health": 0}
        
        try:
            # Check if it's valid python
            subprocess.run(["python3", "-m", "py_compile", path], capture_output=True, check=True)
            size = os.path.getsize(path)
            mtime = datetime.fromtimestamp(os.path.getmtime(path)).isoformat()
            return {"status": "ONLINE", "health": 100, "size": size, "last_modified": mtime}
        except subprocess.CalledProcessError:
            return {"status": "CORRUPTED", "health": 0}

    def generate_report(self):
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_tools": len(self.known_tools),
            "operational_tools": 0,
            "issues": [],
            "tools": {}
        }

        for tool in self.known_tools:
            res = self.check_tool_integrity(tool)
            report["tools"][tool] = res
            if res["status"] == "ONLINE":
                report["operational_tools"] += 1
            else:
                report["issues"].append(f"{tool}: {res['status']}")

        report["overall_health"] = (report["operational_tools"] / report["total_tools"]) * 100
        return report

if __name__ == "__main__":
    monitor = CIHM()
    print(json.dumps(monitor.generate_report(), indent=2))
