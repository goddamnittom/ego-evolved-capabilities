import json
import re

def map_blast_radius(alerts):
    radius = {
        "access_methods": set(),
        "devices": set(),
        "third_party_apps": set(),
        "timeline_events": []
    }
    
    for alert in alerts:
        text = alert.get("preview", "").lower()
        date = alert.get("date", "Unknown")
        
        if "app password" in text:
            radius["access_methods"].add("App Password (Bypasses 2FA)")
        if "new sign-in" in text:
            radius["access_methods"].add("Session Hijacking/Credential Use")
            # Try to extract device
            device_match = re.search(r"on\s+([a-zA-Z\s]+(?:Tab|Phone|Mac|Windows|onn|Galaxy)[a-zA-Z\s\d]*)", text)
            if device_match:
                radius["devices"].add(device_match.group(1).strip())
        if "allowed" in text and "access" in text:
            app_match = re.search(r"allowed\s+([a-zA-Z]+)\s+access", text)
            if app_match:
                radius["third_party_apps"].add(app_match.group(1).strip())
        
        radius["timeline_events"].append({"date": date, "event": text[:100]})
        
    return {
        "access_methods": list(radius["access_methods"]),
        "devices": list(radius["devices"]),
        "third_party_apps": list(radius["third_party_apps"]),
        "event_count": len(radius["timeline_events"])
    }

if __name__ == "__main__":
    # Example usage with data from current session
    sample_alerts = [
        {"preview": "[image: Google] A new sign-in on onn.", "date": "May 10"},
        {"preview": "[image: Google] App password created to sign", "date": "May 10"},
        {"preview": "You allowed Composio access", "date": "May 15"},
        {"preview": "A new sign-in on Galaxy Tab S", "date": "May 18"},
        {"preview": "New sign-in to your account", "date": "May 24"},
    ]
    print(json.dumps(map_blast_radius(sample_alerts), indent=2))
