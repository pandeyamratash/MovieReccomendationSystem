from src.config import (
    MOVIE_FEATURES_CSV,
    WEIGHTED_TFIDF_MATRIX_PATH,
)
from src.content_based.vectorizer import (
    load_movie_features,
    load_saved_tfidf_matrix,
)
from src.content_based.similarity import (
    create_movie_index,
    recommend_movies,
)

# Module-level cache so we only load these once per process
_movie_features = None
_tfidf_matrix = None
_movie_indices = None


def _load_artifacts():
    """
    Load movie features, the saved TF-IDF matrix, and the
    title->index mapping into memory, but only once.
    """
    global _movie_features, _tfidf_matrix, _movie_indices

    if _movie_features is None:
        _movie_features = load_movie_features(MOVIE_FEATURES_CSV)

    if _tfidf_matrix is None:
        _tfidf_matrix = load_saved_tfidf_matrix(WEIGHTED_TFIDF_MATRIX_PATH)

    if _movie_indices is None:
        _movie_indices = create_movie_index(_movie_features)


def recommend(movie_title, n=10):
    """
    Return the top-n movies most similar to movie_title,
    using the saved weighted TF-IDF matrix.
    """
    _load_artifacts()

    return recommend_movies(
        movie_title,
        _movie_features,
        _tfidf_matrix,
        _movie_indices,
        n=n
    )