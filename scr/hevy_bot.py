import time
import random
import os
import sys
import requests

from utils import *
from follow_users import follow_users
from collect_people_to_follow import get_users_to_follow
from unfollow_user import unfollower_users
from like_workouts import like_discovery_users


def get_following(username, headers):
    url = f'https://api.hevyapp.com/following/{username}'
    res = requests.get(url, headers=headers)#send a GET path
    if res.status_code == 429: kill_switch("Rate limited")
    res.raise_for_status() #raised an expection if request failed
    return set(user['username'].lower() for user in res.json()) #converts json response into a set of usernames

def get_followers(username, headers):
    all_followers = []
    offset = 0

    while True:
        res = requests.get(f'https://api.hevyapp.com/followers_paged/{username}/{offset}', headers=headers)
        if res.status_code == 429:
            kill_switch("Rate limited")
        res.raise_for_status()

        page = res.json()  # this is a list, not a dict
        if not page:
            break

        all_followers.extend(page)
        offset += 50
        delay(0.5, 1.0)

    return set(user['username'].lower() for user in all_followers)


def load_temp_follow():
    if not os.path.exists(TEMP_FOLLOWING_PATH):
        return set()
    with open(TEMP_FOLLOWING_PATH, 'r') as f:
        return set(line.strip().split(',')[0].lower() for line in f.readlines())

def main():

    from pathlib import Path    
    my_following = get_following(HEVY_USERNAME, HEADERS)
    my_followers = get_followers(HEVY_USERNAME, HEADERS)
    temp_follow = load_temp_follow()

         #Grab users to follow
    to_follow = get_users_to_follow(my_following, my_followers)
         #Follow those users
    followed_users = follow_users(to_follow, my_following, temp_follow)
         #Unfollow users because of x
    unfollowed_users = unfollower_users(my_following, my_followers)


    summary = "\n**-----------------Session Summary-----------------**\n"

    if followed_users:
        summary += f"\n**Followed ({len(followed_users)}):**\n"
        summary += "\n".join([f"- @{user}" for user in followed_users])
    else:
        summary += "\n**Followed:** None"

    if unfollowed_users:
        summary += f"\n\nUnfollowed ({len(unfollowed_users)}):\n"
        summary += "\n".join([f"- @{u} ({reason})" for u, reason in unfollowed_users])

    else:
        summary += "\n\n**Unfollowed:** None"

    send_discord_alert(summary, True, True)

    print("--FINISHED--")
    


if __name__ == "__main__":
    main()