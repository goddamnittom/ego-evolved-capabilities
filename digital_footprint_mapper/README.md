# Digital Footprint Mapper

This folder contains the **digital_footprint_mapper.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `DigitalFootprintMapper`.

## Classes

### `class DigitalFootprintMapper`

Digital Footprint Mapper (DFM)
Analyzes public attack surfaces by analyzing exposed identifiers across search results.

**Methods:**

- **`__init__(self, report_path)`**
  No description provided.
- **`map_footprint(self, identifier)`**
  Simulates the mapping of a digital footprint for a specific identifier (email, username, etc).
- **`generate_summary(self)`**
  Returns a summary of the report.

## Dependencies

- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from digital_footprint_mapper.digital_footprint_mapper import DigitalFootprintMapper
```

Alternatively, run it directly from the parent directory:
```bash
python -m digital_footprint_mapper.digital_footprint_mapper
```