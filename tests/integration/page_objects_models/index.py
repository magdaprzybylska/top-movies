from bs4 import BeautifulSoup
from typing import List


class IndexPageObject:
    """Page object representation of the first view."""

    def __init__(self, html: str):
        """
        Initializes the IndexPageObject with HTML content.

        Parameters:
        - html (str): The HTML content of the page.
        """
        self.soup = BeautifulSoup(html, "html.parser")

    @property
    def movie_cards(self) -> List["MovieCard"]:
        """
        Extracts and returns a list of MovieCard objects from the page.
        """
        return [MovieCard(card) for card in self.soup.find_all("div", class_="card")]

    def get_top_10_titles(self) -> List[str]:
        """
        Retrieves and returns the titles of the top 10 movies from the page.
        """
        return [movie_card.title for movie_card in self.movie_cards]


class MovieCard:
    """
    Represents a movie card element on the page.
    """

    def __init__(self, card_element):
        """
        Initializes the MovieCard with a card element.

        Parameters:
        - card_element: The BeautifulSoup element representing a movie card.
        """
        self.card_element = card_element

    @property
    def title(self) -> str:
        """
        Extracts and returns the title of the movie from the card.

        Returns:
        - str: Title of the movie.
        """
        return (
            self.card_element.find("div", class_="title")
            .find(text=True, recursive=False)
            .strip()
        )

    @property
    def description(self) -> str:
        """
        Extracts and returns the description of the movie from the card.

        Returns:
        - str: Description of the movie.
        """
        return self.card_element.find("p", class_="description").text.strip()
