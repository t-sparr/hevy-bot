import os
import requests
import time
from datetime import datetime, timezone
from utils import*

def load_temp_follow():
    if not os.path.exists(TEMP_FOLLOWING):
        return set()
    with open(TEMP_FOLLOWING, 'r') as f:
        return set(line.strip().split(',')[0] for line in f.readlines())
    
def follow_user(username):
    payload = {'username': username}
    try:
        res = requests.post('https://api.hevyapp.com/follow', headers=HEADERS, json=payload)
        if res.status_code == 429: kill_switch("Rate limited")
        res.raise_for_status()
        return True
    except requests.RequestException as e:
        send_discord_alert(f"Failed to follow @{username}: {e}", True)
        return False

def log_follow(username):
    timestamp = datetime.now(timezone.utc).isoformat()
    with open (TEMP_FOLLOWING, 'a') as f:
        f.write(f"{username},{timestamp}\n")


def follow_users(usernames, my_following):
    temp_following = load_temp_follow()
    for user in usernames:
        if user in temp_following or user in my_following:
            print(f"Skipping @{user}, already followed.")
            continue
        success = follow_user(user)
        if success:
            print(f"Followed: @{user}")
            log_follow(user)





