import os
import time
import random
from datetime import datetime
import requests
from dotenv import load_dotenv
from collect_people_to_follow import get_users_to_follow
from follow_users import follow_users
from unfollow_user import run_unfollow_logic
from dateutil.parser import isoparse
# --- Load environment variables ---
load_dotenv()

# --- Settings ---
TARGET_COUNT = 10
UNFOLLOWED_FILE = os.getenv("UNFOLLOWED_FILE", "unfollowed_users.txt")
API_KEY = os.getenv('API_KEY')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
HEVY_USERNAME = os.getenv('HEVY_USERNAME')

HEADERS = {
    'x-api-key': API_KEY,
    'auth-token': AUTH_TOKEN,
    'Hevy-Platform': 'web',
    'Accept': 'application/json, text/plain, */*'
}


# --- Utility Functions ---
def delay(min_sec=1.5, max_sec=3.0):
    """Randomized delay between requests to avoid detection."""
    time.sleep(random.uniform(min_sec, max_sec))


def load_unfollowed_users(filepath):
    if not os.path.exists(filepath):
        return set()
    with open(filepath, 'r') as f:
        return set(line.strip() for line in f)


def get_following_usernames(username, headers):
    url = f"https://api.hevyapp.com/following/{username}"
    res = requests.get(url, headers=headers)
    if res.status_code == 429:
        print("⚠️ Rate limited. Sleeping for 5 minutes...")
        time.sleep(300)
        return set()
    res.raise_for_status()
    return set(user['username'] for user in res.json())


def get_all_follower_usernames(username, headers):
    all_followers = []
    offset = 0
    while True:
        res = requests.get(f'https://api.hevyapp.com/followers_paged/{username}/{offset}', headers=headers)
        if res.status_code == 429:
            print("⚠️ Rate limited. Sleeping for 5 minutes...")
            time.sleep(300)
            continue
        res.raise_for_status()
        page = res.json()
        if not page:
            break
        all_followers.extend(page)
        offset += 50
        delay(0.5, 1.0)  # respectful pagination delay

    return set(user['username'] for user in all_followers)


# --- Main Automation ---
# def main():
#     print("🚀 Loading state...")
#     unfollowed = load_unfollowed_users(UNFOLLOWED_FILE)
#     following = get_following_usernames(HEVY_USERNAME, HEADERS)

#     print("🔍 Collecting users to follow...")
#     to_follow = get_users_to_follow(unfollowed, following, TARGET_COUNT)

#     print(f"\n✅ Found {len(to_follow)} new users to follow:")
#     for i, user in enumerate(to_follow, 1):
#         print(f"{i:2}. @{user}")

#     if to_follow:
#         print("\n🔁 Starting follow sequence...")
#         follow_users(to_follow)
        

#     print("\n🎯 Done.")

def main():
    print("🚀 Loading state...")
    unfollowed = load_unfollowed_users(UNFOLLOWED_FILE)
    following = get_following_usernames(HEVY_USERNAME, HEADERS)
    with open("whitelist_file.txt", "r") as f:
        whitelist = set(line.strip() for line in f)
    
    print("🔍 Collecting users to follow...")
    to_follow = get_users_to_follow(unfollowed, following, TARGET_COUNT)

    # print(f"\n✅ Found {len(to_follow)} new users to follow:")
    # for i, user in enumerate(to_follow, 1):
    #     print(f"{i:2}. @{user}")

    # if to_follow:
    #     print("\n🔁 Starting follow sequence...")
    #     follow_users(to_follow)
        






    already_followed = {}
    if os.path.exists("already_followed.txt"):
        with open("already_followed.txt", "r") as f:
            for line in f:
                if "," in line:
                    user, timestamp = line.strip().split(",", 1)
                    already_followed[user] = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f%z")

    run_unfollow_logic(
        followers=get_all_follower_usernames(HEVY_USERNAME, HEADERS),
        following=[{'username': u} for u in following],  # wrap to match dict format
        already_followed=already_followed,
        whitelist=whitelist,
        unfollowed=unfollowed,
        headers=HEADERS,
        unfollow_cap=10,
        unfollowed_file=UNFOLLOWED_FILE
    )



if __name__ == "__main__":
    main()
