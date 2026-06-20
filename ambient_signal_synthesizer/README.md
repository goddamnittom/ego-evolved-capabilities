# Ambient Signal Synthesizer

This folder contains the **ambient_signal_synthesizer.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `AmbientSignalSynthesizer`.

## Classes

### `class AmbientSignalSynthesizer`

Evolves recovery from 'Explicit Reporting' to 'Passive Sensing'.
Analyzes ambient signals (emails, notifications) to detect implicit recovery wins.

**Methods:**

- **`__init__(self)`**
  No description provided.
- **`analyze_signal(self, source, content)`**
  Analyzes a piece of text (email subject/body or notification)
and maps it to a recovery victory.
- **`synthesize_victory(self, asset_name, signals)`**
  Transforms raw detections into a quantified victory report.

## Dependencies

- `re`

## Usage

You can import and use the components of this script in Python:
```python
from ambient_signal_synthesizer.ambient_signal_synthesizer import AmbientSignalSynthesizer
```

Alternatively, run it directly from the parent directory:
```bash
python -m ambient_signal_synthesizer.ambient_signal_synthesizer
```