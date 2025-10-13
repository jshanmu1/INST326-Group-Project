import requests
import csv

def load_db_api_key(path):
    """
    Read a TMDB API key from a text file.

    Arguments: path is a string: Path to the text file that has the key.

    Returns: An API key.

    Possible Errors:
        TypeError: If path is not a string.
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty.
    """

    if not isinstance(path, str):
        raise TypeError("path must be a string")

    with open(path, "r", encoding="utf-8") as f:
        key = f.read().strip()

    if key == "":
        raise ValueError("APIkey file is empty")

    return key
