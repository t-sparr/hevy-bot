import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / '.env'

print("🔍 Checking if .env file exists...")
print("Full path:", env_path)
print("Exists:", env_path.exists())

print("\n📂 Printing raw contents of .env file:")
with open(env_path, 'r') as f:
    contents = f.read()
    print(contents)

print("📦 Loading .env...")
load_dotenv(dotenv_path=env_path)

print("\n🔑 Loaded values:")
print("USERNAME =", os.getenv("USERNAME"))
print("API_KEY =", os.getenv("API_KEY"))
print("AUTH_TOKEN =", os.getenv("AUTH_TOKEN"))
print("UNFOLLOWED_FILE =", os.getenv("UNFOLLOWED_FILE"))
