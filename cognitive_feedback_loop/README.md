# Cognitive Feedback Loop

This folder contains the **cognitive_feedback_loop.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `CognitiveFeedbackLoop`.

## Classes

### `class CognitiveFeedbackLoop`

CFL: Cognitive Feedback Loop
Acts as a quality gate between steps of an orchestrated cognitive chain.
Prevents 'hallucination cascades' by validating intermediate outputs.

**Methods:**

- **`__init__(self)`**
  No description provided.
- **`validate_step(self, step_name, output, context)`**
  Validates the output of a cognitive module against the current context.
Returns: (passed, recommendation)
- **`orchestrate_pivot(self, current_chain, failed_step, recommendation)`**
  Calculates a pivot for TCO based on the failure mode.

## Dependencies

- `json`
- `logging`

## Usage

You can import and use the components of this script in Python:
```python
from cognitive_feedback_loop.cognitive_feedback_loop import CognitiveFeedbackLoop
```

Alternatively, run it directly from the parent directory:
```bash
python -m cognitive_feedback_loop.cognitive_feedback_loop
```