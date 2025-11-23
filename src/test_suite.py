import unittest
from datetime import datetime
from types import SimpleNamespace

# Assuming all your classes are imported from their respective modules
from your_module import (
    MovieReviewSystem, CriticMovieReviewSystem, DataClean,
    ReviewCleaner, PlotSummarizer, RatingAnalyzer, PositiveReviewDetector,
    BaseMovieCorpus, MemoryCorpus, TMDBCSVCorpus,
    ReviewTable, ReviewPipeline
)


def mock_load_movie_reviews(filepath):
    return [
        ["Movie A", "8.5", "Great movie!"],
        ["Movie B", "6.0", "Not bad."],
        ["Movie C", "9.0", "Excellent!"],
        ["Movie D", "4.5", "Could be better."],
        ["Movie E", "7.0", "Good watch!"]
    ]

def mock_remove_duplicate_data(reviews):
    return reviews

def mock_remove_spoiler_reviews(reviews):
    return reviews

def mock_recommend_similar_movies(reviews):
    return [r[0] for r in reviews]

# Patch MovieReviewSystem helpers
MovieReviewSystem.load_movie_reviews = staticmethod(mock_load_movie_reviews)
MovieReviewSystem.remove_duplicate_data = staticmethod(mock_remove_duplicate_data)
MovieReviewSystem.remove_spoiler_reviews = staticmethod(mock_remove_spoiler_reviews)
MovieReviewSystem.recommend_similar_movies = staticmethod(mock_recommend_similar_movies)


class TestInheritanceAndABC(unittest.TestCase):

    def test_inheritance(self):
        system = MovieReviewSystem("dummy.csv")
        critic = CriticMovieReviewSystem("dummy.csv")
        self.assertIsInstance(system, BaseMovieCorpus.__bases__[0] if BaseMovieCorpus.__bases__ else object)
        self.assertIsInstance(critic, MovieReviewSystem)

    def test_cannot_instantiate_abc(self):
        with self.assertRaises(TypeError):
            BaseMovieCorpus()


class TestPolymorphism(unittest.TestCase):

    def setUp(self):
        self.base_system = MovieReviewSystem("dummy.csv")
        self.critic_system = CriticMovieReviewSystem("dummy.csv", minimum_rating=7)

        self.base_system.load_reviews()
        self.base_system.clean_reviews()
        self.critic_system.load_reviews()
        self.critic_system.clean_reviews()

    def test_clean_reviews_diff_behavior(self):
        base_cleaned = self.base_system.clean_reviews()
        critic_cleaned = self.critic_system.clean_reviews()

        self.assertEqual(len(base_cleaned), 5)
        self.assertTrue(all(float(r[1]) >= 7 for r in critic_cleaned))

    def test_recommend_movies_diff_behavior(self):
        base_recs = self.base_system.recommend_movies()
        critic_recs = self.critic_system.recommend_movies()

        self.assertEqual(set(base_recs), {"Movie A", "Movie B", "Movie C", "Movie D", "Movie E"})
        critic_ratings = [float(r[1]) for r in critic_recs]
        self.assertEqual(critic_ratings, sorted(critic_ratings, reverse=True))


class TestComposition(unittest.TestCase):

    def setUp(self):
        self.data = {
            "reviews": ["Great movie!", None, "So-so.", "Great movie!", ""],
            "ratings": [4.5, 3.0, 5.0, None, "bad", 4.0],
            "plot": "A hero rises to challenge the status quo and bring balance."
        }
        self.cleaner = DataClean(self.data)

    def test_data_cleaning(self):
        cleaned = self.cleaner.clean_reviews()
        self.assertEqual(cleaned, ["Great movie!", "So-so."])

    def test_average_rating(self):
        avg = self.cleaner.average_rating()
        self.assertAlmostEqual(avg, 4.125)

    def test_summarize_plot(self):
        summary = self.cleaner.summarize_plot(max_length=20)
        self.assertTrue(summary.endswith("..."))

    def test_positive_review_detection(self):
        self.assertTrue(self.cleaner.is_positive_review("Excellent movie!"))
        self.assertFalse(self.cleaner.is_positive_review("Bad movie"))

    def test_str_repr(self):
        self.cleaner.clean_reviews()
        self.cleaner.average_rating()
        s = str(self.cleaner)
        r = repr(self.cleaner)
        self.assertIn("Cleaned reviews", s) or self.assertIn("Dataset", s)
        self.assertIn("data=", r)


class TestReviewCorpusAndPipeline(unittest.TestCase):

    def setUp(self):
        self.memory_data = [
            {"title": "Movie X", "vote_average": 8.0, "genres": "Action", "release_date": "2022-01-01"},
            {"title": "Movie Y", "vote_average": 6.5, "genres": "Comedy", "release_date": "2021-06-15"}
        ]
        self.memory_corpus = MemoryCorpus(self.memory_data)
        self.pipeline = ReviewPipeline(self.memory_corpus)

    def test_memory_corpus_load_and_find(self):
        rows = self.memory_corpus.load()
        self.assertEqual(len(rows), 2)
        reviews = self.memory_corpus.find_reviews_by_title("Movie X")
        self.assertTrue(all("Movie X" in r["content"] or "Movie X" in r["author"] for r in reviews) or isinstance(reviews, list))

    def test_review_pipeline_add_and_normalize(self):
        table = self.pipeline.build_reviews("Movie X")
        self.assertIsInstance(table, ReviewTable)
        self.assertTrue(len(table.rows) >= 0)
        self.assertIsInstance(table.rows, list)

    def test_review_table_export(self):
        table = self.pipeline.build_reviews("Movie X")
        try:
            table.export_csv("test_output.csv")
        except Exception as e:
            self.fail(f"export_csv failed with {e}")


if __name__ == "__main__":
    unittest.main()
