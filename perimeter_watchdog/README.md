# Perimeter Watchdog

This folder contains the **perimeter_watchdog.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `PerimeterWatchdog`.

## Classes

### `class PerimeterWatchdog`

Perimeter Watchdog (PWG) monitors for anomalies and unauthorized access 
attempts on assets currently in the Hardening Verification Manifest (HVM).

**Methods:**

- **`__init__(self, hvm_path)`**
  No description provided.
- **`load_hvm(self)`**
  No description provided.
- **`scan_evidence(self, evidence_text, asset_id)`**
  Analyzes a piece of evidence (email/log) for anomalies.
- **`run_audit(self, incoming_data)`**
  Runs a batch audit over incoming signals.
incoming_data: list of tuples (asset_id, text)

## Dependencies

- `datetime`
- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from perimeter_watchdog.perimeter_watchdog import PerimeterWatchdog
```

Alternatively, run it directly from the parent directory:
```bash
python -m perimeter_watchdog.perimeter_watchdog
```