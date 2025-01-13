from Book import Book

"""
This class implements the book factory design pattern.
"""
class BookFactory:
    @staticmethod
    def create_book(title: str, author: str, is_loaned: bool, copies: int, genre: str, year: int) -> Book:
        return Book(title=title, author=author, is_loaned=is_loaned, copies=copies, genre=genre, year=year)
