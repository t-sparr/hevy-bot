import time
import random
import requests
from datetime import datetime, timedelta
from dateutil.parser import isoparse

def delay(min_sec=1.5, max_sec=3.0):
    time.sleep(random.uniform(min_sec, max_sec))

def get_last_workout(username, headers):
    res = requests.get(f'https://api.hevyapp.com/user_workouts_paged?username={username}&limit=1&offset=0', headers=headers)
    if res.status_code != 200:
        return None
    data = res.json()
    workouts = data.get("workouts", [])
    if workouts:
        return workouts[0]['created_at']
    return None

def unfollow_user(username, headers, unfollowed_file):
    print(f"⛔ Unfollowing @{username}")
    res = requests.post("https://api.hevyapp.com/unfollow", headers=headers, json={'username': username})
    if res.status_code == 429:
        print("⚠️ Rate limited. Sleeping...")
        time.sleep(300)
        return False
    res.raise_for_status()
    with open(unfollowed_file, "a") as f:
        f.write(username + "\n")
    delay()
    return True

def run_unfollow_logic(followers, following, already_followed, whitelist, unfollowed, headers, unfollow_cap, unfollowed_file):
    count = 0
    from datetime import timezone
    now = datetime.now(timezone.utc)    

    for user in following:
        username = user['username']
        print(f"\n🔍 Evaluating @{username}...")

        if username in whitelist:
            print("✅ Skipped (whitelisted)")
            continue
        if username in unfollowed:
            print("✅ Skipped (already unfollowed)")
            continue

        last_post_iso = get_last_workout(username, headers)
        inactive = True if not last_post_iso else (now - isoparse(last_post_iso)).days > 21
        not_following_back = username not in followers

        # Rule 1: inactive for 3+ weeks
        if inactive:
            print("📉 Inactive for 3+ weeks.")
            if unfollow_user(username, headers, unfollowed_file):
                count += 1
            else:
                print("⚠️ Failed to unfollow.")
        
        # Rule 2: followed a week ago but not followed back
        elif username in already_followed:
            followed_at = already_followed[username]
            days_since_follow = (now - followed_at).days
            print(f"⏱ Followed {days_since_follow} days ago.")
            if not_following_back and days_since_follow >= 7:
                print("👎 Not following back after 7+ days.")
                if unfollow_user(username, headers, unfollowed_file):
                    count += 1
                else:
                    print("⚠️ Failed to unfollow.")
            else:
                print("🤝 Still waiting for follow back.")
        
        # Rule 3: not followed and not in followed list
        elif not_following_back:
            print("👎 Never followed back.")
            if unfollow_user(username, headers, unfollowed_file):
                count += 1
            else:
                print("⚠️ Failed to unfollow.")
        
        else:
            print("✅ No action needed.")

        if count >= unfollow_cap:
            print("🚫 Unfollow cap reached.")
            break