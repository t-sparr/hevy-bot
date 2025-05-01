import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ['API_KEY']
AUTH_TOKEN = os.environ['AUTH_TOKEN']
WEBHOOK_URL = 'https://discord.com/api/webhooks/1367640664669556857/sDi-4OIfk1gvE9Tu8AsoXbK9GhbwD0BIBuAEGrPb_QYwZenAoqsAjfjuEi7pVc-MCTPo'

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
        send_discord_alert("hevy bot boken is expired")
        raise SystemExit("Token expired or invalid!")

def send_discord_alert(message):
    payload = {'content': message}
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"⚠️ Failed to send Discord alert: {e}")

if __name__ == '__main__':
    check_token()
