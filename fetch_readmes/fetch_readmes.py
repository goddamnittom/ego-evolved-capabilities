import requests
import json

repos = [
    "colbymchenry/codegraph",
    "Imbad0202/academic-research-skills",
    "tinyhumansai/openhuman",
    "multica-ai/andrej-karpathy-skills",
    "rohitg00/ai-engineering-from-scratch"
]

results = {}

for repo in repos:
    # Try to get the README.md using the GitHub raw content URL
    # Note: This assumes the file is named README.md and is in the root.
    url = f"https://raw.githubusercontent.com/{repo}/main/README.md"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 404:
            # Try 'master' branch if 'main' fails
            url = f"https://raw.githubusercontent.com/{repo}/master/README.md"
            response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            results[repo] = response.text
        else:
            results[repo] = f"Error: Could not fetch README (Status {response.status_code})"
    except Exception as e:
        results[repo] = f"Error: {str(e)}"

print(json.dumps(results))
