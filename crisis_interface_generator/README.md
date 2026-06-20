# Crisis Interface Generator

This folder contains the **crisis_interface_generator.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `CrisisInterfaceGenerator`.

## Classes

### `class CrisisInterfaceGenerator`

Generates specialized, high-urgency UI configurations for crisis management.
Aggregates data from PPE, SIA, BRV, and HVM to create a 'War Room' dashboard.

**Methods:**

- **`__init__(self)`**
  No description provided.
- **`generate_war_room_dashboard(self, threat_level, ppe_score, sia_status, blast_radius_size, critical_assets)`**
  No description provided.

## Dependencies

- `json`

## Usage

You can import and use the components of this script in Python:
```python
from crisis_interface_generator.crisis_interface_generator import CrisisInterfaceGenerator
```

Alternatively, run it directly from the parent directory:
```bash
python -m crisis_interface_generator.crisis_interface_generator
```