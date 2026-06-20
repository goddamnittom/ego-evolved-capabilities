# Ioai Cognitive Bridge

This folder contains the **ioai_cognitive_bridge.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `IoAICognitiveBridge`.

## Classes

### `class IoAICognitiveBridge`

No description provided.

**Methods:**

- **`__init__(self, agent)`**
  No description provided.
- **`register_capability(self, capability_name, file_path, module_name, class_name, method_name)`**
  Allows dynamic registration of capabilities at runtime.
- **`execute_task_locally(self, capability_name, payload)`**
  Dynamically loads the appropriate local cognitive module,
runs the target method with the payload, and returns the result.
- **`process_and_execute_proposal(self, proposal_msg)`**
  1. Validates the proposal.
2. Accepts/Rejects based on capability.
3. If accepted, dynamically executes the task.
4. Emits progress and returns the signed final result.

## Dependencies

- `datetime`
- `importlib`
- `ioai_task_coordination`
- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from ioai_cognitive_bridge.ioai_cognitive_bridge import IoAICognitiveBridge
```

Alternatively, run it directly from the parent directory:
```bash
python -m ioai_cognitive_bridge.ioai_cognitive_bridge
```