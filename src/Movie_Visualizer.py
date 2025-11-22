"""
Project 2: Movie Data Visualization System 
Author: Emilio Sanchez San Martin
Functions: plot_top_movies, plot_genre_popularity, plot_rating_distribution, plot_review_activity_over_time
Class: MovieVisualizer
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from base_visualizer import BaseVisualizer #New classes
from dataset import Dataset #New Classes


class MovieVisualizer(BaseVisualizer):
    """
    Visualizer that handles movie dataset plotting.
    Inherits from BaseVisualizer and implements plot_data().
    """

    def __init__(self, dataset: Dataset):
        super().__init__(dataset)

    # POLYMORPHIC METHOD (required by abstract class)
    def plot_data(self):
        """Default polymorphic behavior → plot top-rated movies."""
        self.plot_top_movies()

    # VISUALIZATION METHODS

    def plot_top_movies(self, top_n: int = 10) -> None:
        df = self.dataset.get_data()
        top_movies = df.sort_values(by='vote_average', ascending=False).head(top_n)

        plt.figure(figsize=(10, 6))
        plt.barh(top_movies['title'], top_movies['vote_average'])
        plt.gca().invert_yaxis()
        plt.title(f"Top {top_n} Movies by Average Rating")
        plt.xlabel("Average Rating (vote_average)")
        plt.ylabel("Movie Title")
        plt.show()

    def plot_genre_popularity(self) -> None:
        df = self.dataset.get_data()
        genre_split = df.assign(genres=df['genres'].str.split(', ')).explode('genres')

        genre_stats = (
            genre_split.groupby('genres')['vote_average']
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )

        plt.figure(figsize=(12, 6))
        sns.barplot(data=genre_stats, x='genres', y='vote_average')
        plt.xticks(rotation=45, ha='right')
        plt.title("Average Rating by Genre")
        plt.xlabel("Genre")
        plt.ylabel("Average Rating")
        plt.show()

    def plot_rating_distribution(self) -> None:
        df = self.dataset.get_data()

        plt.figure(figsize=(8, 5))
        plt.hist(df['vote_average'], bins=20, edgecolor='black')
        plt.title("Distribution of Movie Ratings")
        plt.xlabel("Rating (vote_average)")
        plt.ylabel("Number of Movies")
        plt.grid(alpha=0.3)
        plt.show()

    def plot_review_activity_over_time(self, genres: list[str] | None = None) -> None:
        df = self.dataset.get_data()
        df['release_date'] = pd.to_datetime(df['release_date'], errors='ignore')
        df['year'] = df['release_date'].dt.year

        genre_expanded = df.assign(genres=df['genres'].str.split(', ')).explode('genres')

        if genres:
            genre_expanded = genre_expanded[genre_expanded['genres'].isin(genres)]
            title_suffix = f" for Genres: {', '.join(genres)}"
        else:
            title_suffix = " (All Genres)"

        yearly_counts = (
            genre_expanded.groupby(['year', 'genres'])
            .size()
            .reset_index(name='movie_count')
        )

        plt.figure(figsize=(12, 6))
        for genre in yearly_counts['genres'].unique():
            data = yearly_counts[yearly_counts['genres'] == genre]
            plt.plot(data['year'], data['movie_count'], marker='o', label=genre)

        plt.title(f"Movies Released Per Year {title_suffix}")
        plt.xlabel("Year")
        plt.ylabel("Number of Movies Released")
        plt.legend(title="Genre", bbox_to_anchor=(1, 1), loc='upper left')
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.show()

    def __repr__(self) -> str:
        return f"MovieVisualizer({len(self.dataset.get_data())} movies)"
