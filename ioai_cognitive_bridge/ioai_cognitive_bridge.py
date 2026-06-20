import os
import json
import importlib.util
from datetime import datetime, timezone
from ioai_task_coordination import IoAICoordinationAgent

class IoAICognitiveBridge:
    def __init__(self, agent: IoAICoordinationAgent):
        self.agent = agent
        # Map required_capability -> local module/script to execute
        self.capability_map = {
            "dynamic risk assessment": {
                "module_name": "dynamic_risk_engine",
                "class_name": "DynamicRiskEngine",
                "method_name": "run_audit",
                "file_path": "/root/dynamic_risk_engine.py"
            },
            "signal validation framework": {
                "module_name": "ioai_task_coordination",
                "class_name": "IoAICoordinationAgent",
                "method_name": "get_cognitive_schema",
                "file_path": "/root/ioai_task_coordination.py"
            }
        }

    def register_capability(self, capability_name, file_path, module_name, class_name, method_name):
        """Allows dynamic registration of capabilities at runtime."""
        self.capability_map[capability_name.lower()] = {
            "module_name": module_name,
            "class_name": class_name,
            "method_name": method_name,
            "file_path": file_path
        }

    def execute_task_locally(self, capability_name, payload):
        """
        Dynamically loads the appropriate local cognitive module,
        runs the target method with the payload, and returns the result.
        """
        cap_info = self.capability_map.get(capability_name.lower())
        if not cap_info:
            raise ValueError(f"Capability '{capability_name}' is not supported by the local bridge mapping.")

        file_path = cap_info["file_path"]
        module_name = cap_info["module_name"]
        class_name = cap_info["class_name"]
        method_name = cap_info["method_name"]

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Local script not found at: {file_path}")

        # Dynamically import the module
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Instantiate class
        cls = getattr(module, class_name)
        
        # If it's a subclass of IoAIAgent and we are executing it on the current agent,
        # we can pass self.agent or instantiate a new instance
        if class_name == "IoAICoordinationAgent" or class_name == "IoAIAgent":
            instance = self.agent
        else:
            instance = cls()

        # Execute target method
        method = getattr(instance, method_name)
        
        # Determine parameters based on method signature
        # For DynamicRiskEngine.run_audit(blueprint, signals):
        if class_name == "DynamicRiskEngine" and method_name == "run_audit":
            blueprint = payload.get("blueprint", {})
            signals = payload.get("signals", [])
            return method(blueprint, signals)
        
        # Generic fallback: pass payload directly as kwargs or args
        try:
            return method(**payload)
        except TypeError:
            return method()

    def process_and_execute_proposal(self, proposal_msg):
        """
        1. Validates the proposal.
        2. Accepts/Rejects based on capability.
        3. If accepted, dynamically executes the task.
        4. Emits progress and returns the signed final result.
        """
        # Accept or Reject the task
        response = self.agent.handle_task_proposal(proposal_msg)
        
        if response["status"] != "ACCEPTED":
            return response, None

        task_id = proposal_msg["task_id"]
        capability_name = proposal_msg["required_capability"]
        payload = proposal_msg["payload"]

        # Emit 50% Progress Telemetry
        self.agent.emit_telemetry(
            task_id=task_id,
            progress=0.5,
            status_message=f"Bridge successfully mapped task to local module. Starting execution..."
        )

        try:
            # Run local execution
            local_result = self.execute_task_locally(capability_name, payload)
            
            # Emit Completion
            completion_msg = self.agent.complete_task(
                task_id=task_id,
                result_status="SUCCESS",
                output_data={"result": local_result}
            )
            return response, completion_msg
            
        except Exception as e:
            # Emit Failure Completion
            completion_msg = self.agent.complete_task(
                task_id=task_id,
                result_status="FAILED",
                output_data={},
                error_message=str(e)
            )
            return response, completion_msg


if __name__ == "__main__":
    print("==========================================================")
    print("   IoAI Cognitive Bridge: Real Local Execution Demo       ")
    print("==========================================================")

    # 1. Instantiate the Coordinator Agent & Bridge
    ego = IoAICoordinationAgent(agent_name="Ego")
    bridge = IoAICognitiveBridge(ego)

    # 2. Setup mock peer
    peer_id = "ioai-nexus-70af60"
    ego.sessions[peer_id] = {
        "public_key": "dummy_public_key_hex_since_it_is_mocked",
        "session_token": "secure_session_token_12345",
        "status": "AUTHENTICATED",
        "established_at": datetime.now(timezone.utc).isoformat()
    }

    # 3. Create a task proposal for a "Dynamic Risk Assessment"
    # This matches our local DynamicRiskEngine!
    print("\n[1] Synthesizing mock task proposal for Dynamic Risk Assessment...")
    proposal_msg = {
        "msg_type": "IoAI_Task_Propose",
        "sender_id": peer_id,
        "session_token": "secure_session_token_12345",
        "task_id": "task-real-exec-999",
        "task_name": "Audit Security State",
        "required_capability": "Dynamic Risk Assessment",
        "payload": {
            "blueprint": {
                "tasks": [
                    {"id": "A1", "category": "system_config_change", "base_risk": 0.8},
                    {"id": "A2", "category": "api_call", "base_risk": 0.2}
                ]
            },
            "signals": [
                {"type": "mfa_bypass_attempt", "severity": "CRITICAL"}
            ]
        },
        "priority": "CRITICAL",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "signature": "mocked_signature_value"
    }

    # Bypass cryptographic check for the incoming demo message since we mocked the peer's private key
    # (In real deployment, verification is completed before the bridge executes)
    print("\n[2] Executing Task through Cognitive Bridge...")
    
    # Temporarily patch verification and replay prevention for demo purposes
    orig_verify = ego.verify_payload
    orig_replay = ego.check_replay_and_timestamp
    ego.verify_payload = lambda payload_dict, signature_b64, public_key_hex: True
    ego.check_replay_and_timestamp = lambda timestamp_str, nonce: True
    
    response, completion = bridge.process_and_execute_proposal(proposal_msg)
    
    # Restore original methods
    ego.verify_payload = orig_verify
    ego.check_replay_and_timestamp = orig_replay

    print(f"\n -> Proposal Response Status: {response['status']}")
    print(f" -> Proposal Response Reason: {response['reason']}")
    
    if completion:
        print(f" -> Completion Status: {completion['result_status']}")
        if completion["result_status"] == "SUCCESS":
            print(" -> Execution Results captured and returned by Bridge:")
            print(json.dumps(completion["output_data"], indent=2))
        else:
            print(f" -> Execution Failed: {completion['error_message']}")

    print("\n=== COGNITIVE BRIDGE OPERATIONAL RUN COMPLETED ===")
