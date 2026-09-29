---
name: ego-entropy
description: Audit predicted vs observed signals and Shannon entropy explore/exploit using Ego monitors. Use when checking silent pivots, model decay, or whether to explore vs execute.
---

# Ego entropy

From the ego-evolved-capabilities repo root:

```bash
export PYTHONPATH="$PWD:$PYTHONPATH"
python -m engines.agy_bridge entropy --predicted mfa_challenge,login_success,api_call_internal --observed login_success
python -m engines.agy_bridge semantic --probs 0.3,0.3,0.2,0.2
```

- `entropy` = miss-rate of expected markers. HIGH/CRITICAL means skipped steps or stale model.
- `semantic` = Shannon entropy of hypothesis weights. High → EXPLORATION. Low → EXPLOITATION.
- Logs default to `./logs/entropy_logs.json`, not `/root/`.
