# Rsg Manager

This folder contains the **rsg_manager.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `RSGManager`.

## Classes

### `class RSGManager`

Recursive Summary Graph (RSG) Manager
Transforms linear mission telemetry into hierarchical Knowledge Nuggets.

**Methods:**

- **`__init__(self, storage_path)`**
  No description provided.
- **`_load_graph(self)`**
  No description provided.
- **`create_nugget(self, title, content, domain, parent_id)`**
  No description provided.
- **`_save_graph(self)`**
  No description provided.
- **`get_domain_summary(self, domain)`**
  No description provided.

## Dependencies

- `datetime`
- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from rsg_manager.rsg_manager import RSGManager
```

Alternatively, run it directly from the parent directory:
```bash
python -m rsg_manager.rsg_manager
```