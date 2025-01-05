from typing import List
from Book import Book
from SearchStrategy import SearchByTitle, SearchByAuthor, SearchByCategory, SearchStrategy

class DynamicSearch:
    def __init__(self):
        # Map search types to their respective strategies
        self.strategy_map = {
            "title": SearchByTitle(),
            "author": SearchByAuthor(),
            "genre": SearchByCategory()
        }

    def search(self, search_type: str, books: List[Book], query: str) -> List[Book]:
        """
        Perform a search based on the specified search type and query.

        Args:
            search_type (str): The type of search ("title", "author", "genre").
            books (List[Book]): The list of books to search.
            query (str): The search query.

        Returns:
            List[Book]: The list of books matching the query.
        """
        strategy = self.strategy_map.get(search_type.lower())
        if not strategy:
            raise ValueError(f"Invalid search type: {search_type}")
        return strategy.search(books, query)

    def suggest(self, search_type: str, books: List[Book], query: str) -> List[str]:
        """
        Generate suggestions based on the specified search type and query.

        Args:
            search_type (str): The type of search ("title", "author", "genre").
            books (List[Book]): The list of books to suggest from.
            query (str): The search query.

        Returns:
            List[str]: Suggestions matching the query.
        """
        strategy = self.strategy_map.get(search_type.lower())
        if not strategy:
            raise ValueError(f"Invalid search type: {search_type}")
        return strategy.suggest(books, query)
