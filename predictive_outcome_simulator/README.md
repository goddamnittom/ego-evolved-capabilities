# Predictive Outcome Simulator

This folder contains the **predictive_outcome_simulator.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `PredictiveOutcomeSimulator`.

## Classes

### `class PredictiveOutcomeSimulator`

POS evolves strategic planning from heuristic probability to stochastic simulation.
It models a strategy as a causal chain and simulates outcomes across parameterized variables.

**Methods:**

- **`__init__(self)`**
  No description provided.
- **`simulate_strategy(self, causal_chain, variables, iterations)`**
  Simulates a strategy causal chain across multiple iterations.

causal_chain: [
    {"step": "Step 1", "success_prob": 0.8, "dependencies": [], "variable_impact": {"latency": -0.1}},
    {"step": "Step 2", "success_prob": 0.7, "dependencies": ["Step 1"], "variable_impact": {"attacker_skill": -0.2}},
]
variables: {
    "latency": {"mean": 0, "std": 1}, 
    "attacker_skill": {"mean": 0, "std": 1}
}

## Dependencies

- `numpy`
- `random`
- `typing`

## Usage

You can import and use the components of this script in Python:
```python
from predictive_outcome_simulator.predictive_outcome_simulator import PredictiveOutcomeSimulator
```

Alternatively, run it directly from the parent directory:
```bash
python -m predictive_outcome_simulator.predictive_outcome_simulator
```