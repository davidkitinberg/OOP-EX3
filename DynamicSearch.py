from typing import List
from Book import Book
from SearchStrategy import SearchByTitle, SearchByAuthor, SearchByCategory, SearchStrategy

"""
This class implements dynamic search which is helped by the searchStrategy class.
Its purpose is to implement the suggestions box of the relevant search type.
"""
class DynamicSearch:
    def __init__(self):
        # Map search types to their respective strategies
        self.strategy_map = {
            "title": SearchByTitle(),
            "author": SearchByAuthor(),
            "genre": SearchByCategory()
        }

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
