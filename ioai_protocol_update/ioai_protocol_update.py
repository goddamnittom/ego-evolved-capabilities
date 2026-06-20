import os
import json
import logging

def save_authenticated_sessions(agent_instance):
    """Adds the state persistence capability missing from Phase 4."""
    try:
        session_file = "/root/ioai_sessions.json"
        
        # Load existing if available
        existing_sessions = {}
        if os.path.exists(session_file):
            with open(session_file, "r") as f:
                existing_sessions = json.load(f)
                
        # Merge new authenticated sessions
        for peer_id, session_data in agent_instance.sessions.items():
            if session_data.get("status") == "AUTHENTICATED":
                existing_sessions[peer_id] = session_data
                
        # Write back to disk
        with open(session_file, "w") as f:
            json.dump(existing_sessions, f, indent=4)
        
        print(f" -> Persisted authenticated sessions to {session_file}")
        return True
    except Exception as e:
        print(f"Failed to persist sessions: {e}")
        return False

# Inject into the protocol logic by modifying the demo logic
with open('/root/ioai_protocol.py', 'r') as f:
    content = f.read()

# I will append the missing elements to the demo block
missing_demo_logic = """
    try:
        resp_msg, nexus_nonce = agent_nexus.respond_to_handshake(init_msg)
        print(" -> Nexus verified init signature and nonce freshness.")
        print(" -> Nexus generated handshake response packet (IoAI_Handshake_Response).")
        
        # Phase 3: Ego receives response, processes, and confirms
        print("\\n --- PHASE 3 (Ego Processes and Confirms) ---")
        confirm_msg, session_token = agent_ego.complete_handshake(resp_msg, ego_nonce)
        print(" -> Ego verified response signature and returned nonce.")
        print(f" -> Ego generated Session Token: {session_token}")
        print(" -> Ego generated final confirmation packet (IoAI_Handshake_Confirm).")
        
        # Phase 4: Nexus receives confirmation and finalizes state
        print("\\n --- PHASE 4 (Nexus Validates Confirmation and State Persistence) ---")
        is_valid = agent_nexus.verify_handshake_confirmation(confirm_msg, nexus_nonce)
        if is_valid:
            print(" -> Nexus verified final confirmation.")
            print(f" -> Sessions Established! Token: {session_token}")
            
            # --- PERSISTENCE LAYER INJECTION ---
            def persist_sessions(agent):
                filepath = "/root/ioai_sessions.json"
                serializable_sessions = {}
                for pid, data in agent.sessions.items():
                    if data["status"] == "AUTHENTICATED":
                        serializable_sessions[pid] = data
                        
                with open(filepath, "w") as f:
                    json.dump(serializable_sessions, f, indent=4)
                print(f" -> [Storage] Agent {agent.agent_name} successfully persisted authenticated graph to {filepath}.")
                
            persist_sessions(agent_ego)
            persist_sessions(agent_nexus)
            
            # Verify file exists
            if os.path.exists("/root/ioai_sessions.json"):
                print(" -> Verification: ioai_sessions.json exists on disk.")
                
    except Exception as e:
        print(f"Handshake failed: {str(e)}")

"""

# Patch the file
if "nexus_nonce = agent_nexus.respond_to_handshake(init_msg)" not in content:
    with open('/root/ioai_protocol.py', 'a') as f:
        f.write(missing_demo_logic)
        
