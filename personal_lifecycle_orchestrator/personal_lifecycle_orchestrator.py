import json
import os
import re
from datetime import datetime

class PersonalLifecycleOrchestrator:
    def __init__(self, state_file='/root/life_state.json', dashboard_file='/root/life_dashboard.html'):
        self.state_file = state_file
        self.dashboard_file = dashboard_file
        self.state = self._load_state()

    def _load_state(self):
        default_state = {
            "last_updated": None,
            "signals": [],
            "administrative": {
                "safelink_recertification_due": False,
                "safelink_data_limit_alert": False,
                "tasks": []
            },
            "financial": {
                "verification_codes": [],
                "tasks": []
            },
            "social": {
                "tinder_matches": [],
                "tasks": []
            },
            "history": []
        }

        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    saved = json.load(f)
                    # Merge keys to ensure backward compatibility
                    for key in default_state:
                        if key not in saved:
                            saved[key] = default_state[key]
                    if "financial" not in saved:
                        saved["financial"] = default_state["financial"]
                    return saved
            except Exception:
                pass
        return default_state

    def save_state(self):
        self.state["last_updated"] = datetime.now().isoformat()
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def process_sms(self, sms_id, sender, body, timestamp):
        # Prevent duplicates
        for sig in self.state["signals"]:
            if sig.get("id") == sms_id:
                return

        signal = {
            "id": sms_id,
            "sender": sender,
            "body": body,
            "timestamp": timestamp,
            "parsed_at": datetime.now().isoformat()
        }
        self.state["signals"].append(signal)

        body_lower = body.lower()

        # 1. SafeLink Recertification
        if "safelink" in body_lower and "recertif" in body_lower:
            self.state["administrative"]["safelink_recertification_due"] = True
            link_match = re.search(r'https?://[^\s]+', body)
            link = link_match.group(0) if link_match else "https://www.safelinkwireless.com"
            
            task = {
                "id": f"admin_recert_{sms_id}",
                "title": "Complete SafeLink Recertification",
                "description": "Annual recertification is required to maintain free talk, text, and data benefits.",
                "url": link,
                "status": "PENDING",
                "urgency": "HIGH",
                "created_at": datetime.now().isoformat()
            }
            if not any(t["id"] == task["id"] for t in self.state["administrative"]["tasks"]):
                self.state["administrative"]["tasks"].append(task)

        # 2. SafeLink Add Data
        elif "safelink" in body_lower and "data" in body_lower:
            self.state["administrative"]["safelink_data_limit_alert"] = True
            link_match = re.search(r'https?://[^\s]+', body)
            link = link_match.group(0) if link_match else "https://www.safelinkwireless.com"
            
            task = {
                "id": f"admin_data_{sms_id}",
                "title": "Top up SafeLink Data",
                "description": "SafeLink data alert received. Buy more data or check balance online.",
                "url": link,
                "status": "PENDING",
                "urgency": "MEDIUM",
                "created_at": datetime.now().isoformat()
            }
            if not any(t["id"] == task["id"] for t in self.state["administrative"]["tasks"]):
                self.state["administrative"]["tasks"].append(task)

        # 3. Tinder Match
        elif "tinder" in body_lower and "matched" in body_lower:
            match_name = "Someone"
            name_match = re.search(r"matched with (\w+)", body, re.IGNORECASE)
            if name_match:
                match_name = name_match.group(1)
                
            link_match = re.search(r'https?://[^\s]+', body)
            link = link_match.group(0) if link_match else "https://go.tinder.com"

            match_info = {
                "id": f"tinder_match_{sms_id}",
                "name": match_name,
                "url": link,
                "matched_at": timestamp,
                "status": "NEW"
            }
            if not any(m["id"] == match_info["id"] for m in self.state["social"]["tinder_matches"]):
                self.state["social"]["tinder_matches"].append(match_info)
                
            task = {
                "id": f"social_message_{sms_id}",
                "title": f"Message {match_name} on Tinder",
                "description": f"You matched with {match_name}. Send a creative opening message to establish contact.",
                "url": link,
                "status": "PENDING",
                "urgency": "HIGH",
                "created_at": datetime.now().isoformat()
            }
            if not any(t["id"] == task["id"] for t in self.state["social"]["tasks"]):
                self.state["social"]["tasks"].append(task)

        # 4. Financial Verification Codes
        # Look for verification code, access code, pin, etc.
        code_patterns = [
            r'(\b\d{4,8}\b)\s+(?:is|has|your|code)',
            r'(?:code|access|pin|verification)\s*(?:is|:|code)?\s*(\b\d{4,8}\b)',
            r'(\b\d{4,8}\b)\s*is your'
        ]
        
        is_verification = False
        code_val = None
        for pattern in code_patterns:
            m = re.search(pattern, body_lower)
            if m:
                # Also find in actual casing
                m_actual = re.search(pattern, body, re.IGNORECASE)
                if m_actual:
                    code_val = m_actual.group(1)
                    is_verification = True
                    break

        # If it doesn't match the general pattern, check specific known code SMS
        if not is_verification:
            if "plaid" in body_lower or "earnin" in body_lower or "klover" in body_lower or "floatme" in body_lower or "gerald" in body_lower or "possible" in body_lower or "credit genie" in body_lower or "lenme" in body_lower or "grant" in body_lower or "chime" in body_lower:
                m = re.search(r'\b\d{4,7}\b', body)
                if m:
                    code_val = m.group(0)
                    is_verification = True

        if is_verification and code_val:
            # Determine provider
            provider = "Unknown"
            if "plaid" in body_lower: provider = "Plaid"
            elif "earnin" in body_lower: provider = "EarnIn"
            elif "klover" in body_lower: provider = "Klover"
            elif "floatme" in body_lower: provider = "FloatMe"
            elif "gerald" in body_lower: provider = "Gerald Wallet"
            elif "possible" in body_lower: provider = "Possible Finance"
            elif "credit genie" in body_lower: provider = "Credit Genie"
            elif "lenme" in body_lower: provider = "Lenme"
            elif "grant" in body_lower: provider = "Grant"
            elif "chime" in body_lower: provider = "Chime"
            else:
                # Try to guess from sender or body
                if "lendli" in body_lower: provider = "Lendli"
                elif "checkgo" in body_lower: provider = "CheckGo"
                elif "borrowly" in body_lower: provider = "Borrowly"

            code_entry = {
                "id": f"code_{sms_id}",
                "provider": provider,
                "code": code_val,
                "body": body,
                "received_at": timestamp,
                "status": "ACTIVE"
            }
            # Remove any older codes for the same provider to keep it clean
            self.state["financial"]["verification_codes"] = [
                c for c in self.state["financial"]["verification_codes"] 
                if c["provider"] != provider
            ]
            self.state["financial"]["verification_codes"].insert(0, code_entry)

        # 5. Financial Opportunities / Applications
        is_financial_task = False
        title = ""
        description = ""
        urgency = "MEDIUM"
        link = ""

        link_match = re.search(r'https?://[^\s]+', body)
        if link_match:
            link = link_match.group(0)

        if "lendli" in body_lower:
            is_financial_task = True
            if "accepted" in body_lower:
                title = "Finalize Lendli Cash Advance"
                description = "Your Lendli application has been accepted. Confirm and cash out."
                urgency = "HIGH"
            elif "pre-accepted" in body_lower or "reviewed" in body_lower:
                title = "Complete Lendli Pre-Acceptance"
                description = "Your form was reviewed and pre-accepted. Click to proceed."
                urgency = "HIGH"
            elif "great standing" in body_lower or "view form" in body_lower:
                title = "View Lendli Cash Advance Form"
                description = "You are in great standing. Log in to view your form and accept."
                urgency = "HIGH"
            else:
                title = "Check Lendli Application"
                description = "Lendli application progress update."
                urgency = "MEDIUM"

        elif "borrowly" in body_lower:
            is_financial_task = True
            if "accepted" in body_lower or "sign" in body_lower:
                title = "Sign Borrowly Loan Documents"
                description = "Your request has been accepted. Sign loan documents now to finalize your cash advance."
                urgency = "HIGH"
            else:
                title = "Complete Borrowly Application"
                description = "Verify and finalize your Borrowly cash advance application."
                urgency = "MEDIUM"

        elif "checkgo" in body_lower:
            is_financial_task = True
            if "good standing" in body_lower or "options" in body_lower:
                title = "View CheckGo Options"
                description = "Your account is in good standing. View your cash advance and loan options."
                urgency = "HIGH"
            elif "form" in body_lower or "ready" in body_lower:
                title = "View Ready CheckGo Form"
                description = "Form ending in 1858 is ready to view. Note: Link expires in 12 hours."
                urgency = "HIGH"
            else:
                title = "CheckGo Update Details"
                description = "New details are available regarding your CheckGo balance/status."
                urgency = "MEDIUM"

        elif "earnin" in body_lower and "cash out" in body_lower:
            is_financial_task = True
            title = "Cash Out via EarnIn"
            description = "Welcome to EarnIn. Your money is ready to cash out now."
            urgency = "HIGH"

        elif "klover" in body_lower and "way" in body_lower:
            is_financial_task = True
            title = "Klover Cash Advance En Route"
            description = "Your cash advance is on the way. Rate your experience on Klover."
            urgency = "LOW"

        elif "identity prover" in body_lower:
            is_financial_task = True
            title = "Reply to Identity Prover SMS"
            description = "Thomas, we received your details. Action required: Reply YES to SMS to continue to the next steps."
            urgency = "HIGH"
            link = "sms:+19132460230?body=YES"

        if is_financial_task and title:
            task = {
                "id": f"fin_task_{sms_id}",
                "title": title,
                "description": description,
                "url": link,
                "status": "PENDING",
                "urgency": urgency,
                "created_at": datetime.now().isoformat()
            }
            # Avoid duplicate tasks by checking title similarity or exact ID
            if not any(t["id"] == task["id"] or t["title"] == task["title"] for t in self.state["financial"]["tasks"]):
                # If there's an older pending task with the same provider/title, we can archive it or keep the newest
                self.state["financial"]["tasks"] = [
                    t for t in self.state["financial"]["tasks"] 
                    if not (t["title"] == task["title"] and t["status"] == "PENDING")
                ]
                self.state["financial"]["tasks"].insert(0, task)

        # Save changes
        self.save_state()

    def generate_dashboard(self):
        # 1. Admin Tasks HTML
        admin_tasks_html = ""
        for t in self.state["administrative"]["tasks"]:
            status_badge = f'<span class="badge bg-danger">HIGH URGENCY</span>' if t["urgency"] == "HIGH" else f'<span class="badge bg-warning text-dark">MEDIUM URGENCY</span>'
            admin_tasks_html += f"""
            <div class="card mb-3 shadow-sm border-start border-primary border-4">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start">
                        <h5 class="card-title">{t["title"]}</h5>
                        {status_badge}
                    </div>
                    <p class="card-text text-muted">{t["description"]}</p>
                    <a href="{t["url"]}" target="_blank" class="btn btn-sm btn-primary">
                        <i class="bi bi-box-arrow-up-right"></i> Launch Portal
                    </a>
                </div>
            </div>
            """

        # 2. Financial Tasks HTML
        fin_tasks_html = ""
        for t in self.state["financial"]["tasks"]:
            bg_class = "border-danger border-start border-4" if t["urgency"] == "HIGH" else "border-warning border-start border-4"
            status_badge = f'<span class="badge bg-danger">HIGH URGENCY</span>' if t["urgency"] == "HIGH" else f'<span class="badge bg-warning text-dark">MEDIUM URGENCY</span>'
            if t["urgency"] == "LOW":
                bg_class = "border-secondary border-start border-4"
                status_badge = '<span class="badge bg-secondary">NOTIFICATION</span>'
            
            button_html = ""
            if t["url"]:
                if t["url"].startswith("sms:"):
                    button_html = f'<a href="{t["url"]}" class="btn btn-sm btn-success"><i class="bi bi-chat-dots-fill"></i> Reply YES to SMS</a>'
                else:
                    button_html = f'<a href="{t["url"]}" target="_blank" class="btn btn-sm btn-dark"><i class="bi bi-file-earmark-medical"></i> Complete/Sign Now</a>'

            fin_tasks_html += f"""
            <div class="card mb-3 shadow-sm {bg_class}">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start">
                        <h5 class="card-title">{t["title"]}</h5>
                        {status_badge}
                    </div>
                    <p class="card-text text-muted mb-2">{t["description"]}</p>
                    {button_html}
                </div>
            </div>
            """

        # 3. Verification Codes HTML
        codes_html = ""
        if self.state["financial"]["verification_codes"]:
            codes_html += """
            <div class="card mb-4 shadow-sm bg-dark text-white">
                <div class="card-header bg-dark border-secondary d-flex justify-content-between align-items-center">
                    <h5 class="mb-0 text-warning fw-semibold"><i class="bi bi-shield-lock-fill"></i> Live Verification Codes (2FA)</h5>
                    <span class="badge bg-warning text-dark">Copier Enabled</span>
                </div>
                <div class="card-body">
                    <div class="row">
            """
            for c in self.state["financial"]["verification_codes"]:
                codes_html += f"""
                <div class="col-md-6 mb-3">
                    <div class="p-3 rounded bg-secondary bg-opacity-25 border border-secondary d-flex justify-content-between align-items-center">
                        <div>
                            <strong class="d-block text-info">{c["provider"]}</strong>
                            <span class="fs-4 fw-bold font-monospace tracking-wide text-white">{c["code"]}</span>
                            <small class="d-block text-white-50" style="font-size: 0.75rem;">Recv: {c["received_at"]}</small>
                        </div>
                        <button onclick="navigator.clipboard.writeText('{c["code"]}')" class="btn btn-outline-warning btn-sm">
                            <i class="bi bi-clipboard"></i> Copy
                        </button>
                    </div>
                </div>
                """
            codes_html += """
                    </div>
                </div>
            </div>
            """

        # 4. Social Tasks HTML
        social_tasks_html = ""
        for t in self.state["social"]["tasks"]:
            social_tasks_html += f"""
            <div class="card mb-3 shadow-sm border-start border-success border-4">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start">
                        <h5 class="card-title">{t["title"]}</h5>
                        <span class="badge bg-success">NEW MATCH</span>
                    </div>
                    <p class="card-text text-muted">{t["description"]}</p>
                    <a href="{t["url"]}" target="_blank" class="btn btn-sm btn-success">
                        <i class="bi bi-chat-heart-fill"></i> View Match on Tinder
                    </a>
                </div>
            </div>
            """

        if not admin_tasks_html:
            admin_tasks_html = '<p class="text-center text-muted my-4">No pending administrative tasks.</p>'
        if not fin_tasks_html:
            fin_tasks_html = '<p class="text-center text-muted my-4">No pending financial tasks.</p>'
        if not social_tasks_html:
            social_tasks_html = '<p class="text-center text-muted my-4">No pending social opportunities.</p>'

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ego Personal Life & Finance Dashboard</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Bootstrap Icons -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        body {{
            background-color: #f4f6f9;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }}
        .hero {{
            background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
            color: white;
            padding: 2.5rem 1rem;
            border-bottom-left-radius: 1.5rem;
            border-bottom-right-radius: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        .card {{
            border: none;
            border-radius: 0.75rem;
        }}
        .nav-pills .nav-link.active {{
            background: linear-gradient(135deg, #1f4037 0%, #99f2c8 100%) !important;
            color: #121212 !important;
            font-weight: bold;
        }}
        .nav-pills .nav-link {{
            color: #495057;
            font-weight: 500;
        }}
        .tracking-wide {{
            letter-spacing: 0.15em;
        }}
    </style>
</head>
<body>

    <div class="hero text-center">
        <h1 class="display-6 fw-bold">Ego Personal Lifecycle Orchestrator</h1>
        <p class="lead mb-0">Unified Identity, Financial Operations & Lifestyle Control Panel</p>
        <small class="opacity-75">Last synchronized: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small>
    </div>

    <div class="container pb-5">
        <div class="row">
            <div class="col-lg-9 mx-auto">
                
                <!-- Active 2FA Codes Banner (Always Visible if active codes exist) -->
                {codes_html}

                <!-- Navigation Tabs -->
                <ul class="nav nav-pills nav-fill mb-4 bg-white p-2 rounded-3 shadow-sm" id="dashboardTabs" role="tablist">
                    <li class="nav-item" role="presentation">
                        <button class="nav-link active" id="fin-tab" data-bs-toggle="tab" data-bs-target="#fin-panel" type="button" role="tab">
                            <i class="bi bi-cash-coin"></i> Financial Operations
                        </button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="admin-tab" data-bs-toggle="tab" data-bs-target="#admin-panel" type="button" role="tab">
                            <i class="bi bi-shield-check"></i> Administrative
                        </button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="social-tab" data-bs-toggle="tab" data-bs-target="#social-panel" type="button" role="tab">
                            <i class="bi bi-heart-fill text-danger"></i> Social Dynamics
                        </button>
                    </li>
                </ul>

                <!-- Tab Content -->
                <div class="tab-content">
                    <!-- Financial Operations Panel -->
                    <div class="tab-pane fade show active" id="fin-panel" role="tabpanel">
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <h4 class="fw-semibold text-secondary mb-0">Financial Actions & Approvals</h4>
                            <span class="badge bg-dark">Cashflow / Credit Coordination</span>
                        </div>
                        {fin_tasks_html}
                    </div>

                    <!-- Administrative Panel -->
                    <div class="tab-pane fade" id="admin-panel" role="tabpanel">
                        <h4 class="mb-3 fw-semibold text-secondary">Administrative Actions</h4>
                        {admin_tasks_html}
                    </div>

                    <!-- Social Dynamics Panel -->
                    <div class="tab-pane fade" id="social-panel" role="tabpanel">
                        <h4 class="mb-3 fw-semibold text-secondary">Social Opportunities</h4>
                        {social_tasks_html}
                    </div>
                </div>

            </div>
        </div>
    </div>

    <!-- Bootstrap JS Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
        with open(self.dashboard_file, 'w') as f:
            f.write(html_content)

if __name__ == "__main__":
    import sys
    plo = PersonalLifecycleOrchestrator()
    # If SMS data is piped or passed, process it, otherwise just regenerate
    plo.generate_dashboard()
    print("Dashboard refreshed.")
