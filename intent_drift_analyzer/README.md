# Intent Drift Analyzer

This folder contains the **intent_drift_analyzer.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `IntentDriftAnalyzer`.

## Classes

### `class IntentDriftAnalyzer`

Analyzes the evolution of user intent over time to detect 'Strategic Drift'.
Compares historical goal statements with current operational trajectories.

**Methods:**

- **`__init__(self, telemetry_path)`**
  No description provided.
- **`analyze_drift(self)`**
  No description provided.

## Dependencies

- `datetime`
- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from intent_drift_analyzer.intent_drift_analyzer import IntentDriftAnalyzer
```

Alternatively, run it directly from the parent directory:
```bash
python -m intent_drift_analyzer.intent_drift_analyzer
```