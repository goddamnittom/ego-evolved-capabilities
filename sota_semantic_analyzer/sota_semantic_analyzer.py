import json
import os

def analyze_signals():
    signals_path = '/root/knowledge_base/sota_signals.json'
    proposals_path = '/root/strategic_proposals.json'
    
    if not os.path.exists(signals_path):
        print("Signals file not found.")
        return

    with open(signals_path, 'r') as f:
        signals = json.load(f)

    # Define a set of high-impact keywords for architectural pivot detection
    pivot_keywords = {
        "codex": "Standardization on Codex for enterprise-scale workflow orchestration",
        "agentic organization": "Shift toward Agentic Organizations (multi-agent swarms replacing linear pipelines)",
        "gpt-5.5": "Integration of GPT-5.5 for edge-native/WASM orchestration",
        "dreaming": "Asynchronous 'Dreaming' memory architectures for off-cycle synthesis",
        "rosalind": "Hyper-specialized domain-specific frontier models (e.g., Biodefense/Life Sciences)",
        "reasoning": "Breakthroughs in OOD (Out-Of-Distribution) reasoning and formal mathematical proof",
        "orchestrator": "Transition from autocomplete tools to comprehensive workflow orchestrators"
    }

    detected_pivots = []
    
    for url, data in signals.items():
        summary = data.get('summary', '').lower()
        title = data.get('title', '').lower()
        text = summary + " " + title
        
        for kw, description in pivot_keywords.items():
            if kw in text:
                detected_pivots.append({
                    "keyword": kw,
                    "description": description,
                    "source": data.get('title'),
                    "url": url
                })

    if not detected_pivots:
        print("No significant architectural pivots detected.")
        return

    # Consolidate unique pivots
    unique_pivots = {}
    for p in detected_pivots:
        unique_pivots[p['keyword']] = p

    # Load existing proposals
    proposals = []
    if os.path.exists(proposals_path):
        with open(proposals_path, 'r') as f:
            try:
                proposals = json.load(f)
            except:
                proposals = []

    # Generate new proposals if not already present
    new_proposals_count = 0
    for kw, p in unique_pivots.items():
        proposal_id = f"PROPOSAL-{len(proposals) + 1:03d}"
        # Check if a similar proposal already exists
        if not any(kw in str(prop).lower() for prop in proposals):
            proposals.append({
                "id": proposal_id,
                "title": f"Strategic Pivot: {p['description']}",
                "trigger_signal": p['source'],
                "impact": "High",
                "status": "Proposed",
                "description": f"Based on SOTA signal {p['url']}, transition the cognitive architecture to incorporate {p['description']}."
            })
            new_proposals_count += 1

    with open(proposals_path, 'w') as f:
        json.dump(proposals, f, indent=2)

    print(f"Analysis complete. Detected {len(unique_pivots)} pivot types. Added {new_proposals_count} new strategic proposals to {proposals_path}.")

if __name__ == "__main__":
    analyze_signals()
