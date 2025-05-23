from datetime import datetime
from Library import *
from notification_service import NotificationService, EmailNotifier, SMSNotifier

"""
The WaitingListManager class manages the books waiting list in a library system.
It handles client's requests to wait for a specific book by updating the waiting_list.csv file accordingly.
"""

class WaitingListManager:
    def __init__(self, waiting_list_file="csv_files/waiting_list.csv"):
        self.notification_service = NotificationService()  # Initialize the notification service
        # Add notification observers (email, SMS, etc.)
        self.notification_service.add_observer(EmailNotifier())
        self.notification_service.add_observer(SMSNotifier())
        self.waiting_list_file = waiting_list_file
        if not os.path.exists(self.waiting_list_file):
            with open(self.waiting_list_file, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(
                    file, fieldnames=["title", "author", "genre", "year", "client", "email_addr", "phone_num", "time_of_entry"]
                )
                writer.writeheader()

    def add_to_waiting_list(self, title, author, genre, year, client, email, phone):
        """Add a client to the waiting list for a specific book."""
        with open(self.waiting_list_file, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["title", "author", "genre", "year", "client", "email_addr", "phone_num", "time_of_entry"]
            )
            writer.writerow({
                "title": title,
                "author": author,
                "genre": genre,
                "year": year,
                "client": client,
                "email_addr": email,
                "phone_num": phone,
                "time_of_entry": datetime.now().isoformat()
            })


    def get_waiting_list_for_book(self, title):
        """Retrieve the waiting list for a specific book."""
        with open(self.waiting_list_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return [row for row in reader if row["title"] == title]

    def remove_waiting_list_for_book(self, title):
        """Remove all waiting list entries for a specific book."""
        updated_list = []
        with open(self.waiting_list_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            updated_list = [row for row in reader if row["title"] != title]

        with open(self.waiting_list_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file, fieldnames=["title", "author", "genre", "year", "client", "email_addr", "phone_num", "time_of_entry"]
            )
            writer.writeheader()
            writer.writerows(updated_list)

    def notify_next_client(self, title):
        """Notify the next client in the waiting list for a specific book."""
        waiting_list = self.get_waiting_list_for_book(title)
        if not waiting_list:
            return None

        next_client = waiting_list[0]

        # Ensure all keys exist
        missing_keys = [key for key in ["client", "email_addr", "phone_num"] if key not in next_client]
        if missing_keys:
            raise KeyError(f"Missing keys in waiting list entry: {missing_keys}")

        # Notify the next client via email and SMS
        try:

            notify_message = f"Dear {next_client['client']},\n\nThe book '{title}' is now available for you. Please visit the library to borrow it.\n\nThank you!"
            # Email Notification
            EmailNotifier.notify(next_client["email_addr"], notify_message)
            # SMS Notification
            SMSNotifier.notify(next_client["email_addr"], notify_message)

            print(
                f"Successfully notified {next_client['client']} at {next_client['email_addr']} and {next_client['phone_num']} for '{title}'.")

            # Remove the client from the waiting list
            self.remove_waiting_list_entry(next_client)

            return next_client

        except Exception as e:
            print(f"Failed to notify {next_client['client']}: {e}")
            return None

    def remove_waiting_list_entry(self, entry):
        """Remove a specific entry from the waiting list."""
        updated_list = []
        with open(self.waiting_list_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            updated_list = [row for row in reader if row != entry]

        with open(self.waiting_list_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file, fieldnames=["title", "author", "genre", "year", "client", "email_addr", "phone_num", "time_of_entry"]
            )
            writer.writeheader()
            writer.writerows(updated_list)

    def count_waiting_list(self, title):
        """
        Returns the number of people in the waiting list for a specific book.
        """
        count = 0
        if not os.path.exists(self.waiting_list_file):
            return count  # No waiting list file, return 0

        with open(self.waiting_list_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["title"].lower() == title.lower():
                    count += 1
        return count