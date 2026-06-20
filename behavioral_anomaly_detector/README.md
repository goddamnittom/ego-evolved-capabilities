# Behavioral Anomaly Detector

This folder contains the **behavioral_anomaly_detector.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `BehavioralAnomalyDetector`.

## Classes

### `class BehavioralAnomalyDetector`

Analyzes email metadata and content patterns to identify signs of Account Takeover (ATO)
and subsequent exploitation (e.g., password spraying, financial fraud, spamming).

**Methods:**

- **`__init__(self)`**
  No description provided.
- **`analyze_batch(self, emails)`**
  No description provided.
- **`synthesize_report(self, findings)`**
  No description provided.

## Dependencies

- `datetime`
- `json`

## Usage

You can import and use the components of this script in Python:
```python
from behavioral_anomaly_detector.behavioral_anomaly_detector import BehavioralAnomalyDetector
```

Alternatively, run it directly from the parent directory:
```bash
python -m behavioral_anomaly_detector.behavioral_anomaly_detector
```