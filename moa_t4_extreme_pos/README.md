# Moa T4 Extreme Pos

This folder contains the **moa_t4_extreme_pos.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `PosMetrics` and the following functions: `moa_dnf_stable_softmax_block_test`, `moa_causal_bma_simulate`.

## Classes

### `class PosMetrics`

No description provided.

## Functions

### `def moa_dnf_stable_softmax_block_test(B, d_k, skew)`

Validates MoA DNF stability under Softmax Extreme Skew constraints.
Injects high variance/skew to trigger standard overflow, testing DNF max-shift stabilization.

### `def moa_causal_bma_simulate(N, d_k, d_v, B, dtype, skew_factor)`

No description provided.

## Dependencies

- `dataclasses`
- `json`
- `numpy`

## Usage

You can import and use the components of this script in Python:
```python
from moa_t4_extreme_pos.moa_t4_extreme_pos import PosMetrics
```

Alternatively, run it directly from the parent directory:
```bash
python -m moa_t4_extreme_pos.moa_t4_extreme_pos
```