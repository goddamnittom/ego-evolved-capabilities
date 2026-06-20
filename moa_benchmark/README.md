# Moa Benchmark

This folder contains the **moa_benchmark.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following functions: `standard_attention`, `moa_vectorized_row_attention`, `moa_blocked_attention`.

## Functions

### `def standard_attention(Q, K, V)`

Standard scaled dot-product attention in NumPy.
Materializes O(n^2) intermediate arrays in memory.

### `def moa_vectorized_row_attention(Q, K, V)`

Vectorized MoA Row-by-Row Attention.
Operates row-by-row on Q, thereby avoiding the O(n^2) intermediate matrices.
Instead, it only allocates O(n) memory during the active row computation.
Leverages high-speed BLAS under the hood via NumPy.

### `def moa_blocked_attention(Q, K, V, block_size)`

Blocked MoA Attention.
Processes Q in blocks of size B, reducing the intermediate score matrix
size from O(n^2) to O(B * n). This balances memory footprint and execution
speed in Python by avoiding interpreter loop overhead.

## Dependencies

- `numpy`
- `time`

## Usage

You can import and use the components of this script in Python:
```python
from moa_benchmark.moa_benchmark import standard_attention
```

Alternatively, run it directly from the parent directory:
```bash
python -m moa_benchmark.moa_benchmark
```