import requests

# Config
API_KEY = 'shelobs_hevy_web'
AUTH_TOKEN = '5b1a4fa0-8a27-4443-9340-f71a10cff525'

HEADERS = {
    'x-api-key': API_KEY,
    'auth-token': AUTH_TOKEN,
    'Hevy-Platform': 'web',
    'Accept': 'application/json, text/plain, */*'
}

BASE_URL = 'https://api.hevyapp.com/feed_workouts_paged'

def fetch_recent_workouts(start_index, pages=1):
    current_index = start_index
    all_workouts = []

    for _ in range(pages):
        url = f'{BASE_URL}/{current_index}'
        res = requests.get(url, headers=HEADERS)
        if res.status_code != 200:
            print(f'❌ Request failed with status {res.status_code}')
            break

        data = res.json()
        workouts = data.get('workouts', [])
        if not workouts:
            print('⚠️ No workouts returned.')
            break

        all_workouts.extend(workouts)

        try:
            current_index = min(w['index'] for w in workouts if 'index' in w)
        except Exception as e:
            print(f'⚠️ Failed to determine next index: {e}')
            break

    return all_workouts


if __name__ == '__main__':
    START_INDEX = 122447021  # Use the latest ID you've seen in browser
    workouts = fetch_recent_workouts(START_INDEX, pages=3)

    print("\n🆕 Recent Workouts:")
    for w in workouts:
        print(f"🏋️ {w.get('username', '???')} | {w.get('name', 'Unnamed')} | {w.get('created_at', 'Unknown')}")
