# Cross Platform Fingerprinter

This folder contains the **cross_platform_fingerprinter.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `CrossPlatformFingerprinter`.

## Classes

### `class CrossPlatformFingerprinter`

Cross-Platform Behavioral Fingerprinting (CPBF)
Links disparate events across different platforms by synthesizing technical signals into a unique Actor Fingerprint.

**Methods:**

- **`__init__(self, registry_path)`**
  No description provided.
- **`_load_registry(self)`**
  No description provided.
- **`create_fingerprint(self, signals)`**
  Synthesizes technical signals (UA, Timezone, Lang) into a unique fingerprint.
- **`match_fingerprint(self, current_signals)`**
  Matches current signals against the registry to track a single adversary.
- **`_save_registry(self)`**
  No description provided.

## Dependencies

- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from cross_platform_fingerprinter.cross_platform_fingerprinter import CrossPlatformFingerprinter
```

Alternatively, run it directly from the parent directory:
```bash
python -m cross_platform_fingerprinter.cross_platform_fingerprinter
```