import requests
from datetime import datetime
from time import sleep

# --- Config ---
API_KEY    = 'shelobs_hevy_web'
AUTH_TOKEN = '5b1a4fa0-8a27-4443-9340-f71a10cff525'
USERNAME   = 'daniiiiii553'

HEADERS = {
    'x-api-key': API_KEY,
    'auth-token': AUTH_TOKEN,
    'Hevy-Platform': 'web',
    'Accept': 'application/json, text/plain, */*'
}

BASE_URL = 'https://api.hevyapp.com'

# --- Fetch followers ---
def get_all_followers():
    all_followers = []
    offset = 0
    while True:
        url = f'{BASE_URL}/followers_paged/{USERNAME}/{offset}'
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        page = res.json()
        if not page:
            break
        all_followers.extend(page)
        offset += 50
        sleep(0.4)
    return all_followers

# --- Get last workout ---
def get_last_workout(username):
    url = f"{BASE_URL}/user_workouts_paged?username={username}&limit=1&offset=0"
    res = requests.get(url, headers=HEADERS)

    if res.status_code != 200:
        return "❌ Error"

    workouts = res.json().get("workouts", [])
    if not workouts:
        return "No workouts"

    created = workouts[0].get("created_at")
    if created:
        return datetime.fromisoformat(created.replace("Z", "+00:00")).strftime('%Y-%m-%d %H:%M:%S')
    return "Unknown"


# --- Main ---
def run():
    followers = get_all_followers()
    print(f"Found {len(followers)} followers.\n")

    for user in followers:
        username = user['username']
        last_workout = get_last_workout(username)
        print(f"@{username:<20} | Last workout: {last_workout}")
        sleep(0.3)  # be polite to the API

if __name__ == '__main__':
    run()
