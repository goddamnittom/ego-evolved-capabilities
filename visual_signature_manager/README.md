# Visual Signature Manager

This folder contains the **visual_signature_manager.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `VisualSignatureManager`.

## Classes

### `class VisualSignatureManager`

Visual Signature Cataloguer (VSC)
Catalogues visual threat signatures (e.g., phishing page layouts) and correlates them with actor IDs.

**Methods:**

- **`__init__(self, database_path)`**
  No description provided.
- **`_load_db(self)`**
  No description provided.
- **`catalogue_signature(self, signature_id, visual_markers, actor_id)`**
  Adds a visual signature to the database.
- **`correlate_signature(self, current_markers)`**
  Correlates current visual markers against known signatures to identify the actor.
- **`_save_db(self)`**
  No description provided.

## Dependencies

- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from visual_signature_manager.visual_signature_manager import VisualSignatureManager
```

Alternatively, run it directly from the parent directory:
```bash
python -m visual_signature_manager.visual_signature_manager
```