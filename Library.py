from idlelib.config_key import AVAILABLE_KEYS
from typing import List, Dict
import csv
import os
import Book
import os
import csv
from BookFactory import BookFactory
from log_decorator import log_decorator

"""
The Library class manages the books in a library system.
It handles the book data from the books.csv file.
"""


class Library:
    def __init__(self, books_file="csv_files/books.csv", available_books_file="csv_files/available_books.csv"):
        self.books_file = books_file
        self.available_books_file = available_books_file
        self.books = []  # List to store book objects
        self.load_books()

    # Loads book data from the CSV file into memory
    def load_books(self):
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
                        year=int(row["year"])
                    )
                    self.books.append(book)

    # Saves the current book data to the CSV file
    def save_books(self):
        with open(self.books_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["title", "author", "is_loaned", "copies", "genre", "year"])
            writer.writeheader()
            for book in self.books:
                writer.writerow({
                    "title": book.title,
                    "author": book.author,
                    "is_loaned": "Yes" if book.is_loaned else "No",
                    "copies": book.copies,
                    "genre": book.genre,
                    "year": book.year
                })

    # Adds a new book to the library by appending it to the list and saving it in the csv file
    @log_decorator("Book added")
    def add_book(self, book):
        self.books.append(book)
        self.save_books()

    # Removes a book by title
    @log_decorator("Book removed")
    def remove_book(self, title):
        #TODO: Implement a better way to remove books
        original_length = len(self.books)
        self.books = [book for book in self.books if book.title != title]
        if len(self.books) == original_length:
            raise ValueError("Book not found")
        self.save_books()

    # Returns a list of all books in the library
    @log_decorator("Displayed all books")
    def display_all_books(self):
        return self.books

    # Returns a list of books that are not currently loaned out
    @log_decorator("Displayed available books")
    def display_available_books(self):
        return [book for book in self.books if not book.is_loaned]

    # Returns a list of books that are currently loaned out
    @log_decorator("Displayed borrowed books")
    def display_borrowed_books(self):
        return [book for book in self.books if book.is_loaned]

    # Returns a list of books in a specific category
    @log_decorator("Displayed books by category")
    def display_books_by_category(self, category):
        return [book for book in self.books if book.genre.lower() == category.lower()]

    # Marks a book as loaned out
    @log_decorator("Book borrowed")
    def borrow_book(self, title):
        for book in self.books:
            if book.title == title:
                if not book.is_loaned:
                    book.is_loaned = True
                    self.save_books()
                    return
                else:
                    raise ValueError(f"The book '{title}' is already loaned out.")
        raise ValueError(f"The book '{title}' does not exist in the library.")

    #Marks a book as returned
    @log_decorator("Book returned")
    def return_book(self, title):
        for book in self.books:
            if book.title == title and book.is_loaned:
                book.is_loaned = False
                self.save_books()
                return
        raise ValueError("Book not borrowed")