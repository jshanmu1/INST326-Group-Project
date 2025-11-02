#Pranavs Class
class MovieReviewSystem:
    """
    A class that basically makes a new set of reviews after removing duplicates and taking out spoiler reviews
    making a set of reviews that are accurate and allows for proper ratings.

    Example:
        >>> system = MovieReviewSystem("reviews.csv")
        >>> system.load_reviews()
        >>> system.clean_reviews()
        >>> system.recommend_movies()
        [['Avengers', 5], ['Space Jam', 4], ['Grownups', 5]]
    """

    def __init__(self, filepath):
        """
        Sets up the MovieReviewSystem with a path to the reviews CSV file.

        Args:
            filepath (str): The path to the CSV file.

        Raises:
            ValueError: If the file path is empty or not a string.
        """
        if not isinstance(filepath, str) or not filepath.strip():
            raise ValueError("File path must be a non-empty string.")

        self._filepath = filepath
        self._reviews = []
        self._cleaned_reviews = []

    @property
    def filepath(self):
        """Returns the path to the movie reviews file."""
        return self._filepath

    @property
    def reviews(self):
        """Returns the list of loaded movie reviews."""
        return self._reviews

    @property
    def cleaned_reviews(self):
        """Returns a clean list of movie reviews."""
        return self._cleaned_reviews

    def load_reviews(self):
        """
        Loads movie reviews from the CSV file using the `load_movie_reviews` function.

        Returns:
            list: A list of reviews loaded from the file.
        """
        from project1_functions import load_movie_reviews
        self._reviews = load_movie_reviews(self._filepath)
        return self._reviews

    def clean_reviews(self):
        """
        Cleans movie reviews by removing duplicates and spoiler reviews.

        Uses:
            - `remove_duplicate_data()`
            - `remove_spoiler_reviews()`

        Returns:
            list: A cleaned list of movie reviews.

        Raises:
            RuntimeError: If no reviews have been loaded.
        """
        from project1_functions import remove_duplicate_data, remove_spoiler_reviews

        if not self._reviews:
            raise RuntimeError("No reviews loaded. Please load reviews first.")

        no_duplicates = remove_duplicate_data(self._reviews)
        self._cleaned_reviews = remove_spoiler_reviews(no_duplicates)
        return self._cleaned_reviews

    def recommend_movies(self):
        """
        Recommends movies based on high ratings using the `recommend_similar_movies` function.

        Returns:
            list: A list of recommended movies.

        Raises:
            RuntimeError: If cleaned reviews are not available.
        """
        from project1_functions import recommend_similar_movies

        if not self._cleaned_reviews:
            raise RuntimeError("No cleaned reviews available. Please clean reviews first.")

        return recommend_similar_movies(self._cleaned_reviews)

    
    def __str__(self):
        """Returns a summary of the review data."""
        total = len(self._reviews)
        cleaned = len(self._cleaned_reviews)
        return f"MovieReviewSystem: {cleaned}/{total} reviews cleaned."

    def __repr__(self):
        """Returns a representation of the class instance."""
        return f"MovieReviewSystem(filepath='{self._filepath}')"

