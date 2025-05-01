import os
import json
import requests
from time import sleep
from datetime import datetime

# --- Configuration ---
API_KEY    = 'shelobs_hevy_web'
AUTH_TOKEN = '5b1a4fa0-8a27-4443-9340-f71a10cff525'
USERNAME   = 'daniiiiii553'
UNFOLLOWED_FILE = 'unfollowed_users.txt'

HEADERS = {
    'x-api-key': API_KEY,
    'auth-token': AUTH_TOKEN,
    'Hevy-Platform': 'web',
    'Accept': 'application/json, text/plain, */*'
}

BASE_URL = 'https://api.hevyapp.com'


# --- File Utilities ---
def save_json(data, label):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'{label}_{timestamp}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f'💾 Saved {label} to {filename}')


def load_unfollowed_users():
    if not os.path.exists(UNFOLLOWED_FILE):
        return set()
    with open(UNFOLLOWED_FILE, 'r') as f:
        return set(line.strip() for line in f)


def save_unfollowed_user(username):
    with open(UNFOLLOWED_FILE, 'a') as f:
        f.write(f'{username}\n')


# --- Hevy API Interaction ---
def get_following():
    res = requests.get(f'{BASE_URL}/following/{USERNAME}', headers=HEADERS)
    res.raise_for_status()
    return res.json()


def get_all_followers():
    all_followers = []
    offset = 0
    while True:
        res = requests.get(f'{BASE_URL}/followers_paged/{USERNAME}/{offset}', headers=HEADERS)
        res.raise_for_status()
        page = res.json()
        if not page:
            break
        all_followers.extend(page)
        offset += 50
        sleep(0.5)  # Respectful delay
    return all_followers


def follow_user(username):
    if username in unfollowed_users:
        print(f'⛔ Skipped (unfollowed before): {username}')
        return
    res = requests.post(f'{BASE_URL}/follow', headers=HEADERS, json={'username': username})
    if res.status_code == 200:
        print(f'+ Followed: {username}')
    else:
        print(f'! Failed to follow: {username}')


def unfollow_user(username):
    res = requests.post(f'{BASE_URL}/unfollow', headers=HEADERS, json={'username': username})
    if res.status_code == 200:
        print(f'- Unfollowed: {username}')
        save_unfollowed_user(username)
    else:
        print(f'! Failed to unfollow: {username}')


# --- Main Automation ---
def automate():
    global unfollowed_users
    unfollowed_users = load_unfollowed_users()

    print('🚀 Fetching data...')
    following = get_following()
    followers = get_all_followers()

    # Save snapshots
    save_json(following, 'following')
    save_json(followers, 'followers')
    



    

    print('✅ Automation complete.')


if __name__ == '__main__':
    automate()
