from utils import *
from datetime import datetime, timedelta
from datetime import timezone
from dateutil.parser import isoparse

def get_whitelist():
    with open("data/whitelist_file.txt", "r") as f:
        return set(line.strip() for line in f)

def get_unfollowed_users(filepath):
    if not os.path.exists(filepath):
        return set()
    with open(filepath, 'r') as f:
        return set(line.strip() for line in f)
    
def get_last_workout(username):
    res = requests.get(f'https://api.hevyapp.com/user_workouts_paged?username={username}&limit=1&offset=0', headers=HEADERS)
    if res.status_code != 200:
        return None
    data = res.json()
    workouts = data.get("workouts", [])
    if workouts:
        return workouts[0]['created_at']
    return None

def unfollow_user(username):
    res = requests.post("https://api.hevyapp.com/unfollow", headers=HEADERS, json={'username': username})
    if res.status_code == 429: kill_switch("Rate limited")
    res.raise_for_status()
    with open(UNFOLLOWED_USERS_PATH, "a") as f:
        f.write(username + "\n")
    delay()
    return True

def get_temp_follow():
    temp_follow = {}
    with open(TEMP_FOLLOWING_PATH, 'a+') as f:
        f.seek(0)  # Move file pointer to start so we can read
        for line in f:
            if "," in line:
                user, timestamp = line.strip().split(",", 1)
                temp_follow[user] = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f%z")
    return temp_follow

def unfollower_users(my_following, my_followers):
    unfollowed = []
    count = 0
    whitelist = get_whitelist()
    unfollowed_list = get_unfollowed_users(UNFOLLOWED_USERS_PATH)
    now = datetime.now(timezone.utc)
    inactive_time = CONFIG["unfollow"]["inactive_days"]
    unfollow_time = CONFIG["unfollow"]["unfollow_timer_days"]
    temp_follow = get_temp_follow()

    for user in my_following:
        if user in whitelist:
            print(f"Skipped @{user} - Whitelisted")
            continue

        last_post_iso = get_last_workout(user)
        inactive = True if not last_post_iso else (now - isoparse(last_post_iso)).days > inactive_time
        not_following_back = user not in my_followers

        if inactive:
            reason = f"Inactive for {inactive_time}+ days"
            print(f"Unfollowed @{user} - {reason}")
            if unfollow_user(user):
                count += 1
                unfollowed.append((user, reason))
            else:
                print(f"Failed to unfollow @{user}")

        elif user in temp_follow:
            followed_at = temp_follow[user]
            days_since_follow = (now - followed_at).days
            if not_following_back and days_since_follow >= unfollow_time:
                reason = f"Hasn't followed back after {unfollow_time}+ days"
                if unfollow_user(user):
                    count += 1
                    unfollowed.append((user, reason))
                    print(f"Unfollowed @{user} - {reason}")
                else:
                    print(f"[FAILED] Unfollowed @{user} - {reason}")
            else:
                print(f"Skipped @{user} - Has {unfollow_time - days_since_follow} days left to follow")

        elif not_following_back:
            reason = "Not in temp list & never followed back"
            if unfollow_user(user):
                count += 1
                unfollowed.append((user, reason))
                print(f"Unfollowed @{user} - {reason}")
            else:
                print(f"[FAILED] Unfollowed @{user} - {reason}")
        
        else:
            print(f"Skipped @{user} - F4F")

        if count >= CONFIG["unfollow"]["unfollow_cap"]:
            print("Unfollow cap reached")
            break

    return unfollowed

        
            






