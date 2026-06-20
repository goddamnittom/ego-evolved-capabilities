# Evidence Correlator

This folder contains the **evidence_correlator.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `EvidenceCorrelator`.

## Classes

### `class EvidenceCorrelator`

No description provided.

**Methods:**

- **`__init__(self, storage_path)`**
  No description provided.
- **`_load(self)`**
  No description provided.
- **`_save(self)`**
  No description provided.
- **`bundle_evidence(self, event_id, log_text, screenshot_path, metadata)`**
  Links textual logs and visual screenshots to a single event identifier.
- **`get_bundle(self, event_id)`**
  No description provided.
- **`list_bundles(self)`**
  No description provided.
- **`verify_bundle(self, event_id)`**
  No description provided.

## Dependencies

- `datetime`
- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from evidence_correlator.evidence_correlator import EvidenceCorrelator
```

Alternatively, run it directly from the parent directory:
```bash
python -m evidence_correlator.evidence_correlator
```