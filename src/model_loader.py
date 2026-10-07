import joblib
import numpy as np
from scipy import sparse

from src.config import (
    MOVIE_FEATURES_PATH,
    WEIGHTED_TFIDF_VECTORIZER_PATH,
    WEIGHTED_TFIDF_MATRIX_PATH,
    USER_ID_TO_INDEX_PATH,
    MOVIE_ID_TO_INDEX_PATH,
    INDEX_TO_MOVIE_ID_PATH,
    USER_FACTORS_PATH,
    MOVIE_FACTORS_PATH,
    USER_RATED_MOVIES_PATH,
    USER_LIKED_MOVIES_PATH,
    SVD_MODEL_PATH
)

from src.content_based.vectorizer import (
    load_movie_features
)


def load_content_models():
    """
    Load movie features and weighted TF-IDF artifacts.
    """

    movie_features = load_movie_features(
        MOVIE_FEATURES_PATH
    )

    tfidf_vectorizer = joblib.load(
        WEIGHTED_TFIDF_VECTORIZER_PATH
    )

    tfidf_matrix = sparse.load_npz(
        WEIGHTED_TFIDF_MATRIX_PATH
    )

    return (
        movie_features,
        tfidf_vectorizer,
        tfidf_matrix
    )


def load_collaborative_models():
    """
    Load collaborative filtering artifacts.
    """

    user_id_to_index = joblib.load(
        USER_ID_TO_INDEX_PATH
    )

    movie_id_to_index = joblib.load(
        MOVIE_ID_TO_INDEX_PATH
    )

    index_to_movie_id = joblib.load(
        INDEX_TO_MOVIE_ID_PATH
    )

    user_factors = np.load(
        USER_FACTORS_PATH
    )

    movie_factors = np.load(
        MOVIE_FACTORS_PATH
    )

    svd_model = joblib.load(
        SVD_MODEL_PATH
    )

    user_rated_movies = joblib.load(
        USER_RATED_MOVIES_PATH
    )

    user_liked_movies = joblib.load(
        USER_LIKED_MOVIES_PATH
    )

    return {
        "user_id_to_index": user_id_to_index,
        "movie_id_to_index": movie_id_to_index,
        "index_to_movie_id": index_to_movie_id,
        "user_factors": user_factors,
        "movie_factors": movie_factors,
        "svd_model": svd_model,
        "user_rated_movies": user_rated_movies,
        "user_liked_movies": user_liked_movies
    }