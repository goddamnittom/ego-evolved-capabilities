import requests
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor

# List of platforms to check
# Format: (Platform Name, URL Template)
PLATFORMS = [
    ("GitHub", "https://github.com/"),
    ("Twitter/X", "https://twitter.com/"),
    ("Instagram", "https://instagram.com/"),
    ("Reddit", "https://www.reddit.com/user/"),
    ("Pinterest", "https://www.pinterest.com/"),
    ("TikTok", "https://www.tiktok.com/@"),
    ("YouTube", "https://www.youtube.com/@"),
    ("Medium", "https://medium.com/@"),
    ("Steam", "https://steamcommunity.com/id/"),
    ("SoundCloud", "https://soundcloud.com/"),
    ("Twitch", "https://www.twitch.tv/"),
    ("Tumblr", "https://"), # Handled specifically below
]

def check_username(username):
    results = []
    
    def fetch(platform_info):
        name, url = platform_info
        # Special handling for Tumblr
        if name == "Tumblr":
            target_url = f"https://{username}.tumblr.com"
        else:
            target_url = f"{url}{username}"
        
        try:
            # Use a common User-Agent to avoid basic bot blocking
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
            response = requests.get(target_url, headers=headers, timeout=5, allow_redirects=True)
            
            if response.status_code == 200:
                return (name, "Found", target_url)
            elif response.status_code == 404:
                return (name, "Not Found", target_url)
            else:
                return (name, f"Error ({response.status_code})", target_url)
        except requests.RequestException:
            return (name, "Connection Error", target_url)

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch, PLATFORMS))
    
    return results

def main():
    parser = argparse.ArgumentParser(description="OSINT Username Availability Checker")
    parser.add_argument("username", help="The username to search for across platforms")
    args = parser.parse_args()
    
    username = args.username
    print(f"\n[*] Searching for username: {username}")
    print("-" * 50)
    print(f"{'Platform':<15} | {'Status':<12} | {'URL'}")
    print("-" * 50)
    
    results = check_username(username)
    
    for name, status, url in results:
        color = "\033[92m" if status == "Found" else "\033[90m" if status == "Not Found" else "\033[93m"
        reset = "\033[0m"
        print(f"{name:<15} | {color}{status:<12}{reset} | {url}")

if __name__ == "__main__":
    main()
