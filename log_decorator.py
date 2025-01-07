import os
import functools
from datetime import datetime

# Log file path
LOG_FILE = "log.txt"

# Ensure the log file exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as file:
        file.write("--- Library Log ---\n")


def log_decorator(func):
    """
    Decorator to log actions to a file based on the function's returned message.

    The function must return a specific success or failure message.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            log_message = f"[{datetime.now()}] {result}\n"
            with open(LOG_FILE, "a") as log_file:
                log_file.write(log_message)
            return result
        except Exception as e:
            log_message = f"[{datetime.now()}] {str(e)}\n"
            with open(LOG_FILE, "a") as log_file:
                log_file.write(log_message)
            raise e
    return wrapper
