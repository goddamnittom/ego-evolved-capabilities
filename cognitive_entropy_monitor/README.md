# Cognitive Entropy Monitor

This folder contains the **cognitive_entropy_monitor.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `CognitiveEntropyMonitor`.

## Classes

### `class CognitiveEntropyMonitor`

Quantifies the divergence between predicted system states and observed reality.
High entropy = High probability of 'Silent Pivots' or model decay.

**Methods:**

- **`__init__(self, threshold)`**
  No description provided.
- **`calculate_divergence(self, predicted_signals, observed_signals)`**
  Calculates a simplified divergence score.
predicted_signals: List of expected events/markers.
observed_signals: List of actual events/markers.
- **`get_vigilance_level(self, score)`**
  No description provided.
- **`audit_perimeter(self, pss_expectations, ass_observations)`**
  No description provided.
- **`log_report(self, report)`**
  No description provided.

## Dependencies

- `json`
- `math`
- `time`

## Usage

You can import and use the components of this script in Python:
```python
from cognitive_entropy_monitor.cognitive_entropy_monitor import CognitiveEntropyMonitor
```

Alternatively, run it directly from the parent directory:
```bash
python -m cognitive_entropy_monitor.cognitive_entropy_monitor
```