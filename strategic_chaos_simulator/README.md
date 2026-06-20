# Strategic Chaos Simulator

This folder contains the **strategic_chaos_simulator.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `StrategicChaosSimulator`.

## Classes

### `class StrategicChaosSimulator`

SCS shifts strategic planning from 'Success-Probability' to 'Failure-Hardened Resilience'.
It stress-tests Tactical Execution Blueprints (TEB) by injecting 'Black Swan' events
to identify structural fragility and single points of failure.

**Methods:**

- **`__init__(self)`**
  No description provided.
- **`simulate(self, blueprint)`**
  Simulates the execution of a blueprint under chaotic conditions.
blueprint: List of tasks with dependencies.

## Dependencies

- `json`
- `random`

## Usage

You can import and use the components of this script in Python:
```python
from strategic_chaos_simulator.strategic_chaos_simulator import StrategicChaosSimulator
```

Alternatively, run it directly from the parent directory:
```bash
python -m strategic_chaos_simulator.strategic_chaos_simulator
```