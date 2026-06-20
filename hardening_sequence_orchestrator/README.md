# Hardening Sequence Orchestrator

This folder contains the **hardening_sequence_orchestrator.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `HardeningSequenceOrchestrator`.

## Classes

### `class HardeningSequenceOrchestrator`

The HSO optimizes the order of security operations to minimize the 'Window of Re-entry'.
It prevents scenarios where securing one asset allows an attacker to use 
another un-secured asset to revert the changes.

**Methods:**

- **`__init__(self, manifest_path)`**
  No description provided.
- **`calculate_optimal_sequence(self, assets)`**
  No description provided.
- **`generate_orchestration_plan(self, current_state)`**
  No description provided.

## Dependencies

- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from hardening_sequence_orchestrator.hardening_sequence_orchestrator import HardeningSequenceOrchestrator
```

Alternatively, run it directly from the parent directory:
```bash
python -m hardening_sequence_orchestrator.hardening_sequence_orchestrator
```