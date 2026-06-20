# Adversarial Path Simulator

This folder contains the **adversarial_path_simulator.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `AdversarialPathSimulator`.

## Classes

### `class AdversarialPathSimulator`

No description provided.

**Methods:**

- **`__init__(self, trust_graph, hardening_manifest)`**
  trust_graph: { "node_a": ["node_b", "node_c"], ... }
hardening_manifest: { "node_a": 0.9, "node_b": 0.1, ... } (0.0 = compromised, 1.0 = fully hardened)
- **`calculate_pivot_cost(self, start_node, end_node)`**
  No description provided.
- **`find_most_likely_path(self, start_node, target_node)`**
  No description provided.
- **`identify_choke_points(self, start_node, target_node)`**
  No description provided.

## Dependencies

- `heapq`
- `json`

## Usage

You can import and use the components of this script in Python:
```python
from adversarial_path_simulator.adversarial_path_simulator import AdversarialPathSimulator
```

Alternatively, run it directly from the parent directory:
```bash
python -m adversarial_path_simulator.adversarial_path_simulator
```