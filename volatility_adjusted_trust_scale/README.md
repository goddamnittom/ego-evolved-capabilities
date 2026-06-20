# Volatility Adjusted Trust Scale

This folder contains the **volatility_adjusted_trust_scale.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `VolatilityAdjustedTrustScale`.

## Classes

### `class VolatilityAdjustedTrustScale`

VATS: Dynamic Threshold Adaptation.
Links the FDER thresholds to a real-time Environmental Volatility Index (EVI).
As volatility increases, trust thresholds tighten, forcing more Pilot Missions.

**Methods:**

- **`__init__(self, evi_source, fder_config)`**
  No description provided.
- **`_ensure_files(self)`**
  No description provided.
- **`get_current_evi(self)`**
  No description provided.
- **`calculate_adjusted_threshold(self, risk_level)`**
  No description provided.
- **`sync_fder(self)`**
  Pushes the updated thresholds to the FDER system.

## Dependencies

- `datetime`
- `json`
- `os`

## Usage

You can import and use the components of this script in Python:
```python
from volatility_adjusted_trust_scale.volatility_adjusted_trust_scale import VolatilityAdjustedTrustScale
```

Alternatively, run it directly from the parent directory:
```bash
python -m volatility_adjusted_trust_scale.volatility_adjusted_trust_scale
```