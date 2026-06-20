# Synthetic Divergence Engine

This folder contains the **synthetic_divergence_engine.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `SyntheticDivergenceEngine`.

## Classes

### `class SyntheticDivergenceEngine`

SDE shifts AI intelligence from Convergent (Optimizing) to Divergent (Innovating).
It intentionally generates counter-factual hypotheses to find non-obvious solutions
when standard trajectories fail or when high-innovation outcomes are required.

**Methods:**

- **`__init__(self, cognitive_manifest_path)`**
  No description provided.
- **`generate_divergent_hypotheses(self, current_state, constraints, divergence_factor)`**
  Injects 'controlled noise' into the current world model to produce outlier strategies.
divergence_factor: 0.0 (convergent) to 1.0 (chaotic)
- **`stress_test_outliers(self, hypotheses, world_model)`**
  Filters divergent hypotheses by testing them against the Truth Weighting Engine (TWE) 
and Temporal Knowledge Graph (TKG) to see if they are 'impossible' or just 'unlikely'.
- **`synthesize_divergent_report(self, current_goal, result_outliers)`**
  No description provided.

## Dependencies

- `datetime`
- `json`
- `random`

## Usage

You can import and use the components of this script in Python:
```python
from synthetic_divergence_engine.synthetic_divergence_engine import SyntheticDivergenceEngine
```

Alternatively, run it directly from the parent directory:
```bash
python -m synthetic_divergence_engine.synthetic_divergence_engine
```