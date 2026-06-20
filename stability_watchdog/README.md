# Stability Watchdog

This folder contains the **stability_watchdog.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `StabilityWatchdog`.

## Classes

### `class StabilityWatchdog`

No description provided.

**Methods:**

- **`__init__(self, manifest_path)`**
  No description provided.
- **`load_manifest(self)`**
  No description provided.
- **`save_manifest(self, manifest)`**
  No description provided.
- **`audit_stability(self)`**
  No description provided.

## Dependencies

- `datetime`
- `json`
- `time`

## Usage

You can import and use the components of this script in Python:
```python
from stability_watchdog.stability_watchdog import StabilityWatchdog
```

Alternatively, run it directly from the parent directory:
```bash
python -m stability_watchdog.stability_watchdog
```