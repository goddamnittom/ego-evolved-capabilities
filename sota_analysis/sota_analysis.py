import json
import re

with open("/root/knowledge_base/sota_signals.json") as f:
    data = json.load(f)

# Find keywords
topics = {
    'agents': [],
    'reasoning': [],
    'memory': [],
    'edge': [],
    'domain_specific': []
}

for k, v in data.items():
    title = v.get("title", "").lower()
    summary = v.get("summary", "").lower()
    text = title + " " + summary

    if "agent" in text or "codex" in text or "warp" in text or "endava" in text:
        topics['agents'].append(v)
    if "reasoning" in text or "conjecture" in text or "geometry" in text or "logic" in text:
        topics['reasoning'].append(v)
    if "dreaming" in text or "memory" in text:
        topics['memory'].append(v)
    if "edge" in text or "wasmer" in text:
        topics['edge'].append(v)
    if "rosalind" in text or "biodefense" in text or "domain" in text:
        topics['domain_specific'].append(v)

print("--- SOTA Signals Analysis ---")
for t, signals in topics.items():
    print(f"\nCategory: {t.upper()} ({len(signals)} signals)")
    for s in signals[:2]: # First 2
        print(f" - {s['title']}")

