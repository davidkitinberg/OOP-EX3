import os
import unittest
import csv
from UserManager import UserManager

class TestUserManager(unittest.TestCase):
    def setUp(self):
        # Use a temporary file for testing
        self.test_users_file = "test_users_temp.csv"
        with open(self.test_users_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["username", "password"])  # Add headers for the CSV file

        self.user_manager = UserManager(self.test_users_file)

    def tearDown(self):
        # Clean up the temporary file
        if os.path.exists(self.test_users_file):
            os.remove(self.test_users_file)


    def test_save_users(self):
        # Register a user and save to file
        self.user_manager.register_user("test_user", "secure_password")
        self.user_manager.save_users()

        # Verify the user is in the file
        with open(self.test_users_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            users = list(reader)
        self.assertTrue(any(user["username"] == "test_user" for user in users), "User should be saved in the file.")

    def test_authenticate_user(self):
        # Register a user
        self.user_manager.register_user("test_user", "secure_password")

        # Authenticate the user
        self.assertTrue(self.user_manager.authenticate_user("test_user", "secure_password"))
        self.assertFalse(self.user_manager.authenticate_user("test_user", "wrong_password"))
        self.assertFalse(self.user_manager.authenticate_user("nonexistent_user", "secure_password"))

    def test_load_users(self):
        # Prepopulate the CSV file with a user
        with open(self.test_users_file, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["test_user", "secure_password"])

        # Load users and verify
        self.user_manager.load_users()
        self.assertTrue(
            "test_user" in self.user_manager.users,
            "The user should be loaded from the file."
        )

if __name__ == "__main__":
    unittest.main()