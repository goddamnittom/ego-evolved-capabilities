import json
import os

MANIFEST_PATH = '/root/hardening_manifest.json'

class SOPE:
    def __init__(self):
        self.risk_weights = {
            "High": 3,
            "Medium": 2,
            "Low": 1
        }

    def load_manifest(self):
        if not os.path.exists(MANIFEST_PATH):
            return {}
        with open(MANIFEST_PATH, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # Handle the case where JSON might be malformed (like the trailing brace issue)
                with open(MANIFEST_PATH, 'r') as f:
                    content = f.read().strip()
                    if not content.endswith('}'):
                        content += '}'
                    return json.loads(content)

    def calculate_priority(self, asset_data):
        risk = asset_data.get('risk', 'Low')
        status = asset_data.get('status', 'PENDING')
        if status == 'VERIFIED':
            return 0
        return self.risk_weights.get(risk, 1)

    def get_hardening_sprint(self):
        data = self.load_manifest()
        assets = data.get('assets', {})
        if not assets:
            return "No assets found in manifest."

        priorities = []
        for asset, info in assets.items():
            score = self.calculate_priority(info)
            priorities.append((asset, score))

        priorities.sort(key=lambda x: x[1], reverse=True)
        
        if not priorities or priorities[0][1] == 0:
            return "All assets VERIFIED. Fortress complete."

        top_asset = priorities[0][0]
        return f"URGENT: {top_asset} is the highest risk pending asset. Immediate verification recommended."

if __name__ == "__main__":
    sope = SOPE()
    print(sope.get_hardening_sprint())
