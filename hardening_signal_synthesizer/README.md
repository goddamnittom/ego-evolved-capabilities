# Hardening Signal Synthesizer

This folder contains the **hardening_signal_synthesizer.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `HardeningSignalSynthesizer`.

## Classes

### `class HardeningSignalSynthesizer`

HSS: Hardening Signal Synthesizer
Transitions recovery from manual reporting to proactive victory detection.
Scans communication channels for Positive Hardening Markers (PHMs).

**Methods:**

- **`__init__(self)`**
  No description provided.
- **`analyze_signal(self, source, content)`**
  Analyzes a signal (email body, notification text, SMS) for hardening markers.
- **`synthesize_integrity_gain(self, markers)`**
  Calculates the psychological and technical gain based on detected markers.

## Dependencies

- `datetime`
- `json`
- `re`

## Usage

You can import and use the components of this script in Python:
```python
from hardening_signal_synthesizer.hardening_signal_synthesizer import HardeningSignalSynthesizer
```

Alternatively, run it directly from the parent directory:
```bash
python -m hardening_signal_synthesizer.hardening_signal_synthesizer
```