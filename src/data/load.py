import pandas as pd

from src.config import (
    MOVIES_CSV,
    RATINGS_CSV,
    TAGS_CSV,
)


def load_movies(path=MOVIES_CSV):
    """
    Load raw movies.csv (movieId, title, genres).
    """
    return pd.read_csv(path)


def load_ratings(path=RATINGS_CSV):
    """
    Load raw ratings.csv (userId, movieId, rating, timestamp).
    NOTE: locally this file is TAB-separated.
    """
    return pd.read_csv(path, sep="\t")


def load_tags(path=TAGS_CSV):
    """
    Load raw tags.csv (userId, movieId, tag, timestamp).
    """
    return pd.read_csv(path)