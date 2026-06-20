# Discord Bridge

This folder contains the **discord_bridge.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following functions: `load_config`, `save_config`, `load_inbox`, `save_inbox`, `send_message`, `fetch_messages`, `poll_channel`, `main`.

## Functions

### `def load_config()`

No description provided.

### `def save_config(config)`

No description provided.

### `def load_inbox()`

No description provided.

### `def save_inbox(messages)`

No description provided.

### `def send_message(content, config)`

No description provided.

### `def fetch_messages(config, limit, after_id)`

No description provided.

### `def poll_channel(config)`

No description provided.

### `def main()`

No description provided.

## Dependencies

- `argparse`
- `datetime`
- `json`
- `os`
- `requests`
- `sys`

## Usage

You can import and use the components of this script in Python:
```python
from discord_bridge.discord_bridge import load_config
```

Alternatively, run it directly from the parent directory:
```bash
python -m discord_bridge.discord_bridge
```