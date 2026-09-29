import json
import os
from datetime import datetime

class ActorBehavioralProfiler:
    def __init__(self, profiles_path='/root/actor_profiles.json'):
        self.profiles_path = profiles_path
        self.profiles = self._load_profiles()

    def _load_profiles(self):
        if os.path.exists(self.profiles_path):
            with open(self.profiles_path, 'r') as f:
                return json.load(f)
        return {}

    def _save_profiles(self):
        with open(self.profiles_path, 'w') as f:
            json.dump(self.profiles, f, indent=4)

    def ingest_event(self, event_data):
        """
        Ingests a security event and updates the corresponding actor profile.
        event_data: { 'actor_id': '...', 'timestamp': '...', 'action': '...', 'target': '...', 'marker': '...' }
        """
        actor_id = event_data.get('actor_id', 'unknown_actor')
        if actor_id not in self.profiles:
            self.profiles[actor_id] = {
                'first_seen': event_data.get('timestamp'),
                'last_seen': event_data.get('timestamp'),
                'actions': [],
                'targets': [],
                'markers': [],
                'pattern_score': 0
            }
        
        profile = self.profiles[actor_id]
        profile['last_seen'] = event_data.get('timestamp')
        profile['actions'].append(event_data.get('action'))
        profile['targets'].append(event_data.get('target'))
        if event_data.get('marker'):
            profile['markers'].append(event_data.get('marker'))
        
        profile['pattern_score'] = len(set(profile['markers']))
        self._save_profiles()
        return profile

    def predict_next_move(self, actor_id):
        """
        Predicts the next target/action based on the actor's history.
        """
        if actor_id not in self.profiles:
            return "Insufficient data to predict."
        
        profile = self.profiles[actor_id]
        if not profile['actions']:
            return "No behavioral history."
            
        most_common_action = max(set(profile['actions']), key=profile['actions'].count)
        most_common_target = max(set(profile['targets']), key=profile['targets'].count)
        
        return f"Predicted move: {most_common_action} on {most_common_target} based on historical frequency."

if __name__ == "__main__":
    profiler = ActorBehavioralProfiler()
    test_event = {
        'actor_id': 'attacker_alpha',
        'timestamp': datetime.now().isoformat(),
        'action': 'password_reset',
        'target': 'gmail',
        'marker': 'rapid_fire_requests'
    }
    print(f"Ingesting event... Result: {profiler.ingest_event(test_event)}")
    print(f"Prediction: {profiler.predict_next_move('attacker_alpha')}")
