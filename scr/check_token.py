from utils import *
from datetime import datetime
from like_workouts import like_discovery_users

def check_token():
    url = "https://api.hevyapp.com/user/account"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        print("Token is valid")
        send_discord_alert(f"[{now}] Token is valid", False, False)
    else:
        print(f"Token check failed. Status: {res.status_code}")
        send_discord_alert(f"[{now}] Token is invalid: {res.status_code}", True, False)
        kill_switch("Token expired or invalid!")


if __name__ == '__main__':
    check_token()
    like_discovery_users()

