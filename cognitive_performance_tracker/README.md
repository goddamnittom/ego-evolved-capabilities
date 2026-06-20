# Cognitive Performance Tracker

This folder contains the **cognitive_performance_tracker.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following functions: `log_task`, `generate_report`.

## Functions

### `def log_task(task_id, category, duration, success, errors, user_correction, notes)`

Logs the metrics for a completed cognitive task.

### `def generate_report()`

Generates a high-level summary of performance across categories.

## Dependencies

- `datetime`
- `json`
- `os`
- `time`

## Usage

You can import and use the components of this script in Python:
```python
from cognitive_performance_tracker.cognitive_performance_tracker import log_task
```

Alternatively, run it directly from the parent directory:
```bash
python -m cognitive_performance_tracker.cognitive_performance_tracker
```