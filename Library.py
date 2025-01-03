from typing import List, Dict
import csv
import os
import Book
from BookFactory import BookFactory


# --- Lending and Returning Books ---
class Library:
    def __init__(self, books_file="books.csv"):
        self.books_file = books_file
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        if os.path.exists(self.books_file):
            with open(self.books_file, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    book = BookFactory.create_book(
                        row["title"],
                        row["author"],
                        int(row["year"]),
                        row["genre"],
                        int(row["copies"])
                    )
                    self.books.append(book)

    def save_books(self):
        with open(self.books_file, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["title", "author", "year", "category", "copies"])
            writer.writeheader()
            for book in self.books:
                writer.writerow(book.to_dict())

    def add_book(self, book: Book):
        self.books.append(book)
        self.save_books()

    def remove_book(self, title: str):
        self.books = [book for book in self.books if book.title != title]
        self.save_books()

    def borrow_book(self, title: str) -> bool:
        for book in self.books:
            if book.title == title and book.copies > 0:
                book.copies -= 1
                self.save_books()
                return True
        return False

    def return_book(self, title: str):
        for book in self.books:
            if book.title == title:
                book.copies += 1
                self.save_books()
                return