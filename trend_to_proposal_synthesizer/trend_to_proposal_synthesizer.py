import json
import os
from datetime import datetime, timedelta

class TrendToProposalSynthesizer:
    def __init__(self, signal_log_path='/root/csi_signals.json', proposals_path='/root/strategic_proposals.json'):
        self.signal_log_path = signal_log_path
        self.proposals_path = proposals_path

    def _load_json(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return []

    def _save_json(self, path, data):
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    def synthesize(self):
        signals = self._load_json(self.signal_log_path)
        if not signals:
            return "No signals to analyze."

        # Cluster signals by keyword/topic (simulated clustering)
        clusters = {}
        for s in signals:
            text = s.get('text', '').lower()
            # Basic keyword extraction for demonstration
            keywords = ['ai', 'gpu', 'webgpu', 'security', 'finance', 'automation', 'rust', 'python']
            for kw in keywords:
                if kw in text:
                    clusters.setdefault(kw, []).append(s)

        new_proposals = []
        for topic, matches in clusters.items():
            if len(matches) >= 3:  # Threshold for a "trend"
                hypothesis = f"Emerging trend detected in {topic} based on {len(matches)} signals. High probability of strategic ROI."
                proposal = {
                    "id": f"prop_{datetime.now().strftime('%Y%m%d%H%M%S')}_{topic}",
                    "topic": topic,
                    "hypothesis": hypothesis,
                    "confidence": 0.85,
                    "timestamp": datetime.now().isoformat(),
                    "status": "DRAFT",
                    "source_signals": [m.get('id') for m in matches]
                }
                new_proposals.append(proposal)

        if new_proposals:
            all_proposals = self._load_json(self.proposals_path)
            all_proposals.extend(new_proposals)
            self._save_json(self.proposals_path, all_proposals)
            return f"Synthesized {len(new_proposals)} new strategic proposals from ambient trends."
        
        return "No significant trends detected."

if __name__ == "__main__":
    tps = TrendToProposalSynthesizer()
    print(tps.synthesize())
