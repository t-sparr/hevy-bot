import os
import requests
import time
from dotenv import load_dotenv

# --- Load Environment ---
load_dotenv()

API_KEY = os.getenv('API_KEY')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')

if not API_KEY or not AUTH_TOKEN:
    raise RuntimeError("❌ Missing API_KEY or AUTH_TOKEN. Check your .env file.")

HEADERS = {
    'x-api-key': API_KEY,
    'auth-token': AUTH_TOKEN,
    'Hevy-Platform': 'web',
    'Accept': 'application/json, text/plain, */*'
}

BASE_URL = 'https://api.hevyapp.com'
DISCOVER_FEED_URL = f'{BASE_URL}/discover_feed_workouts_paged'


def fetch_discover_page(index=None):
    url = f"{DISCOVER_FEED_URL}/{index}" if index else DISCOVER_FEED_URL
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return res.json()


def fetch_likes(workout_id):
    url = f"{BASE_URL}/workout_likes/{workout_id}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return [u['username'] for u in res.json()]
    return []


def get_users_to_follow(unfollowed_users: set, already_following: set, target_count: int = 60) -> list:
    to_follow = []
    index = None

    # Normalize for case-insensitive comparison
    unfollowed_users = set(u.lower() for u in unfollowed_users)
    already_following = set(u.lower() for u in already_following)

    while len(to_follow) < target_count:
        data = fetch_discover_page(index)
        workouts = data.get('workouts', [])
        if not workouts or len(workouts) < 2:
            break

        workout = workouts[0]
        workout_id = workout['id']

        # Commenters first
        for comment in workout.get('comments', []):
            user = comment['username'].lower()
            if user in already_following:
                print(f"🔁 Skipping @{user} — already followed")
                continue
            if user in unfollowed_users:
                print(f"🚫 Skipping @{user} — previously unfollowed")
                continue
            if user not in to_follow:
                to_follow.insert(0, user)
                if len(to_follow) >= target_count:
                    return to_follow

        # Then likers
        likers = [u.lower() for u in fetch_likes(workout_id)]
        for user in likers:
            if user in already_following:
                print(f"🔁 Skipping @{user} — already followed")
                continue
            if user in unfollowed_users:
                print(f"🚫 Skipping @{user} — previously unfollowed")
                continue
            if user not in to_follow:
                to_follow.append(user)
                if len(to_follow) >= target_count:
                    return to_follow

        index = workouts[1]['index']
        time.sleep(0.5)

    return to_follow


# # Optional standalone test
# if __name__ == "__main__":
#     unfollowed = set()
#     following = set()

#     users = get_users_to_follow(unfollowed, following)
#     print(f"\n✅ Collected {len(users)} users to follow:")
#     for i, user in enumerate(users, 1):
#         print(f"{i:2}. @{user}")
