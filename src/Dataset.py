import pandas as pd

class Dataset:
    """
    Stores and validates movie data.
    Ensures the visualizer works with a clean DataFrame.
    """

    def __init__(self, df: pd.DataFrame):
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df has to be a pandas DataFrame.")
        if df.empty:
            raise ValueError("DataFrame can't be empty.")

        required_cols = {'title', 'vote_average', 'genres', 'release_date'}
        if not required_cols.issubset(df.columns):
            missing = required_cols - set(df.columns)
            raise ValueError(f"Missing required columns: {missing}")

        self._df = df.copy()

    def get_data(self) -> pd.DataFrame:
        """Return a defensive copy of the dataset."""
        return self._df.copy()