# Sentinel Delta Analyzer

This folder contains the **sentinel_delta_analyzer.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `SentinelDeltaAnalyzer`.

## Classes

### `class SentinelDeltaAnalyzer`

Analyzes email streams to detect 'Threat Deltas'—specific, time-bound actions 
taken by an attacker that indicate active lateral movement or account hijacking.

**Methods:**

- **`__init__(self)`**
  No description provided.
- **`analyze_emails(self, emails)`**
  Processes a list of email summaries to find high-signal threat indicators.
- **`generate_report(self, deltas)`**
  No description provided.

## Dependencies

- `datetime`
- `json`

## Usage

You can import and use the components of this script in Python:
```python
from sentinel_delta_analyzer.sentinel_delta_analyzer import SentinelDeltaAnalyzer
```

Alternatively, run it directly from the parent directory:
```bash
python -m sentinel_delta_analyzer.sentinel_delta_analyzer
```