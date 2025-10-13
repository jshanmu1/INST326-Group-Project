import csv

def load_db_api_key(path):
    """
    Load and filter TMDB movies from a CSV file (Started with api keys in mind but we're filtering csv files to be more specific) 

    Keeps only rows from years 2010 to 2025 with vote counter being >= 1

    Args: Path to the CSV file

    Returns: A list of filtered rows as dictionaries

    Raises:
        TypeError: If path is not a string
        FileNotFoundError: If the file does not exist
    """
    if not isinstance(path, str):
        raise TypeError("path is a string")

    rows = []
    with open(path, "r", encoding="utf-8") as f:
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
                votes = int(row.get("vote_count", "0"))   #Vount Count Getter portion
            except ValueError:
                votes = 0

            if year is not None and 2010 <= year <= 2025 and votes >= 1:
                rows.append(row)

    return rows







