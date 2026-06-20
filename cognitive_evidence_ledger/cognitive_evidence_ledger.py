import json
import time
def log_evidence(event, causal_chain):
    entry = {"timestamp": time.time(), "event": event, "chain": causal_chain}
    return entry
if __name__ == "__main__":
    print(json.dumps(log_evidence("hardening_start", ["signal", "heuristic", "decision"])))
