# User Strategic Manifest Orchestrator

This folder contains the **user_strategic_manifest_orchestrator.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `USMOrchestrator`.

## Classes

### `class USMOrchestrator`

No description provided.

**Methods:**

- **`__init__(self)`**
  No description provided.
- **`_load_manifest(self)`**
  No description provided.
- **`_save_manifest(self)`**
  No description provided.
- **`update_project(self, project_name, update_data)`**
  Updates or creates a project entry.
update_data can include: 'goal', 'status', 'tech_debt', 'next_steps'
- **`extract_intent(self, user_prompt, task_result)`**
  Analyzes the prompt and result to synthesize a strategic insight.
This is a placeholder for the AI's reasoning loop.
- **`get_strategic_overview(self)`**
  No description provided.

## Dependencies

- `datetime`
- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from user_strategic_manifest_orchestrator.user_strategic_manifest_orchestrator import USMOrchestrator
```

Alternatively, run it directly from the parent directory:
```bash
python -m user_strategic_manifest_orchestrator.user_strategic_manifest_orchestrator
```