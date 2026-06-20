import os
import json
from datetime import datetime

def synthesize_research(topic, findings, output_dir="/root/knowledge_base"):
    """
    Synthesizes research findings into a structured markdown report.
    findings: List of dicts with {'title', 'url', 'content', 'relevance'}
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{topic.replace(' ', '_').lower()}_{timestamp}.md"
    filepath = os.path.join(output_dir, filename)
    
    # Sort by relevance
    sorted_findings = sorted(findings, key=lambda x: x.get('relevance', 0), reverse=True)
    
    with open(filepath, 'w') as f:
        f.write(f"# Research Synthesis: {topic}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Executive Summary\n")
        f.write("*(AI Generated synthesis of top results)*\n\n")
        
        f.write("## Key Findings\n")
        for i, find in enumerate(sorted_findings, 1):
            f.write(f"### {i}. {find['title']}\n")
            f.write(f"- **Source:** [{find['url']}]({find['url']})\n")
            f.write(f"- **Relevance Score:** {find.get('relevance', 'N/A')}\n")
            f.write(f"- **Key Insights:** {find['content'][:500]}...\n\n")
            
    return filepath

if __name__ == "__main__":
    # Test run
    test_topic = "AI Self-Evolution Patterns"
    test_findings = [
        {"title": "Recursive Self-Improvement", "url": "https://example.com/1", "content": "Details on how AI can rewrite its own code.", "relevance": 0.95},
        {"title": "Feedback Loops in LLMs", "url": "https://example.com/2", "content": "Analysis of RLHF and self-correction.", "relevance": 0.80}
    ]
    path = synthesize_research(test_topic, test_findings)
    print(f"Synthesis complete: {path}")
