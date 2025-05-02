# utils.py
import time
import random

def delay(min_sec=1.5, max_sec=3.0):
    """Randomized delay between requests to avoid detection."""
    time.sleep(random.uniform(min_sec, max_sec))