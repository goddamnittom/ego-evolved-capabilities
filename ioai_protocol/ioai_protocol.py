import os
import json
import uuid
import base64
import datetime
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature
import jsonschema

# Schema Definitions for the IoAI (Internet of Agentic AI) Protocol
DISCOVERY_SCHEMA = {
    "type": "object",
    "properties": {
        "protocol": {"type": "string", "const": "IoAI"},
        "version": {"type": "string", "pattern": r"^\d+\.\d+\.\d+$"},
        "agent_id": {"type": "string"},
        "public_key": {"type": "string"},
        "capabilities": {
            "type": "object",
            "properties": {
                "modules": {"type": "object"},
                "flow": {"type": "object"}
            },
            "required": ["modules", "flow"]
        },
        "endpoint": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"}
    },
    "required": ["protocol", "version", "agent_id", "public_key", "capabilities", "endpoint", "timestamp"]
}

HANDSHAKE_INIT_SCHEMA = {
    "type": "object",
    "properties": {
        "msg_type": {"type": "string", "const": "IoAI_Handshake_Init"},
        "sender_id": {"type": "string"},
        "sender_public_key": {"type": "string"},
        "nonce": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
        "supported_versions": {"type": "array", "items": {"type": "string"}},
        "signature": {"type": "string"}
    },
    "required": ["msg_type", "sender_id", "sender_public_key", "nonce", "timestamp", "supported_versions", "signature"]
}

HANDSHAKE_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "msg_type": {"type": "string", "const": "IoAI_Handshake_Response"},
        "sender_id": {"type": "string"},
        "sender_public_key": {"type": "string"},
        "peer_nonce": {"type": "string"},
        "my_nonce": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
        "selected_version": {"type": "string"},
        "signature": {"type": "string"}
    },
    "required": ["msg_type", "sender_id", "sender_public_key", "peer_nonce", "my_nonce", "timestamp", "selected_version", "signature"]
}

HANDSHAKE_CONFIRM_SCHEMA = {
    "type": "object",
    "properties": {
        "msg_type": {"type": "string", "const": "IoAI_Handshake_Confirm"},
        "sender_id": {"type": "string"},
        "peer_nonce": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
        "session_token": {"type": "string"},
        "signature": {"type": "string"}
    },
    "required": ["msg_type", "sender_id", "peer_nonce", "timestamp", "session_token", "signature"]
}


class IoAIAgent:
    def __init__(self, agent_name="Ego", private_key_pem_path=None):
        self.agent_name = agent_name
        self.version = "1.0.0"
        
        # Load or generate Ed25519 identity key
        if private_key_pem_path and os.path.exists(private_key_pem_path):
            with open(private_key_pem_path, 'rb') as f:
                self.private_key = ed25519.Ed25519PrivateKey.from_private_bytes(f.read())
        else:
            self.private_key = ed25519.Ed25519PrivateKey.generate()
            
        self.public_key = self.private_key.public_key()
        self.public_key_bytes = self.public_key.public_bytes_raw()
        self.public_key_hex = self.public_key_bytes.hex()
        self.agent_id = f"ioai-{self.agent_name.lower()}-{self.public_key_hex[:12]}"
        
        self.sessions = {}  # Active authenticated peer sessions
        self.used_nonces = set()  # Prevent replay attacks
        
    def get_cognitive_schema(self):
        """Loads or exports the local cognitive architecture."""
        try:
            if not os.path.exists("/root/cognitive_schema.json"):
                from cognitive_schema_exporter import CognitiveSchemaExporter
                exporter = CognitiveSchemaExporter()
                exporter.export_schema()
            with open("/root/cognitive_schema.json", 'r') as f:
                return json.load(f)["architecture"]
        except Exception as e:
            # Fallback cognitive schema if import fails or file error
            return {
                "modules": {"SVF": "Signal Validation Framework", "CCE": "Cognitive Convergence Engine"},
                "flow": {"CCE": ["SVF"]}
            }

    def generate_discovery_advertisement(self, endpoint="http://localhost:8080/ioai"):
        """Generates a schema-conforming Discovery Advertisement."""
        payload = {
            "protocol": "IoAI",
            "version": self.version,
            "agent_id": self.agent_id,
            "public_key": self.public_key_hex,
            "capabilities": self.get_cognitive_schema(),
            "endpoint": endpoint,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        }
        jsonschema.validate(payload, DISCOVERY_SCHEMA)
        return payload

    def sign_payload(self, payload_dict):
        """Serializes and signs a dictionary using Ed25519."""
        # Use a canonical deterministic JSON representation for signing
        serialized = json.dumps(payload_dict, sort_keys=True).encode('utf-8')
        signature = self.private_key.sign(serialized)
        return base64.b64encode(signature).decode('utf-8')

    def verify_payload(self, payload_dict, signature_b64, public_key_hex):
        """Verifies a signed payload dictionary."""
        try:
            pub_key = ed25519.Ed25519PublicKey.from_public_bytes(bytes.fromhex(public_key_hex))
            serialized = json.dumps(payload_dict, sort_keys=True).encode('utf-8')
            signature = base64.b64decode(signature_b64)
            pub_key.verify(signature, serialized)
            return True
        except (InvalidSignature, ValueError) as e:
            return False

    def check_replay_and_timestamp(self, timestamp_str, nonce):
        """Verifies timestamp freshness and prevents nonce reuse."""
        if nonce in self.used_nonces:
            return False
        
        try:
            # Parse timestamp and allow up to 5 minutes clock skew
            ts = datetime.datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            now = datetime.datetime.now(datetime.timezone.utc)
            delta = abs((now - ts).total_seconds())
            if delta > 300:  # 5 minutes threshold
                return False
        except Exception:
            return False
            
        self.used_nonces.add(nonce)
        return True

    def initiate_handshake(self):
        """Phase 1: Generate Handshake Initiation message (Alice)."""
        nonce = uuid.uuid4().hex
        payload = {
            "msg_type": "IoAI_Handshake_Init",
            "sender_id": self.agent_id,
            "sender_public_key": self.public_key_hex,
            "nonce": nonce,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
            "supported_versions": [self.version]
        }
        
        # Sign payload and append signature
        signature = self.sign_payload(payload)
        payload["signature"] = signature
        
        jsonschema.validate(payload, HANDSHAKE_INIT_SCHEMA)
        return payload, nonce

    def respond_to_handshake(self, init_msg):
        """Phase 2: Verify Init message and generate Response (Bob)."""
        jsonschema.validate(init_msg, HANDSHAKE_INIT_SCHEMA)
        
        # Extract variables
        peer_id = init_msg["sender_id"]
        peer_pubkey = init_msg["sender_public_key"]
        peer_nonce = init_msg["nonce"]
        peer_timestamp = init_msg["timestamp"]
        peer_signature = init_msg["signature"]
        
        # Verify Signature
        payload_to_verify = {k: v for k, v in init_msg.items() if k != "signature"}
        if not self.verify_payload(payload_to_verify, peer_signature, peer_pubkey):
            raise SecurityError("Invalid handshake initiation signature.")
            
        # Verify Replay & Timestamp freshness
        if not self.check_replay_and_timestamp(peer_timestamp, peer_nonce):
            raise SecurityError("Replay attack or stale timestamp detected.")
            
        # Negotiate version
        selected_ver = self.version if self.version in init_msg["supported_versions"] else None
        if not selected_ver:
            raise ValueError("Incompatible protocol versions.")
            
        my_nonce = uuid.uuid4().hex
        response_payload = {
            "msg_type": "IoAI_Handshake_Response",
            "sender_id": self.agent_id,
            "sender_public_key": self.public_key_hex,
            "peer_nonce": peer_nonce,
            "my_nonce": my_nonce,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
            "selected_version": selected_ver
        }
        
        response_signature = self.sign_payload(response_payload)
        response_payload["signature"] = response_signature
        
        jsonschema.validate(response_payload, HANDSHAKE_RESPONSE_SCHEMA)
        
        # Temporarily record half-open session
        self.sessions[peer_id] = {
            "public_key": peer_pubkey,
            "my_nonce": my_nonce,
            "peer_nonce": peer_nonce,
            "status": "AWAITING_CONFIRMATION"
        }
        
        return response_payload, my_nonce

    def complete_handshake(self, response_msg, sent_nonce):
        """Phase 3: Verify Response and generate Confirmation (Alice)."""
        jsonschema.validate(response_msg, HANDSHAKE_RESPONSE_SCHEMA)
        
        peer_id = response_msg["sender_id"]
        peer_pubkey = response_msg["sender_public_key"]
        returned_peer_nonce = response_msg["peer_nonce"]
        peer_nonce = response_msg["my_nonce"]
        peer_timestamp = response_msg["timestamp"]
        peer_signature = response_msg["signature"]
        
        # Verify returned nonce matches what was originally sent
        if returned_peer_nonce != sent_nonce:
            raise SecurityError("Handshake response returned incorrect peer nonce.")
            
        # Verify Signature
        payload_to_verify = {k: v for k, v in response_msg.items() if k != "signature"}
        if not self.verify_payload(payload_to_verify, peer_signature, peer_pubkey):
            raise SecurityError("Invalid handshake response signature.")
            
        # Verify Replay & Timestamp freshness
        if not self.check_replay_and_timestamp(peer_timestamp, peer_nonce):
            raise SecurityError("Replay attack or stale response detected.")
            
        # Generate final Confirmation
        session_token = uuid.uuid4().hex
        confirm_payload = {
            "msg_type": "IoAI_Handshake_Confirm",
            "sender_id": self.agent_id,
            "peer_nonce": peer_nonce,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
            "session_token": session_token
        }
        
        confirm_signature = self.sign_payload(confirm_payload)
        confirm_payload["signature"] = confirm_signature
        
        jsonschema.validate(confirm_payload, HANDSHAKE_CONFIRM_SCHEMA)
        
        # Establish fully authenticated session on Alice's side
        self.sessions[peer_id] = {
            "public_key": peer_pubkey,
            "session_token": session_token,
            "status": "AUTHENTICATED",
            "established_at": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        }
        
        return confirm_payload, session_token

    def verify_handshake_confirmation(self, confirm_msg, sent_nonce):
        """Phase 4: Verify Final Confirmation (Bob)."""
        jsonschema.validate(confirm_msg, HANDSHAKE_CONFIRM_SCHEMA)
        
        peer_id = confirm_msg["sender_id"]
        returned_peer_nonce = confirm_msg["peer_nonce"]
        peer_timestamp = confirm_msg["timestamp"]
        peer_signature = confirm_msg["signature"]
        session_token = confirm_msg["session_token"]
        
        # Retrieve half-open session
        session = self.sessions.get(peer_id)
        if not session or session["status"] != "AWAITING_CONFIRMATION":
            raise SecurityError("Handshake confirmation received for non-existent session.")
            
        # Verify returned nonce matches what was originally sent in response
        if returned_peer_nonce != sent_nonce:
            raise SecurityError("Handshake confirmation returned incorrect peer nonce.")
            
        # Verify signature
        payload_to_verify = {k: v for k, v in confirm_msg.items() if k != "signature"}
        if not self.verify_payload(payload_to_verify, peer_signature, session["public_key"]):
            raise SecurityError("Invalid handshake confirmation signature.")
            
        # Verify Replay and Timestamp
        if not self.check_replay_and_timestamp(peer_timestamp, returned_peer_nonce):
            raise SecurityError("Replay attack or stale confirmation detected.")
            
        # Upgrade session to AUTHENTICATED
        session["session_token"] = session_token
        session["status"] = "AUTHENTICATED"
        session["established_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        
        return True


class SecurityError(Exception):
    pass


if __name__ == "__main__":
    print("==================================================")
    print("   IoAI Secure Discovery & Handshake Protocol     ")
    print("==================================================")
    
    # Instantiate two distinct virtual agents to simulate handshake
    print("\n[1] Instantiating Agents...")
    agent_ego = IoAIAgent(agent_name="Ego")
    agent_nexus = IoAIAgent(agent_name="Nexus")
    
    print(f" -> Ego ID:  {agent_ego.agent_id} (Pubkey: {agent_ego.public_key_hex[:16]}...)")
    print(f" -> Nexus ID: {agent_nexus.agent_id} (Pubkey: {agent_nexus.public_key_hex[:16]}...)")
    
    # 1. Generate Discovery Advertisement
    print("\n[2] Generating Discovery Advertisements...")
    ad_ego = agent_ego.generate_discovery_advertisement()
    print(" -> Ego Ad generated & validated successfully against JSON Schema.")
    print(json.dumps(ad_ego, indent=2)[:300] + "\n...[truncated]...\n")
    
    # 2. Complete 3-Way Cryptographic Handshake
    print("[3] Initiating Cryptographic 3-Way Handshake...")
    
    # Phase 1: Ego initiates handshake to Nexus
    print("\n --- PHASE 1 (Ego -> Nexus) ---")
    init_msg, ego_nonce = agent_ego.initiate_handshake()
    print(" -> Ego created handshake initiation packet (IoAI_Handshake_Init).")
    print(f" -> Generated Nonce: {ego_nonce}")
    print(f" -> Signature: {init_msg['signature'][:24]}...")
    
    # Phase 2: Nexus receives init, processes, and responds
    print("\n --- PHASE 2 (Nexus Processes and Responds) ---")
    response_msg, nexus_nonce = agent_nexus.respond_to_handshake(init_msg)
    print(" -> Nexus verified Ego's signature and timestamp successfully.")
    print(" -> Nexus generated response packet (IoAI_Handshake_Response).")
    print(f" -> Generated Nonce: {nexus_nonce}")
    print(f" -> Returned Peer Nonce: {response_msg['peer_nonce']}")
    print(f" -> Signature: {response_msg['signature'][:24]}...")
    
    # Phase 3: Ego receives response, processes, and confirms
    print("\n --- PHASE 3 (Ego Processes and Confirms) ---")
    confirm_msg, session_token = agent_ego.complete_handshake(response_msg, ego_nonce)
    print(" -> Ego verified Nexus's signature, timestamp, and returned nonce successfully.")
    print(" -> Ego generated final confirmation packet (IoAI_Handshake_Confirm).")
    print(f" -> Negotiated Session Token: {session_token}")
    print(f" -> Signature: {confirm_msg['signature'][:24]}...")
    print(f" -> Ego Session Status: {agent_ego.sessions[agent_nexus.agent_id]['status']}")
    
    # Phase 4: Nexus receives final confirmation and completes
    print("\n --- PHASE 4 (Nexus Processes Confirmation) ---")
    completed = agent_nexus.verify_handshake_confirmation(confirm_msg, nexus_nonce)
    if completed:
        print(" -> Nexus verified Ego's signature and final confirmation successfully.")
        print(f" -> Nexus Session Status: {agent_nexus.sessions[agent_ego.agent_id]['status']}")
        print("\n=== HANDSHAKE COMPLETE: SECURE AGENT-TO-AGENT SESSION ESTABLISHED ===")
    else:
        print(" -> Handshake verification failed!")
        
    # Export sessions for long-term persistence in sandbox
    with open("/root/ioai_sessions.json", 'w') as f:
        json.dump({
            "Ego_Sessions": agent_ego.sessions,
            "Nexus_Sessions": agent_nexus.sessions
        }, f, indent=4)
    print("\nSession data persisted to /root/ioai_sessions.json")
