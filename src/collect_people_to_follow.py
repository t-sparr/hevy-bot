from utils import *

DISCOVER_FEED_URL = f'https://api.hevyapp.com/discover_feed_workouts_paged'

def load_unfollowed_users(filepath):
    if not os.path.exists(filepath):
        return set()
    with open(filepath, 'r') as f:
        return set(line.strip() for line in f)
    
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



def get_users_to_follow(my_following, my_followers):
    to_follow = []
    index = None
    target_count = CONFIG["follow"]["follow_target"]

    commenter_goal = int(target_count * CONFIG["follow"]["comment_ratio"])
    liker_goal = target_count - commenter_goal
    commenters_added = 0
    likers_added = 0

    unfollowed_users = set(u.lower() for u in load_unfollowed_users(UNFOLLOWED_USERS_PATH))
    my_following = set(u.lower() for u in my_following)
    my_followers = set(u.lower() for u in my_followers)

    while len(to_follow) < target_count:
        data = fetch_discover_page(index)
        workouts = data.get('workouts', [])
        if not workouts or len(workouts) < 2:
            break

        workout = workouts[0]
        workout_id = workout['id']

        # Add from commenters
        for comment in workout.get('comments', []):
            if commenters_added >= commenter_goal:
                break
            user = comment['username'].lower()
            if user in my_following or user in my_followers or user in unfollowed_users or user in to_follow:
                continue
            to_follow.append(user)
            commenters_added += 1
            print(f"[COMMENT] @{user} added")
            if len(to_follow) >= target_count:
                return to_follow

        # Add from likers
        likers = [u.lower() for u in fetch_likes(workout_id)]
        for user in likers:
            if likers_added >= liker_goal:
                break
            if user in my_following or user in my_followers or user in unfollowed_users or user in to_follow:
                continue
            to_follow.append(user)
            likers_added += 1
            print(f"[LIKE] @{user} added")
            if len(to_follow) >= target_count:
                return to_follow

        index = workouts[1]['index'] if len(workouts) > 1 else None
        if not index:
            break
        delay()

    return to_follow

        