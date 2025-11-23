#Pranavs Class
#UPDATED WITH COMPOSITION AND POLYMORPHISM.
from BaseReviewSystem import AbstractMovieReviewItem

class MovieReviewSystem(AbstractMovieReviewItem):
    """
    Represents a movie review processing system.

    This class loads reviews from a CSV file, cleans them using helper 
    functions, and generates movie recommendations based on review ratings.

    Demonstrates:
    - Inheritance from AbstractMovieReviewItem
    - Polymorphism through overridden methods
    - Composition by delegating tasks to external helper functions

    Example:
        >>> system = MovieReviewSystem("reviews.csv")
        >>> system.load_reviews()
        >>> system.clean_reviews()
        >>> system.recommend_movies()
    """

    def __init__(self, filepath: str):
        """Initialize the MovieReviewSystem with a CSV filepath.

        Args:
            filepath (str): Path to the CSV file containing movie reviews.

        Raises:
            ValueError: If the filepath is empty or not a string.
        """
        if not isinstance(filepath, str) or not filepath.strip():
            raise ValueError("File path must be a non-empty string.")

        self._filepath = filepath
        self._reviews = []
        self._cleaned_reviews = []


    @property
    def filepath(self):
        return self._filepath

    @property
    def reviews(self):
        return self._reviews

    @property
    def cleaned_reviews(self):
        return self._cleaned_reviews


    def load_reviews(self):
        """Loads reviews from the CSV file using composition."""
        from movie_library import load_movie_reviews

        self._reviews = load_movie_reviews(self._filepath)
        return self._reviews

    def clean_reviews(self):
        """Cleans reviews by removing duplicates and spoiler content."""
        from movie_library import remove_duplicate_data, remove_spoiler_reviews

        if not self._reviews:
            raise RuntimeError("No reviews loaded. Call load_reviews() first.")

        no_duplicates = remove_duplicate_data(self._reviews)
        self._cleaned_reviews = remove_spoiler_reviews(no_duplicates)
        return self._cleaned_reviews

    def recommend_movies(self):
        """Generates movie recommendations from cleaned reviews."""
        from movie_library import recommend_similar_movies

        if not self._cleaned_reviews:
            raise RuntimeError("No cleaned reviews available.")

        return recommend_similar_movies(self._cleaned_reviews)


    def summary(self):
        total = len(self._reviews)
        cleaned = len(self._cleaned_reviews)
        return f"Loaded {total} reviews, cleaned down to {cleaned}."

    def __str__(self):
        return f"MovieReviewSystem({len(self._cleaned_reviews)} cleaned reviews)"

    def __repr__(self):
        return f"MovieReviewSystem(filepath={self._filepath!r})"
