# Persistence Audit Engine

This folder contains the **persistence_audit_engine.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `PersistenceAuditEngine`.

## Classes

### `class PersistenceAuditEngine`

No description provided.

**Methods:**

- **`__init__(self, blast_radius_file, remediation_log_file)`**
  No description provided.
- **`load_json(self, path)`**
  No description provided.
- **`audit_persistence(self)`**
  No description provided.

## Dependencies

- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from persistence_audit_engine.persistence_audit_engine import PersistenceAuditEngine
```

Alternatively, run it directly from the parent directory:
```bash
python -m persistence_audit_engine.persistence_audit_engine
```