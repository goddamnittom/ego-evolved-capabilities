# Evidence Verification Engine

This folder contains the **evidence_verification_engine.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `EvidenceVerificationEngine`.

## Classes

### `class EvidenceVerificationEngine`

EVE transitions security verification from trust-based (user claims) 
to evidence-based (analysis of provided artifacts).

**Methods:**

- **`__init__(self)`**
  No description provided.
- **`_load_manifest(self)`**
  No description provided.
- **`verify_evidence(self, asset_id, goal, evidence_content)`**
  Analyzes evidence content against a specific verification goal.
Returns a confidence score and updates the HVM.
- **`_save_manifest(self)`**
  No description provided.

## Dependencies

- `datetime`
- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from evidence_verification_engine.evidence_verification_engine import EvidenceVerificationEngine
```

Alternatively, run it directly from the parent directory:
```bash
python -m evidence_verification_engine.evidence_verification_engine
```