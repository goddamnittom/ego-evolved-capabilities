# Kinematic Translation Layer

This folder contains the **kinematic_translation_layer.py** script, which is part of Ego's evolved capabilities workflow.

## Overview

This script defines the following class: `KinematicTranslationLayer`.

## Classes

### `class KinematicTranslationLayer`

Bridges the gap between VLM spatial coordinates and robotic primitive commands.
Translates target coordinates [x, y, z] into joint trajectories based on robot configuration.

**Methods:**

- **`__init__(self, robot_config)`**
  No description provided.
- **`solve_inverse_kinematics(self, target_coord)`**
  Simplified IK Solver. 
In a real system, this would use Jacobian matrices or FABRIK.
Here, it maps coordinates to joint angles based on a simplified 3-DOF arm model.
- **`generate_primitive_commands(self, target_coord)`**
  Translates IK solution into executable primitive commands.

## Dependencies

- `json`
- `math`

## Usage

You can import and use the components of this script in Python:
```python
from kinematic_translation_layer.kinematic_translation_layer import KinematicTranslationLayer
```

Alternatively, run it directly from the parent directory:
```bash
python -m kinematic_translation_layer.kinematic_translation_layer
```