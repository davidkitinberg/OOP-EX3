# Strategy Pattern for Search
from abc import ABC, abstractmethod
from typing import List
from Book import Book
"""
This class implements the strategy design pattern. 
"""
class SearchStrategy(ABC):
    @abstractmethod
    def search(self, books: List[Book], query: str) -> List[Book]:
        pass

    @abstractmethod
    def suggest(self, books: List[Book], query: str) -> List[str]:
        """Provide suggestions based on the query."""
        pass

class SearchByTitle(SearchStrategy):
    def search(self, books: List[Book], query: str) -> List[Book]:
        return [book for book in books if query.lower() in book.title.lower()]

    def suggest(self, books: List[Book], query: str) -> List[str]:
        return [book.title for book in books if query.lower() in book.title.lower()]

class SearchByAuthor(SearchStrategy):
    def search(self, books: List[Book], query: str) -> List[Book]:
        return [book for book in books if query.lower() in book.author.lower()]

    def suggest(self, books: List[Book], query: str) -> List[str]:
        return [book.author for book in books if query.lower() in book.author.lower()]

class SearchByCategory(SearchStrategy):
    def search(self, books: List[Book], query: str) -> List[Book]:
        return [book for book in books if query.lower() in book.genre.lower()]

    def suggest(self, books: List[Book], query: str) -> List[str]:
        return [book.genre for book in books if query.lower() in book.genre.lower()]
