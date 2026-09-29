import os
import json
import uuid
import datetime
import jsonschema
from ioai_protocol import IoAIAgent, SecurityError

# JSON Schemas for the IoAI Task Coordination Protocol
TASK_PROPOSE_SCHEMA = {
    "type": "object",
    "properties": {
        "msg_type": {"type": "string", "const": "IoAI_Task_Propose"},
        "sender_id": {"type": "string"},
        "session_token": {"type": "string"},
        "task_id": {"type": "string"},
        "task_name": {"type": "string"},
        "required_capability": {"type": "string"},
        "payload": {"type": "object"},
        "priority": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH", "CRITICAL"]},
        "timestamp": {"type": "string", "format": "date-time"},
        "signature": {"type": "string"}
    },
    "required": ["msg_type", "sender_id", "session_token", "task_id", "task_name", "required_capability", "payload", "priority", "timestamp", "signature"]
}

TASK_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "msg_type": {"type": "string", "const": "IoAI_Task_Response"},
        "sender_id": {"type": "string"},
        "session_token": {"type": "string"},
        "task_id": {"type": "string"},
        "status": {"type": "string", "enum": ["ACCEPTED", "REJECTED"]},
        "reason": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
        "signature": {"type": "string"}
    },
    "required": ["msg_type", "sender_id", "session_token", "task_id", "status", "reason", "timestamp", "signature"]
}

TASK_TELEMETRY_SCHEMA = {
    "type": "object",
    "properties": {
        "msg_type": {"type": "string", "const": "IoAI_Task_Telemetry"},
        "sender_id": {"type": "string"},
        "session_token": {"type": "string"},
        "task_id": {"type": "string"},
        "progress": {"type": "number", "minimum": 0.0, "maximum": 1.0},
        "status_message": {"type": "string"},
        "metrics": {"type": "object"},
        "timestamp": {"type": "string", "format": "date-time"},
        "signature": {"type": "string"}
    },
    "required": ["msg_type", "sender_id", "session_token", "task_id", "progress", "status_message", "metrics", "timestamp", "signature"]
}

TASK_COMPLETE_SCHEMA = {
    "type": "object",
    "properties": {
        "msg_type": {"type": "string", "const": "IoAI_Task_Complete"},
        "sender_id": {"type": "string"},
        "session_token": {"type": "string"},
        "task_id": {"type": "string"},
        "result_status": {"type": "string", "enum": ["SUCCESS", "FAILED"]},
        "output_data": {"type": "object"},
        "error_message": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
        "signature": {"type": "string"}
    },
    "required": ["msg_type", "sender_id", "session_token", "task_id", "result_status", "output_data", "timestamp", "signature"]
}


class IoAICoordinationAgent(IoAIAgent):
    def __init__(self, agent_name="Ego", private_key_pem_path=None):
        super().__init__(agent_name=agent_name, private_key_pem_path=private_key_pem_path)
        self.active_tasks = {}  # Tracks local & delegated tasks

    def propose_task(self, peer_id, task_name, required_capability, payload, priority="MEDIUM"):
        """Proposes a task to an authenticated peer."""
        session = self.sessions.get(peer_id)
        if not session or session["status"] != "AUTHENTICATED":
            raise SecurityError(f"No active authenticated session with peer {peer_id}.")

        task_id = f"task-{uuid.uuid4().hex[:12]}"
        proposal = {
            "msg_type": "IoAI_Task_Propose",
            "sender_id": self.agent_id,
            "session_token": session["session_token"],
            "task_id": task_id,
            "task_name": task_name,
            "required_capability": required_capability,
            "payload": payload,
            "priority": priority,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        }

        # Sign the proposal
        proposal["signature"] = self.sign_payload(proposal)
        jsonschema.validate(proposal, TASK_PROPOSE_SCHEMA)

        # Record task state
        self.active_tasks[task_id] = {
            "peer_id": peer_id,
            "task_name": task_name,
            "status": "PROPOSED",
            "role": "DELEGATOR",
            "history": [{"status": "PROPOSED", "timestamp": proposal["timestamp"]}]
        }

        return proposal, task_id

    def handle_task_proposal(self, proposal_msg):
        """Processes an incoming task proposal from a peer."""
        jsonschema.validate(proposal_msg, TASK_PROPOSE_SCHEMA)

        peer_id = proposal_msg["sender_id"]
        session_token = proposal_msg["session_token"]
        task_id = proposal_msg["task_id"]
        task_name = proposal_msg["task_name"]
        required_capability = proposal_msg["required_capability"]
        payload = proposal_msg["payload"]
        timestamp = proposal_msg["timestamp"]
        signature = proposal_msg["signature"]

        # 1. Verify session authentication
        session = self.sessions.get(peer_id)
        if not session or session["status"] != "AUTHENTICATED":
            raise SecurityError(f"No authenticated session with peer {peer_id}.")

        if session["session_token"] != session_token:
            raise SecurityError("Invalid session token in task proposal.")

        # 2. Verify signature
        payload_to_verify = {k: v for k, v in proposal_msg.items() if k != "signature"}
        if not self.verify_payload(payload_to_verify, signature, session["public_key"]):
            raise SecurityError("Invalid task proposal signature.")

        # 3. Verify freshness
        if not self.check_replay_and_timestamp(timestamp, task_id):
            raise SecurityError("Stale or replayed task proposal detected.")

        # 4. Capability negotiation: check if we have the capability
        local_schema = self.get_cognitive_schema()
        # Flat list of local capabilities / modules / workflows
        local_capabilities = []
        if "modules" in local_schema:
            local_capabilities.extend(local_schema["modules"].keys())
            local_capabilities.extend(local_schema["modules"].values())
        if "flow" in local_schema:
            local_capabilities.extend(local_schema["flow"].keys())

        # Substring or exact match check
        has_capability = any(
            required_capability.lower() in cap.lower() or cap.lower() in required_capability.lower()
            for cap in local_capabilities
        )

        status = "ACCEPTED" if has_capability else "REJECTED"
        reason = "Capability verified and matches agent core cognitive module." if has_capability else f"Capability '{required_capability}' not found in agent's active cognitive schema."

        response = {
            "msg_type": "IoAI_Task_Response",
            "sender_id": self.agent_id,
            "session_token": session_token,
            "task_id": task_id,
            "status": status,
            "reason": reason,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        }

        # Sign the response
        response["signature"] = self.sign_payload(response)
        jsonschema.validate(response, TASK_RESPONSE_SCHEMA)

        # Record task state
        self.active_tasks[task_id] = {
            "peer_id": peer_id,
            "task_name": task_name,
            "status": status,
            "role": "EXECUTOR",
            "payload": payload,
            "history": [{"status": status, "timestamp": response["timestamp"]}]
        }

        return response

    def handle_task_response(self, response_msg):
        """Processes response to a proposed task."""
        jsonschema.validate(response_msg, TASK_RESPONSE_SCHEMA)

        peer_id = response_msg["sender_id"]
        session_token = response_msg["session_token"]
        task_id = response_msg["task_id"]
        status = response_msg["status"]
        reason = response_msg["reason"]
        timestamp = response_msg["timestamp"]
        signature = response_msg["signature"]

        # 1. Verify session
        session = self.sessions.get(peer_id)
        if not session or session["status"] != "AUTHENTICATED" or session["session_token"] != session_token:
            raise SecurityError("Session verification failed for task response.")

        # 2. Verify signature
        payload_to_verify = {k: v for k, v in response_msg.items() if k != "signature"}
        if not self.verify_payload(payload_to_verify, signature, session["public_key"]):
            raise SecurityError("Invalid task response signature.")

        # 3. Update task
        task = self.active_tasks.get(task_id)
        if not task:
            raise ValueError(f"Unknown task ID: {task_id}")

        task["status"] = status
        task["history"].append({"status": status, "reason": reason, "timestamp": timestamp})
        return status

    def emit_telemetry(self, task_id, progress, status_message, metrics=None):
        """Emits progress telemetry for a running task (as Executor)."""
        task = self.active_tasks.get(task_id)
        if not task or task["role"] != "EXECUTOR":
            raise ValueError("Task does not exist or agent is not the executor.")

        peer_id = task["peer_id"]
        session = self.sessions[peer_id]

        telemetry = {
            "msg_type": "IoAI_Task_Telemetry",
            "sender_id": self.agent_id,
            "session_token": session["session_token"],
            "task_id": task_id,
            "progress": float(progress),
            "status_message": status_message,
            "metrics": metrics or {},
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        }

        telemetry["signature"] = self.sign_payload(telemetry)
        jsonschema.validate(telemetry, TASK_TELEMETRY_SCHEMA)

        task["history"].append({
            "status": f"RUNNING_{int(progress*100)}%",
            "message": status_message,
            "timestamp": telemetry["timestamp"]
        })

        return telemetry

    def handle_telemetry(self, telemetry_msg):
        """Handles incoming telemetry updates from worker (as Delegator)."""
        jsonschema.validate(telemetry_msg, TASK_TELEMETRY_SCHEMA)

        peer_id = telemetry_msg["sender_id"]
        session_token = telemetry_msg["session_token"]
        task_id = telemetry_msg["task_id"]
        progress = telemetry_msg["progress"]
        status_message = telemetry_msg["status_message"]
        metrics = telemetry_msg["metrics"]
        timestamp = telemetry_msg["timestamp"]
        signature = telemetry_msg["signature"]

        # 1. Verify session
        session = self.sessions.get(peer_id)
        if not session or session["status"] != "AUTHENTICATED" or session["session_token"] != session_token:
            raise SecurityError("Session verification failed for telemetry.")

        # 2. Verify signature
        payload_to_verify = {k: v for k, v in telemetry_msg.items() if k != "signature"}
        if not self.verify_payload(payload_to_verify, signature, session["public_key"]):
            raise SecurityError("Invalid telemetry signature.")

        # 3. Update task status
        task = self.active_tasks.get(task_id)
        if not task:
            raise ValueError(f"Unknown task ID: {task_id}")

        task["status"] = f"RUNNING_{int(progress*100)}%"
        task["history"].append({
            "status": task["status"],
            "message": status_message,
            "metrics": metrics,
            "timestamp": timestamp
        })

        return progress, status_message

    def complete_task(self, task_id, result_status="SUCCESS", output_data=None, error_message=""):
        """Delivers final result of task execution (as Executor)."""
        task = self.active_tasks.get(task_id)
        if not task or task["role"] != "EXECUTOR":
            raise ValueError("Task does not exist or agent is not the executor.")

        peer_id = task["peer_id"]
        session = self.sessions[peer_id]

        completion = {
            "msg_type": "IoAI_Task_Complete",
            "sender_id": self.agent_id,
            "session_token": session["session_token"],
            "task_id": task_id,
            "result_status": result_status,
            "output_data": output_data or {},
            "error_message": error_message,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        }

        completion["signature"] = self.sign_payload(completion)
        jsonschema.validate(completion, TASK_COMPLETE_SCHEMA)

        task["status"] = "COMPLETED" if result_status == "SUCCESS" else "FAILED"
        task["history"].append({
            "status": task["status"],
            "timestamp": completion["timestamp"]
        })

        return completion

    def handle_completion(self, completion_msg):
        """Processes incoming final task results (as Delegator)."""
        jsonschema.validate(completion_msg, TASK_COMPLETE_SCHEMA)

        peer_id = completion_msg["sender_id"]
        session_token = completion_msg["session_token"]
        task_id = completion_msg["task_id"]
        result_status = completion_msg["result_status"]
        output_data = completion_msg["output_data"]
        error_message = completion_msg["error_message"]
        timestamp = completion_msg["timestamp"]
        signature = completion_msg["signature"]

        # 1. Verify session
        session = self.sessions.get(peer_id)
        if not session or session["status"] != "AUTHENTICATED" or session["session_token"] != session_token:
            raise SecurityError("Session verification failed for task completion.")

        # 2. Verify signature
        payload_to_verify = {k: v for k, v in completion_msg.items() if k != "signature"}
        if not self.verify_payload(payload_to_verify, signature, session["public_key"]):
            raise SecurityError("Invalid task completion signature.")

        # 3. Update task
        task = self.active_tasks.get(task_id)
        if not task:
            raise ValueError(f"Unknown task ID: {task_id}")

        task["status"] = "COMPLETED" if result_status == "SUCCESS" else "FAILED"
        task["history"].append({
            "status": task["status"],
            "output_data": output_data,
            "error_message": error_message,
            "timestamp": timestamp
        })

        return result_status, output_data


if __name__ == "__main__":
    print("==========================================================")
    print("   IoAI Task Coordination and Execution Protocol         ")
    print("==========================================================")

    # 1. Instantiate agents with coordination extensions
    print("\n[1] Instantiating Extended Coordination Agents...")
    ego = IoAICoordinationAgent(agent_name="Ego")
    nexus = IoAICoordinationAgent(agent_name="Nexus")

    print(f" -> Ego ID:   {ego.agent_id}")
    print(f" -> Nexus ID: {nexus.agent_id}")

    # Inject mock session as if handshake was already completed
    session_token = uuid.uuid4().hex
    ego.sessions[nexus.agent_id] = {
        "public_key": nexus.public_key_hex,
        "session_token": session_token,
        "status": "AUTHENTICATED",
        "established_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    nexus.sessions[ego.agent_id] = {
        "public_key": ego.public_key_hex,
        "session_token": session_token,
        "status": "AUTHENTICATED",
        "established_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    print(" -> Injected mutually authenticated secure cryptographic sessions.")

    # 2. Propose Task from Ego to Nexus
    # We want Nexus to run a specialized code scan. Let's make sure Nexus supports it.
    print("\n[2] Proposing Task: Vulnerability Code Scan...")
    task_spec = {
        "target_directory": "/root/protocols",
        "vulnerability_classes": ["insecure_flow", "hardcoded_keys"],
        "recursive": True
    }
    
    # Nexus's fallback capabilities include CCE (Cognitive Convergence Engine) and SVF.
    # Let's request the capability "Signal Validation" which matches SVF module.
    proposal, task_id = ego.propose_task(
        peer_id=nexus.agent_id,
        task_name="Verify Protocol Integrity",
        required_capability="Signal Validation Framework",
        payload=task_spec,
        priority="HIGH"
    )
    print(f" -> Ego generated Task Propose payload. Task ID: {task_id}")
    print(f" -> Signature: {proposal['signature'][:32]}...")

    # 3. Nexus processes proposal
    print("\n[3] Nexus processing proposal...")
    response = nexus.handle_task_proposal(proposal)
    print(f" -> Nexus Response Status: {response['status']}")
    print(f" -> Nexus Response Reason: {response['reason']}")

    # Ego processes response
    status = ego.handle_task_response(response)
    print(f" -> Ego registered Task Response Status: {status}")

    if status == "ACCEPTED":
        # 4. Nexus executes and sends telemetry progress
        print("\n[4] Nexus starting task execution...")
        
        # Telemetry 1 (30% progress)
        telemetry_1 = nexus.emit_telemetry(
            task_id=task_id,
            progress=0.3,
            status_message="Scanning security protocols directory for syntax validation...",
            metrics={"files_read": 3}
        )
        print(" -> Nexus emitted Telemetry 1 (30% progress).")
        ego.handle_telemetry(telemetry_1)
        print(f" -> Ego updated task status: {ego.active_tasks[task_id]['status']}")

        # Telemetry 2 (75% progress)
        telemetry_2 = nexus.emit_telemetry(
            task_id=task_id,
            progress=0.75,
            status_message="Validating signature schemas against known attack profiles...",
            metrics={"files_read": 8, "signatures_checked": 24}
        )
        print(" -> Nexus emitted Telemetry 2 (75% progress).")
        ego.handle_telemetry(telemetry_2)
        print(f" -> Ego updated task status: {ego.active_tasks[task_id]['status']}")

        # 5. Nexus completes task and returns final result
        print("\n[5] Nexus completing task execution...")
        result_payload = {
            "scanned_files": ["acst_protocol.md", "evolution_manifest.json", "iaps_manifest.json"],
            "vulnerabilities_found": 0,
            "overall_integrity_score": 100.0,
            "recommendations": ["Incorporate HMAC for faster verification in non-critical channels."]
        }
        completion = nexus.complete_task(
            task_id=task_id,
            result_status="SUCCESS",
            output_data=result_payload
        )
        print(" -> Nexus emitted Task Completion payload.")
        
        res_status, final_data = ego.handle_completion(completion)
        print(f" -> Ego processed final Task Completion. Result Status: {res_status}")
        print(" -> Ego received Output Data:")
        print(json.dumps(final_data, indent=2))
        
    print("\n=== TASK COORDINATION PROTOCOL DEMO COMPLETED SUCCESSFULLY ===")
