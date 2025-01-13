from typing import List, Dict
import csv
import os
from BookFactory import BookFactory
from WaitingListManager import WaitingListManager
from notification_service import NotificationService, EmailNotifier, SMSNotifier


"""
The Library class manages the books in a library system.
It handles the book data from the books.csv file and keeps track of available/loaned copies in the available_books.csv & loaned_books.csv files.
"""

class Library:
    def __init__(self, books_file="csv_files/books.csv", available_books_file="csv_files/available_books.csv", loaned_books_file="csv_files/loaned_books.csv"):
        self.books_file = books_file
        self.available_books_file = available_books_file
        self.loaned_books_file = loaned_books_file
        self.books = []  # List to store book objects
        self.available_copies = {}  # Dictionary to track available copies
        self.loaned_books = {} # Dictionary to track loaned copies
        self.waiting_list_manager = WaitingListManager("csv_files/waiting_list.csv")  # Initialize the waiting list manager
        self.notification_service = NotificationService()  # Initialize the notification service

        self.load_books_to_memory()

    def load_books_to_memory(self):
        """Load books from the books file to the memory and initialize available copies."""
        if os.path.exists(self.books_file):
            with open(self.books_file, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    book = BookFactory.create_book(
                        title=row["title"],
                        author=row["author"],
                        is_loaned=row["is_loaned"].lower() == "yes",
                        copies=int(row["copies"]),
                        genre=row["genre"],
                        year=int(row["year"]),
                    )
                    self.books.append(book)

        # Initialize `available_copies` based on the `available_books_file`
        if os.path.exists(self.available_books_file):
            with open(self.available_books_file, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.available_copies[row["title"]] = int(row["available_copies"])
        else:
            # Default initialization for available copies
            for book in self.books:
                self.available_copies[book.title] = book.copies
            self.update_available_books_file()

        # Initialize `loaned_copies` based on the `loaned_books_file`
        if os.path.exists(self.loaned_books_file):
            with open(self.loaned_books_file, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.loaned_books[row["title"]] = int(row["loaned_copies"])
        else:
            # Default initialization for loaned copies if the file doesn't exist
            for book in self.books:
                total_copies = book.copies
                available_copies = self.available_copies.get(book.title, 0)
                self.loaned_books[book.title] = total_copies - available_copies



    def update_loaned_books_file(self):
        """
        Update or create the loaned_books.csv file based on current books and available copies.
        """
        loaned_books_data = []

        # Calculate loaned books data
        for book in self.books:
            total_copies = book.copies
            available_copies = self.available_copies.get(book.title, 0)
            loaned_copies = total_copies - available_copies
            in_waiting_list = self.waiting_list_manager.count_waiting_list(book.title)

            loaned_books_data.append({
                "title": book.title,
                "author": book.author,
                "loaned_copies": loaned_copies,
                "in_waiting_list": in_waiting_list,
                "genre": book.genre,
                "year": book.year,
            })

        # Write loaned_books.csv
        with open(self.loaned_books_file, "w", newline="", encoding="utf-8") as file:
            fieldnames = ["title", "author", "loaned_copies", "in_waiting_list", "genre", "year"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(loaned_books_data)


    def update_available_books_file(self):
        """Save the current available books state to the available_books file."""
        with open(self.available_books_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["title", "author", "available_copies", "genre", "year"])
            writer.writeheader()
            for book in self.books:
                writer.writerow({
                    "title": book.title,
                    "author": book.author,
                    "available_copies": self.available_copies.get(book.title, book.copies),
                    "genre": book.genre,
                    "year": book.year,
                })

    def update_books_file(self):
        """Save the current state of all books to the books.csv file."""
        with open(self.books_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["title", "author", "is_loaned", "copies", "genre", "year"])
            writer.writeheader()
            for book in self.books:
                writer.writerow({
                    "title": book.title,
                    "author": book.author,
                    "is_loaned": "Yes" if book.is_loaned else "No",  # Convert to "Yes"/"No"
                    "copies": book.copies,
                    "genre": book.genre,
                    "year": book.year,
                })

    def switch_is_loaned_state(self, title):
        """Switch the is_loaned state based on available copies."""
        for book in self.books:
            if book.title == title:
                available = self.available_copies.get(title, 0)

                # Update the is_loaned state
                if available == 0:
                    book.is_loaned = True
                else:
                    book.is_loaned = False

                # Save the updated is_loaned state to the books.csv file
                self.update_books_file()
                self.update_available_books_file()
                self.update_loaned_books_file()
                return
        raise ValueError(f"Book '{title}' not found in the library.")



    def borrow_book(self, title):
        """
        Borrow a book, or return information about its availability.
        Returns:
            - "book borrowed successfully" if the book was successfully borrowed.
            - "book borrowed fail - no available copies" if the book is currently unavailable.
            - Raises ValueError if the book does not exist.
        """
        # Check if the book is in the system
        if title in self.available_copies:
            # Check if there are available copies to lend
            if self.available_copies[title] > 0:
                self.available_copies[title] -= 1
                self.loaned_books[title] += 1
                self.switch_is_loaned_state(title)
                self.notification_service.notify_all(f"The book '{title}' has been borrowed.")
                return "book borrowed successfully"
            else: # If there are no available copies -> start waiting list sequence BEEP BOP
                return "book borrowed fail - no available copies"
        else: # If book does not exist in the library
            raise ValueError(f"'{title}' does not exist in the library.")


    def return_book(self, title):
        """Return a book, notify the next client if there's a waiting list."""
        try:
            for book in self.books:
                if book.title == title:
                    if self.available_copies[title] < book.copies:

                        # Notify the first client on the waiting list
                        waiting_list = self.waiting_list_manager.get_waiting_list_for_book(title)
                        if waiting_list: # If there is a waiting list for that book
                            next_client = self.waiting_list_manager.notify_next_client(title)
                            self.switch_is_loaned_state(title)
                            return f"book '{title}' returned successfully, notified '{next_client['client']}'"

                        self.available_copies[title] += 1
                        self.loaned_books[title] -= 1
                        self.switch_is_loaned_state(title)
                        return f"book '{title}' returned successfully"
                    else:
                        raise ValueError(f"All copies of '{title}' are already returned.")
            raise ValueError(f"'{title}' does not exist in the library.")
        except Exception:
            return f"book '{title}' returned fail"



    def add_book(self, book):
        """Add a book to the library."""
        try:
            for book in self.books: # Check if book already exists in the library
                if (book.title == book.title
                        and book.author == book.author
                        and book.genre == book.genre
                        and book.year == book.year):
                    raise ValueError(f"'{book.title}' already exists in the library.")
            self.books.append(book)
            if book.is_loaned:  # If the book is marked as loaned
                self.available_copies[book.title] = 0  # All copies are loaned out
                self.loaned_books[book.title] = book.copies  # Loaned copies equal total copies
            else:  # If the book is not loaned
                self.available_copies[book.title] = book.copies  # All copies are available
                self.loaned_books[book.title] = 0  # No copies are loaned

            # Notify users
            self.notification_service.notify_all(f"Book '{book.title}' has been added to the library.")

            # Update files
            self.update_available_books_file()
            self.update_books_file()
            self.update_loaned_books_file()
            return f"book added successfully"
        except Exception as e:
            raise RuntimeError(f"Book added fail: {str(e)}")


    def remove_book(self, title):
        """Remove a book and notify clients on the waiting list."""
        # Check if the book is in the system
        try:
            original_length = len(self.books)
            self.books = [book for book in self.books if book.title != title]
            if len(self.books) == original_length:
                raise ValueError(f"'{title}' not found in the library.")
            # Delete the book from all listings + update the miss fortunes clients that waited for it
            self.available_copies.pop(title, None)
            self.loaned_books.pop(title, None)
            self.waiting_list_manager.remove_waiting_list_for_book(title)
            self.notification_service.notify_all(f"Book '{title}' has been removed from the library.")
            self.update_available_books_file()
            self.update_loaned_books_file()
            self.update_books_file()
            return f"book '{title}' removed successfully"
        except Exception:
            return f"book '{title}' removed fail"

    def popular_books(self):
        """
        Returns the top 5 popular books based on the sum of loaned_copies and in_waiting_list.
        """
        popular_books_data = []

        # Load loaned_books data
        if os.path.exists(self.loaned_books_file):
            with open(self.loaned_books_file, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    loaned_copies = int(row["loaned_copies"])
                    in_waiting_list = int(row["in_waiting_list"])
                    popularity_score = loaned_copies + in_waiting_list

                    popular_books_data.append({
                        "title": row["title"],
                        "author": row["author"],
                        "popularity": popularity_score,
                        "genre": row["genre"],
                        "year": row["year"],
                    })

        # Sort books by popularity in descending order and get the top 5
        top_books = sorted(popular_books_data, key=lambda x: x["popularity"], reverse=True)[:5]
        return top_books

