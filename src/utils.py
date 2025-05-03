# utils.py
import time 
import os
import random
import requests
import sys

from dotenv import load_dotenv


load_dotenv()

TARGET_FOLLOW = 1
API_KEY = os.getenv('API_KEY')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
HEVY_USERNAME = os.getenv('HEVY_USERNAME')
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
DISCORD_ID = os.getenv("DISCORD_ID")
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMP_FOLLOWING = os.path.join(BASE_DIR, "data", "temp_following.txt")

HEADERS = {
    'x-api-key': API_KEY,
    'auth-token': AUTH_TOKEN,
    'Hevy-Platform': 'web',
    'Accept': 'application/json, text/plain, */*'
}


def delay(min_sec=1.5, max_sec=3.0):
    time.sleep(random.uniform(min_sec, max_sec))

def send_discord_alert(message, notify):
    payload = {'content': message}
    try:
        if notify: message += f" <@{DISCORD_ID}>"
        requests.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"Failed to send Discord alert: {e}")

def kill_switch(reason):
    print(f"Program Killed: {reason}")
    send_discord_alert(f"Program Killed: {reason} <@{DISCORD_ID}>")
    sys.exit(reason)