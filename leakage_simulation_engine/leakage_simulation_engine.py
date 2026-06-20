import json
import os

class LeakageSimulationEngine:
    def __init__(self, manifest_path='/root/hardening_manifest.json', blast_radius_path='/root/blast_radius_map.json'):
        self.manifest_path = manifest_path
        self.blast_radius_path = blast_radius_path

    def load_data(self):
        manifest = {}
        if os.path.exists(self.manifest_path):
            with open(self.manifest_path, 'r') as f:
                manifest = json.load(f)
        
        blast_radius = {}
        if os.path.exists(self.blast_radius_path):
            with open(self.blast_radius_path, 'r') as f:
                blast_radius = json.load(f)
        
        return manifest, blast_radius

    def simulate_attack_paths(self):
        manifest, blast_radius = self.load_data()
        if not manifest or not blast_radius:
            return {"error": "Insufficient data for simulation. Manifest or Blast Radius map missing."}

        leakages = []
        critical_paths = []
        
        # Analyze every asset in the blast radius
        for asset, data in blast_radius.items():
            # Check if the asset is listed in the manifest and if it's fully 'verified'
            status = manifest.get(asset, {}).get('status', 'unsecured')
            
            if status != 'verified':
                # If not verified, it's a potential leakage point
                leakages.append(asset)
                
                # Check dependencies: if this asset is a hub for others, it's a critical path
                dependencies = data.get('downstream', [])
                if dependencies:
                    critical_paths.append({
                        "source": asset,
                        "targets": dependencies,
                        "risk": "High" if status == 'unsecured' else "Medium"
                    })

        return {
            "leakage_score": len(leakages) / len(blast_radius) if blast_radius else 0,
            "leakage_points": leakages,
            "critical_paths": critical_paths,
            "status": "Vulnerable" if leakages else "Hardened"
        }

if __name__ == "__main__":
    lse = LeakageSimulationEngine()
    print(json.dumps(lse.simulate_attack_paths(), indent=2))
