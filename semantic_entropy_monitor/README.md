# Semantic Entropy Monitor

This folder contains the **semantic_entropy_monitor.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `SemanticEntropyMonitor`.

## Classes

### `class SemanticEntropyMonitor`

SEM calculates the Shannon Entropy of strategic hypotheses to determine
whether the AI should be in 'Exploration' (high entropy) or 'Exploitation' (low entropy) mode.

**Methods:**

- **`__init__(self, entropy_threshold)`**
  No description provided.
- **`calculate_entropy(self, probabilities)`**
  Calculates Shannon Entropy: H = -sum(p * log2(p))
- **`evaluate_mode(self, probabilities)`**
  Determines the cognitive mode based on entropy.
- High Entropy: Multiple competing hypotheses -> EXPLORATION (Search/Diverge)
- Low Entropy: Single dominant hypothesis -> EXPLOITATION (Execute/Converge)

## Dependencies

- `numpy`
- `typing`

## Usage

You can import and use the components of this script in Python:
```python
from semantic_entropy_monitor.semantic_entropy_monitor import SemanticEntropyMonitor
```

Alternatively, run it directly from the parent directory:
```bash
python -m semantic_entropy_monitor.semantic_entropy_monitor
```