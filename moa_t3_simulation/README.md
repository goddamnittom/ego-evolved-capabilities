# Moa T3 Simulation

This folder contains the **moa_t3_simulation.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `MoASimulatorT3`.

## Classes

### `class MoASimulatorT3`

Task T3: Simulation & Complexity Modeling for MoA Attention.
Models memory traffic, compute latency, and energy savings under roofline limits.

**Methods:**

- **`__init__(self)`**
  No description provided.
- **`compute_flops(self, n, d_k, d_v)`**
  Calculates standard FLOP count for scaled dot-product attention.
1. QK^T: 2 * n^2 * d_k
2. Scale and Softmax: 5 * n^2 (approx for subtract max, exp, sum, div)
3. Attn * V: 2 * n^2 * d_v
- **`compute_memory_traffic_bytes(self, n, d_k, d_v, precision_bytes)`**
  Calculates total memory traffic (DRAM read/writes in bytes) for:
- Standard (Classical) Attention
- FlashAttention
- MoA (Mathematics of Arrays) Attention (theoretical minimum)
- **`run_roofline_simulation(self, hw_name, n, d_k, d_v, precision_bytes)`**
  Runs latency and energy modeling using the Roofline parameters.
- **`run_stochastic_scenarios(self, n, d_k, d_v)`**
  Integrates with PredictiveOutcomeSimulator to compute probability-weighted matrix of gains.
Varies variables: bandwidth congestion, core scaling efficiency, and L1 cache hits.
- **`run_comprehensive_sweep(self)`**
  No description provided.
- **`print_markdown_report(self, report)`**
  No description provided.

## Dependencies

- `json`
- `numpy`
- `os`
- `predictive_outcome_simulator`
- `sys`

## Usage

You can import and use the components of this script in Python:
```python
from moa_t3_simulation.moa_t3_simulation import MoASimulatorT3
```

Alternatively, run it directly from the parent directory:
```bash
python -m moa_t3_simulation.moa_t3_simulation
```