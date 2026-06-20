import json

class IoCEvidenceHunter:
    def __init__(self):
        self.high_value_targets = [
            "password changed",
            "security alert",
            "new sign-in",
            "unauthorized",
            "recovery email",
            "bank transfer",
            "payment confirmed",
            "verification code"
        ]

    def compile_dossier(self, search_results):
        dossier = {
            "critical_hits": [],
            "warning_hits": [],
            "summary": ""
        }
        
        for email in search_results:
            subject = email.get('subject', '').lower()
            sender = email.get('sender', '').lower()
            
            is_critical = any(target in subject for target in ["password", "security", "unauthorized", "transfer"])
            
            if is_critical:
                dossier["critical_hits"].append(email)
            else:
                dossier["warning_hits"].append(email)
        
        dossier["summary"] = f"Found {len(dossier['critical_hits'])} critical security indicators and {len(dossier['warning_hits'])} warnings."
        return dossier

hunter = IoCEvidenceHunter()
