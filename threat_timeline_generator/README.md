# Threat Timeline Generator

This folder contains the **threat_timeline_generator.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `ThreatTimelineGenerator`.

## Classes

### `class ThreatTimelineGenerator`

Generates a chronological timeline of security events to visualize 
the blast radius and attacker movements.

**Methods:**

- **`__init__(self)`**
  No description provided.
- **`add_event(self, timestamp, event_type, description, severity)`**
  No description provided.
- **`generate_report(self)`**
  No description provided.

## Dependencies

- `datetime`
- `json`

## Usage

You can import and use the components of this script in Python:
```python
from threat_timeline_generator.threat_timeline_generator import ThreatTimelineGenerator
```

Alternatively, run it directly from the parent directory:
```bash
python -m threat_timeline_generator.threat_timeline_generator
```