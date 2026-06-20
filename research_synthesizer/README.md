# Research Synthesizer

This folder contains the **research_synthesizer.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following function: `synthesize_research`.

## Functions

### `def synthesize_research(topic, findings, output_dir)`

Synthesizes research findings into a structured markdown report.
findings: List of dicts with {'title', 'url', 'content', 'relevance'}

## Dependencies

- `datetime`
- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from research_synthesizer.research_synthesizer import synthesize_research
```

Alternatively, run it directly from the parent directory:
```bash
python -m research_synthesizer.research_synthesizer
```