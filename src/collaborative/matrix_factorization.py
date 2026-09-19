import joblib
import numpy as np
from scipy import sparse
from sklearn.decomposition import TruncatedSVD


def load_user_item_matrix(path):
    """
    Load the saved sparse user-item ratings matrix.
    """
    return sparse.load_npz(path)


def load_id_mappings(user_id_to_index_path, movie_id_to_index_path, index_to_movie_id_path):
    """
    Load the saved userId/movieId <-> matrix-index mappings.
    """
    user_id_to_index = joblib.load(user_id_to_index_path)
    movie_id_to_index = joblib.load(movie_id_to_index_path)
    index_to_movie_id = joblib.load(index_to_movie_id_path)
    return user_id_to_index, movie_id_to_index, index_to_movie_id


def fit_svd(user_item_matrix, n_components=50, random_state=42):
    """
    Fit Truncated SVD on the sparse user-item matrix.

    Returns:
        svd: the fitted TruncatedSVD object (needed to transform new data later)
        user_factors: (n_users, n_components) latent factor matrix
        movie_factors: (n_movies, n_components) latent factor matrix
    """
    svd = TruncatedSVD(n_components=n_components, random_state=random_state)
    user_factors = svd.fit_transform(user_item_matrix)
    movie_factors = svd.components_.T
    return svd, user_factors, movie_factors


def recommend_for_user(
    user_id,
    user_id_to_index,
    movie_id_to_index,
    index_to_movie_id,
    user_factors,
    movie_factors,
    rated_movie_ids_by_user,
    n=10
):
    """
    Recommend movies for a given user based on their latent factor vector.

    rated_movie_ids_by_user: a set of movieIds this user has already rated,
    so we don't recommend movies they've already seen.
    """
    if user_id not in user_id_to_index:
        return f"userId {user_id} not found."

    user_idx = user_id_to_index[user_id]
    user_vector = user_factors[user_idx]

    predicted_scores = movie_factors @ user_vector

    already_rated_indices = {
        movie_id_to_index[mid] for mid in rated_movie_ids_by_user
        if mid in movie_id_to_index
    }

    top_indices = predicted_scores.argsort()[::-1]
    top_indices = [i for i in top_indices if i not in already_rated_indices][:n]

    results = []
    for i in top_indices:
        movie_id = index_to_movie_id[i]
        results.append({
            "movieId": movie_id,
            "predicted_score": predicted_scores[i]
        })
    return results