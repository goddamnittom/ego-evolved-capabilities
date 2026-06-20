# Prescriptive Hardening Engine

This folder contains the **prescriptive_hardening_engine.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `PrescriptiveHardeningEngine`.

## Classes

### `class PrescriptiveHardeningEngine`

PHE: Maps Actor Behavioral Profiles (ABP) and Adversarial Paths (APS) 
to specific, tailored hardening controls to maximize 'Integrity Gain' 
while minimizing user friction.

**Methods:**

- **`__init__(self, actor_profile_path, path_sim_path)`**
  No description provided.
- **`generate_prescriptive_sequence(self)`**
  No description provided.

## Dependencies

- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from prescriptive_hardening_engine.prescriptive_hardening_engine import PrescriptiveHardeningEngine
```

Alternatively, run it directly from the parent directory:
```bash
python -m prescriptive_hardening_engine.prescriptive_hardening_engine
```