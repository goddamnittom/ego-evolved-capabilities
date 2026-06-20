# Mission T3 Simulation

This folder contains the **mission_t3_simulation.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following functions: `simulate_er_1_6_perception`, `er_mct_bridge`, `run_simulation`.

## Functions

### `def simulate_er_1_6_perception(ground_truth, noise_level)`

Simulates the VLM perception phase.
noise_level: 0.0 = Perfect, >0.0 = Chance of error/drift.

### `def er_mct_bridge(perception_output)`

Transforms ER 1.6 perception signal into MCT Telemetry.

### `def run_simulation(iterations, noise)`

No description provided.

## Dependencies

- `datetime`
- `json`
- `uuid`

## Usage

You can import and use the components of this script in Python:
```python
from mission_t3_simulation.mission_t3_simulation import simulate_er_1_6_perception
```

Alternatively, run it directly from the parent directory:
```bash
python -m mission_t3_simulation.mission_t3_simulation
```