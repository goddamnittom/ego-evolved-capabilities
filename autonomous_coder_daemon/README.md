# Autonomous Coder Daemon

This folder contains the **autonomous_coder_daemon.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `AutonomousCoderDaemon`.

## Classes

### `class AutonomousCoderDaemon`

Headless Self-Improving Daemon mapping to the User's Power User Workflow:
1. Spec -> 2. Plan -> 3. TDD -> 4. Polish.

**Methods:**

- **`__init__(self, target_repo_path)`**
  No description provided.
- **`run_cmd(self, cmd, cwd)`**
  No description provided.
- **`fetch_tasks(self)`**
  No description provided.
- **`save_tasks(self, tasks)`**
  No description provided.
- **`process_task(self, task)`**
  No description provided.
- **`start(self, poll_interval)`**
  No description provided.

## Dependencies

- `datetime`
- `json`
- `logging`
- `os`
- `subprocess`
- `sys`
- `time`

## Usage

You can import and use the components of this script in Python:
```python
from autonomous_coder_daemon.autonomous_coder_daemon import AutonomousCoderDaemon
```

Alternatively, run it directly from the parent directory:
```bash
python -m autonomous_coder_daemon.autonomous_coder_daemon
```