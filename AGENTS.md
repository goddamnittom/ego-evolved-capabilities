# Ego evolved capabilities — Antigravity workspace

This repo is a library of standalone Python modules, not one app.
When working here, use the packages instead of inventing parallel engines.

## Import / run

Repo root must be on PYTHONPATH.

```bash
export PYTHONPATH="$PWD:$PYTHONPATH"
python -m engines.agy_bridge entropy --predicted mfa_challenge,login_success --observed login_success
python -m engines.agy_bridge semantic --probs 0.3,0.3,0.2,0.2
python -m engines.agy_bridge gravity
python -m engines.ioai_protocol
```

```python
from cognitive.cognitive_entropy_monitor import CognitiveEntropyMonitor
from cognitive.semantic_entropy_monitor import SemanticEntropyMonitor
from engines.antigravity import AntigravityEngine
```

## Map

- `engines/` IOAI, MoA, coder daemons, antigravity, orchestrators
- `cognitive/` monitors, entropy, strategy
- `adversarial/` red team, evidence, threat
- `hardening/` IR, hardening
- `memory/` dreaming / hyper memory
- `CATALOG.md` full module list

## Rules for the agent

- Prefer existing modules over new files with the same job.
- Do not treat module names as proof of behavior. Read the file.
- CognitiveEntropyMonitor is a predicted-vs-observed miss-rate, not Shannon entropy.
- SemanticEntropyMonitor is Shannon entropy over hypothesis weights (needs numpy).
- Default log paths under `/root/` will fail outside the old sandbox. Point them at `./logs/`.
- `engines/antigravity.py` is an audit/roadmap generator, not the Google `agy` binary.
