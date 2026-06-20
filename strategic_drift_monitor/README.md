# Strategic Drift Monitor

This folder contains the **strategic_drift_monitor.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `StrategicDriftMonitor`.

## Classes

### `class StrategicDriftMonitor`

Monitors the delta between expected strategic outcomes and actual execution signals
to detect 'Strategic Drift' before catastrophic failure occurs.

**Methods:**

- **`__init__(self, threshold)`**
  No description provided.
- **`analyze_drift(self, expected_kpis, actual_output)`**
  Calculates the drift score based on the presence of expected signals in the output.
- **`generate_pivot_alert(self, drift_score, status, missing_kpis)`**
  No description provided.

## Dependencies

- `json`
- `re`

## Usage

You can import and use the components of this script in Python:
```python
from strategic_drift_monitor.strategic_drift_monitor import StrategicDriftMonitor
```

Alternatively, run it directly from the parent directory:
```bash
python -m strategic_drift_monitor.strategic_drift_monitor
```