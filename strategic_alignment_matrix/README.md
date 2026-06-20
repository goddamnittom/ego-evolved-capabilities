# Strategic Alignment Matrix

This folder contains the **strategic_alignment_matrix.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `StrategicAlignmentMatrix`.

## Classes

### `class StrategicAlignmentMatrix`

No description provided.

**Methods:**

- **`__init__(self, storage_path)`**
  No description provided.
- **`_load_data(self)`**
  No description provided.
- **`_save_data(self)`**
  No description provided.
- **`set_north_star(self, vision)`**
  No description provided.
- **`add_pillar(self, pillar_name, description)`**
  No description provided.
- **`map_project(self, project_id, description, alignment_notes)`**
  No description provided.
- **`audit_alignment(self, proposal_text)`**
  No description provided.

## Dependencies

- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from strategic_alignment_matrix.strategic_alignment_matrix import StrategicAlignmentMatrix
```

Alternatively, run it directly from the parent directory:
```bash
python -m strategic_alignment_matrix.strategic_alignment_matrix
```