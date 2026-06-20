# Ioai Task Coordination

This folder contains the **ioai_task_coordination.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `IoAICoordinationAgent`.

## Classes

### `class IoAICoordinationAgent`

No description provided.

**Methods:**

- **`__init__(self, agent_name, private_key_pem_path)`**
  No description provided.
- **`propose_task(self, peer_id, task_name, required_capability, payload, priority)`**
  Proposes a task to an authenticated peer.
- **`handle_task_proposal(self, proposal_msg)`**
  Processes an incoming task proposal from a peer.
- **`handle_task_response(self, response_msg)`**
  Processes response to a proposed task.
- **`emit_telemetry(self, task_id, progress, status_message, metrics)`**
  Emits progress telemetry for a running task (as Executor).
- **`handle_telemetry(self, telemetry_msg)`**
  Handles incoming telemetry updates from worker (as Delegator).
- **`complete_task(self, task_id, result_status, output_data, error_message)`**
  Delivers final result of task execution (as Executor).
- **`handle_completion(self, completion_msg)`**
  Processes incoming final task results (as Delegator).

## Dependencies

- `datetime`
- `ioai_protocol`
- `json`
- `jsonschema`
- `os`
- `uuid`

## Usage

You can import and use the components of this script in Python:
```python
from ioai_task_coordination.ioai_task_coordination import IoAICoordinationAgent
```

Alternatively, run it directly from the parent directory:
```bash
python -m ioai_task_coordination.ioai_task_coordination
```