"""
INST326 Project 3
Main collection + reviews module with ABC, inheritance, polymorphism, and composition.

Design:
- Abstract source: BaseMovieCorpus (ABC)
- Concrete sources (inheritance + polymorphism):
    TMDBCSVCorpus: loads from TMDB CSV via load_db()
    MemoryCorpus: in memory rows (useful (helper) for tests)
- Composition:
    ReviewPipeline has a BaseMovieCorpus and a ReviewTable
"""

from __future__ import annotations
import csv
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Sequence

# Helpers to keep columns consistent for Dataset/Visualizer integration my teammates functions


_REQUIRED_COLS = {"title", "vote_average", "genres", "release_date"}

def _normalize_row_for_required_cols(row: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure required keys exist (non-destructive; adds safe fallbacks)."""
    r = dict(row)
    if not r.get("title"):
        r["title"] = (r.get("original_title") or "").strip()

    va = r.get("vote_average")
    if va in (None, ""):
        r["vote_average"] = None
    else:
        try:
            r["vote_average"] = float(va)
        except (TypeError, ValueError):
            r["vote_average"] = None

    if not r.get("release_date"):
        year = None
        if r.get("release_year"):
            try:
                year = int(r["release_year"])
            except (TypeError, ValueError):
                year = None
        if isinstance(year, int) and 1800 <= year <= 3000:
            r["release_date"] = f"{year}-01-01"
        else:
            r.setdefault("release_date", "")

  
    r.setdefault("genres", "")

    return r


# Project 1 functions

def load_db(path: str) -> List[Dict[str, Any]]:
    """
    Load TMDB rows from CSV and filter:
      - keep 2010 <= release year <= 2025
      - keep vote_count >= 1

    Returns:
        list of row dicts (with required columns normalized/present)
    """
    if not isinstance(path, str):
        raise TypeError("path must be a string")

    rows: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            year: Optional[int] = None
            if row.get("release_year"):
                try:
                    year = int(row["release_year"])
                except ValueError:
                    year = None
            if year is None and row.get("release_date"):
                d = row["release_date"]
                if isinstance(d, str) and len(d) >= 4 and d[:4].isdigit():
                    year = int(d[:4])

            
            try:
                votes = int(row.get("vote_count", "0"))
            except ValueError:
                votes = 0

            if year is not None and 2010 <= year <= 2025 and votes >= 1:
                rows.append(_normalize_row_for_required_cols(row))

    return rows


def fetch_tmdb_movie_reviews(title: str, movie_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Create pseudo-reviews from TMDB rows for a matching title (case-insensitive).
    Uses 'overview' as the review text and 'vote_average' as the rating.

    Returns:
        [{"author": "TMDB users", "content": str, "author_details": {"rating": float|None}}, ...]
    """
    if not isinstance(title, str):
        raise TypeError("title must be a string")
    if not isinstance(movie_rows, list):
        raise TypeError("movie_rows must be a list")

    q = title.strip().lower()
    found: List[Dict[str, Any]] = []

    for row in movie_rows:
        row_title = (row.get("title") or row.get("original_title") or "").strip()
        if not row_title:
            continue
        if q in row_title.lower():
            overview = (row.get("overview") or "").strip()
            rating = None
            va = row.get("vote_average")
            if va not in (None, ""):
                try:
                    rating = float(va)
                except (TypeError, ValueError):
                    rating = None
            found.append({
                "author": "TMDB users",
                "content": overview,
                "author_details": {"rating": rating},
            })

    return found


def normalize_tmdb_reviews(reviews: List[Dict[str, Any]]) -> List[List[Any]]:
    """
    Convert review dicts to simple rows: [author, content, rating].
    Ignores malformed items.
    """
    if not isinstance(reviews, list):
        raise TypeError("reviews must be a list")

    out: List[List[Any]] = []
    for item in reviews:
        if not isinstance(item, dict):
            continue
        author = item.get("author", "TMDB users")
        content = (item.get("content", "") or "").strip()
        details = item.get("author_details", {})
        rating = details.get("rating") if isinstance(details, dict) else None
        out.append([author, content, rating])
    return out


def export_reviews_to_csv(reviews: Sequence[Sequence[Any]], filename: str) -> None:
    """
    Save normalized rows to CSV with columns: Author, Content, Rating.
    """
    if not isinstance(reviews, (list, tuple)):
        raise TypeError("reviews must be a list or tuple")
    if not isinstance(filename, str):
        raise TypeError("filename must be a string")
    if len(reviews) == 0:
        raise ValueError("no reviews to export")

    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Author", "Content", "Rating"])
        for row in reviews:
            if isinstance(row, (list, tuple)) and len(row) >= 3:
                writer.writerow([row[0], row[1], row[2]])

# Abstract Base Class + Inheritance (polymorphic)

class BaseMovieCorpus(ABC):
    """
    Abstract base for a movie corpus (polymorphic source of rows + reviews).

    Subclasses must implement:
      - load() -> list[dict]
      - find_reviews_by_title(title) -> list[dict]
    """

    def __init__(self):
        self._loaded: bool = False
        self._rows: List[Dict[str, Any]] = []

    @property
    def rows(self) -> List[Dict[str, Any]]:
        """Copy of loaded rows."""
        return [dict(r) for r in self._rows]

    def __len__(self) -> int:
        return len(self._rows)

    @abstractmethod
    def load(self) -> List[Dict[str, Any]]:
        """Load rows into memory and return them."""
        raise NotImplementedError

    @abstractmethod
    def find_reviews_by_title(self, title: str) -> List[Dict[str, Any]]:
        """Return pseudo-review dicts for the given title."""
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(rows={len(self)})"


class TMDBCSVCorpus(BaseMovieCorpus):
    """
    CSV-backed corpus. Specializes BaseMovieCorpus.
    Uses P1 functions under the hood.
    """

    def __init__(self, path: str):
        super().__init__()
        if not isinstance(path, str) or not path.strip():
            raise ValueError("path must be a non-empty string")
        self._path = path

    @property
    def path(self) -> str:
        return self._path

    def load(self) -> List[Dict[str, Any]]:
        self._rows = load_db(self._path)
        self._loaded = True
        return self.rows

    def find_reviews_by_title(self, title: str) -> List[Dict[str, Any]]:
        if not self._loaded:
            self.load()
        return fetch_tmdb_movie_reviews(title, self._rows)

    def __str__(self) -> str:
        return f"TMDBCSVCorpus(path='{self._path}', rows={len(self)})"


class MemoryCorpus(BaseMovieCorpus):
    """
    In-memory corpus (useful for tests). Also specializes BaseMovieCorpus.
    """

    def __init__(self, rows: Optional[List[Dict[str, Any]]] = None):
        super().__init__()
        self._rows = [ _normalize_row_for_required_cols(r) for r in (rows or []) ]
        self._loaded = True

    def load(self) -> List[Dict[str, Any]]:
        return self.rows

    def find_reviews_by_title(self, title: str) -> List[Dict[str, Any]]:
        return fetch_tmdb_movie_reviews(title, self._rows)

    def __str__(self) -> str:
        return f"MemoryCorpus(rows={len(self)})"


# Composition: ReviewTable + Pipeline 

class ReviewTable:
    """
    Holds review items and provides normalization + CSV export.

    Used by ReviewPipeline (composition), independent of which BaseMovieCorpus
    subclass provides the raw data (polymorphism).
    """

    def __init__(self, reviews: Optional[List[Any]] = None):
        self._raw: List[Any] = []
        self._rows: Optional[List[List[Any]]] = None
        if reviews:
            self.add_reviews(reviews)

    @property
    def raw(self) -> List[Any]:
        return list(self._raw)

    @property
    def rows(self) -> Optional[List[List[Any]]]:
        return None if self._rows is None else [list(r) for r in self._rows]

    def add_reviews(self, reviews: List[Any]) -> None:
        if not isinstance(reviews, list):
            raise TypeError("reviews must be a list")
        self._raw.extend(reviews)
        self._rows = None  # invalidate cache

    def normalize(self) -> List[List[Any]]:
        self._rows = normalize_tmdb_reviews(self._raw)
        return [list(r) for r in self._rows]

    def export_csv(self, filename: str) -> None:
        if self._rows is None:
            self.normalize()
        export_reviews_to_csv(self._rows or [], filename)

    def __len__(self) -> int:
        return 0 if self._rows is None else len(self._rows)

    def __str__(self) -> str:
        n_raw = len(self._raw)
        n_rows = len(self) if self._rows is not None else 0
        return f"ReviewTable(raw={n_raw}, rows={n_rows})"


class ReviewPipeline:
    """
    Composition-based orchestrator.
    - has-a BaseMovieCorpus (polymorphic source)
    - has-a ReviewTable (storage/normalization/export)

    Example:
        corpus = TMDBCSVCorpus("data/TMDB.csv")
        pipe = ReviewPipeline(corpus)
        table = pipe.build_reviews("Dune")
        table.export_csv("out/dune_reviews.csv")
    """

    def __init__(self, corpus: BaseMovieCorpus):
        if not isinstance(corpus, BaseMovieCorpus):
            raise TypeError("corpus must be a BaseMovieCorpus")
        self._corpus = corpus
        self._table = ReviewTable()

    @property
    def corpus(self) -> BaseMovieCorpus:
        return self._corpus

    @property
    def table(self) -> ReviewTable:
        return self._table

    def build_reviews(self, title: str) -> ReviewTable:
        """Fetch reviews from the corpus, store, normalize, and return the table."""
        reviews = self._corpus.find_reviews_by_title(title)
        self._table.add_reviews(reviews)
        self._table.normalize()
        return self._table

    def __str__(self) -> str:
        return f"ReviewPipeline(source={self._corpus.__class__.__name__}, table={self._table})"


__all__ = [
    # Original functions
    "load_db", "fetch_tmdb_movie_reviews", "normalize_tmdb_reviews", "export_reviews_to_csv",
    # ABC and the inheritance
    "BaseMovieCorpus", "TMDBCSVCorpus", "MemoryCorpus",
    # Composition parts
    "ReviewTable", "ReviewPipeline",
]
