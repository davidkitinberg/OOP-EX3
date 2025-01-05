from typing import List, Dict
import csv
import os
from BookFactory import BookFactory
from log_decorator import log_decorator

"""
The Library class manages the books in a library system.
It handles the book data from the books.csv file and keeps track of available copies in the available_books.csv file.
"""

class Library:
    def __init__(self, books_file="csv_files/books.csv", available_books_file="csv_files/available_books.csv"):
        self.books_file = books_file
        self.available_books_file = available_books_file
        self.books = []  # List to store book objects
        self.available_copies = {}  # Dictionary to track available copies
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
        print("Books file updated successfully.")

    def switch_is_loaned_state(self, title):
        """Switch the is_loaned state based on available copies."""
        for book in self.books:
            if book.title == title:
                available = self.available_copies.get(title, 0)
                print(f"Switching is_loaned state for '{title}': available_copies={available}")

                # Update the is_loaned state
                if available == 0:
                    print(f"Setting '{title}' as loaned")
                    book.is_loaned = True
                else:
                    print(f"Setting '{title}' as available")
                    book.is_loaned = False

                # Save the updated is_loaned state to the books.csv file
                self.update_books_file()
                self.update_available_books_file()
                return
        raise ValueError(f"Book '{title}' not found in the library.")

    @log_decorator("Book borrowed")
    def borrow_book(self, title):
        """Borrow a book, decrementing its available copies."""
        if title in self.available_copies:
            if self.available_copies[title] > 0:
                self.available_copies[title] -= 1
                self.switch_is_loaned_state(title)
            else:
                raise ValueError(f"'{title}' is currently unavailable.")
        else:
            raise ValueError(f"'{title}' does not exist in the library.")

    @log_decorator("Book returned")
    def return_book(self, title):
        """Return a book, incrementing its available copies."""
        for book in self.books:
            if book.title == title:
                if self.available_copies[title] < book.copies:
                    self.available_copies[title] += 1
                    self.switch_is_loaned_state(title)
                    return
                else:
                    raise ValueError(f"All copies of '{title}' are already returned.")
        raise ValueError(f"'{title}' does not exist in the library.")

    @log_decorator("Book added")
    def add_book(self, book):
        """Add a book to the library."""
        self.books.append(book)
        self.available_copies[book.title] = book.copies
        self.update_available_books_file()

    @log_decorator("Book removed")
    def remove_book(self, title):
        """Remove a book from the library."""
        original_length = len(self.books)
        self.books = [book for book in self.books if book.title != title]
        if len(self.books) == original_length:
            raise ValueError(f"'{title}' not found in the library.")
        self.available_copies.pop(title, None)
        self.update_available_books_file()
        self.update_books_file()

    # Returns a list of all books in the library
    @log_decorator("Displayed all books")
    def display_all_books(self):
        return self.books

    # Returns a list of books that are not currently loaned out
    @log_decorator("Displayed available books")
    def display_available_books(self):
        return [book for book in self.books if self.available_copies.get(book.title, 0) > 0]

    # Returns a list of books in a specific category
    @log_decorator("Displayed books by category")
    def display_books_by_category(self, category):
        return [book for book in self.books if book.genre.lower() == category.lower()]
