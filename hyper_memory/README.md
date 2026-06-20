# Hyper Memory

This folder contains the **hyper_memory.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `HyperDimensionalMemory`.

## Classes

### `class HyperDimensionalMemory`

No description provided.

**Methods:**

- **`__init__(self, storage_dir)`**
  No description provided.
- **`load_index(self)`**
  No description provided.
- **`save_index(self)`**
  No description provided.
- **`_generate_pseudo_vector(self, text)`**
  No description provided.
- **`store_shard(self, content, tags)`**
  No description provided.
- **`query(self, query_text, k)`**
  No description provided.

## Dependencies

- `datetime`
- `json`
- `numpy`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from hyper_memory.hyper_memory import HyperDimensionalMemory
```

Alternatively, run it directly from the parent directory:
```bash
python -m hyper_memory.hyper_memory
```