# Blast Radius Visualizer

This folder contains the **blast_radius_visualizer.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `BlastRadiusVisualizer`.

## Classes

### `class BlastRadiusVisualizer`

No description provided.

**Methods:**

- **`__init__(self, map_file)`**
  No description provided.
- **`_load_map(self)`**
  No description provided.
- **`add_asset(self, asset_id, name, asset_type)`**
  No description provided.
- **`add_dependency(self, from_id, to_id, relation)`**
  No description provided.
- **`calculate_blast_radius(self, compromised_id)`**
  No description provided.
- **`_save_map(self)`**
  No description provided.

## Dependencies

- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from blast_radius_visualizer.blast_radius_visualizer import BlastRadiusVisualizer
```

Alternatively, run it directly from the parent directory:
```bash
python -m blast_radius_visualizer.blast_radius_visualizer
```