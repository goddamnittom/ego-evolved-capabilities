# Ioai Protocol

This folder contains the **ioai_protocol.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following classes: `IoAIAgent`, `SecurityError`.

## Classes

### `class IoAIAgent`

No description provided.

**Methods:**

- **`__init__(self, agent_name, private_key_pem_path)`**
  No description provided.
- **`get_cognitive_schema(self)`**
  Loads or exports the local cognitive architecture.
- **`generate_discovery_advertisement(self, endpoint)`**
  Generates a schema-conforming Discovery Advertisement.
- **`sign_payload(self, payload_dict)`**
  Serializes and signs a dictionary using Ed25519.
- **`verify_payload(self, payload_dict, signature_b64, public_key_hex)`**
  Verifies a signed payload dictionary.
- **`check_replay_and_timestamp(self, timestamp_str, nonce)`**
  Verifies timestamp freshness and prevents nonce reuse.
- **`initiate_handshake(self)`**
  Phase 1: Generate Handshake Initiation message (Alice).
- **`respond_to_handshake(self, init_msg)`**
  Phase 2: Verify Init message and generate Response (Bob).
- **`complete_handshake(self, response_msg, sent_nonce)`**
  Phase 3: Verify Response and generate Confirmation (Alice).
- **`verify_handshake_confirmation(self, confirm_msg, sent_nonce)`**
  Phase 4: Verify Final Confirmation (Bob).

### `class SecurityError`

No description provided.

## Dependencies

- `base64`
- `cryptography`
- `datetime`
- `json`
- `jsonschema`
- `os`
- `uuid`

## Usage

You can import and use the components of this script in Python:
```python
from ioai_protocol.ioai_protocol import IoAIAgent
```

Alternatively, run it directly from the parent directory:
```bash
python -m ioai_protocol.ioai_protocol
```