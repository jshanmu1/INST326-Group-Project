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

