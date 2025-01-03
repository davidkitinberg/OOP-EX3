import hashlib
from abc import ABC, abstractmethod
from typing import List, Dict
from werkzeug.security import generate_password_hash, check_password_hash
import csv
import os
from User import User


class UserManager:
    def __init__(self, file_path="users.csv"):
        self.file_path = file_path
        self.users: Dict[str, User] = {}
        self.load_users()

    # Loads users from users.csv file to the program
    def load_users(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.users[row["username"]] = User(row["username"], row["password"])
    # Writes users from program to the users.csv file
    def save_users(self):
        with open(self.file_path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["username", "password"])
            writer.writeheader()
            for user in self.users.values():
                writer.writerow({"username": user.username, "password": user.password})

    # Add new user to the data list and users.csv
    def register_user(self, username: str, password: str):
        if username in self.users:
            raise ValueError("Username already exists")
        user = User(username, password)
        self.users[username] = user
        self.save_users()

    # Authenticate user's sign in details
    def authenticate_user(self, username: str, password: str) -> bool:
        user = self.users.get(username)
        if not user:
            return False
        return user.verify_password(password)