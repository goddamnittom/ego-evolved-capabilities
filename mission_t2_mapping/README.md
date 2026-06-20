# Mission T2 Mapping

This folder contains the **mission_t2_mapping.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `ER16_MCT_Bridge`.

## Classes

### `class ER16_MCT_Bridge`

No description provided.

**Methods:**

- **`__init__(self)`**
  No description provided.
- **`map_success_marker(self, er_marker, mct_node)`**
  Maps ER 1.6's Success Detection logic to a Mission Control Telemetry node.
er_marker: The semantic success signal from Gemini Robotics-ER 1.6
mct_node: The corresponding objective ID in the MCT graph
- **`synchronize_telemetry(self, current_state, er_success_bool)`**
  Synchronizes the internal MCT state with the ER 1.6 success signal.

## Dependencies

- `datetime`
- `json`
- `uuid`

## Usage

You can import and use the components of this script in Python:
```python
from mission_t2_mapping.mission_t2_mapping import ER16_MCT_Bridge
```

Alternatively, run it directly from the parent directory:
```bash
python -m mission_t2_mapping.mission_t2_mapping
```