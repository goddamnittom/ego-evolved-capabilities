# Temporal Knowledge Graph

This folder contains the **temporal_knowledge_graph.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `TemporalKnowledgeGraph`.

## Classes

### `class TemporalKnowledgeGraph`

No description provided.

**Methods:**

- **`__init__(self, storage_path)`**
  No description provided.
- **`_load_graph(self)`**
  No description provided.
- **`_save_graph(self)`**
  No description provided.
- **`update_entity(self, entity_id, properties, source)`**
  Updates an entity with new properties, maintaining a temporal history of changes.
- **`get_entity(self, entity_id)`**
  No description provided.
- **`get_evolution(self, entity_id)`**
  Returns the history of changes for an entity.
- **`query_all_entities(self)`**
  No description provided.

## Dependencies

- `datetime`
- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from temporal_knowledge_graph.temporal_knowledge_graph import TemporalKnowledgeGraph
```

Alternatively, run it directly from the parent directory:
```bash
python -m temporal_knowledge_graph.temporal_knowledge_graph
```