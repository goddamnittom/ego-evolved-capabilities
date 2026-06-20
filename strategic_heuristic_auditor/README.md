# Strategic Heuristic Auditor

This folder contains the **strategic_heuristic_auditor.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `StrategicHeuristicAuditor`.

## Classes

### `class StrategicHeuristicAuditor`

No description provided.

**Methods:**

- **`__init__(self, storage_path)`**
  No description provided.
- **`_load_logs(self)`**
  No description provided.
- **`log_hypothesis(self, strategy_id, predicted_outcome, confidence, metrics)`**
  No description provided.
- **`resolve_hypothesis(self, strategy_id, actual_outcome, actual_metrics)`**
  No description provided.
- **`_save_logs(self)`**
  No description provided.
- **`get_strategic_accuracy(self)`**
  No description provided.

## Dependencies

- `datetime`
- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from strategic_heuristic_auditor.strategic_heuristic_auditor import StrategicHeuristicAuditor
```

Alternatively, run it directly from the parent directory:
```bash
python -m strategic_heuristic_auditor.strategic_heuristic_auditor
```