import os
import time
import random
import requests
import json
from dotenv import load_dotenv
from pathlib import Path

# --- Load .env from script directory ---
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# --- Settings ---
TARGET_COUNT = 3
API_KEY = os.getenv('API_KEY')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
HEVY_USERNAME = os.getenv('HEVY_USERNAME')  # ✅ renamed to avoid conflict
UNFOLLOWED_FILE = os.getenv("UNFOLLOWED_FILE", "unfollowed_users.txt")

HEADERS = {
    'x-api-key': API_KEY,
    'auth-token': AUTH_TOKEN,
    'Hevy-Platform': 'web',
    'Accept': 'application/json, text/plain, */*'
}

# --- Utility Functions ---
def delay(min_sec=1.5, max_sec=3.0):
    time.sleep(random.uniform(min_sec, max_sec))

def load_unfollowed_users(filepath):
    if not os.path.exists(filepath):
        return set()
    with open(filepath, 'r') as f:
        return set(line.strip() for line in f)

def get_following_usernames(username, headers):
    url = f"https://api.hevyapp.com/following/{username}"
    res = requests.get(url, headers=headers)
    print("📡 Status code:", res.status_code)
    res.raise_for_status()

    users = res.json()
    print(f"🔍 Raw user count: {len(users)}")

    usernames = set()
    for user in users:
        uname = user.get('username', '').lower()
        print(f"👤 Found user: {uname}")
        if uname:
            usernames.add(uname)

    print(f"✅ Collected {len(usernames)} usernames from following")
    return usernames

# Stubbed — replace with real logic
def get_users_to_follow(unfollowed, following, target_count):
    sample_users = ['johnnygym', 'fitgal21', 'beastmode88']
    return [u for u in sample_users if u not in unfollowed and u not in following][:target_count]

# Stubbed — replace with real follow API logic
def follow_users(usernames):
    for user in usernames:
        print(f"🤝 (Pretend) following {user}")
        delay()

# --- Main Automation ---
def main():
    print("🚀 Loading state...")

    # Debug environment
    print(f"🔑 HEVY_USERNAME from .env is: {HEVY_USERNAME}")
    print(f"API_KEY = {API_KEY}")
    print(f"AUTH_TOKEN = {AUTH_TOKEN[:10]}...")  # Hide rest for safety
    print(f"UNFOLLOWED_FILE = {UNFOLLOWED_FILE}")

    unfollowed = load_unfollowed_users(UNFOLLOWED_FILE)
    following = get_following_usernames(HEVY_USERNAME, HEADERS)

    print("🔍 Collecting users to follow...")
    to_follow = get_users_to_follow(unfollowed, following, TARGET_COUNT)

    print(f"\n✅ Found {len(to_follow)} new users to follow:")
    for i, user in enumerate(to_follow, 1):
        print(f"{i:2}. @{user}")
        delay()

    if to_follow:
        top_user = to_follow[0]
        print(f"\n🎯 Testing follow on top user: @{top_user}")
        follow_users([top_user])
    else:
        print("🚫 No users to follow.")

    print("\n🎯 Done.")
    print(f"Loaded {len(following)} already-followed users")

if __name__ == "__main__":
    main()
 