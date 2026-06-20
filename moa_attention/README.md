# Moa Attention

This folder contains the **moa_attention.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following functions: `standard_attention`, `moa_dnf_attention`.

## Functions

### `def standard_attention(Q, K, V)`

Reference standard attention with numerically stable softmax using NumPy.
Recreates intermediate matrices: scores (n x n), max_scores (n x 1),
exp_scores (n x n), sum_exp (n x 1), and attn_weights (n x n).

### `def moa_dnf_attention(Q, K, V)`

MoA Denotational Normal Form (DNF) Attention.
Computes elements on-the-fly directly from input indexing without materializing
the intermediate O(n^2) score, exponent, or attention weight matrices.
Memory traffic is O(n*d_k + n*d_v) with O(1) scratch space per thread/lane.

## Dependencies

- `numpy`

## Usage

You can import and use the components of this script in Python:
```python
from moa_attention.moa_attention import standard_attention
```

Alternatively, run it directly from the parent directory:
```bash
python -m moa_attention.moa_attention
```