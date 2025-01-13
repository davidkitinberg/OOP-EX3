# --- Book Management ---
"""
This class represents a simple book object for our library
"""
class Book:
    def __init__(self, title: str, author: str, is_loaned: bool, copies: int, genre: str, year: int):
        self.title = title
        self.author = author
        self.is_loaned = is_loaned
        self.copies = copies
        self.genre = genre
        self.year = year
