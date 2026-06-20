import re

class AmbientSignalSynthesizer:
    """
    Evolves recovery from 'Explicit Reporting' to 'Passive Sensing'.
    Analyzes ambient signals (emails, notifications) to detect implicit recovery wins.
    """
    
    RECOVERY_PATTERNS = {
        "password_change": [
            r"password.*?changed",
            r"security.*?update.*?password",
            r"your.*?password.*?was.*?successfully.*?updated"
        ],
        "mfa_enrollment": [
            r"mfa.*?enabled",
            r"two-factor.*?authentication.*?activated",
            r"new.*?security.*?key.*?added",
            r"authenticator.*?app.*?linked"
        ],
        "session_termination": [
            r"all.*?sessions.*?signed.*?out",
            r"active.*?sessions.*?flushed",
            r"security.*?reset.*?all.*?devices"
        ],
        "account_recovery": [
            r"account.*?successfully.*?recovered",
            r"access.*?restored.*?to.*?your.*?account"
        ]
    }

    def __init__(self):
        self.recovery_heatmap = {}

    def analyze_signal(self, source, content):
        """
        Analyzes a piece of text (email subject/body or notification)
        and maps it to a recovery victory.
        """
        detections = []
        content_lower = content.lower()
        
        for category, patterns in self.RECOVERY_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, content_lower):
                    detections.append(category)
                    break
        
        return detections

    def synthesize_victory(self, asset_name, signals):
        """
        Transforms raw detections into a quantified victory report.
        """
        if not signals:
            return None
            
        return {
            "asset": asset_name,
            "signals": signals,
            "impact": "Implicitly Verified",
            "status": "SIGNAL_DETECTED"
        }

if __name__ == "__main__":
    # Test the synthesizer
    ass = AmbientSignalSynthesizer()
    test_signals = [
        "Your Chase bank password has been successfully updated",
        "New MFA device added to your Microsoft account",
        "All active sessions have been signed out for security"
    ]
    
    for s in test_signals:
        print(f"Signal: {s} -> Detections: {ass.analyze_signal('test', s)}")
