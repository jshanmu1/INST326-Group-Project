# Jayraj's Class 
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
        self._cleaned_reviews = None
        self._average_rating = None

    # ----- Properties -----
    @property
    def data(self):
        """dict: Get a copy of the dataset."""
        return self._data.copy()
    
    @property
    def cleaned_reviews(self):
        """list | None: Returns the most recently cleaned reviews (if available)."""
        return self._cleaned_reviews

    @property
    def avg_rating(self):
        """float | None: Returns the last computed average rating."""
        return self._average_rating

    # ----- Methods -----
    def clean_reviews(self):
        """Cleans the review data by removing empty, duplicate, or invalid entries.
        
        Returns:
            list: A cleaned list of reviews.
        
        Raises:
            TypeError: If 'reviews' in data is not a list.
        """
        reviews = self._data.get("reviews", [])
        if not isinstance(reviews, list):
            raise TypeError("Expected 'reviews' to be a list.")
        
        cleaned = []
        seen = set()
        for rev in reviews:
            if rev in (None, "", 0, [], {}):
                continue
            if isinstance(rev, str) and rev not in seen:
                cleaned.append(rev)
                seen.add(rev)
        
        self._cleaned_reviews = cleaned
        return cleaned

    def average_rating(self):
        """Calculates the average rating from numeric values in the dataset.
        
        Returns:
            float: The average rating, or 0 if no valid ratings exist.
        
        Raises:
            TypeError: If 'ratings' in data is not a list.
        """
        ratings = self._data.get("ratings", [])
        if not isinstance(ratings, list):
            raise TypeError("Expected 'ratings' to be a list.")
        
        total = count = 0
        for rating in ratings:
            if isinstance(rating, (int, float)):
                total += rating
                count += 1
        
        self._average_rating = total / count if count > 0 else 0
        return self._average_rating

    def summary(self):
        """Generates a formatted summary of the cleaned data.
        
        Returns:
            str: Summary report including number of reviews and average rating.
        """
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
