# Mission Temporal Forensics

This folder contains the **mission_temporal_forensics.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `MissionTemporalForensicEngine`.

## Classes

### `class MissionTemporalForensicEngine`

MTFE: Analyzes MCT telemetry and ER 1.6 visual signals to reconstruct 
the causal chain of a mission failure.

**Methods:**

- **`__init__(self)`**
  No description provided.
- **`analyze_failure(self, mct_logs, er_signals, expected_state)`**
  mct_logs: List of {'timestamp': datetime, 'node': str, 'value': any}
er_signals: List of {'timestamp': datetime, 'signal': str, 'value': bool}
expected_state: The MCT node value that was supposed to be reached.

## Dependencies

- `datetime`
- `json`

## Usage

You can import and use the components of this script in Python:
```python
from mission_temporal_forensics.mission_temporal_forensics import MissionTemporalForensicEngine
```

Alternatively, run it directly from the parent directory:
```bash
python -m mission_temporal_forensics.mission_temporal_forensics
```