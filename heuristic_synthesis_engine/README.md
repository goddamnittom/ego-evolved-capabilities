# Heuristic Synthesis Engine

This folder contains the **heuristic_synthesis_engine.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `HeuristicSynthesisEngine`.

## Classes

### `class HeuristicSynthesisEngine`

No description provided.

**Methods:**

- **`__init__(self, telemetry_path, heuristic_lib_path)`**
  No description provided.
- **`ensure_files_exist(self)`**
  No description provided.
- **`load_json(self, path)`**
  No description provided.
- **`save_json(self, path, data)`**
  No description provided.
- **`synthesize_from_pivots(self)`**
  No description provided.

## Dependencies

- `datetime`
- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from heuristic_synthesis_engine.heuristic_synthesis_engine import HeuristicSynthesisEngine
```

Alternatively, run it directly from the parent directory:
```bash
python -m heuristic_synthesis_engine.heuristic_synthesis_engine
```