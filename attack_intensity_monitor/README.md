# Attack Intensity Monitor

This folder contains the **attack_intensity_monitor.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `AttackIntensityMonitor`.

## Classes

### `class AttackIntensityMonitor`

No description provided.

**Methods:**

- **`__init__(self, log_file)`**
  No description provided.
- **`_load_signals(self)`**
  No description provided.
- **`record_signal(self, source, target, signal_type)`**
  No description provided.
- **`calculate_velocity(self, window_minutes)`**
  No description provided.

## Dependencies

- `datetime`
- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from attack_intensity_monitor.attack_intensity_monitor import AttackIntensityMonitor
```

Alternatively, run it directly from the parent directory:
```bash
python -m attack_intensity_monitor.attack_intensity_monitor
```