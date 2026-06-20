import math
import json

class KinematicTranslationLayer:
    """
    Bridges the gap between VLM spatial coordinates and robotic primitive commands.
    Translates target coordinates [x, y, z] into joint trajectories based on robot configuration.
    """
    def __init__(self, robot_config):
        self.config = robot_config
        self.joints = robot_config.get('joints', [])
        self.base_offset = robot_config.get('base_offset', [0, 0, 0])

    def solve_inverse_kinematics(self, target_coord):
        """
        Simplified IK Solver. 
        In a real system, this would use Jacobian matrices or FABRIK.
        Here, it maps coordinates to joint angles based on a simplified 3-DOF arm model.
        """
        x, y, z = target_coord
        ox, oy, oz = self.base_offset
        
        # Relative target
        dx, dy, dz = x - ox, y - oy, z - oz
        
        # Base Rotation (Theta 0)
        theta0 = math.atan2(dy, dx)
        
        # Reach distance in XY plane
        r = math.sqrt(dx**2 + dy**2)
        
        # Simple 2-link approximation for Theta 1 and 2 (Shoulder/Elbow)
        L1 = self.config.get('L1', 1.0)
        L2 = self.config.get('L2', 1.0)
        
        dist_sq = r**2 + dz**2
        cos_theta2 = (dist_sq - L1**2 - L2**2) / (2 * L1 * L2)
        cos_theta2 = max(-1, min(1, cos_theta2)) # Clamp
        
        theta2 = math.acos(cos_theta2)
        
        # Theta 1 calculation
        phi1 = math.atan2(dz, r)
        phi2 = math.atan2(L2 * math.sin(theta2), L1 + L2 * math.cos(theta2))
        theta1 = phi1 - phi2
        
        return {
            "joint_0": math.degrees(theta0),
            "joint_1": math.degrees(theta1),
            "joint_2": math.degrees(theta2)
        }

    def generate_primitive_commands(self, target_coord):
        """
        Translates IK solution into executable primitive commands.
        """
        angles = self.solve_inverse_kinematics(target_coord)
        commands = []
        
        for joint, angle in angles.items():
            commands.append({
                "primitive": "MOVE_JOINT",
                "params": {"joint_id": joint, "target_angle": round(angle, 2), "speed": "medium"}
            })
        
        commands.append({
            "primitive": "ACTUATE_END_EFFECTOR",
            "params": {"action": "CLOSE", "force": "low"}
        })
        
        return commands

if __name__ == "__main__":
    mock_config = {
        "name": "EgoBot-Alpha",
        "L1": 1.0,
        "L2": 1.0,
        "base_offset": [0, 0, 0],
        "joints": ["joint_0", "joint_1", "joint_2"]
    }
    
    ktl = KinematicTranslationLayer(mock_config)
    target = [1.2, 0.5, 0.8]
    print(f"Target Coordinate: {target}")
    commands = ktl.generate_primitive_commands(target)
    print("\nGenerated Primitive Commands:")
    print(json.dumps(commands, indent=2))
