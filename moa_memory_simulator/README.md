# Moa Memory Simulator

This folder contains the **moa_memory_simulator.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following functions: `standard_attention_memory`, `moa_dnf_attention_memory`, `run_simulation`.

## Functions

### `def standard_attention_memory(n, d_k, d_v)`

Memory for Q, K, V (n x d), intermediate scores (n x n), softmax (n x n), Output (n x d)

### `def moa_dnf_attention_memory(n, d_k, d_v)`

Memory for Q, K, V (n x d), and scalar/vector intermediaries, avoiding n x n.

### `def run_simulation(n_list, d_k, d_v)`

No description provided.

## Dependencies

- `numpy`

## Usage

You can import and use the components of this script in Python:
```python
from moa_memory_simulator.moa_memory_simulator import standard_attention_memory
```

Alternatively, run it directly from the parent directory:
```bash
python -m moa_memory_simulator.moa_memory_simulator
```