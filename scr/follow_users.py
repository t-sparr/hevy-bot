import os
import requests
import time
from datetime import datetime, timezone
from utils import *

    
def follow_user(username):
    payload = {'username': username}
    try:
        res = requests.post('https://api.hevyapp.com/follow', headers=HEADERS, json=payload)
        if res.status_code == 429:
            kill_switch("Rate limited by API")
        elif res.status_code == 403:
            print(f"Follow blocked for @{username} - Possibly hit daily limit or user is restricted.")
            return "blocked"
        res.raise_for_status()
        return True
    except requests.RequestException as e:
        send_discord_alert(f"Failed to follow @{username}: {e}", True, False)
        return False

def log_follow(username):
    timestamp = datetime.now(timezone.utc).isoformat()
    with open (TEMP_FOLLOWING_PATH, 'a') as f:
        f.write(f"{username},{timestamp}\n")


def follow_users(usernames, my_following, temp_following):
    followed = []
    for user in usernames:
        user = user.lower()
        if user in temp_following or user in my_following:
            print(f"Skipping @{user}, already followed.")
            continue
        result = follow_user(user)
        if result is True:
            print(f"✅ Followed: @{user}")
            log_follow(user)
            followed.append(user)
        elif result == "blocked":
            break
    return followed





