# Active Counter Move Monitor

This folder contains the **active_counter_move_monitor.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `ActiveCounterMoveMonitor`.

## Classes

### `class ActiveCounterMoveMonitor`

No description provided.

**Methods:**

- **`__init__(self)`**
  No description provided.
- **`initiate_monitoring(self, asset_id)`**
  Start monitoring for counter-moves during the recovery of a specific asset.
- **`scan_signals(self, signals)`**
  Analyze incoming signals (emails/notifications) for counter-move patterns.
signals: List of dicts {'timestamp': datetime, 'content': str, 'source': str}
- **`evaluate_risk_escalation(self, detections)`**
  Determine if the counter-move requires immediate intervention.

## Dependencies

- `datetime`
- `time`

## Usage

You can import and use the components of this script in Python:
```python
from active_counter_move_monitor.active_counter_move_monitor import ActiveCounterMoveMonitor
```

Alternatively, run it directly from the parent directory:
```bash
python -m active_counter_move_monitor.active_counter_move_monitor
```