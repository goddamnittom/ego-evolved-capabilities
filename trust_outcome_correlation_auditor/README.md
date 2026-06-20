# Trust Outcome Correlation Auditor

This folder contains the **trust_outcome_correlation_auditor.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `TrustOutcomeCorrelationAuditor`.

## Classes

### `class TrustOutcomeCorrelationAuditor`

TOCA: Trust-Outcome Correlation Auditor
Closes the loop between Volatility-Adaptive Trust (VATS) decisions 
and actual Post-Mission Retrospective (PMR) outcomes.

**Methods:**

- **`__init__(self, routing_log, pmr_log)`**
  No description provided.
- **`load_json(self, path)`**
  No description provided.
- **`save_json(self, path, data)`**
  No description provided.
- **`audit_decisions(self)`**
  No description provided.
- **`refine_thresholds(self, correlations)`**
  Analyzes correlation patterns to suggest shifts in the EVI-to-Threshold mapping.

## Dependencies

- `datetime`
- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from trust_outcome_correlation_auditor.trust_outcome_correlation_auditor import TrustOutcomeCorrelationAuditor
```

Alternatively, run it directly from the parent directory:
```bash
python -m trust_outcome_correlation_auditor.trust_outcome_correlation_auditor
```