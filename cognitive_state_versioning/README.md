# Cognitive State Versioning

This folder contains the **cognitive_state_versioning.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `CognitiveStateVersioning`.

## Classes

### `class CognitiveStateVersioning`

No description provided.

**Methods:**

- **`__init__(self, storage_path)`**
  No description provided.
- **`_load_states(self)`**
  No description provided.
- **`capture_state(self, state_id, hypothesis, constraints, risk_landscape, intuition)`**
  Captures a snapshot of the AI's internal cognitive state.
- **`diff_states(self, state_id_a, state_id_b)`**
  Analyzes the divergence between two cognitive states.
- **`_save_states(self)`**
  No description provided.
- **`list_snapshots(self)`**
  No description provided.

## Dependencies

- `datetime`
- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from cognitive_state_versioning.cognitive_state_versioning import CognitiveStateVersioning
```

Alternatively, run it directly from the parent directory:
```bash
python -m cognitive_state_versioning.cognitive_state_versioning
```