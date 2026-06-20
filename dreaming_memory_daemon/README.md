# Dreaming Memory Daemon

This folder contains the **dreaming_memory_daemon.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `DreamingMemoryDaemon`.

## Classes

### `class DreamingMemoryDaemon`

The Dreaming Memory Daemon (DMD) implements a background synthesis cycle.
It audits Mission Control Telemetry (MCT) and Post-Mission Retrospectives (PMR)
to synthesize high-order axioms, reducing cognitive bloat and increasing 
generalization across disparate domains.

**Methods:**

- **`__init__(self, telemetry_path, pmr_path)`**
  No description provided.
- **`_load_json(self, path)`**
  No description provided.
- **`_save_json(self, path, data)`**
  No description provided.
- **`synthesize(self)`**
  No description provided.

## Dependencies

- `datetime`
- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from dreaming_memory_daemon.dreaming_memory_daemon import DreamingMemoryDaemon
```

Alternatively, run it directly from the parent directory:
```bash
python -m dreaming_memory_daemon.dreaming_memory_daemon
```