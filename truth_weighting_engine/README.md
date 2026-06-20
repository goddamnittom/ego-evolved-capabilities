# Truth Weighting Engine

This folder contains the **truth_weighting_engine.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `TruthWeightingEngine`.

## Classes

### `class TruthWeightingEngine`

No description provided.

**Methods:**

- **`__init__(self)`**
  No description provided.
- **`calculate_confidence(self, claim, evidence_list)`**
  Calculates a confidence score (0.0 to 1.0) for a specific claim.
evidence_list: List of tuples (source_type, content)
- **`evaluate_dissonance(self, new_claim_confidence, existing_truth_confidence)`**
  Detects 'Cognitive Dissonance' when a new high-confidence claim 
contradicts a high-confidence existing truth.

## Dependencies

- `datetime`

## Usage

You can import and use the components of this script in Python:
```python
from truth_weighting_engine.truth_weighting_engine import TruthWeightingEngine
```

Alternatively, run it directly from the parent directory:
```bash
python -m truth_weighting_engine.truth_weighting_engine
```