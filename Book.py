# --- Book Management ---
class Book:
    def __init__(self, title: str, author: str, year: int, category: str, copies: int):
        self.title = title
        self.author = author
        self.year = year
        self.category = category
        self.copies = copies

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "category": self.category,
            "copies": self.copies
        }
    def getCopies(self):
        return self.copies

