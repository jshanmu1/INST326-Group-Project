
# Jayraj's Class updated to reflect composition
# DataClean Class
class DataClean:
    """Represents a dataset cleaning tool for movie reviews and ratings.
    
    This class provides methods to clean review data, calculate average ratings,
    and generate summaries. It integrates multiple data-cleaning operations into
    one cohesive object.

    Example:
        >>> data = {
        ...     "reviews": ["Great movie!", None, "So-so.", "Great movie!", ""],
        ...     "ratings": [4.5, 3.0, 5.0, None, "bad", 4.0]
        ... }
        >>> cleaner = DataClean(data)
        >>> cleaner.clean_reviews()
        ['Great movie!', 'So-so.']
        >>> cleaner.average_rating()
        4.125
        >>> print(cleaner)
        Dataset with 2 cleaned reviews and average rating 4.12
    """

    def __init__(self, data: dict):
        """Initialize the DataClean instance.
        
        Args:
            data (dict): Dictionary containing at least 'reviews' and/or 'ratings' keys.
        
        Raises:
            TypeError: If data is not a dictionary.
            ValueError: If required keys are missing.
        """
        if not isinstance(data, dict):
            raise TypeError("Data must be provided as a dictionary.")
        if "reviews" not in data and "ratings" not in data:
            raise ValueError("Data must contain at least 'reviews' or 'ratings' keys.")
        
        self._data = data
        self.ReviewCleaner = ReviewCleaner()
        self.PlotSummarizer = PlotSummarizer()
        self.RatingAnalyzer = RatingAnalyzer()
        self.PositiveReviewDetector = PositiveReviewDetector()
        self._cleaned_reviews = None
        self._average_rating = None

    # ----- Properties -----
    @property
    def data(self):
        return self._data.copy()
    
    @property
    def cleaned_reviews(self):
        return self._cleaned_reviews

    @property
    def avg_rating(self):
        return self._average_rating

    # ----- Methods -----
    def clean_reviews(self):
        reviews = self._data.get("reviews", [])
        self._cleaned_reviews = self.ReviewCleaner.clean_review(reviews)
        return self._cleaned_reviews
    
    def average_rating(self):
        ratings = self._data.get("ratings", [])
        self._average_rating = self.RatingAnalyzer.average(ratings)
        return self._average_rating
    def summarize_plot(self, max_length=100):
        plot = self._data.get("plot", "")
        return self.PlotSummarizer.summarize(plot, max_length=max_length)
    
    def is_positive_review(self, review):
        return self.PositiveReviewDetector.is_positive(review)
    def summary(self):
        reviews = self._cleaned_reviews or []
        avg = self._average_rating if self._average_rating is not None else "N/A"
        return f"Cleaned {len(reviews)} reviews. Average rating: {avg}"

    # ----- String Representations -----
    def __str__(self):
        reviews_count = len(self._cleaned_reviews) if self._cleaned_reviews else 0
        avg = f"{self._average_rating:.2f}" if self._average_rating is not None else "N/A"
        return f"Dataset with {reviews_count} cleaned reviews and average rating {avg}"

    def __repr__(self):
        return f"DataClean(data={self._data!r})"
