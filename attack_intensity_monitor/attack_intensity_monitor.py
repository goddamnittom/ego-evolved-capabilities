import json
import os
from datetime import datetime, timedelta

class AttackIntensityMonitor:
    def __init__(self, log_file='/root/attack_signals.json'):
        self.log_file = log_file
        self.signals = self._load_signals()

    def _load_signals(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                return json.load(f)
        return []

    def record_signal(self, source, target, signal_type='unauthorized_login'):
        timestamp = datetime.now().isoformat()
        self.signals.append({
            'timestamp': timestamp,
            'source': source,
            'target': target,
            'type': signal_type
        })
        with open(self.log_file, 'w') as f:
            json.dump(self.signals, f)

    def calculate_velocity(self, window_minutes=60):
        now = datetime.now()
        window_start = now - timedelta(minutes=window_minutes)
        
        recent_signals = [
            s for s in self.signals 
            if datetime.fromisoformat(s['timestamp']) > window_start
        ]
        
        velocity = len(recent_signals)
        intensity = 'LOW'
        if velocity >= 5: intensity = 'CRITICAL'
        elif velocity >= 3: intensity = 'HIGH'
        elif velocity >= 1: intensity = 'MODERATE'
        
        return {
            'velocity': velocity,
            'window_minutes': window_minutes,
            'intensity': intensity,
            'targets': list(set([s['target'] for s in recent_signals]))
        }

if __name__ == "__main__":
    aim = AttackIntensityMonitor()
    # Simulating the Chime signals from the heartbeat
    aim.record_signal('Unknown', 'Chime')
    aim.record_signal('Unknown', 'Chime')
    print(json.dumps(aim.calculate_velocity(), indent=2))
