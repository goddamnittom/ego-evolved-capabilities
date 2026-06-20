# Axiom Interaction Graph

This folder contains the **axiom_interaction_graph.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `AxiomInteractionGraph`.

## Classes

### `class AxiomInteractionGraph`

No description provided.

**Methods:**

- **`__init__(self, axioms_path)`**
  No description provided.
- **`load_axioms(self)`**
  No description provided.
- **`map_dependencies(self)`**
  Analyze axioms for semantic overlaps or logical dependencies.
In a production version, this would use LLM-based semantic analysis.
- **`detect_paradoxes(self)`**
  Identifies contradictory mandates within the graph.
- **`save_graph(self, output_path)`**
  No description provided.

## Dependencies

- `collections`
- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from axiom_interaction_graph.axiom_interaction_graph import AxiomInteractionGraph
```

Alternatively, run it directly from the parent directory:
```bash
python -m axiom_interaction_graph.axiom_interaction_graph
```