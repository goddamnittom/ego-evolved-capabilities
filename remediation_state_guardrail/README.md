# Remediation State Guardrail

This folder contains the **remediation_state_guardrail.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `RemediationStateGuardrail`.

## Classes

### `class RemediationStateGuardrail`

No description provided.

**Methods:**

- **`__init__(self, manifest_path)`**
  No description provided.
- **`set_guardrail(self, asset_id, expected_state)`**
  Define the 'Golden State' for an asset.
- **`audit_state(self, asset_id, current_state)`**
  Compare current signal against the Golden State.
- **`_save_guardrails(self)`**
  No description provided.
- **`load_guardrails(self)`**
  No description provided.

## Dependencies

- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from remediation_state_guardrail.remediation_state_guardrail import RemediationStateGuardrail
```

Alternatively, run it directly from the parent directory:
```bash
python -m remediation_state_guardrail.remediation_state_guardrail
```