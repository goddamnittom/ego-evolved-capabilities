# Attack Surface Delta Mapper

This folder contains the **attack_surface_delta_mapper.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `AttackSurfaceDeltaMapper`.

## Classes

### `class AttackSurfaceDeltaMapper`

No description provided.

**Methods:**

- **`__init__(self, knowledge_base_path)`**
  No description provided.
- **`map_delta(self, asset_name, compromised_vectors, hardened_vectors)`**
  Compares the compromised state against the hardened state to identify
exactly which attack vectors were neutralized.
- **`generate_victory_report(self, report)`**
  Transforms a raw delta report into a high-impact 'Victory Report' for the user.

## Dependencies

- `datetime`
- `json`

## Usage

You can import and use the components of this script in Python:
```python
from attack_surface_delta_mapper.attack_surface_delta_mapper import AttackSurfaceDeltaMapper
```

Alternatively, run it directly from the parent directory:
```bash
python -m attack_surface_delta_mapper.attack_surface_delta_mapper
```