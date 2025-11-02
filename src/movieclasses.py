"""
Functions + OOP classes for TMDB CSV loading, review extraction, normalization, and export.

Functions: load_db, fetch_tmdb_movie_reviews, normalize_tmdb_reviews, export_reviews_to_csv
Classes:  MovieDataset, ReviewTable
Jayden Williams
"""

from __future__ import annotations
import csv
from typing import Any, Dict, List, Optional, Sequence

#Project 1 functions

def load_db(path: str) -> List[Dict[str, Any]]:
    """
    Load TMDB rows from CSV and filter:
      - keep 2010 <= release year <= 2025
      - keep vote_count >= 1

    Returns:
        list of row dicts
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
                if len(d) >= 4 and d[:4].isdigit():
                    year = int(d[:4])

            # vote_count
            try:
                votes = int(row.get("vote_count", "0"))
            except ValueError:
                votes = 0

            if year is not None and 2010 <= year <= 2025 and votes >= 1:
                rows.append(row)

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


#Project 2 Portion

class MovieDataset:
    """
    Represents a TMDB CSV dataset with simple filters.

    Methods:
      - load(): read and filter CSV into list[dict]
      - find_reviews_by_title(title): produce pseudo-reviews from loaded rows
    """

    def __init__(self, path: str, year_min: int = 2010, year_max: int = 2025, min_votes: int = 1):
        if not isinstance(path, str) or not path.strip():
            raise ValueError("path must be a non-empty string")
        if not isinstance(year_min, int) or not isinstance(year_max, int) or year_min > year_max:
            raise ValueError("year_min/year_max must be ints and year_min <= year_max")
        if not isinstance(min_votes, int) or min_votes < 0:
            raise ValueError("min_votes must be a non-negative int")

        self._path = path
        self._year_min = year_min
        self._year_max = year_max
        self._min_votes = min_votes
        self._rows: Optional[List[Dict[str, Any]]] = None

    # Listing all of the Properties
    @property
    def path(self) -> str:
        return self._path

    @property
    def year_min(self) -> int:
        return self._year_min

    @year_min.setter
    def year_min(self, value: int) -> None:
        if not isinstance(value, int) or value > self._year_max:
            raise ValueError("year_min must be an int <= year_max")
        self._year_min = value
        self._rows = None  # invalidate cache

    @property
    def year_max(self) -> int:
        return self._year_max

    @year_max.setter
    def year_max(self, value: int) -> None:
        if not isinstance(value, int) or value < self._year_min:
            raise ValueError("year_max must be an int >= year_min")
        self._year_max = value
        self._rows = None

    @property
    def min_votes(self) -> int:
        return self._min_votes

    @min_votes.setter
    def min_votes(self, value: int) -> None:
        if not isinstance(value, int) or value < 0:
            raise ValueError("min_votes must be a non-negative int")
        self._min_votes = value
        self._rows = None

    @property
    def rows(self) -> Optional[List[Dict[str, Any]]]:
        """A copy of the last loaded rows, or None."""
        return None if self._rows is None else [dict(r) for r in self._rows]

    # Behavior
    def load(self) -> List[Dict[str, Any]]:
        """Load filtered rows using load_db(), then apply tighter object filters."""
        data = load_db(self._path)
      
        filtered: List[Dict[str, Any]] = []
        for row in data:
            year = None
            if row.get("release_year"):
                try:
                    year = int(row["release_year"])
                except ValueError:
                    year = None
            if year is None and row.get("release_date"):
                d = row["release_date"]
                if len(d) >= 4 and d[:4].isdigit():
                    year = int(d[:4])

            try:
                votes = int(row.get("vote_count", "0"))
            except ValueError:
                votes = 0

            if (
                year is not None
                and self._year_min <= year <= self._year_max
                and votes >= self._min_votes
            ):
                filtered.append(row)

        self._rows = filtered
        return [dict(r) for r in self._rows]

    def find_reviews_by_title(self, title: str) -> List[Dict[str, Any]]:
        """Return pseudo-review dicts for movies whose title contains `title`."""
        if self._rows is None:
            self.load()
        return fetch_tmdb_movie_reviews(title, self._rows or [])

    def __len__(self) -> int:
        return 0 if self._rows is None else len(self._rows)

    def __str__(self) -> str:
        return f"MovieDataset(path='{self._path}', rows={len(self)})"

    def __repr__(self) -> str:
        return (
            f"MovieDataset(path={self._path!r}, year_min={self._year_min}, "
            f"year_max={self._year_max}, min_votes={self._min_votes})"
        )


class ReviewTable:
    """
    Holds review items and provides normalization + CSV export.

    Workflow:
      rt = ReviewTable(reviews_from_dataset)
      rows = rt.normalize()
      rt.export_csv("out.csv")
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

    @property
    def is_empty(self) -> bool:
        return len(self._raw) == 0

    def add_reviews(self, reviews: List[Any]) -> None:
        if not isinstance(reviews, list):
            raise TypeError("reviews must be a list")
        self._raw.extend(reviews)
        self._rows = None  # invalidate cache

    def normalize(self) -> List[List[Any]]:
        # If already normalized shape, just copy
        if self._raw and all(isinstance(x, (list, tuple)) and len(x) >= 3 for x in self._raw):
            self._rows = [list(x) for x in self._raw]
        else:
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

    def __repr__(self) -> str:
        return f"ReviewTable(raw={len(self._raw)}, rows={(len(self._rows) if self._rows else 0)})"


__all__ = [
    # Functions
    "load_db", "fetch_tmdb_movie_reviews", "normalize_tmdb_reviews", "export_reviews_to_csv",
    # Classes
    "MovieDataset", "ReviewTable",
]
