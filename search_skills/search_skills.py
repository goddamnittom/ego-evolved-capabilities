import os
import sys

# Add the project root to sys.path
sys.path.append('/root/aiskillstore')

try:
    from mcp_server.skill_store_mcp import SkillStoreMCP
    
    # Initialize the MCP class (mocking the server environment)
    store = SkillStoreMCP()
    # Assuming there's a search_skills method in the class
    results = store.search_skills("productivity automation devops infrastructure data")
    print(results)
except Exception as e:
    print(f"Error: {e}")
