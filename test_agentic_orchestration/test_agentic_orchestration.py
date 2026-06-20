import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')

class BaseAgent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.logger = logging.getLogger(f"Agent-{self.name}")

    async def run(self, context, artifact=""):
        self.logger.info(f"Executing role: {self.role}")
        await asyncio.sleep(0.5) # Simulate API latency
        artifact += f"\n[{self.name} Output]: {self.role} completed for {context}."
        return artifact

class CodexOrchestrator:
    def __init__(self):
        self.logger = logging.getLogger("CodexOrchestrator")
        # Instantiate the Multi-Agent Swarm
        self.architect = BaseAgent("Architect", "Define specifications and TDD plan")
        self.coders = [BaseAgent(f"Coder-{i}", "Implementation generation") for i in range(2)]
        self.tester = BaseAgent("QA-Bot", "Pytest execution and verification")

    async def execute_task(self, task):
        self.logger.info(f"==== INITIATING CODEX WORKFLOW FOR: {task} ====")
        
        # 1. Spec Phase
        spec_artifact = await self.architect.run(task)
        
        # 2. Distributed Coding Phase (Simulating Warp-style concurrent delegation)
        self.logger.info("Delegating sub-tasks to concurrent coder agents...")
        coder_tasks = [coder.run(f"Sub-module {i} for {task}", spec_artifact) for i, coder in enumerate(self.coders)]
        coder_artifacts = await asyncio.gather(*coder_tasks)
        merged_code = "\n".join(coder_artifacts)
        
        # 3. QA Loop
        qa_artifact = await self.tester.run(task, merged_code)
        
        # Simulate a 30% chance QA fails and requires a re-roll
        if random.random() < 0.3:
            self.logger.warning("QA Failed! Triggering self-correction loop...")
            fix_artifact = await self.coders[0].run(f"Bugfix for {task}", qa_artifact)
            qa_artifact = await self.tester.run(task, fix_artifact)
            
        self.logger.info("==== CODEX WORKFLOW COMPLETE ====")
        return qa_artifact

if __name__ == "__main__":
    orchestrator = CodexOrchestrator()
    asyncio.run(orchestrator.execute_task("Implement MoA Memory Tracking Utility"))

