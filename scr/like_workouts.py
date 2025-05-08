from utils import *
import requests

DISCOVER_FEED_URL = 'https://api.hevyapp.com/discover_feed_workouts_paged'


def fetch_discover_page(index=None):
    url = f"{DISCOVER_FEED_URL}/{index}" if index else DISCOVER_FEED_URL
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return res.json()


def fetch_likes(workout_id):
    url = f"https://api.hevyapp.com/workout_likes/{workout_id}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return [u['username'] for u in res.json()]
    return []


def get_last_workout_id(username):
    res = requests.get(f'https://api.hevyapp.com/user_workouts_paged?username={username}&limit=1', headers=HEADERS)
    if res.status_code != 200:
        return None
    data = res.json()
    workouts = data.get("workouts", [])
    return workouts[0]['id'] if workouts else None


from utils import *
from datetime import datetime, timedelta, timezone
import requests

DISCOVER_FEED_URL = 'https://api.hevyapp.com/discover_feed_workouts_paged'
LIKED_LOG_PATH = BASE_DIR / "data" / "liked_workouts.txt"
LIKE_LOOKBACK_HOURS = CONFIG["like"]["lookback_hours"]


def clean_old_likes():
    if not LIKED_LOG_PATH.exists():
        return set()

    valid_likes = {}
    cutoff = datetime.now(timezone.utc) - timedelta(hours=LIKE_LOOKBACK_HOURS)

    with open(LIKED_LOG_PATH, 'r') as f:
        for line in f:
            if "," in line:
                wid, timestamp = line.strip().split(",", 1)
                liked_time = datetime.fromisoformat(timestamp)
                if liked_time > cutoff:
                    valid_likes[wid] = liked_time

    # Rewrite file with only valid likes
    with open(LIKED_LOG_PATH, 'w') as f:
        for wid, ts in valid_likes.items():
            f.write(f"{wid},{ts.isoformat()}\n")

    return set(valid_likes.keys())


def log_like(workout_id):
    now = datetime.now(timezone.utc).isoformat()
    with open(LIKED_LOG_PATH, 'a') as f:
        f.write(f"{workout_id},{now}\n")


def fetch_discover_page(index=None):
    url = f"{DISCOVER_FEED_URL}/{index}" if index else DISCOVER_FEED_URL
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return res.json()


def fetch_likes(workout_id):
    url = f"https://api.hevyapp.com/workout_likes/{workout_id}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return [u['username'] for u in res.json()]
    return []


def get_last_workout_id(username):
    res = requests.get(f'https://api.hevyapp.com/user_workouts_paged?username={username}&limit=1', headers=HEADERS)
    if res.status_code != 200:
        return None
    data = res.json()
    workouts = data.get("workouts", [])
    return workouts[0]['id'] if workouts else None


def like_workout(workout_id):
    url = f"https://api.hevyapp.com/workout/like/{workout_id}"
    res = requests.post(url, headers=HEADERS)
    if res.status_code == 429:
        kill_switch("Rate limited")
    res.raise_for_status()
    return res.status_code == 200


def like_discovery_users():
    index = None
    liked_users = set()
    recently_liked_ids = clean_old_likes()

    while len(liked_users) < CONFIG["like"]["like_cap"]:
        data = fetch_discover_page(index)
        workouts = data.get("workouts", [])
        if not workouts or len(workouts) < 2:
            break

        workout = workouts[0]
        workout_id = workout["id"]

        for source in ["comments", "likes"]:
            users = workout.get("comments", []) if source == "comments" else fetch_likes(workout_id)
            for user_entry in users:
                username = user_entry["username"] if isinstance(user_entry, dict) else user_entry
                username = username.lower()
                if username in liked_users:
                    continue

                last_id = get_last_workout_id(username)
                if not last_id or last_id in recently_liked_ids:
                    continue

                if like_workout(last_id):
                    print(f"❤️ Liked @{username}'s workout ({last_id})")
                    log_like(last_id)
                    liked_users.add(username)
                    delay()
                if len(liked_users) >= CONFIG["like"]["like_cap"]:
                    break
            if len(liked_users) >= CONFIG["like"]["like_cap"]:
                break

        index = workouts[1]["index"] if len(workouts) > 1 else None
        if not index:
            break


    send_discord_alert(f"-- Liked {len(liked_users)} users' workouts --", False, False)
