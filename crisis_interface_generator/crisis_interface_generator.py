import json

class CrisisInterfaceGenerator:
    """
    Generates specialized, high-urgency UI configurations for crisis management.
    Aggregates data from PPE, SIA, BRV, and HVM to create a 'War Room' dashboard.
    """
    def __init__(self):
        self.urgency_levels = {
            "LOW": {"color": "primary", "icon": "info", "style": "body"},
            "MEDIUM": {"color": "secondary", "icon": "warning", "style": "title"},
            "HIGH": {"color": "error", "icon": "bolt", "style": "headline"},
            "CRITICAL": {"color": "error", "icon": "shield", "style": "headline"}
        }

    def generate_war_room_dashboard(self, threat_level, ppe_score, sia_status, blast_radius_size, critical_assets):
        config = self.urgency_levels.get(threat_level, self.urgency_levels["LOW"])
        
        dashboard = {
            "type": "column",
            "children": [
                {
                    "type": "alert",
                    "title": f"🚨 CRISIS MODE: {threat_level}",
                    "message": "High-criticality security event detected. Switching to War Room Orchestration.",
                    "severity": "error" if threat_level in ["HIGH", "CRITICAL"] else "warning"
                },
                {
                    "type": "row",
                    "children": [
                        {
                            "type": "stat",
                            "value": str(ppe_score),
                            "label": "Pivot Prob.",
                            "description": "PPE Engine"
                        },
                        {
                            "type": "stat",
                            "value": sia_status,
                            "label": "Session Int.",
                            "description": "SIA Auditor"
                        },
                        {
                            "type": "stat",
                            "value": str(blast_radius_size),
                            "label": "Blast Radius",
                            "description": "BRV Mapper"
                        }
                    ]
                },
                {
                    "type": "divider"
                },
                {
                    "type": "text",
                    "value": "Critical Assets at Risk",
                    "style": "title",
                    "bold": True
                },
                {
                    "type": "list",
                    "items": critical_assets
                },
                {
                    "type": "button",
                    "label": "Execute Immediate Lockdown",
                    "action": {"type": "callback", "event": "crisis_lockdown"},
                    "variant": "filled"
                }
            ]
        }
        return dashboard

# Example usage
if __name__ == "__main__":
    cig = CrisisInterfaceGenerator()
    print(json.dumps(cig.generate_war_room_dashboard("CRITICAL", 1.0, "COMPROMISED", "MAX", ["Primary Email", "Browser Vault", "Chime"]), indent=2))
