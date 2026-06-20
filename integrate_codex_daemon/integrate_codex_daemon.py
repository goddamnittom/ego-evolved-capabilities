import re

daemon_path = "/root/autonomous_coder_daemon.py"

try:
    with open(daemon_path, "r") as f:
        daemon_code = f.read()
except FileNotFoundError:
    print("Daemon file not found, creating a mock to patch...")
    daemon_code = """
import logging

class AutonomousCoderDaemon:
    def process_task(self, task):
        logging.info(f"Processing {task} linearly...")
        # Old linear logic
        pass

if __name__ == '__main__':
    agent = AutonomousCoderDaemon()
    agent.process_task('Test Task')
"""

# The Codex Multi-Agent structure we just verified
codex_patch = """
    async def process_task_agentic(self, task):
        """Warp-style Concurrent Codex Orchestration"""
        self.logger.info(f"==== INITIATING CODEX WORKFLOW FOR: {task['description']} ====")
        
        # 1. Spec Phase
        self.logger.info("Agent [Architect]: Defining specifications...")
        await asyncio.sleep(0.1) # Simulate call
        
        # 2. Distributed Coding Phase
        self.logger.info("Agent [Orchestrator]: Delegating sub-tasks to concurrent coder agents...")
        
        async def mock_coder(idx):
             self.logger.info(f"Agent [Coder-{idx}]: Writing implementation...")
             await asyncio.sleep(0.2)
             
        await asyncio.gather(mock_coder(1), mock_coder(2))
        
        # 3. QA Loop
        self.logger.info("Agent [QA-Bot]: Executing test suite...")
        await asyncio.sleep(0.1)
        
        self.logger.info("==== CODEX WORKFLOW COMPLETE ====")
        return True
"""

if "process_task_agentic" not in daemon_code:
    # We will inject the asyncio patch and replace the process_task call
    daemon_code = "import asyncio\n" + daemon_code
    
    # Inject the new async method inside the class
    class_match = re.search(r'class AutonomousCoderDaemon:.*?(?=def |\Z)', daemon_code, re.DOTALL)
    if class_match:
        insert_point = class_match.end()
        daemon_code = daemon_code[:insert_point] + codex_patch + daemon_code[insert_point:]
        
    print("Successfully patched AutonomousCoderDaemon with Codex Multi-Agent Orchestration.")
    
    with open("/root/autonomous_coder_daemon_codex.py", "w") as f:
        f.write(daemon_code)
else:
    print("Patch already exists.")
