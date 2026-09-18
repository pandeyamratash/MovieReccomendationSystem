import pandas as pd
import joblib
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer


def load_movie_features(path):
    """
    Load processed movie features.
    """
    return pd.read_csv(path)


def create_tfidf_vectorizer(
    movie_features,
    max_features=50000
):
    """
    Create and fit a TF-IDF vectorizer
    using weighted movie content.
    """

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=max_features
    )

    tfidf_matrix = vectorizer.fit_transform(
        movie_features["weighted_content"]
    )

    return vectorizer, tfidf_matrix


def load_saved_vectorizer(vectorizer_path):
    """
    Load a previously trained TF-IDF vectorizer from disk.
    Use this instead of refitting at runtime.
    """
    return joblib.load(vectorizer_path)


def load_saved_tfidf_matrix(matrix_path):
    """
    Load a previously saved sparse TF-IDF matrix from disk.
    """
    return sparse.load_npz(matrix_path)