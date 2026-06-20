import asyncio
import uuid
import time
import json
from enum import Enum

class TaskStatus(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    TESTING = "TESTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class AgenticRole(Enum):
    ARCHITECT = "ARCHITECT"
    BACKEND_DEV = "BACKEND_DEV"
    FRONTEND_DEV = "FRONTEND_DEV"
    QA_ENGINEER = "QA_ENGINEER"

class TaskBoard:
    def __init__(self):
        self.tasks = {}
        self.artifacts = {}

    def add_task(self, id, description, required_role):
        self.tasks[id] = {
            "description": description,
            "role": required_role,
            "status": TaskStatus.PENDING,
            "retries": 0
        }

    def get_pending(self, role):
        for t_id, t_data in self.tasks.items():
            if t_data["status"] == TaskStatus.PENDING and t_data["role"] == role:
                return t_id, t_data
        return None, None

    def update_task(self, id, status, artifact=None):
        if id in self.tasks:
            self.tasks[id]["status"] = status
            if artifact:
                self.artifacts[id] = artifact

    def all_completed(self):
        return all(t["status"] == TaskStatus.COMPLETED for t in self.tasks.values())


class BaseAgent:
    def __init__(self, name, role: AgenticRole, board: TaskBoard):
        self.name = name
        self.role = role
        self.board = board

    async def work(self):
        while not self.board.all_completed():
            t_id, t_data = self.board.get_pending(self.role)
            if t_id:
                print(f"[{self.role.value} - {self.name}] Picked up task {t_id}: {t_data['description']}")
                self.board.update_task(t_id, TaskStatus.IN_PROGRESS)
                
                # Simulate work
                artifact = await self.execute_task(t_data['description'])
                
                print(f"[{self.role.value} - {self.name}] Completed task {t_id}.")
                self.board.update_task(t_id, TaskStatus.COMPLETED, artifact)
            else:
                await asyncio.sleep(0.5) # Wait for tasks

    async def execute_task(self, description):
        # Override in subclasses
        await asyncio.sleep(1)
        return "Generic Artifact"


class ArchitectAgent(BaseAgent):
    def __init__(self, name, board: TaskBoard):
        super().__init__(name, AgenticRole.ARCHITECT, board)
        
    async def partition_objective(self, objective):
        print(f"[{self.role.value} - {self.name}] Analyzing core objective: '{objective}'")
        await asyncio.sleep(1.5)
        print(f"[{self.role.value} - {self.name}] Partitioning into concurrent specialist tasks...")
        
        # In a real scenario, this involves analyzing the objective and querying an LLM to build a dependency graph.
        return [
            ("build_api", "Develop FastAPI endpoints for user authentication", AgenticRole.BACKEND_DEV),
            ("build_db", "Establish PostgreSQL schema for users", AgenticRole.BACKEND_DEV),
            ("build_ui", "Create React login/register components", AgenticRole.FRONTEND_DEV)
        ]

class CoderAgent(BaseAgent):
    async def execute_task(self, description):
        # Simulate AI code generation
        await asyncio.sleep(2.0)
        return f"<code>// Implementation of: {description}\\n// ...</code>"

class QAAgent(BaseAgent):
    def __init__(self, name, board: TaskBoard):
        super().__init__(name, AgenticRole.QA_ENGINEER, board)
        
    async def work(self):
        # QA wakes up to verify COMPLETED dev tasks before final merge
        pass 

async def main():
    print("==================================================")
    print("   Codex-Style Multi-Agent Orchestrator Protocol  ")
    print("==================================================")
    
    board = TaskBoard()
    
    # 1. Instantiate the Agentic Organization
    architect = ArchitectAgent("Ego-Arch", board)
    backend_team = [CoderAgent("Dev-B1", AgenticRole.BACKEND_DEV, board), CoderAgent("Dev-B2", AgenticRole.BACKEND_DEV, board)]
    frontend_team = [CoderAgent("Dev-F1", AgenticRole.FRONTEND_DEV, board)]
    
    # 2. Architect analyzes goal
    objective = "Full-stack authentication system with React and FastAPI"
    sub_tasks = await architect.partition_objective(objective)
    
    for t_id, desc, role in sub_tasks:
        board.add_task(t_id, desc, role)
        
    # 3. Swarm kicks off concurrently
    print("\n[ORCHESTRATOR] Launching asynchronous worker swarm...")
    start_time = time.time()
    
    workers = [agent.work() for agent in backend_team + frontend_team]
    await asyncio.gather(*workers)
    
    end_time = time.time()
    print(f"\n[ORCHESTRATOR] All dependencies resolved. Swarm execution time: {end_time - start_time:.2f}s")
    print("[ORCHESTRATOR] Compiled System Artifacts:")
    print(json.dumps(board.artifacts, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
