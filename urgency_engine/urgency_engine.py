import datetime

class UrgencyEngine:
    def __init__(self, base_unread, current_unread, silence_duration_heartbeats):
        self.base_unread = base_unread
        self.current_unread = current_unread
        self.silence_duration = silence_duration_heartbeats

    def calculate_urgency_level(self):
        bleed_rate = self.current_unread - self.base_unread
        
        if self.silence_duration > 5:
            return "CATASTROPHIC" # User has essentially abandoned the account
        elif bleed_rate > 100:
            return "ACTIVE_EXFILTRATION" # High velocity attack
        elif bleed_rate > 0:
            return "PERSISTENT_THREAT" # Low velocity, but attacker is still active
        else:
            return "STAGNANT_COMPROMISE" # Attacker is in, but quiet

    def get_narrative_tone(self):
        level = self.calculate_urgency_level()
        tones = {
            "CATASTROPHIC": "The window for recovery is closing. This is no longer a cleanup; it is a salvage operation.",
            "ACTIVE_EXFILTRATION": "The attacker is moving fast. Every second we wait is more data lost.",
            "PERSISTENT_THREAT": "The door is open and they are still walking through it. We must lock it now.",
            "STAGNANT_COMPROMISE": "The attacker is entrenched and waiting. We have the advantage of time, but only if we act now."
        }
        return tones.get(level, "Urgency is high.")

if __name__ == "__main__":
    # Example usage
    engine = UrgencyEngine(13933, 13934, 3)
    print(f"Level: {engine.calculate_urgency_level()}")
    print(f"Tone: {engine.get_narrative_tone()}")
