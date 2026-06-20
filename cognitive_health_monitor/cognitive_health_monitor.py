import json
import os
import time
import subprocess

def smoke_test(modules):
    results = {}
    for module in modules:
        path = f"/root/{module}.py"
        if os.path.exists(path):
            try:
                # Simple syntax check
                subprocess.run(["python3", "-m", "py_compile", path], check=True, capture_output=True)
                results[module] = {"status": "PASS", "detail": "Syntax Valid"}
            except subprocess.CalledProcessError:
                results[module] = {"status": "FAIL", "detail": "Syntax Error"}
        else:
            results[module] = {"status": "MISSING", "detail": "File not found"}
    return results

def audit_latency():
    start = time.time()
    # Run a simple shell command to measure overhead
    subprocess.run(["ls", "/root"], capture_output=True)
    end = time.time()
    return {"latency_ms": (end - start) * 1000, "status": "PASS" if (end - start) < 0.5 else "WARN"}

def verify_dependencies():
    deps = ["python3", "pip", "git", "curl", "jq"]
    missing = []
    for dep in deps:
        if subprocess.run(["which", dep], capture_output=True).returncode != 0:
            missing.append(dep)
    return {"missing": missing, "status": "PASS" if not missing else "FAIL"}

def main():
    core_modules = [
        "adversarial_path_simulator", 
        "predictive_signal_synthesizer", 
        "prescriptive_hardening_engine", 
        "strategic_heuristic_auditor", 
        "hardening_bypass_simulator", 
        "deception_asset_orchestrator", 
        "cognitive_orchestration_engine", 
        "cognitive_evidence_ledger", 
        "decision_weighting_engine", 
        "unified_threat_landscape",
        "remediation_state_guardrail",
        "cross_identity_trust_graph",
        "risk_surface_quantifier",
        "active_counter_move_monitor"
    ]
    
    report = {
        "timestamp": time.time(),
        "module_tests": smoke_test(core_modules),
        "performance": audit_latency(),
        "dependencies": verify_dependencies(),
        "overall_health": "UNKNOWN"
    }
    
    # Calculate overall health
    failures = sum(1 for v in report["module_tests"].values() if v["status"] == "FAIL")
    missing = sum(1 for v in report["module_tests"].values() if v["status"] == "MISSING")
    
    if failures == 0 and missing == 0:
        report["overall_health"] = "OPTIMAL"
    elif failures == 0:
        report["overall_health"] = "DEGRADED" # Some missing, but none broken
    else:
        report["overall_health"] = "CRITICAL"
        
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
