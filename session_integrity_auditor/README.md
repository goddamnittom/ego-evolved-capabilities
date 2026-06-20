# Session Integrity Auditor

This folder contains the **session_integrity_auditor.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `SessionIntegrityAuditor`.

## Classes

### `class SessionIntegrityAuditor`

SIA closes the loop between Pivot Prediction (PPE) and Signal Detection.
It monitors for 'Silent Pivots'—successful unauthorized accesses that
do not trigger MFA alerts but leave ambient footprints (e.g., 'New Login' emails).

**Methods:**

- **`__init__(self, ppe_probability)`**
  No description provided.
- **`analyze_signal(self, signal_type, details)`**
  No description provided.

## Dependencies

- `datetime`
- `json`

## Usage

You can import and use the components of this script in Python:
```python
from session_integrity_auditor.session_integrity_auditor import SessionIntegrityAuditor
```

Alternatively, run it directly from the parent directory:
```bash
python -m session_integrity_auditor.session_integrity_auditor
```