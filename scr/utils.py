import os
import time
import random
import requests
import sys
import yaml
from pathlib import Path
from dotenv import load_dotenv

# --- Load .env from project root ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

# --- Verify required environment variables ---
def verify_env():
    required_vars = ["API_KEY", "AUTH_TOKEN", "HEVY_USERNAME", "WEBHOOK_URL", "DISCORD_ID"]
    for var in required_vars:
        if not os.getenv(var):
            kill_switch(f"Missing required .env variable: {var}")

verify_env()

# --- Load environment variables ---
API_KEY = "shelobs_hevy_web"
# AUTH_TOKEN = "8832813e-5f3c-4397-be2d-bef91091f9fb"
# HEVY_USERNAME = "ilovecatssomuch"
AUTH_TOKEN = "8832813e-5f3c-4397-be2d-bef91091f9fb"
HEVY_USERNAME = "not_marco"
WEBHOOK_MAIN_URL = "https://discord.com/api/webhooks/1368605777249435759/AWfjsHOFix8JPYtwVkjwRdtF4VE3B6zfO3jyIKZAv5YqF6zAW0-CG9f8IFFXd_L2bTJo"
WEBHOOK_OTHER_URL = "https://discord.com/api/webhooks/1368605890998960251/TcjMlJ3keHcb8k24TJASKH6T0k2R_xMgKCyUZzZVcJf7aa7lYbmAbEDTh4KSdlVBx85a"

DISCORD_ID = os.getenv("DISCORD_ID")

# --- Paths ---
BASE_DIR = PROJECT_ROOT
TEMP_FOLLOWING_PATH = BASE_DIR / "data" / "temp_following.txt"
UNFOLLOWED_USERS_PATH = BASE_DIR / "data" / "unfollowed_users.txt"

# --- Hevy API headers ---
HEADERS = {
    "x-api-key": API_KEY,
    "auth-token": AUTH_TOKEN,
    "Hevy-Platform": "web",
    "Accept": "application/json, text/plain, */*"
}

# --- Load config YAML ---
def load_config(path=BASE_DIR / "config" / "config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

CONFIG = load_config()

# --- Utility functions ---
def delay(min_sec=3, max_sec=7):
    time.sleep(random.uniform(min_sec, max_sec))

def send_discord_alert(message, notify, main):
    if notify:
        message += f" <@{DISCORD_ID}>"
    payload = {"content": message}
    try:
        if main: requests.post(WEBHOOK_MAIN_URL, json=payload)
        else: requests.post(WEBHOOK_OTHER_URL, json=payload)
    except Exception as e:
        print(f"Failed to send Discord alert: {e}")

def kill_switch(reason):
    print(f"Program Killed: {reason}")
    send_discord_alert(f"Program Killed: {reason}", True)
    sys.exit(reason)
