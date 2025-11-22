# Jayraj Class updated to reflect composition
#clean reviews
# I updated the class name to ReviewCleaner to reflect composition 
class ReviewCleaner:
     """ cleans a list of movie reviews by removing missing data and duplicates, and reviews that are not specific

This function iterates through the provided list of reviews and performs
    two main cleaning operations:
    1. Removes any review entries that are considered incomplete (e.g., None, "", 0, or empty lists/dicts).
    2. Removes duplicate review strings, keeping the first occurrence.

Args:
reviews_list(list): List of raw movie reviews / potential mixed data types

Returns:
list: A cleaned list of movie reviews.

Raises:
   TypeError: If the input 'reviews' is not a list.

Example:
movie_reviews = ["Great movie!", None, "So-so.", "Great movie!", ""]
clean_review(movie_reviews)
# Output: ['Great movie!', 'So-so.']
"""
def clean_review(review):
    if not isinstance(review, list):
        raise TypeError("Input must be a list.")

    cleaned_reviews = []
    seen_reviews = set()

    for rev in review:

        if rev in (None, "", 0, [], {}):
            continue


        if isinstance(rev, str) and rev not in seen_reviews:
            cleaned_reviews.append(rev)
            seen_reviews.add(rev)

    return cleaned_reviews
     
#summarize_plot
# Jayraj Class PlotSummarizer updated to reflect composition
class PlotSummarizer:
    
    """Summarizes a movie plot to a specified maximum length.

    This function takes a movie plot as input and truncates it to the specified
    maximum length, appending an ellipsis ("...") if the plot exceeds that length.

    Args:
        plot (str): The original movie plot.
        max_length (int): The maximum length of the summarized plot. Default is 100 characters.

    Returns:
        str: The summarized movie plot.

    Raises:
        TypeError: If 'plot' is not a string or 'max_length' is not an integer.
        ValueError: If 'max_length' is less than or equal to 0.

    Example:
        original_plot = "In a world where technology has advanced beyond imagination, a young hero rises to challenge the status quo and bring balance to society."
        summarized_plot = summarize_plot(original_plot, max_length=50)
        print(summarized_plot)
        # Output: "In a world where technology has advanced beyo..."
    """
    def summarize(self, plot, max_length=100):
        if not isinstance(plot, str):
            raise TypeError("Plot must be a string.")
        if not isinstance(max_length, int):
            raise TypeError("Max length must be an integer.")
        if max_length <= 0:
            raise ValueError("Max length must be greater than 0.")

        return plot[:max_length - 3] + "..." if len(plot) > max_length else plot
     
#Jayraj Class RatingAnalyzer updated to reflect composition
#average_rating
class RatingAnalyzer:
    """Calculates the average rating from a list of ratings.

    This function takes a list of numerical ratings and computes the average.
    It ignores any non-numeric values in the list.

    Args:
        ratings (list): A list of numerical ratings (int or float).

    Returns:
        float: The average rating, or 0 if there are no valid ratings.

    Raises:
        TypeError: If 'ratings' is not a list.

    Example:
        movie_ratings = [4.5, 3.0, 5.0, None, "bad", 4.0]
        avg_rating = average_rating(movie_ratings)
        print(avg_rating)
        # Output: 4.125
    """
    def average(self, ratings):
        if not isinstance(ratings, list):
            raise TypeError("Input must be a list.")

        total = count = 0

        for rating in ratings:
            if isinstance(rating, (int, float)):
                total += rating
                count += 1

        return total / count if count > 0 else 0
     
#Jayraj Function
#is_positive
class PositiveReviewDetector:
    """Determines if a movie review is positive based on the presence of positive keywords.

    This function checks if the review contains any of the predefined positive keywords.
    If any positive keyword is found, the review is considered positive.

    Args:
        review (str): The movie review text.
        """
    positive_keywords = {"good", "great", "excellent", "amazing", "fantastic", "love", "wonderful", "best", "awesome", "positive"}
    def is_positive(self, review):
        if not isinstance(review, str):
            raise TypeError("Review must be a string.")

        text = review.lower()
        return any(word in text for word in self.POSITIVE_WORDS)

# (All commits are found on our Colab document)

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


