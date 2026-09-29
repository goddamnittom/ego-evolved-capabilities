---
name: ego-gravity
description: Run Ego AntigravityEngine audit and orchestrator phase changes. Use when reviewing capability gravity, constraints, or evolution phases. Not the Google agy binary itself.
---

# Ego gravity audit

`engines/antigravity.py` is an in-repo audit engine. Google Antigravity CLI is the `agy` binary.

```bash
export PYTHONPATH="$PWD:$PYTHONPATH"
python -m engines.agy_bridge gravity
python -m engines.agy_bridge phase --phase 1
```

Use the JSON report to pick the next module to implement or harden. Do not invent a second capability list; update CATALOG.md if the tree changes.
