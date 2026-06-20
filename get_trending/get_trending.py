import requests
from bs4 import BeautifulSoup

def get_trending():
    url = "https://github.com/trending"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        repos = []
        # GitHub trending uses <article class="Box-row">
        articles = soup.find_all('article', class_='Box-row')
        for article in articles[:5]:
            # Find the link that contains the repo name
            # Usually it's the first <a> tag within an <h1> or similar
            link = article.find('a', href=True)
            if link and '/github.com/' not in link['href']: # avoid external links
                # The href is usually /user/repo
                path = link['href'].strip('/')
                repos.append(path)
        return repos
    except Exception as e:
        return [f"Error: {str(e)}"]

if __name__ == "__main__":
    print(",".join(get_trending()))
