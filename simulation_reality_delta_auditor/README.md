# Simulation Reality Delta Auditor

This folder contains the **simulation_reality_delta_auditor.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `SimulationRealityDeltaAuditor`.

## Classes

### `class SimulationRealityDeltaAuditor`

SRDA: Calibration-Aware Intelligence Module.
Calculates the "Simulation Fidelity Score" by comparing predicted resilience
(from ASSi) with actual mission outcomes (from PMR).

**Methods:**

- **`__init__(self, sim_log, pmr_log, fidelity_store)`**
  No description provided.
- **`_ensure_files(self)`**
  No description provided.
- **`calculate_fidelity(self, axiom_id)`**
  Computes the delta between predicted avg_resilience and empirical success rate.
Fidelity = 1.0 - abs(Predicted - Actual)
- **`audit_all_axioms(self)`**
  Audits all known axioms to update the global fidelity map.

## Dependencies

- `datetime`
- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from simulation_reality_delta_auditor.simulation_reality_delta_auditor import SimulationRealityDeltaAuditor
```

Alternatively, run it directly from the parent directory:
```bash
python -m simulation_reality_delta_auditor.simulation_reality_delta_auditor
```