# Predictive Signal Synthesizer

This folder contains the **predictive_signal_synthesizer.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `PredictiveSignalSynthesizer`.

## Classes

### `class PredictiveSignalSynthesizer`

Shifts security monitoring from 'Correlation' (what happened) 
to 'Expectation' (what should happen next).

**Methods:**

- **`__init__(self, actor_profile, utl_state)`**
  No description provided.
- **`generate_expectations(self)`**
  Synthesizes a Signal Expectation Matrix (SEM) based on actor behavior 
and current perimeter vulnerabilities.
- **`resolve_signal(self, actual_signal)`**
  Compares an incoming signal against the expectation matrix to 
calculate 'Predictive Accuracy'.

## Dependencies

- `datetime`
- `json`
- `random`

## Usage

You can import and use the components of this script in Python:
```python
from predictive_signal_synthesizer.predictive_signal_synthesizer import PredictiveSignalSynthesizer
```

Alternatively, run it directly from the parent directory:
```bash
python -m predictive_signal_synthesizer.predictive_signal_synthesizer
```