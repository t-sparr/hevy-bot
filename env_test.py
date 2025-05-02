from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

print("USERNAME =", os.getenv("USERNAME"))
print("API_KEY =", os.getenv("API_KEY"))
print("AUTH_TOKEN =", os.getenv("AUTH_TOKEN"))