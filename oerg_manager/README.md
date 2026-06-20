# Oerg Manager

This folder contains the **oerg_manager.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `OERGManager`.

## Classes

### `class OERGManager`

No description provided.

**Methods:**

- **`__init__(self, storage_path)`**
  No description provided.
- **`_load_graph(self)`**
  No description provided.
- **`_save_graph(self)`**
  No description provided.
- **`add_node(self, node_id, node_type, name)`**
  No description provided.
- **`add_edge(self, source, target, relation, confidence)`**
  No description provided.
- **`get_entity_details(self, node_id)`**
  No description provided.
- **`find_connections(self, node_id)`**
  No description provided.
- **`list_all_nodes(self)`**
  No description provided.

## Dependencies

- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from oerg_manager.oerg_manager import OERGManager
```

Alternatively, run it directly from the parent directory:
```bash
python -m oerg_manager.oerg_manager
```