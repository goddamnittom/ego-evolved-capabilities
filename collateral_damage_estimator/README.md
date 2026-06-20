# Collateral Damage Estimator

This folder contains the **collateral_damage_estimator.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `CollateralDamageEstimator`.

## Classes

### `class CollateralDamageEstimator`

No description provided.

**Methods:**

- **`__init__(self)`**
  No description provided.
- **`estimate_damage(self, sent_emails)`**
  Analyzes sent emails to estimate reputation damage.
sent_emails: List of dicts with {'to': ..., 'subject': ..., 'body': ...}

## Dependencies

- `collections`
- `datetime`
- `json`

## Usage

You can import and use the components of this script in Python:
```python
from collateral_damage_estimator.collateral_damage_estimator import CollateralDamageEstimator
```

Alternatively, run it directly from the parent directory:
```bash
python -m collateral_damage_estimator.collateral_damage_estimator
```