import requests
from bs4 import BeautifulSoup
import json

def get_trending():
    url = "https://github.com/trending"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        repos = []
        articles = soup.find_all('article', class_='Box-row')
        
        for article in articles[:5]:
            title_element = article.find('h2', class_='h3')
            if title_element:
                # Extract repo path (e.g., /owner/repo)
                link = title_element.find('a')['href']
                repo_path = link.strip('/')
                
                desc_element = article.find('p', class_='col-9')
                description = desc_element.text.strip() if desc_element else "No description"
                
                lang_element = article.find('span', class_='text-bold')
                language = lang_element.text.strip().replace(' ', '') if lang_element else "Unknown"
                
                repos.append({
                    "repo_id": repo_path,
                    "name": repo_path,
                    "description": description,
                    "language": language,
                    "url": f"https://github.com/{repo_path}"
                })
        return repos
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print(json.dumps(get_trending()))
