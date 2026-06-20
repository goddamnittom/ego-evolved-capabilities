# Cross Identity Trust Graph

This folder contains the **cross_identity_trust_graph.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `CrossIdentityTrustGraph`.

## Classes

### `class CrossIdentityTrustGraph`

No description provided.

**Methods:**

- **`__init__(self)`**
  No description provided.
- **`add_trust_relationship(self, source, target, relationship_type)`**
  No description provided.
- **`calculate_cascade_risk(self, compromised_node)`**
  No description provided.
- **`find_root_of_trust(self)`**
  No description provided.

## Dependencies

- `json`

## Usage

You can import and use the components of this script in Python:
```python
from cross_identity_trust_graph.cross_identity_trust_graph import CrossIdentityTrustGraph
```

Alternatively, run it directly from the parent directory:
```bash
python -m cross_identity_trust_graph.cross_identity_trust_graph
```