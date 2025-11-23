#Pranavs Class
#UPDATED WITH COMPOSITION AND POLYMORPHISM.
from BaseReviewSystem import AbstractMovieReviewItem

class MovieReviewSystem(AbstractMovieReviewItem):
    """
    Loads, cleans, and recommends movies from a CSV of reviews.
    Inherits from AbstractMovieReviewItem to fulfill interface requirements.

    POLYMORPHISM:
    This class implements the abstract methods defined in
    AbstractMovieReviewItem. Any other subclass could implement 
    those same methods differently, but they would all share a common interface.
    """

    def __init__(self, filepath):
        if not isinstance(filepath, str) or not filepath.strip():
            raise ValueError("File path must be a non-empty string.")

        self._filepath = filepath

        # COMPOSITION:
        # These lists store the raw and cleaned review data.
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
        # COMPOSITION:
        # MovieReviewSystem gives work to helper functions.
        from project1_functions import load_movie_reviews
        self._reviews = load_movie_reviews(self._filepath)
        return self._reviews

    def clean_reviews(self):
        from project1_functions import remove_duplicate_data, remove_spoiler_reviews

        if not self._reviews:
            raise RuntimeError("No reviews loaded.")

        # COMPOSITION continues here as it is using external helper functions.
        no_duplicates = remove_duplicate_data(self._reviews)
        self._cleaned_reviews = remove_spoiler_reviews(no_duplicates)
        return self._cleaned_reviews

    def recommend_movies(self):
        from project1_functions import recommend_similar_movies

        if not self._cleaned_reviews:
            raise RuntimeError("No cleaned reviews available.")

        # COMPOSITION again as it is using an external recommendation function.
        return recommend_similar_movies(self._cleaned_reviews)

    # POLYMORPHISM:
    # __str__ and __repr__ override the base object implementations,
    # giving MovieReviewSystem a custom string representation.
    def __str__(self):
        total = len(self._reviews)
        cleaned = len(self._cleaned_reviews)
        return f"MovieReviewSystem: {cleaned}/{total} reviews cleaned."

    def __repr__(self):
        return f"MovieReviewSystem(filepath='{self._filepath}')"
