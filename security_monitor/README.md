# Security Monitor

This folder contains the **security_monitor.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `SecurityMonitor`.

## Classes

### `class SecurityMonitor`

Security Threat Heuristic Monitor (STHM)
Analyzes message patterns to identify potential account takeovers or phishing.

**Methods:**

- **`__init__(self)`**
  No description provided.
- **`analyze(self, messages)`**
  Analyzes a list of messages. 
messages: list of dicts {'text': '...', 'timestamp': '...'}

## Dependencies

- `datetime`
- `re`

## Usage

You can import and use the components of this script in Python:
```python
from security_monitor.security_monitor import SecurityMonitor
```

Alternatively, run it directly from the parent directory:
```bash
python -m security_monitor.security_monitor
```