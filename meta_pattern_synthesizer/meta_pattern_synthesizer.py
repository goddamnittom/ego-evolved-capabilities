import json
import os
from collections import Counter
from datetime import datetime

class MetaPatternSynthesizer:
    def __init__(self, pmr_dir='/root/pmr_logs', meta_store='/root/meta_patterns.json'):
        self.pmr_dir = pmr_dir
        self.meta_store = meta_store
        self.taxonomy = {
            "EnvironmentStateDrift": ["ModuleNotFoundError", "version mismatch", "dependency conflict", "apk add", "env var"],
            "ResourceExhaustion": ["MemoryError", "timeout", "disk full", "OOM", "CPU spike"],
            "AuthFragility": ["401 Unauthorized", "403 Forbidden", "token expired", "MFA bypass", "permission denied"],
            "InterfaceLatency": ["Rate limit", "429", "Too Many Requests", "throttling", "slow response"],
            "LogicDrift": ["Unexpected output", "assertion failed", "wrong value", "cognitive amnesia"]
        }

    def load_pmrs(self):
        pmrs = []
        if not os.path.exists(self.pmr_dir):
            return pmrs
        for file in os.listdir(self.pmr_dir):
            if file.endswith('.json'):
                with open(os.path.join(self.pmr_dir, file), 'r') as f:
                    pmrs.append(json.load(f))
        return pmrs

    def synthesize(self):
        pmrs = self.load_pmrs()
        if not pmrs:
            return {"status": "no_data", "message": "No PMR logs found to synthesize."}

        all_failures = []
        for pmr in pmrs:
            # Extract failure markers from MCT telemetry in PMR
            failures = pmr.get('failures', [])
            all_failures.extend(failures)

        # Map failures to taxonomy
        pattern_counts = Counter()
        for failure in all_failures:
            for category, markers in self.taxonomy.items():
                if any(marker.lower() in failure.lower() for marker in markers):
                    pattern_counts[category] += 1

        # Identify "Meta-Fragilities" (patterns occurring across multiple missions)
        meta_fragilities = {cat: count for cat, count in pattern_counts.items() if count >= 2}
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "missions_analyzed": len(pmrs),
            "meta_fragilities": meta_fragilities,
            "dominant_pathology": max(meta_fragilities, key=meta_fragilities.get) if meta_fragilities else "None"
        }

        with open(self.meta_store, 'w') as f:
            json.dump(report, f, indent=4)

        return report

if __name__ == "__main__":
    mps = MetaPatternSynthesizer()
    print(json.dumps(mps.synthesize(), indent=2))
