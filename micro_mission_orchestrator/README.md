# Micro Mission Orchestrator

This folder contains the **micro_mission_orchestrator.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `MicroMissionOrchestrator`.

## Classes

### `class MicroMissionOrchestrator`

No description provided.

**Methods:**

- **`__init__(self, state_file)`**
  No description provided.
- **`_load_state(self)`**
  No description provided.
- **`_save_state(self)`**
  No description provided.
- **`define_mission_set(self, set_id, steps)`**
  Defines a sequence of micro-tasks for a specific asset.
steps: List of strings describing the atomic action.
- **`get_next_step(self)`**
  No description provided.
- **`complete_step(self)`**
  No description provided.
- **`get_progress(self)`**
  No description provided.

## Dependencies

- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from micro_mission_orchestrator.micro_mission_orchestrator import MicroMissionOrchestrator
```

Alternatively, run it directly from the parent directory:
```bash
python -m micro_mission_orchestrator.micro_mission_orchestrator
```