import os
import csv
import unittest
from Library import Library
from BookFactory import BookFactory

class TestLibrary(unittest.TestCase):
    def setUp(self):
        # Define test-specific file paths
        self.books_file = os.path.join("test_csv_files", "books.csv")
        self.available_books_file = os.path.join("test_csv_files", "available_books.csv")
        self.loaned_books_file = os.path.join("test_csv_files", "loaned_books.csv")
        self.waiting_list_file = os.path.join("test_csv_files", "waiting_list.csv")

        # Ensure necessary directories and files exist
        self.ensure_csv_files_exist()

        # Populate CSVs with test data
        self.populate_books_file()

        # Initialize Library instance
        self.library = Library(
            books_file=self.books_file,
            available_books_file=self.available_books_file,
            loaned_books_file=self.loaned_books_file,
        )

    def ensure_csv_files_exist(self):
        """Ensure that all test CSV files exist and create them if needed."""
        os.makedirs(os.path.dirname(self.books_file), exist_ok=True)
        for file_path in [self.books_file, self.available_books_file, self.loaned_books_file, self.waiting_list_file]:
            if not os.path.exists(file_path):
                with open(file_path, "w", newline="", encoding="utf-8") as file:
                    pass  # Create an empty file

    def populate_books_file(self):
        """Populate the books CSV file with test data."""
        with open(self.books_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file, fieldnames=["title", "author", "is_loaned", "copies", "genre", "year"]
            )
            writer.writeheader()
            writer.writerows([
                {"title": "Book A", "author": "Author A", "is_loaned": "No", "copies": 3, "genre": "Fiction", "year": 2000},
                {"title": "Book B", "author": "Author B", "is_loaned": "No", "copies": 2, "genre": "Science", "year": 2010},
                {"title": "Book C", "author": "Author C", "is_loaned": "No", "copies": 1, "genre": "Fiction", "year": 2020},
            ])

        # Populate available_books_file with initial data
        with open(self.available_books_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file, fieldnames=["title", "author", "available_copies", "genre", "year"]
            )
            writer.writeheader()
            writer.writerows([
                {"title": "Book A", "author": "Author A", "available_copies": 3, "genre": "Fiction", "year": 2000},
                {"title": "Book B", "author": "Author B", "available_copies": 2, "genre": "Science", "year": 2010},
                {"title": "Book C", "author": "Author C", "available_copies": 1, "genre": "Fiction", "year": 2020},
            ])

        # Populate loaned_books_file with initial data
        with open(self.loaned_books_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file, fieldnames=["title", "author", "loaned_copies", "in_waiting_list", "genre", "year"]
            )
            writer.writeheader()
            writer.writerows([
                {"title": "Book A", "author": "Author A", "loaned_copies": 0, "in_waiting_list": 0, "genre": "Fiction", "year": 2000},
                {"title": "Book B", "author": "Author B", "loaned_copies": 0, "in_waiting_list": 0, "genre": "Science", "year": 2010},
                {"title": "Book C", "author": "Author C", "loaned_copies": 0, "in_waiting_list": 0, "genre": "Fiction", "year": 2020},
            ])

    def tearDown(self):
        """Clean up after tests by clearing the test CSV files."""
        for file_path in [self.books_file, self.available_books_file, self.loaned_books_file, self.waiting_list_file]:
            with open(file_path, "w", newline="", encoding="utf-8") as file:
                file.write("")  # Clear the file content

    def test_borrow_book(self):
        result = self.library.borrow_book("Book A")
        self.assertEqual(result, "book borrowed successfully")
        self.assertEqual(self.library.available_copies["Book A"], 2)

    def test_return_book(self):
        self.library.borrow_book("Book A")
        result = self.library.return_book("Book A")
        self.assertEqual(result, "book 'Book A' returned successfully")
        self.assertEqual(self.library.available_copies["Book A"], 3)

    def test_add_book(self):
        # Create a fresh instance of the library with empty test files
        temp_books_file = "test_temp_books.csv"
        temp_available_books_file = "test_temp_available_books.csv"
        temp_loaned_books_file = "test_temp_loaned_books.csv"

        # Ensure the test files are empty
        for file in [temp_books_file, temp_available_books_file, temp_loaned_books_file]:
            with open(file, "w", newline="", encoding="utf-8") as f:
                f.write("")  # Clear all content

        # Create a new library instance with these empty test files
        library_for_test = Library(
            books_file=temp_books_file,
            available_books_file=temp_available_books_file,
            loaned_books_file=temp_loaned_books_file,
        )

        # Create a unique book
        unique_book = BookFactory.create_book(
            "Unique Book", "Unique Author", False, 5, "Fantasy", 2025
        )

        # Add the unique book
        result = library_for_test.add_book(unique_book)

        # Assertions
        self.assertEqual(result, "book added successfully")
        self.assertIn("Unique Book", [book.title for book in library_for_test.books])
        self.assertEqual(library_for_test.available_copies["Unique Book"], 5)

        # Clean up the test files after the test
        for file in [temp_books_file, temp_available_books_file, temp_loaned_books_file]:
            os.remove(file)

    def test_remove_book(self):
        result = self.library.remove_book("Book A")
        self.assertEqual(result, "book 'Book A' removed successfully")
        self.assertNotIn("Book A", [book.title for book in self.library.books])

    def test_popular_books(self):
        self.library.borrow_book("Book A")
        self.library.borrow_book("Book A")
        self.library.borrow_book("Book B")
        popular_books = self.library.popular_books()
        self.assertEqual(len(popular_books), 3)
        self.assertEqual(popular_books[0]["title"], "Book A")  # Most popular

    def test_waiting_list_management(self):
        self.library.waiting_list_manager.add_to_waiting_list("Book A", "Author A", "Fiction", 2000, "Client 1", "client1@example.com", "123456789")
        waiting_list = self.library.waiting_list_manager.get_waiting_list_for_book("Book A")
        self.assertEqual(len(waiting_list), 1)

if __name__ == "__main__":
    unittest.main()
