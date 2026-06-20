# Actor Behavioral Profiling

This folder contains the **actor_behavioral_profiling.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `ActorBehavioralProfiler`.

## Classes

### `class ActorBehavioralProfiler`

No description provided.

**Methods:**

- **`__init__(self, profiles_path)`**
  No description provided.
- **`_load_profiles(self)`**
  No description provided.
- **`_save_profiles(self)`**
  No description provided.
- **`ingest_event(self, event_data)`**
  Ingests a security event and updates the corresponding actor profile.
event_data: { 'actor_id': '...', 'timestamp': '...', 'action': '...', 'target': '...', 'marker': '...' }
- **`predict_next_move(self, actor_id)`**
  Predicts the next target/action based on the actor's history.

## Dependencies

- `datetime`
- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from actor_behavioral_profiling.actor_behavioral_profiling import ActorBehavioralProfiler
```

Alternatively, run it directly from the parent directory:
```bash
python -m actor_behavioral_profiling.actor_behavioral_profiling
```