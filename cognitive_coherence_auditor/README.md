# Cognitive Coherence Auditor

This folder contains the **cognitive_coherence_auditor.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `CognitiveCoherenceAuditor`.

## Classes

### `class CognitiveCoherenceAuditor`

The CCA monitors the integrity of Ego's evolved cognitive state.
It prevents 'Cognitive Fragmentation'—the emergence of contradictory 
assumptions as new modules are added.

**Methods:**

- **`__init__(self, memory_path)`**
  No description provided.
- **`audit_contradictions(self, knowledge_graph)`**
  Scans the knowledge graph for conflicting nodes or edges 
that imply contradictory states for the same asset.
- **`run_regression_benchmarks(self, benchmark_suite)`**
  Executes a set of standard 'Reasoning Tests' to ensure a new 
evolution (e.g., RIS) hasn't degraded a previous capability (e.g., DCE).
- **`prune_obsolete_hypotheses(self, hypotheses_list)`**
  Identifies hypotheses that have been superseded by higher-confidence 
evidence but still exist in memory.

## Dependencies

- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from cognitive_coherence_auditor.cognitive_coherence_auditor import CognitiveCoherenceAuditor
```

Alternatively, run it directly from the parent directory:
```bash
python -m cognitive_coherence_auditor.cognitive_coherence_auditor
```