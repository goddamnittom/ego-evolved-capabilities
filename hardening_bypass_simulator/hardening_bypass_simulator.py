import json
import os

class HardeningBypassSimulator:
    def __init__(self, manifest_path='/root/hardening_manifest.json', citg_path='/root/cross_identity_trust_graph.json'):
        self.manifest_path = manifest_path
        self.citg_path = citg_path

    def load_json(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {}

    def simulate_bypasses(self):
        manifest = self.load_json(self.manifest_path)
        citg = self.load_json(self.citg_path)
        
        leakages = []
        
        # Identify hardened assets
        hardened_assets = [asset for asset, data in manifest.items() if data.get('status') == 'VERIFIED']
        
        # Check CITG for recovery paths to these assets
        # Simplified logic: If A is the root of trust for B, and B is hardened but A is NOT, that's a leakage.
        for asset, connections in citg.items():
            for connection in connections:
                target = connection.get('target')
                rel = connection.get('relationship')
                
                if rel == 'recovery_root' and target in hardened_assets:
                    if asset not in hardened_assets:
                        leakages.append({
                            'source': asset,
                            'target': target,
                            'risk': 'High',
                            'description': f'Asset {target} is hardened, but its recovery root {asset} is NOT. Attacker can reset {target} via {asset}.'
                        })
        
        return leakages

if __name__ == "__main__":
    hbs = HardeningBypassSimulator()
    results = hbs.simulate_bypasses()
    print(json.dumps(results, indent=2))
