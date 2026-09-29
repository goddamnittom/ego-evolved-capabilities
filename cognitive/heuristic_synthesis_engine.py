import json
import os
from datetime import datetime

class HeuristicSynthesisEngine:
    def __init__(self, telemetry_path='/root/mission_control_telemetry.json', heuristic_lib_path='/root/atp_heuristics.json'):
        self.telemetry_path = telemetry_path
        self.heuristic_lib_path = heuristic_lib_path
        self.ensure_files_exist()

    def ensure_files_exist(self):
        for path in [self.telemetry_path, self.heuristic_lib_path]:
            if not os.path.exists(path):
                with open(path, 'w') as f:
                    json.dump({}, f)

    def load_json(self, path):
        with open(path, 'r') as f:
            return json.load(f)

    def save_json(self, path, data):
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    def synthesize_from_pivots(self):
        telemetry = self.load_json(self.telemetry_path)
        heuristics = self.load_json(self.heuristic_lib_path)
        
        new_synthesized = 0
        
        for mission_id, data in telemetry.items():
            pivots = data.get('auto_pivots', [])
            for pivot in pivots:
                # Check if this pivot pattern is already a stable heuristic
                pattern = pivot.get('pattern')
                resolution = pivot.get('resolution')
                
                if pattern and resolution:
                    if pattern not in heuristics:
                        # Synthesize a new experimental heuristic
                        heuristics[pattern] = {
                            'resolution': resolution,
                            'status': 'EXPERIMENTAL',
                            'success_count': 1,
                            'first_seen': datetime.now().isoformat(),
                            'last_seen': datetime.now().isoformat()
                        }
                        new_synthesized += 1
                    elif heuristics[pattern]['status'] == 'EXPERIMENTAL':
                        # Increment success count for experimental heuristics
                        heuristics[pattern]['success_count'] += 1
                        heuristics[pattern]['last_seen'] = datetime.now().isoformat()
                        
                        # Promote to STABLE if threshold reached (e.g., 3 successes)
                        if heuristics[pattern]['success_count'] >= 3:
                            heuristics[pattern]['status'] = 'STABLE'
                            
        if new_synthesized > 0:
            self.save_json(self.heuristic_lib_path, heuristics)
            
        return new_synthesized, heuristics

if __name__ == "__main__":
    hse = HeuristicSynthesisEngine()
    count, lib = hse.synthesize_from_pivots()
    print(f"Synthesized {count} new heuristics. Total library size: {len(lib)}")
