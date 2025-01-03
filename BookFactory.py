from Book import Book


class BookFactory:
    @staticmethod
    def create_book(title, author, year, category, copies):
        return Book(title, author, year, category, copies)
