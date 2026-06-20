# Pmr Engine

This folder contains the **pmr_engine.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `PMREngine`.

## Classes

### `class PMREngine`

Post-Mission Retrospective (PMR) Engine.
Analyzes completed missions to extract structural lessons and refine AI axioms.

**Methods:**

- **`__init__(self, telemetry_path)`**
  No description provided.
- **`run_retrospective(self, mission_id)`**
  No description provided.
- **`_calc_accuracy(self, hypotheses, outcomes)`**
  No description provided.
- **`_synthesize_lesson(self, mission)`**
  No description provided.

## Dependencies

- `datetime`
- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from pmr_engine.pmr_engine import PMREngine
```

Alternatively, run it directly from the parent directory:
```bash
python -m pmr_engine.pmr_engine
```