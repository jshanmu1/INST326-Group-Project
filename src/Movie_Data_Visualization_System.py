"""
Project 2: Movie Data Visualization System 
Author: Emilio Sanchez San Martin
Functions: plot_top_movies, plot_genre_popularity, plot_rating_distribution, plot_review_activity_over_time
Class: MovieVisualizer
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class MovieVisualizer:
    """
    Represents a visualization system for movie datasets (2010–2025).

    This class handles different types of charts of movie data with csv files to analyze movie popularity, ratings, and release trends.

    Methods:
        - plot_top_movies(): shows top-rated movies
        - plot_genre_popularity(): shows average rating per genre
        - plot_rating_distribution(): shows distribution of movie ratings
        - plot_review_activity_over_time(): shows movies released per year, filtered by genre
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize the MovieVisualizer with a dataset.

        Args:
            df (pd.DataFrame): The DataFrame containing movie data.

        Raises:
            ValueError: If the DataFrame is empty or missing key columns.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame.")
        if df.empty:
            raise ValueError("DataFrame cannot be empty.")
        required_cols = {'title', 'vote_average', 'genres', 'release_date'}
        if not required_cols.issubset(df.columns):
            raise ValueError(f"DataFrame missing required columns: {required_cols - set(df.columns)}")

        self._df = df.copy()

    @property
    def df(self) -> pd.DataFrame:
        """Return a copy of the dataset."""
        return self._df.copy()

    # 1️⃣ Top Movies
    def plot_top_movies(self, top_n: int = 10) -> None:
        """Display a bar chart of the top-rated movies."""
        top_movies = self._df.sort_values(by='vote_average', ascending=False).head(top_n)
        plt.figure(figsize=(10, 6))
        plt.barh(top_movies['title'], top_movies['vote_average'], color='skyblue')
        plt.gca().invert_yaxis()
        plt.title(f"Top {top_n} Movies by Average Rating")
        plt.xlabel("Average Rating (vote_average)")
        plt.ylabel("Movie Title")
        plt.show()

    # 2️⃣ Genre Popularity
    def plot_genre_popularity(self) -> None:
        """Display a bar chart showing average rating per genre."""
        genre_split = self._df.assign(genres=self._df['genres'].str.split(', ')).explode('genres')
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

    # 3️⃣ Rating Distribution
    def plot_rating_distribution(self) -> None:
        """Display a histogram of movie rating distribution."""
        plt.figure(figsize=(8, 5))
        plt.hist(self._df['vote_average'], bins=20, color='lightgreen', edgecolor='black')
        plt.title("Distribution of Movie Ratings")
        plt.xlabel("Rating (vote_average)")
        plt.ylabel("Number of Movies")
        plt.grid(alpha=0.3)
        plt.show()

    # 4️⃣ Review Activity Over Time
    def plot_review_activity_over_time(self, genres: list[str] | None = None) -> None:
        """Display a line chart of movie releases per year, optionally filtered by genre."""
        df = self._df.copy()
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
        df['year'] = df['release_date'].dt.year

        genre_expanded = df.assign(genres=df['genres'].str.split(', ')).explode('genres')
        if genres:
            genre_expanded = genre_expanded[genre_expanded['genres'].isin(genres)]
            title_suffix = f" for Selected Genres: {', '.join(genres)}"
        else:
            title_suffix = " (All Genres)"

        yearly_counts = (
            genre_expanded.groupby(['year', 'genres'])
            .size()
            .reset_index(name='movie_count')
        )

        plt.figure(figsize=(12, 6))
        for genre in yearly_counts['genres'].unique():
            genre_data = yearly_counts[yearly_counts['genres'] == genre]
            plt.plot(genre_data['year'], genre_data['movie_count'], marker='o', label=genre)

        plt.title(f"Movies Released Per Year {title_suffix}")
        plt.xlabel("Year")
        plt.ylabel("Number of Movies Released")
        plt.legend(title="Genre", bbox_to_anchor=(1, 1), loc='upper left')
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.show()

    def __str__(self) -> str:
        return f"MovieVisualizer(df={len(self._df)} movies)"

    def __repr__(self) -> str:
        return f"MovieVisualizer(rows={len(self._df)})" 