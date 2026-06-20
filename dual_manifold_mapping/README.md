# Dual Manifold Mapping

This folder contains the **dual_manifold_mapping.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `DualManifoldMapper`.

## Classes

### `class DualManifoldMapper`

Non-Parametric Dual-Manifold Mapping via 8-Bit Bounded Transformation Matrices
Inspired by SOTA arXiv:2606.13328v1.

**Methods:**

- **`__init__(self, n_spatial, n_structural, seed)`**
  No description provided.
- **`encode_spatial(self, spatial_vector)`**
  Binarize or sign-encode spatial inputs to simplify multiplication into bitwise/accumulation logic.
- **`forward_inference(self, spatial_encoded)`**
  FP-multiplier-free inference. Accumulates directional sign-charges.
We accumulate the Z-matrix coefficients based on the sign of the input.
If spatial_encoded is +1, we add Z. If -1, we subtract Z.
This represents pure accumulation logic: Out = Sum(Z_ij * Input_j) -> Sum(Sign(Input_j) * Z_ij).
- **`update_matrix(self, spatial_encoded, target_structural, lr, noise_scale)`**
  Localized, bounded update mechanism restricted strictly within [-127, 127],
modulated by stochastic noise injection.
- **`simulate_holographic_resilience(self, spatial_vector, truncation_sparsity, node_destruction)`**
  Demonstrate holographic resilience under severe truncation sparsity and random node destruction.

## Dependencies

- `numpy`
- `time`

## Usage

You can import and use the components of this script in Python:
```python
from dual_manifold_mapping.dual_manifold_mapping import DualManifoldMapper
```

Alternatively, run it directly from the parent directory:
```bash
python -m dual_manifold_mapping.dual_manifold_mapping
```