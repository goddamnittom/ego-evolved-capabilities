import re
import json
from datetime import datetime

class HardeningSignalSynthesizer:
    """
    HSS: Hardening Signal Synthesizer
    Transitions recovery from manual reporting to proactive victory detection.
    Scans communication channels for Positive Hardening Markers (PHMs).
    """
    def __init__(self):
        self.phm_patterns = {
            "password_change": [
                r"password has been changed",
                r"password successfully updated",
                r"changed your password",
                r"security update: password"
            ],
            "mfa_enabled": [
                r"two-factor authentication enabled",
                r"2FA has been activated",
                r"multi-factor authentication set up",
                r"MFA successfully added"
            ],
            "session_flush": [
                r"all other sessions have been signed out",
                r"logged out of all devices",
                r"security alert: all sessions terminated"
            ],
            "recovery_email_update": [
                r"recovery email address has been changed",
                r"updated your recovery contact"
            ]
        }

    def analyze_signal(self, source, content):
        """
        Analyzes a signal (email body, notification text, SMS) for hardening markers.
        """
        detected_markers = []
        for marker, patterns in self.phm_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    detected_markers.append(marker)
                    break
        
        if detected_markers:
            return {
                "status": "VICTORY_DETECTED",
                "markers": detected_markers,
                "timestamp": datetime.now().isoformat(),
                "source": source
            }
        return {"status": "NO_MARKER"}

    def synthesize_integrity_gain(self, markers):
        """
        Calculates the psychological and technical gain based on detected markers.
        """
        gains = {
            "password_change": "Attacker's legacy password nullified. Entry vector closed.",
            "mfa_enabled": "Account fortified. Unauthorized access now requires physical token.",
            "session_flush": "Attacker's active sessions terminated. All ghosts evicted.",
            "recovery_email_update": "Recovery chain reclaimed. Backdoor eliminated."
        }
        return [gains[m] for m in markers if m in gains]

if __name__ == "__main__":
    # Test Case
    hss = HardeningSignalSynthesizer()
    test_content = "Your bank password has been changed successfully. If you did not do this, contact us."
    result = hss.analyze_signal("email", test_content)
    print(json.dumps(result, indent=2))
