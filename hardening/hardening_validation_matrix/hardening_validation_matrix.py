import json

# Simplified mapping of hardening controls to MITRE ATT&CK-like techniques
CONTROL_MAPPING = {
    "Financials (MFA/Phone)": {
        "techniques": ["T1556.006 (Modify Authentication Process: Multi-Factor Authentication)", "T1098 (Account Manipulation)"],
        "impact": "Prevents account takeover via MFA reset/bypass"
    },
    "Financials (Password/Sessions)": {
        "techniques": ["T1539 (Steal Web Session Cookie)", "T1078 (Valid Accounts)"],
        "impact": "Neutralizes session hijacking and stolen credential usage"
    },
    "Identities (MS/Mozilla)": {
        "techniques": ["T1555 (Credentials from Password Stores)", "T1098.001 (Account Manipulation: Add Account)"],
        "impact": "Prevents lateral movement and credential harvesting"
    },
    "Dev Tools": {
        "techniques": ["T1552.001 (Unsecured Credentials: Credentials in Files)", "T1078.004 (Valid Accounts: Cloud Accounts)"],
        "impact": "Protects API keys, SSH keys, and cloud infrastructure"
    }
}

def calculate_coverage(verified_assets):
    total_techniques = sum(len(v['techniques']) for v in CONTROL_MAPPING.values())
    covered_techniques = 0
    report = []

    for asset, status in verified_assets.items():
        if status == "VERIFIED":
            mapping = CONTROL_MAPPING.get(asset, {})
            covered_techniques += len(mapping.get('techniques', []))
            report.append(f"✅ {asset}: Mitigates {mapping.get('techniques', [])}")
        else:
            report.append(f"❌ {asset}: Vulnerable to {CONTROL_MAPPING.get(asset, {}).get('techniques', 'Unknown')}")

    coverage_pct = (covered_techniques / total_techniques) * 100 if total_techniques > 0 else 0
    return coverage_pct, report

if __name__ == "__main__":
    # Mock state from current HVM
    current_hvm = {
        "Financials (MFA/Phone)": "VERIFIED",
        "Financials (Password/Sessions)": "VERIFIED",
        "Identities (MS/Mozilla)": "PENDING",
        "Dev Tools": "PENDING"
    }
    
    score, details = calculate_coverage(current_hvm)
    print(f"Overall Security Coverage: {score:.2f}%")
    print("\nDetailed Validation:")
    for line in details:
        print(line)
