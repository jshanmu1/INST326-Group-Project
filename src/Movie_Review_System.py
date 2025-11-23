#Pranavs Class
#UPDATED WITH COMPOSITION AND POLYMORPHISM.
from BaseReviewSystem import AbstractMovieReviewItem

class MovieReviewSystem(AbstractMovieReviewItem):
    """
    Standard movie review processing system that loads reviews from a CSV,
    cleans them, and generates recommendations.
    """
    
    #These methods use external helper functions rather than
    # inheriting from multiple classes. MovieReviewSystem "has-a" relationship
    # with these utilities: it uses them to perform work.
    def __init__(self, filepath: str):
        if not isinstance(filepath, str) or not filepath.strip():
            raise ValueError("File path must be a non-empty string.")

        self._filepath = filepath
        self._reviews = []
        self._cleaned_reviews = []

    def load_reviews(self):
        """Load reviews using composition functions."""
        self._reviews = load_movie_reviews(self._filepath)
        return self._reviews

    def clean_reviews(self):
        """Remove duplicates and spoiler reviews."""
        if not self._reviews:
            raise RuntimeError("No reviews loaded")

        no_duplicates = remove_duplicate_data(self._reviews)
        self._cleaned_reviews = remove_spoiler_reviews(no_duplicates)
        return self._cleaned_reviews

    def recommend_movies(self):
        """Recommend movies using the base logic."""
        if not self._cleaned_reviews:
            raise RuntimeError("No cleaned reviews available")

        return recommend_similar_movies(self._cleaned_reviews)

    

# CriticMovieReviewSystem is a subclass of MovieReviewSystem which indicates inheritance as it does the same process but for critic reviews.
# It overrides clean_reviews() and recommend_movies() 
# It shows Polymorphism as the same method name called on base class reference behaves differently in subclass
class CriticMovieReviewSystem(MovieReviewSystem):
    """
    Specialized system where reviews come from critics.
    Extends MovieReviewSystem but changes behavior to reflect stricter rules.

    """

    def __init__(self, filepath, minimum_rating=7):
        super().__init__(filepath) # call parent method first
        self.minimum_rating = minimum_rating  

    def clean_reviews(self):
        """Critics system removes spoilers using parent logic AND removes low-rating reviews."""
        cleaned = super().clean_reviews()

        high_quality_only = []
        for review in cleaned:
            try:
                rating = float(review[1])
                if rating >= self.minimum_rating:
                    high_quality_only.append(review)
            except (ValueError, IndexError):
                continue 

        self._cleaned_reviews = high_quality_only
        return self._cleaned_reviews

    def recommend_movies(self):
        """
        Critic recommendations: return movies sorted by rating (high → low),
        not just all movies ≥ 4 stars.
        """
        if not self._cleaned_reviews:
            raise RuntimeError("No cleaned reviews available")

        sorted_reviews = sorted(
            self._cleaned_reviews,
            key=lambda r: float(r[1]),
            reverse=True
        )
        return sorted_reviews

    def __str__(self):
        return f"CriticMovieReviewSystem({len(self._cleaned_reviews)} high-quality reviews)"

    def __repr__(self):
        return f"CriticMovieReviewSystem(filepath={self._filepath!r}, minimum_rating={self.minimum_rating})"
