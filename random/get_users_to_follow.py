import requests
import time

# --- CONFIG ---
API_KEY = 'shelobs_hevy_web'
AUTH_TOKEN = '5b1a4fa0-8a27-4443-9340-f71a10cff525'

HEADERS = {
    'x-api-key': API_KEY,
    'auth-token': AUTH_TOKEN,
    'Hevy-Platform': 'web',
    'Accept': 'application/json, text/plain, */*'
}

DISCOVER_BASE = 'https://api.hevyapp.com/discover_feed_workouts_paged'
TARGET_COUNT = 60

def fetch_discover_page(index=None):
    url = f"{DISCOVER_BASE}/{index}" if index else DISCOVER_BASE
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return res.json()

def fetch_likes(workout_id):
    url = f"https://api.hevyapp.com/workout_likes/{workout_id}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return [u['username'] for u in res.json()]
    return []

def process_workout(workout, collected_usernames):
    workout_id = workout['id']
    username = workout['username']
    print(f"\n🏋️ Workout by @{username} (ID: {workout_id})")

    # Collect commenters
    print("💬 Comments:")
    for comment in workout.get('comments', []):
        commenter = comment['username']
        print(f"  - @{commenter}: {comment['comment']}")
        if commenter not in collected_usernames:
            collected_usernames.append(commenter)
            if len(collected_usernames) >= TARGET_COUNT:
                return True  # Stop if we hit the target

    # Collect likers
    print("❤️ Likes:")
    likers = fetch_likes(workout_id)
    for liker in likers:
        print(f"  - @{liker}")
        if liker not in collected_usernames:
            collected_usernames.append(liker)
            if len(collected_usernames) >= TARGET_COUNT:
                return True  # Stop if we hit the target

    return False

def main():
    index = None
    collected_usernames = []

    while len(collected_usernames) < TARGET_COUNT:
        data = fetch_discover_page(index)
        workouts = data.get('workouts', [])
        if len(workouts) < 2:
            print("⚠️ Not enough workouts found.")
            break

        should_stop = process_workout(workouts[0], collected_usernames)
        if should_stop:
            break

        index = workouts[1]['index']
        time.sleep(0.5)

    print(f"\n✅ Final list of {len(collected_usernames)} usernames (commenters first):")
    for username in collected_usernames:
        print(f"@{username}")

if __name__ == "__main__":
    main()
