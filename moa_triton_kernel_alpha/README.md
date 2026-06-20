# Moa Triton Kernel Alpha

This folder contains the **moa_triton_kernel_alpha.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following functions: `moa_dnf_fwd_kernel`, `moa_attention_forward`.

## Functions

### `def moa_dnf_fwd_kernel(Q, K, V, sm_scale, Out, stride_qz, stride_qh, stride_qm, stride_qk, stride_kz, stride_kh, stride_kn, stride_kk, stride_vz, stride_vh, stride_vn, stride_vk, stride_oz, stride_oh, stride_om, stride_ok, Z, H, N_ctx, BLOCK_M, BLOCK_DMODEL, BLOCK_N, IS_CAUSAL)`

MoA DNF Forward Math Kernel compiled via OpenAI Triton.
Forces extreme L1 cache utilization by executing the Disjunctive Normal Form
sub-blocks, mapping query and key-value tensors strictly into SRAM.

### `def moa_attention_forward(q, k, v, causal)`

No description provided.

## Dependencies

- `time`
- `torch`
- `triton`

## Usage

You can import and use the components of this script in Python:
```python
from moa_triton_kernel_alpha.moa_triton_kernel_alpha import moa_dnf_fwd_kernel
```

Alternatively, run it directly from the parent directory:
```bash
python -m moa_triton_kernel_alpha.moa_triton_kernel_alpha
```