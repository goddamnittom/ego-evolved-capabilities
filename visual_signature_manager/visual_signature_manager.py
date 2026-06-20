import json
import os

class VisualSignatureManager:
    """
    Visual Signature Cataloguer (VSC)
    Catalogues visual threat signatures (e.g., phishing page layouts) and correlates them with actor IDs.
    """
    def __init__(self, database_path="/root/visual_signatures.json"):
        self.database_path = database_path
        self.signatures = self._load_db()

    def _load_db(self):
        if os.path.exists(self.database_path):
            with open(self.database_path, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def catalogue_signature(self, signature_id, visual_markers, actor_id=None):
        """
        Adds a visual signature to the database.
        """
        self.signatures[signature_id] = {
            "markers": visual_markers, 
            "actor_id": actor_id,
            "timestamp": "2026-06-01T20:30:00Z"
        }
        self._save_db()
        return f"Catalogued {signature_id} with markers {visual_markers}"

    def correlate_signature(self, current_markers):
        """
        Correlates current visual markers against known signatures to identify the actor.
        """
        for sid, data in self.signatures.items():
            if set(current_markers).intersection(set(data["markers"])):
                return sid, data["actor_id"]
        return None, None

    def _save_db(self):
        with open(self.database_path, 'w') as f:
            json.dump(self.signatures, f, indent=2)

if __name__ == "__main__":
    vsc = VisualSignatureManager()
    vsc.catalogue_signature("SIGNATURE_01", ["blue_header", "fake_google_logo", "urgency_banner"], "ACTOR_ALPHA")
    print(vsc.correlate_signature(["fake_google_logo", "wrong_font"]))
