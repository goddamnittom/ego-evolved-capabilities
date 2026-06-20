# Moa Hf Llama Patch

This folder contains the **moa_hf_llama_patch.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following functions: `moa_llama_attention_forward`, `apply_moa_patch`.

## Functions

### `def moa_llama_attention_forward(self, hidden_states, attention_mask, position_ids, past_key_value, output_attentions, use_cache)`

Drop-in replacement for HF LlamaAttention forward pass.
Intercepts the Q/K/V tensors post-RoPE and routes them through the MoA Triton Kernel,
bypassing the standard torch.nn.functional.scaled_dot_product_attention.

### `def apply_moa_patch(model)`

Traverses the Hugging Face model and replaces all LlamaAttention layers
with the MoA optimized pathway.

## Dependencies

- `importlib`
- `logging`
- `torch`
- `transformers`
- `types`

## Usage

You can import and use the components of this script in Python:
```python
from moa_hf_llama_patch.moa_hf_llama_patch import moa_llama_attention_forward
```

Alternatively, run it directly from the parent directory:
```bash
python -m moa_hf_llama_patch.moa_hf_llama_patch
```