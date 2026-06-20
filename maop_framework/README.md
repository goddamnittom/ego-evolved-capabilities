# Maop Framework

This folder contains the **maop_framework.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following classes: `TaskStatus`, `AgenticRole`, `TaskBoard`, `BaseAgent`, `ArchitectAgent`, `CoderAgent`, `QAAgent`.

## Classes

### `class TaskStatus`

No description provided.

### `class AgenticRole`

No description provided.

### `class TaskBoard`

No description provided.

**Methods:**

- **`__init__(self)`**
  No description provided.
- **`add_task(self, id, description, required_role)`**
  No description provided.
- **`get_pending(self, role)`**
  No description provided.
- **`update_task(self, id, status, artifact)`**
  No description provided.
- **`all_completed(self)`**
  No description provided.

### `class BaseAgent`

No description provided.

**Methods:**

- **`__init__(self, name, role, board)`**
  No description provided.

### `class ArchitectAgent`

No description provided.

**Methods:**

- **`__init__(self, name, board)`**
  No description provided.

### `class CoderAgent`

No description provided.

### `class QAAgent`

No description provided.

**Methods:**

- **`__init__(self, name, board)`**
  No description provided.

## Dependencies

- `asyncio`
- `enum`
- `json`
- `time`
- `uuid`

## Usage

You can import and use the components of this script in Python:
```python
from maop_framework.maop_framework import TaskStatus
```

Alternatively, run it directly from the parent directory:
```bash
python -m maop_framework.maop_framework
```