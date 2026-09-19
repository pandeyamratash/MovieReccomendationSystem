import os

# Project root = one level above src/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
MODELS_DIR = os.path.join(BASE_DIR, "models")

MOVIES_CSV = os.path.join(RAW_DATA_DIR, "movies.csv")
RATINGS_CSV = os.path.join(RAW_DATA_DIR, "ratings.csv")
TAGS_CSV = os.path.join(RAW_DATA_DIR, "tags.csv")

MOVIE_FEATURES_CSV = os.path.join(PROCESSED_DATA_DIR, "movie_features.csv")

WEIGHTED_TFIDF_VECTORIZER_PATH = os.path.join(MODELS_DIR, "weighted_tfidf_vectorizer.pkl")
WEIGHTED_TFIDF_MATRIX_PATH = os.path.join(MODELS_DIR, "weighted_tfidf_matrix.npz")

USER_ITEM_MATRIX_PATH = os.path.join(MODELS_DIR, "user_item_matrix.npz")
USER_ID_TO_INDEX_PATH = os.path.join(MODELS_DIR, "user_id_to_index.pkl")
MOVIE_ID_TO_INDEX_PATH = os.path.join(MODELS_DIR, "movie_id_to_index.pkl")
INDEX_TO_MOVIE_ID_PATH = os.path.join(MODELS_DIR, "index_to_movie_id.pkl")
USER_FACTORS_PATH = os.path.join(MODELS_DIR, "user_factors.npy")
MOVIE_FACTORS_PATH = os.path.join(MODELS_DIR, "movie_factors.npy")
SVD_MODEL_PATH = os.path.join(MODELS_DIR, "svd_model.pkl")
USER_RATED_MOVIES_PATH = os.path.join(MODELS_DIR, "user_rated_movies.pkl")