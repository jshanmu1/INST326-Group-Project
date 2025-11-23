from abc import ABC, abstractmethod

class AbstractMovieReviewItem(ABC):
    """
    Abstract interface for movie review processors.
    Enforces required methods for loading, cleaning, and summarizing review data.
    """

    @abstractmethod
    def load_reviews(self):
        pass

    @abstractmethod
    def clean_reviews(self):
        pass

    @abstractmethod
    def recommend_movies(self):
        pass
