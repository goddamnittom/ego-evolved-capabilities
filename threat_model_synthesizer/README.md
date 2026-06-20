# Threat Model Synthesizer

This folder contains the **threat_model_synthesizer.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `ThreatModelSynthesizer`.

## Classes

### `class ThreatModelSynthesizer`

No description provided.

**Methods:**

- **`__init__(self, manifest_path, logs_path)`**
  No description provided.
- **`load_manifest(self)`**
  No description provided.
- **`analyze_attack_surface(self, evidence_logs)`**
  Analyzes logs and manifest state to synthesize a threat model.
evidence_logs: List of observed attacker actions or anomalies.
- **`save_profile(self, path)`**
  No description provided.

## Dependencies

- `datetime`
- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from threat_model_synthesizer.threat_model_synthesizer import ThreatModelSynthesizer
```

Alternatively, run it directly from the parent directory:
```bash
python -m threat_model_synthesizer.threat_model_synthesizer
```