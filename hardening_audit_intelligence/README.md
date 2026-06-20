# Hardening Audit Intelligence

This folder contains the **hardening_audit_intelligence.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `HardeningAuditIntelligence`.

## Classes

### `class HardeningAuditIntelligence`

HAI: Hardening Audit Intelligence
Moves security verification from 'Trust-Based' to 'Evidence-Based'.

**Methods:**

- **`__init__(self, manifest_path)`**
  No description provided.
- **`load_manifest(self)`**
  No description provided.
- **`save_manifest(self, manifest)`**
  No description provided.
- **`define_evidence_heuristics(self)`**
  Defines what constitutes 'evidence' for verification.
In a real scenario, this would be mapped to email patterns, log entries, etc.
- **`audit_evidence(self, asset_id, evidence_text)`**
  Analyzes provided text (e.g., email body) against heuristics to 
suggest a verification status change.
- **`suggest_verification(self, asset_id, evidence_text)`**
  No description provided.

## Dependencies

- `datetime`
- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from hardening_audit_intelligence.hardening_audit_intelligence import HardeningAuditIntelligence
```

Alternatively, run it directly from the parent directory:
```bash
python -m hardening_audit_intelligence.hardening_audit_intelligence
```