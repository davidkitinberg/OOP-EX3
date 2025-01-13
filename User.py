from werkzeug.security import generate_password_hash, check_password_hash

"""
This is a simple class that represents users (by their username and password).
"""
class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)