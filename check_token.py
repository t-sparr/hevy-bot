import os
import requests

API_KEY = os.environ['API_KEY']
AUTH_TOKEN = os.environ['AUTH_TOKEN']

HEADERS = {
    'x-api-key': API_KEY,
    'auth-token': AUTH_TOKEN,
    'Hevy-Platform': 'web',
    'Accept': 'application/json, text/plain, */*'
}

def check_token():
    url = "https://api.hevyapp.com/user/account"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        print("✅ Token is valid")
    else:
        print(f"❌ Token check failed. Status: {res.status_code}")
        raise SystemExit("Token expired or invalid!")

if __name__ == '__main__':
    check_token()
