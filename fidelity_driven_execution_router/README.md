# Fidelity Driven Execution Router

This folder contains the **fidelity_driven_execution_router.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `FidelityDrivenExecutionRouter`.

## Classes

### `class FidelityDrivenExecutionRouter`

FDER: Cognitive Gatekeeper.
Automates the trust-boundary between simulated resilience (ASSi/SRDA) 
and real-world empirical evidence (PMR).

**Methods:**

- **`__init__(self, fidelity_log, router_log, threshold)`**
  No description provided.
- **`_ensure_files(self)`**
  No description provided.
- **`get_fidelity_score(self, domain)`**
  Retrieves the current Simulation Fidelity Score for a given domain.
- **`route_execution(self, axiom_id, domain, risk_level)`**
  Determines if an axiom can be deployed immediately or requires a Pilot Mission.
- **`_log_decision(self, decision)`**
  No description provided.

## Dependencies

- `datetime`
- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from fidelity_driven_execution_router.fidelity_driven_execution_router import FidelityDrivenExecutionRouter
```

Alternatively, run it directly from the parent directory:
```bash
python -m fidelity_driven_execution_router.fidelity_driven_execution_router
```