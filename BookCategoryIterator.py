"""
This class implements the iterator design pattern to efficiently navigate through the books by category
"""
class BookCategoryIterator:
    def __init__(self, books):
        self.books_by_category = {}
        for book in books:
            genre = book.genre
            if genre not in self.books_by_category:
                self.books_by_category[genre] = []
            self.books_by_category[genre].append(book)
        self.category_iter = iter(sorted(self.books_by_category.items()))
        self.current_category = None
        self.book_iter = iter([])

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self.book_iter)
        except StopIteration:
            self.current_category, books = next(self.category_iter)
            self.book_iter = iter(books)
            return self.current_category