# Proposal: Physical Action Layer (PAL) for Gemini Robotics-ER 1.6
**Version:** 1.0.0
**Status:** Draft / Conceptual
**Project:** Antigravity Phase 4 - Embodied Reasoning Integration

## 1. Executive Summary
The Physical Action Layer (PAL) serves as the "spinal cord" of the robotic system. It is the critical translation engine that converts high-level, semantic reasoning outputs from the Gemini Robotics-ER 1.6 VLM into low-level, deterministic robotic primitive commands. The PAL ensures that abstract intent (e.g., "Grasp the gauge") is executed with millimeter precision and safety-guarded movements.

## 2. Architectural Workflow
The PAL operates on a **three-stage pipeline**:

### Stage 1: Semantic Parsing (The Translator)
The PAL intercepts the VLM's output string and extracts the `ACTION` primitive and its associated `COORDINATES`.
- **Input:** `ACTION: GRASP ([450, 200, 550, 300])`
- **Process:** Normalizes the 0-1000 VLM coordinates into the robot's actual Cartesian space (e.g., millimeters relative to the base).
- **Output:** `primitive="grasp", target=[x, y, z, roll, pitch, yaw]`

### Stage 2: Kinematic Mapping (The Planner)
The PAL maps the target coordinates to a sequence of joint-level movements.
- **Inverse Kinematics (IK):** Calculates the necessary joint angles to reach the target.
- **Trajectory Generation:** Creates a smooth, collision-free path from the current position to the target.
- **Constraint Checking:** Ensures the movement doesn't violate physical joint limits or environmental obstacles.

### Stage 3: Actuation (The Driver)
The PAL sends the trajectory to the motor controllers via a real-time interface (e.g., ROS2 / EtherCAT).
- **Execution:** Streams joint commands at 1kHz.
- **Force Feedback:** Monitors torque/current sensors to detect physical contact (e.g., "Grip closure detected").

---

## 3. The "Fast-Path" Tactical Loop (Latency Mitigation)
To prevent "reasoning lag," the PAL implements a dual-track execution model:

1.  **The Slow-Path (Cognitive):** Gemini ER 1.6 $\rightarrow$ High-level goal $\rightarrow$ PAL $\rightarrow$ Complex movement. (Used for planning).
2.  **The Fast-Path (Reactive):** Sensor Input $\rightarrow$ PAL $\rightarrow$ Immediate Adjustment. (Used for safety/fine-tuning).
    - *Example:* If a tactile sensor detects a slip during a `GRASP`, the Fast-Path increases grip pressure instantly without waiting for a new VLM inference.

---

## 4. Conceptual API Specification: Robotic Primitives

The PAL exposes a set of "Atomic Primitives" that the VLM can invoke:

| Primitive | Input | Description | Success Metric |
| :--- | :--- | :--- | :--- |
| `MOVE_TO` | `coord` | Move end-effector to target point. | $\text{dist}(\text{current, target}) < 1\text{mm}$ |
| `GRASP` | `coord, force` | Close gripper at target coordinates. | $\text{Current Spike} \geq \text{threshold}$ |
| `RELEASE` | `none` | Open gripper. | $\text{Gripper Width} = \text{Max}$ |
| `SCAN_AREA` | `bbox` | Perform a multi-view visual sweep. | $\text{Image Coverage} \geq 90\%$ |
| `PUSH` | `coord, vector` | Apply linear force in a specific direction. | $\text{Displacement} \geq \text{target}$ |

---

## 5. Integration with MCT & ER Bridge
The PAL closes the loop by feeding execution state back into the **Mission Control Telemetry (MCT)**:
- **PAL $\rightarrow$ MCT:** `STATE: MOVING` $\rightarrow$ `STATE: CONTACT_MADE` $\rightarrow$ `STATE: ACTION_COMPLETE`.
- **MCT $\rightarrow$ ER 1.6:** The VLM sees the `ACTION_COMPLETE` signal and performs a visual check to confirm if the action actually achieved the strategic goal (e.g., "Is the gauge now read?").

## 6. Conclusion
The Physical Action Layer transforms Gemini ER 1.6 from a "Seeing-Thinking" model into a "Seeing-Thinking-Doing" agent. By separating high-level reasoning from low-level actuation, the system gains the stability of traditional robotics and the flexibility of frontier AI.
