# Cognitive Friction Reducer

This folder contains the **cognitive_friction_reducer.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `CognitiveFrictionReducer`.

## Classes

### `class CognitiveFrictionReducer`

Analyzes complex security tasks and decomposes them into atomic, 
low-friction 'Micro-Wins' to overcome user stagnation.

**Methods:**

- **`__init__(self)`**
  No description provided.
- **`decompose_task(self, task_name, steps)`**
  Transforms a high-level task into a structured sequence of low-friction actions.
- **`suggest_path_of_least_resistance(self, decomposed_task)`**
  Re-orders or highlights the easiest wins first to build momentum.

## Dependencies

- `json`

## Usage

You can import and use the components of this script in Python:
```python
from cognitive_friction_reducer.cognitive_friction_reducer import CognitiveFrictionReducer
```

Alternatively, run it directly from the parent directory:
```bash
python -m cognitive_friction_reducer.cognitive_friction_reducer
```