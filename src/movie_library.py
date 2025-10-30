# (All commits are found on our Colab document) # As well as the tmdb_functions.py file
#### Jayden Williams Functions
import csv

def load_db(path):
    """
    Load and filter TMDB movies from a CSV file (Started with api keys in mind but we're filtering csv files to be more specific).

    Keeps only rows from years 2010 to 2025 with vote counter being >= 1,

    Args:
        path (str): Path to the CSV file.

    Returns:
        list: Filtered rows as dictionaries.

    Raises:
        TypeError: If path is not a string.
        FileNotFoundError: If the file does not exist.
    """
    if not isinstance(path, str):
        raise TypeError("path must be a string")

    rows = []
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            year = None
            if "release_year" in row and row["release_year"]:
                try:
                    year = int(row["release_year"])
                except ValueError:
                    year = None
            if year is None and "release_date" in row and row["release_date"]:
                d = row["release_date"]
                if len(d) >= 4 and d[:4].isdigit():
                    year = int(d[:4])

            try:
                votes = int(row.get("vote_count", "0"))   #Vount Count Getter 
            except ValueError:
                votes = 0

            if year is not None and 2010 <= year <= 2025 and votes >= 1:
                rows.append(row)

    return rows

#Second function
def fetch_tmdb_movie_reviews(title, movie_rows):
    """
    Create a reviews list from the CSV rows per the movie title.

    Uses the movie overview as the review text and vote_average as the rating.

    Args:
        title (str): Movie title to match (case-insensitive).
        movie_rows (list): Rows returned by load_db().

    Returns:
        List of dicts: {"author": "TMDB users", "content": <overview>, "author_details": {"rating": <float or None>}}

    Raises:
        TypeError: If the inputs are invalid types.
    """
    if not isinstance(title, str):
        raise TypeError("title must be a string")
    if not isinstance(movie_rows, list):
        raise TypeError("movie_rows must be a list")

    found = []
    q = title.strip().lower()

    for row in movie_rows:
        row_title = (row.get("title") or row.get("original_title") or "").strip()
        if not row_title:
            continue
        name = row_title.lower()

        if name == q or q in name:
            overview = (row.get("overview") or "").strip()
            rating = None
            va = row.get("vote_average")
            if va not in (None, ""):
                try:
                    rating = float(va)
                except ValueError:
                    rating = None
            found.append({
                "author": "TMDB users",
                "content": overview,
                "author_details": {"rating": rating}
            })

    return found


#Third function 
def normalize_tmdb_reviews(reviews):
    """
    Convert review dicts into list form

    Input:  [{"author": "...", "content": "...", "author_details": {"rating": X}}, ...]
    Output: [["TMDB users", "some text", X], ...]

    Args:
        reviews (list): List of review dicts.

    Returns:
        list: [author, content, rating]

    Raises:
        TypeError: If reviews is not a list.
    """
    if not isinstance(reviews, list):
        raise TypeError("reviews must be a type of list")

    clean = []
    for item in reviews:
        if not isinstance(item, dict):
            continue
        author = item.get("author", "TMDB users")
        content = (item.get("content", "")).strip()
        details = item.get("author_details", {})
        rating = None
        if isinstance(details, dict):
            rating = details.get("rating", None)
        clean.append([author, content, rating])

    return clean


#Fourth function 
def export_reviews_to_csv(reviews, filename):
    """
    Save reviews to a CSV file with columns.

    Args:
        reviews (list): [author, content, rating].
        filename (str): Output CSV path.
        
    Returns:
        None
        
    Raises:
        TypeError: If inputs are wrong types.
        ValueError: If reviews is empty.
    """
    if not isinstance(reviews, list):
        raise TypeError("reviews must be in a list")
    if not isinstance(filename, str):
        raise TypeError("filename must be a string")
    if len(reviews) == 0:
        raise ValueError("no reviews to export")

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Author", "Content", "Rating"])
        for row in reviews:
            if isinstance(row, (list, tuple)) and len(row) >= 3:
                writer.writerow([row[0], row[1], row[2]])

###################################################################

# Emilio Sanchez San Martin Functions

# plot_top_movies()
# I will need to use pandas library in order to create the functions fo visualization
import pandas as pd
import matplotlib.pyplot as plt

def plot_top_movies(df, top_n=10):
  """
  Plotting the first top movies (how ever much you'd like to see) based on average ratings

  Args:
    df (pandas.DataFrame): The DataFrame containing movie data.
    top_movies (int): The number of top movies to plot.

  Returns:
    None: Show's a bar chat of the rop rated movies

  Raises:
    ValueError: if the data is showing NA's or missing values

  Example:
    plot_top_movies(df, top_n=)

  """
  if df.empty:
    raise ValueError("DataFrame is empty. No data to plot.")
  if not {'title', 'vote_average'}.issubset(df.columns):
    raise ValueError("DataFrame must have 'title' and 'average_rating' columns.")

  top_movies = df.sort_values(by='vote_average', ascending=False).head(top_n)
    plt.figure(figsize=(10, 6))
    plt.barh(top_movies['title'], top_movies['vote_average'], color='skyblue')
    plt.gca().invert_yaxis()
    plt.title(f"Top {top_n} Movies by Average Rating")
    plt.xlabel("Average Rating (vote_average)")
    plt.ylabel("Movie Title")
    plt.show() # Had to use Gemini AI to understand how to work with Matplot.lib (plt) to make visualizations

     

# Emilio Sanchez San Martin Functions

# plot_genre_popularity()
import seaborn as sns

def plot_genre_popularity(df):
  """
  Plotting average rating per genre to find which genres do best!

  Args:
    df (pd.DataFrame): The DataFrame containing variables 'genres' and 'vote_average'.

  Returns:
    None: Show's a bar chat of average rating by genre

  Example:
    plot_genre_popularity(df)

  """
  if 'genres' not in df.columns or 'vote_average' not in df.columns:
    raise ValueError("DataFrame must have 'genres' and 'vote_average' columns.")

  # Splitting genres (since there are multiple per movie)
  genre_split = df.assign(genres=df['genres'].str.split(', ')).explode('genres')

  genre_stats = (
      genre_split.groupby('genres')['vote_average']
      .mean()
      .sort_values(ascending=False)
      .reset_index()
  )

  plt.figure(figsize=(12, 6))
  sns.barplot(data=genre_stats, x='genres', y='vote_average', palette='coolwarm')
  plt.xticks(rotation=45, ha='right')
  plt.title("Average Rating by Genre")
  plt.xlabel("Genre")
  plt.ylabel("Average Rating")
  plt.show()

     

# Emilio Sanchez San Martin Functions

def plot_rating_distribution(df):
  """
  Histogram showing the distribution of movie ratings.

  Args:
     df (pd.DataFrame): Dataset with the 'vote_average' column.

  Returns:
      None: Displays a histogram.

  Example:
  plot_rating_distribution(df)
  """
  if 'vote_average' not in df.columns:
    raise ValueError("DataFrame must have 'vote_average' column.")

  plt.figure(figsize=(8, 5))
  plt.hist(df['vote_average'], bins=20, color='lightgreen', edgecolor='black')
  plt.title("Distribution of Movie Ratings")
  plt.xlabel("Rating (vote_average)")
  plt.ylabel("Number of Movies")
  plt.grid(alpha=0.3)
  plt.show()
     

# Emilio Sanchez San Martin Functions

import pandas as pd
import matplotlib.pyplot as plt

def plot_review_activity_over_time (df, genres=None):

  """
  Plotting the # of movies realeased per year, which allows you to
  filter by specific genres

  This visualization helps analyze which genres had the most movie
  releases over time and how production trends evolved between 2010 and 2025.

  Args:
    df (pd.DataFrame): TMDB movie dataset containing 'release_date' and 'genres' columns.
    genres (list[str], optional): A list of genre names to filter by. (If None, includes all genres).

  Returns:
    None: A line chart comparing movie release trends per genre.

  Raises:
    ValueError: If required columns ('release_date', 'genres') are missing.

  Example:
    plot_review_activity_over_time(df)
    plot_review_activity_over_time(df, genres=['Action', 'Comedy', 'Drama'])

  """
  # Validating columns
  required_cols = {'release_date', 'genres'}
  if not required_cols.issubset(df.columns):
      raise ValueError(f"Missing required columns: {required_cols - set(df.columns)}")

  # Parse release dates
  df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
  df['year'] = df['release_date'].dt.year

  # Expand genres (some rows have multiple genres separated by commas)
  genre_expanded = df.assign(genres=df['genres'].str.split(', ')).explode('genres')

  # Filter by specific genres if provided
  if genres:
      genre_expanded = genre_expanded[genre_expanded['genres'].isin(genres)]
      title_suffix = f" for Selected Genres: {', '.join(genres)}"
  else:
      title_suffix = " (All Genres)"

  # Count movies released per year per genre
  yearly_genre_counts = (
      genre_expanded.groupby(['year', 'genres'])
      .size()
      .reset_index(name='movie_count')
  )

  plt.figure(figsize=(12, 6))

  # Plot each genre separately
  for genre in yearly_genre_counts['genres'].unique():
      genre_data = yearly_genre_counts[yearly_genre_counts['genres'] == genre]
      plt.plot(genre_data['year'], genre_data['movie_count'], marker='o', label=genre)

  plt.title(f"Movies Released Per Year {title_suffix}")
  plt.xlabel("Year")
  plt.ylabel("Number of Movies Released")
  plt.legend(title="Genre", bbox_to_anchor=(1.05, 1), loc='upper left')
  plt.grid(alpha=0.3)
  plt.tight_layout()
  plt.show()

###################################################################

#load_movie_reviews- Pranav Rishi
def load_movie_reviews(filepath):
    """
    Loads movie reviews from a CSV file.

    Args:
        filepath: The path to the CSV file.

    Returns:
        A list of rows from the CSV file, each row as a list [review, rating].
    """
    reviews = []
    with open(filepath, 'r') as file:
        for line in file:
            reviews.append(line.strip().split(','))
    return reviews

#remove_duplicate_data- Pranav Rishi
def remove_duplicate_data(reviews):
    """
    Removes duplicate reviews from a list of reviews.

    This function removes any duplicates within the data, making a new list
    without any duplicate entries.

    Args:
        reviews (list): A list of reviews, where each review can be any data type.

    Returns:
        list: A new list with duplicate reviews removed.

    Raises:
        TypeError: If 'reviews' is not a list.
    """
    if not isinstance(reviews, list):
        raise TypeError("Reviews must be a list.")

    unique_reviews = []
    for review in reviews:
        if review not in unique_reviews:
            unique_reviews.append(review)
    return unique_reviews
     

#remove_spoiler_reviews()- Pranav Rishi
def remove_spoiler_reviews(reviews):
    """
    Removes movie reviews that contain spoilers from the list.

    This function checks each review for the word spoiler
    and removes any review that contains the word in it.

    Args:
        reviews (list): A list of reviews, where each review is a list.


    Returns:
        list: A new list of reviews with all spoiler reviews removed.

    Raises:
        TypeError: If 'reviews' is not a list.

    Example:
        reviews = [
            ["Loved the movie!!", 5],
            ["Spoiler! lebron dies", 3],
            ["Amazing plot twist", 5]
        ]
        unspoiled_reviews = remove_spoiler_reviews(reviews)
        print(unspoiled_reviews)
        # Output: [['Loved the movie!!', 5], ['Amazing plot twist', 5]]
    """
    if not isinstance(reviews, list):
        raise TypeError("Reviews must be a list.")

    unspoiled_reviews = []
    for review in reviews:
        if "spoiler" not in review[0].lower():
            unspoiled_reviews.append(review)
    return unspoiled_reviews
     

#recommend_similar_movies()-Pranav Rishi
def recommend_similar_movies(reviews):
    """
    Recommends movies based on previous high ratings.

    This function looks at the user's rated movies and recommends other movies
    that have similar high ratings.

    Args:
        reviews (list): A list of reviews, where each review is a list

    Returns:
        list: A list of recommended movies with high ratings.

    Raises:
        TypeError: If 'reviews' is not a list.

    Example:
        reviews = [
            ["Avengers", 5],
            ["Space Jam", 4],
            ["Scream", 2],
            ["Grownups", 5]
        ]
        recommendations = recommend_similar_movies(reviews)
        print(recommendations)
        # Output: [['Avengers', 5], ['Space Jam', 4], ['Grown Ups', 5]]
    """
    if not isinstance(reviews, list):
        raise TypeError("Reviews must be a list.")

    recommended = []
    for review in reviews:
        if len(review) == 2:
            title, rating = review
            if isinstance(rating, (int, float)) and rating >= 4:
                recommended.append(review)

    return recommended

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


###################################################################
# Jayraj Function
#clean reviews
def clean_review(review):
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
     
# Jayraj Function
#summarize_plot
def summarize_plot(plot, max_length=100):
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
    if not isinstance(plot, str):
        raise TypeError("Plot must be a string.")
    if not isinstance(max_length, int):
        raise TypeError("Max length must be an integer.")
    if max_length <= 0:
        raise ValueError("Max length must be greater than 0.")

    if len(plot) > max_length:
        return plot[:max_length - 3] + "..."
    return plot
     
#Jayraj Function
#average_rating
def average_rating(ratings):
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
    if not isinstance(ratings, list):
        raise TypeError("Input must be a list.")

    total = 0
    count = 0

    for rating in ratings:
        if isinstance(rating, (int, float)):
            total += rating
            count += 1

    return total / count if count > 0 else 0
     
#Jayraj Function
#is_positive
def is_positive(review):
    """Determines if a movie review is positive based on the presence of positive keywords.

    This function checks if the review contains any of the predefined positive keywords.
    If any positive keyword is found, the review is considered positive.

    Args:
        review (str): The movie review text.
        """
    positive_keywords = {"good", "great", "excellent", "amazing", "fantastic", "love", "wonderful", "best", "awesome", "positive"}

    if not isinstance(review, str):
        raise TypeError("Review must be a string.")

    review_lower = review.lower()

    for keyword in positive_keywords:
        if keyword in review_lower:
            return True
    return False

# (All commits are found on our Colab document)

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

