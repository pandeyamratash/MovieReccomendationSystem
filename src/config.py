from pathlib import Path


# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent


# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"


# Model directory
MODELS_DIR = PROJECT_ROOT / "models"


# Important files
MOVIE_FEATURES_PATH = (
    PROCESSED_DATA_DIR / "movie_features.csv"
)

MODEL_COMPARISON_PATH = (
    PROCESSED_DATA_DIR / "model_comparison.csv"
)

TFIDF_VECTORIZER_PATH = (
    MODELS_DIR / "tfidf_vectorizer.pkl"
)

WEIGHTED_TFIDF_VECTORIZER_PATH = (
    MODELS_DIR / "weighted_tfidf_vectorizer.pkl"
)

WEIGHTED_TFIDF_MATRIX_PATH = (
    MODELS_DIR / "weighted_tfidf_matrix.npz"
)
# Collaborative filtering artifacts

USER_ITEM_MATRIX_PATH = (
    MODELS_DIR / "user_item_matrix.npz"
)

USER_ID_TO_INDEX_PATH = (
    MODELS_DIR / "user_id_to_index.pkl"
)

MOVIE_ID_TO_INDEX_PATH = (
    MODELS_DIR / "movie_id_to_index.pkl"
)

INDEX_TO_MOVIE_ID_PATH = (
    MODELS_DIR / "index_to_movie_id.pkl"
)

USER_FACTORS_PATH = (
    MODELS_DIR / "user_factors.npy"
)

MOVIE_FACTORS_PATH = (
    MODELS_DIR / "movie_factors.npy"
)

SVD_MODEL_PATH = (
    MODELS_DIR / "svd_model.pkl"
)

USER_RATED_MOVIES_PATH = (
    MODELS_DIR / "user_rated_movies.pkl"
)