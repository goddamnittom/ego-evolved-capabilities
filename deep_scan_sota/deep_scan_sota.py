import json

try:
    with open('/root/knowledge_base/sota_signals.json', 'r') as f:
        data = json.load(f)

    keywords = ["Codex", "Endava", "Wasmer", "GPT-Rosalind", "Dreaming", "agent", "planning", "reasoning", "orchestrat"]
    relevant_signals = []

    # Handle dictionary format
    if isinstance(data, dict):
        for key, item in data.items():
            text = json.dumps(item).lower()
            if any(kw.lower() in text for kw in keywords):
                relevant_signals.append(item)

    print(f"Extracted {len(relevant_signals)} signals matching key architectural pivots.")
    if len(relevant_signals) > 0:
        for i, sig in enumerate(relevant_signals[:10]):
            print(f"\nSignal {i+1}:")
            print(json.dumps(sig, indent=2))

except Exception as e:
    print(f"Error reading sota_signals.json: {e}")

