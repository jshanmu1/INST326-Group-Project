#Pranavs Class
#UPDATED WITH COMPOSITION AND POLYMORPHISM.
from BaseReviewSystem import AbstractMovieReviewItem

class MovieReviewSystem(AbstractMovieReviewItem):
    """
    Loads, cleans, and recommends movies from a CSV of reviews.
    Inherits from AbstractMovieReviewItem to enforce required behaviors.

    POLYMORPHISM:
        Implements the abstract methods in different ways than other subclasses might.

    COMPOSITION:
        Uses helper functions from project1_functions rather than inheritance.
    """

    def __init__(self, filepath):
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
        """Loads raw movie reviews from CSV (COMPOSITION)."""
        from project1_functions import load_movie_reviews
        self._reviews = load_movie_reviews(self._filepath)
        return self._reviews

    def clean_reviews(self):
        """Clean duplicate/spoiler reviews using helper functions."""
        from project1_functions import remove_duplicate_data, remove_spoiler_reviews

        if not self._reviews:
            raise RuntimeError("No reviews loaded.")

        no_dupes = remove_duplicate_data(self._reviews)
        self._cleaned_reviews = remove_spoiler_reviews(no_dupes)
        return self._cleaned_reviews

    def recommend_movies(self):
        """Return movie recommendations using cleaned reviews."""
        from project1_functions import recommend_similar_movies

        if not self._cleaned_reviews:
            raise RuntimeError("No cleaned reviews available.")

        return recommend_similar_movies(self._cleaned_reviews)


    def __str__(self):
        total = len(self._reviews)
        cleaned = len(self._cleaned_reviews)
        return f"MovieReviewSystem: {cleaned}/{total} reviews cleaned."

    def __repr__(self):
        return f"MovieReviewSystem(filepath='{self._filepath}')"
