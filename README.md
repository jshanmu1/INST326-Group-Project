# Research Data Pipeline Project — Data Transformers ## Course: INST326: Object-Oriented Programming for Information Science — Section 0201 ## Team: Data Transformers ## Date: September 11, 2025 ## 1. Project title & short description Movie Review Data Pipeline & Visualization A modular Python function library that ingests large movie datasets (TMDB CSV), cleans and normalizes ratings/reviews, performs data transformations, and produces visual reports and visualizations (top-rated movies, genre popularity, rating distributions, and trends over time). ## 2. Team members and roles • Pranav Rishi — Data ingestion & duplicate/spoiler filtering (load_movie_reviews, remove_duplicate_data, remove_spoiler_reviews, recommend_similar_movies) • Jayraj Shanmugam — Text & rating cleaning, summarization (clean_reviews, summarize_plot, average_rating, is_positive) • Jayden Williams — Data I/O & normalization (load_movie_dataset, normalize_tmdb_reviews, export_reviews_to_csv) — adapted to CSV workflow • Emilio Sanchez San Martin — Visualizations & reporting (plot_top_movies, plot_genre_popularity, plot_rating_distribution, plot_review_activity_over_time) ## 3. Domain focus & problem statement Domain: Research Data Management & Information Science (movie metadata & reviews) Problem: Movie review data sets can sometimes be really large and hard to work with when it's messy. There could be duplicated, missing information, or confusing data, hard to interpret and show visually. This project aims to make a reproducible pipeline to clean the data, make good statistics, and be able to visualize clear results for certain questions, so analysts who work with movie data may use it to find useful information regarding movies. ## 4. Installations pandas matplotlib seaborn python-dotenv ## 5. Usage Examples Below are sample examples showing how our main functions work in sequence. ### Example: Load and Clean the Movie Dataset
python
from movie_pipeline import *

# Load TMDB dataset
df = load_movie_dataset("TMDB_movie_dataset_v12.csv")

# Remove duplicates and invalid rows
df_clean = remove_duplicate_data(df)

# Normalize ratings and text fields
df_clean = normalize_tmdb_reviews(df_clean)
## 6. Function Library Overview
markdown
## 6. Function Library Overview

Our function library is divided by member responsibility and processing stage:

| Member | Category | Functions | Description |
|---------|------------|------------|--------------|
| **Pranav Rishi** | Data Cleaning | `load_movie_reviews()`, `remove_duplicate_data()`, `remove_spoiler_reviews()`, `recommend_similar_movies()` | Handles ingestion, duplicate/spoiler filtering, and basic recommendation logic. |
| **Jayraj Shanmugam** | Review Processing | `clean_reviews()`, `summarize_plot()`, `average_rating()`, `is_positive()` | Processes and evaluates reviews, computes averages, and detects sentiment. |
| **Jayden Williams** | Data Handling | `load_movie_dataset()`, `normalize_tmdb_reviews()`, `export_reviews_to_csv()` | Handles CSV I/O, normalization, and export for cleaned datasets. |
| **Emilio Sanchez San Martin** | Visualization | `plot_top_movies()`, `plot_genre_popularity()`, `plot_rating_distribution()`, `plot_review_activity_over_time()` | Creates visual reports showing top-rated movies, genre trends, and release patterns. |
## 7. Contribution Guidelines All team members will follow these guidelines for consistent collaboration: - **Version Control:** Use GitHub for all commits. Members should submit code for review and test before merging to main. - **Code Style:** Follow PEP 8 naming conventions and maintain clear, consistent indentation and comments. - **Docstrings:** Each function must have a proper docstring explaining purpose, parameters, returns, and examples. - **Testing:** Test all functions locally before committing. Include sample CSV input/output tests where possible. - **Collaboration:** Reach out to teammates to review functions, code, and get feedback. update it like this




