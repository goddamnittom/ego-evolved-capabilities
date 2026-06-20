# Horizon Scanning Protocol

This folder contains the **horizon_scanning_protocol.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `HorizonScanningProtocol`.

## Classes

### `class HorizonScanningProtocol`

HSP shifts Ego's awareness from 'Internal Optimization' to 'External Contextual Awareness'.
It tracks external technical and strategic shifts and maps them to the user's project goals.

**Methods:**

- **`__init__(self, knowledge_base_path)`**
  No description provided.
- **`_load_interests(self)`**
  No description provided.
- **`update_interest_graph(self, domain, tool, benchmark)`**
  No description provided.
- **`_save_interests(self)`**
  No description provided.
- **`analyze_external_signal(self, signal_text, source)`**
  Compares an external signal against the interest graph to determine 
if it represents a 'Horizon Event' (a significant shift in the landscape).

## Dependencies

- `datetime`
- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from horizon_scanning_protocol.horizon_scanning_protocol import HorizonScanningProtocol
```

Alternatively, run it directly from the parent directory:
```bash
python -m horizon_scanning_protocol.horizon_scanning_protocol
```