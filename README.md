Research Data Pipeline Project — Data Transformers
Course: INST326: Object-Oriented Programming for Information Science — Section 0201
Team: Data Transformers
Date: September 11, 2025
1. Project Title & Short Description
Movie Review Data Pipeline & Visualization
A modular Python function library that ingests large movie datasets (TMDB CSV), cleans and normalizes ratings and reviews, performs data transformations, and produces visual reports and visualizations (top-rated movies, genre popularity, rating distributions, and trends over time).
The system emphasizes object-oriented principles such as inheritance, polymorphism, abstract base classes (ABCs), and composition for maintainable and extensible design.
2. Team Members & Roles
Member	Role	Responsibility
Pranav Rishi	Data Ingestion & Duplicate/Spoiler Filtering	load_movie_reviews(), remove_duplicate_data(), remove_spoiler_reviews(), recommend_similar_movies()
Jayraj Shanmugam	Text & Rating Cleaning & Summarization	clean_reviews(), summarize_plot(), average_rating(), is_positive()
Jayden Williams	Data I/O & Normalization	load_movie_dataset(), normalize_tmdb_reviews(), export_reviews_to_csv()
Emilio Sanchez San Martin	Visualization & Reporting	plot_top_movies(), plot_genre_popularity(), plot_rating_distribution(), plot_review_activity_over_time()
3. Domain Focus & Problem Statement
Domain: Research Data Management & Information Science (movie metadata & reviews)
Problem:
Movie review datasets can be large and messy, with duplicates, missing values, or confusing data. This makes analysis and visualization difficult.
Solution:
We created a reproducible pipeline that:
Loads datasets from CSV or in-memory sources
Cleans and normalizes reviews and ratings
Summarizes plots and detects sentiment
Provides visualizations for top-rated movies, genre popularity, and release trends
The pipeline uses OOP features such as inheritance, composition, and polymorphism to organize the code in a modular and extensible way.
4. Installations
pip install pandas matplotlib seaborn python-dotenv
5. Usage Examples
Load and clean a movie dataset:
from movie_pipeline import *

# Load TMDB dataset
df = load_movie_dataset("TMDB_movie_dataset_v12.csv")

# Remove duplicates and invalid rows
df_clean = remove_duplicate_data(df)

# Normalize ratings and text fields
df_normalized = normalize_tmdb_reviews(df_clean)
Use object-oriented review system:
from movie_review_system import MovieReviewSystem, CriticMovieReviewSystem

system = MovieReviewSystem("reviews.csv")
system.load_reviews()
system.clean_reviews()
recommendations = system.recommend_movies()

critic_system = CriticMovieReviewSystem("critic_reviews.csv", minimum_rating=8)
critic_system.clean_reviews()
top_critic_reviews = critic_system.recommend_movies()
Data cleaning & summarization via composition:
from data_clean import DataClean

data = {
    "reviews": ["Great movie!", None, "So-so.", "Great movie!", ""],
    "ratings": [4.5, 3.0, 5.0, None, "bad", 4.0],
    "plot": "An epic story of heroes and villains saving the universe."
}

cleaner = DataClean(data)
cleaned_reviews = cleaner.clean_reviews()
avg_rating = cleaner.average_rating()
summary_plot = cleaner.summarize_plot(50)
is_positive = cleaner.is_positive_review("Great movie!")
Visualizations:
from visualizer import MovieVisualizer
from dataset import Dataset

dataset = Dataset("TMDB_movie_dataset_v12.csv")
visualizer = MovieVisualizer(dataset)

visualizer.plot_top_movies(top_n=10)
visualizer.plot_genre_popularity()
visualizer.plot_rating_distribution()
visualizer.plot_review_activity_over_time(genres=["Action", "Drama"])
6. Function Library Overview
Member	Category	Functions	Description
Pranav Rishi	Data Cleaning	load_movie_reviews(), remove_duplicate_data(), remove_spoiler_reviews(), recommend_similar_movies()	Handles ingestion, duplicate/spoiler filtering, and basic recommendation logic.
Jayraj Shanmugam	Review Processing	clean_reviews(), summarize_plot(), average_rating(), is_positive()	Processes and evaluates reviews, computes averages, and detects sentiment.
Jayden Williams	Data Handling	load_movie_dataset(), normalize_tmdb_reviews(), export_reviews_to_csv()	Handles CSV I/O, normalization, and export for cleaned datasets.
Emilio Sanchez San Martin	Visualization	plot_top_movies(), plot_genre_popularity(), plot_rating_distribution(), plot_review_activity_over_time()	Creates visual reports showing top-rated movies, genre trends, and release patterns.
Class Hierarchy & Relationships
Inheritance (is-a):
AbstractMovieReviewItem (ABC)
        │
        └── MovieReviewSystem
                │
                └── CriticMovieReviewSystem

BaseMovieCorpus (ABC)
        ├── TMDBCSVCorpus
        └── MemoryCorpus

BaseVisualizer (ABC)
        └── MovieVisualizer
Composition (has-a):
DataClean
 ├── ReviewCleaner
 ├── PlotSummarizer
 ├── RatingAnalyzer
 └── PositiveReviewDetector

ReviewPipeline
 ├── BaseMovieCorpus (any subclass)
 └── ReviewTable
Polymorphism (method overrides that behave differently across subclasses):
clean_reviews() → MovieReviewSystem vs CriticMovieReviewSystem
recommend_movies() → MovieReviewSystem vs CriticMovieReviewSystem
plot_data() → MovieVisualizer override
7. Contribution Guidelines
Version Control: Use GitHub. Commit frequently, test before merging to main.
Code Style: Follow PEP 8, use clear naming, consistent indentation, and comments.
Docstrings: Document each function/class with purpose, parameters, return types, and examples.
Testing: Include unit tests for functions, CSV input/output, and class behavior.
Collaboration: Review teammates’ code, give feedback, maintain communication.


