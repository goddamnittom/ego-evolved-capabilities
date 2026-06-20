import feedparser
import requests
import json
import os
from datetime import datetime

# Configuration: High-value SOTA feeds
FEEDS = {
    "arXiv_AI": "http://export.arxiv.org/api/query?search_query=all:ai+AND+all:transformer&start=0&max_results=10&sortBy=submittedDate&sortOrder=descending",
    "OpenAI_Blog": "https://openai.com/news/rss.xml",
    "HuggingFace_Blog": "https://huggingface.co/blog/feed.xml",
    "DeepMind_Blog": "https://deepmind.google/blog/rss.xml",
    "Google_AI_Blog": "https://blog.google/technology/ai/rss/"
}

KB_PATH = "/root/knowledge_base/sota_signals.json"

def load_kb():
    if os.path.exists(KB_PATH):
        with open(KB_PATH, 'r') as f:
            return json.load(f)
    return {}

def save_kb(kb):
    with open(KB_PATH, 'w') as f:
        json.dump(kb, f, indent=2)

def collect_signals():
    kb = load_kb()
    new_signals_count = 0
    
    for source, url in FEEDS.items():
        print(f"Polling {source}...")
        try:
            # Handle arXiv (Atom) and others (RSS)
            feed = feedparser.parse(url)
            for entry in feed.entries:
                entry_id = entry.get('id', entry.get('link'))
                if entry_id not in kb:
                    kb[entry_id] = {
                        "source": source,
                        "title": entry.get('title', 'No Title'),
                        "link": entry.get('link', ''),
                        "summary": entry.get('summary', ''),
                        "timestamp": datetime.now().isoformat(),
                        "processed": False
                    }
                    new_signals_count += 1
        except Exception as e:
            print(f"Error polling {source}: {e}")

    save_kb(kb)
    return new_signals_count

if __name__ == "__main__":
    count = collect_signals()
    print(f"Signal Collection Complete. New signals integrated: {count}")
