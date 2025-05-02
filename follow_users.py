import os
import requests
import time
from datetime import datetime, timezone
from dotenv import load_dotenv
from utils import delay

# --- Load environment ---
load_dotenv()
API_KEY = os.getenv('API_KEY')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')

HEADERS = {
    'x-api-key': API_KEY,
    'auth-token': AUTH_TOKEN,
    'Hevy-Platform': 'web',
    'Accept': 'application/json, text/plain, */*'
}

FOLLOW_URL = 'https://api.hevyapp.com/follow'
ALREADY_FOLLOWED_FILE = 'already_followed.txt'

def load_already_followed():
    if not os.path.exists(ALREADY_FOLLOWED_FILE):
        return set()
    with open(ALREADY_FOLLOWED_FILE, 'r') as f:
        return set(line.strip().split(',')[0] for line in f.readlines())

def log_follow(username):
    timestamp = datetime.now(timezone.utc).isoformat()
    with open(ALREADY_FOLLOWED_FILE, 'a') as f:
        f.write(f"{username},{timestamp}\n")

def follow_user(username):
    payload = {'username': username}
    try:
        res = requests.post(FOLLOW_URL, headers=HEADERS, json=payload)
        if res.status_code == 429:
            print("⏳ Rate limited. Sleeping for 5 minutes...")
            time.sleep(300)
            return False
        res.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"❌ Error following @{username}: {e}")
        return False

def follow_users(usernames):
    already_followed = load_already_followed()
    for user in usernames:
        if user in already_followed:
            print(f"⏩ Skipping @{user}, already followed.")
            continue
        print(f"➕ Following @{user}...")
        success = follow_user(user)
        if success:
            print(f"✅ Followed @{user}")
            log_follow(user)
        else:
            print(f"❌ Failed to follow @{user}")
        delay()

# Test
if __name__ == "__main__":
    sample_users = ['testuser1', 'testuser2']
    follow_users(sample_users)
