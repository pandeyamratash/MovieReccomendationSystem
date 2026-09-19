from src.config import (
    USER_ITEM_MATRIX_PATH,
    USER_ID_TO_INDEX_PATH,
    MOVIE_ID_TO_INDEX_PATH,
    INDEX_TO_MOVIE_ID_PATH,
    USER_FACTORS_PATH,
    MOVIE_FACTORS_PATH,
    USER_RATED_MOVIES_PATH,
    MOVIE_FEATURES_CSV,
)
from src.collaborative.matrix_factorization import (
    load_id_mappings,
    recommend_for_user as _recommend_for_user,
)
from src.content_based.vectorizer import load_movie_features

import numpy as np
import joblib

# Module-level cache so we only load these once per process
_user_id_to_index = None
_movie_id_to_index = None
_index_to_movie_id = None
_user_factors = None
_movie_factors = None
_user_rated_movies = None
_movies_lookup = None


def _load_artifacts():
    global _user_id_to_index, _movie_id_to_index, _index_to_movie_id
    global _user_factors, _movie_factors, _user_rated_movies, _movies_lookup

    if _user_id_to_index is None:
        _user_id_to_index, _movie_id_to_index, _index_to_movie_id = load_id_mappings(
            USER_ID_TO_INDEX_PATH, MOVIE_ID_TO_INDEX_PATH, INDEX_TO_MOVIE_ID_PATH
        )

    if _user_factors is None:
        _user_factors = np.load(USER_FACTORS_PATH)

    if _movie_factors is None:
        _movie_factors = np.load(MOVIE_FACTORS_PATH)

    if _user_rated_movies is None:
        _user_rated_movies = joblib.load(USER_RATED_MOVIES_PATH)

    if _movies_lookup is None:
        movie_features = load_movie_features(MOVIE_FEATURES_CSV)
        _movies_lookup = movie_features.set_index("movieId")["title"]


def recommend_for_user(user_id, n=10):
    """
    Return the top-n movie recommendations for a given userId,
    using the trained collaborative filtering (SVD) model.
    """
    _load_artifacts()

    rated = _user_rated_movies.get(user_id, set())

    results = _recommend_for_user(
        user_id,
        _user_id_to_index,
        _movie_id_to_index,
        _index_to_movie_id,
        _user_factors,
        _movie_factors,
        rated,
        n=n
    )

    if isinstance(results, str):
        return results

    for r in results:
        r["title"] = _movies_lookup.get(r["movieId"], "Unknown")

    return results